import unittest
import os
import wget
from libvirt_provider.utils.io import join, makedirs, exists, load_json
from libvirt_provider.defaults import LIBVIRT
from libvirt_provider.models import Node
from libvirt_provider.client import new_client
from libvirt_provider.instance.create import create
from libvirt_provider.instance.remove import remove
from libvirt_provider.instance.stop import stop
from libvirt_provider.instance.get import get
from libvirt_provider.instance.state import state
from deling.io.datastores.core import SFTPStore
from deling.authenticators.ssh import SSHAuthenticator
from deling.helpers import (
    make_container,
    wait_for_container_output,
    remove_container,
    wait_for_session,
)


class TestContext():

    def __init__(self):
        self.init_done = False

    async def setUp(self):
        if self.init_done:
            return

        # Start dummy mount container where the public key is an
        # authorized key.
        # Expose a random SSH port on the host that can be used for SSH
        # testing againt the container
        cls.host = "127.0.0.1"
        cls.random_ssh_port = random.randint(2200, 2299)
        ssh_dummy_cont = {
            "image": IMAGE,
            "detach": True,
            "ports": {22: cls.random_ssh_port},
        }
        cls.container = make_container(ssh_dummy_cont)
        assert cls.container
        assert cls.container.status == "running"
        assert wait_for_container_output(cls.container.id, "Running the OpenSSH Server")
        try:
            assert wait_for_session(cls.host, cls.random_ssh_port, max_attempts=10)
        except AssertionError as err:
            print(f"Assertion error: {err}")
            assert remove_container(cls.container.id)
            raise err
        self.init_done = True

    async def tearDown(self):
        # Remove container
        if self.init_done:
            assert remove_container(self.container.id)
            self.init_done = False


class TestLibvirtRemote(unittest.IsolatedAsyncioTestCase):

    context = TestContext()

    async def asyncSetUp(self):
        await self.context.setUp()
        self.remote_user = "qemu"
        self.architecture = "x86_64"
        self.name = f"libvirt-remote-{self.architecture}"
        self.images_dir = join("tests", "images", self.architecture)
        if not exists(self.images_dir):
            self.assertTrue(makedirs(self.images_dir))

        self.image = join(self.images_dir, f"{self.name}-Rocky-9.qcow2")
        if not exists(self.image):
            # Download the image
            url = f"https://download.rockylinux.org/pub/rocky/9/images/{self.architecture}/Rocky-9-GenericCloud-Base.latest.{self.architecture}.qcow2"
            try:
                print(f"Downloading image: {url} for testing")
                wget.download(url, self.image)
            except Exception as err:
                print(f"Failed to download image: {url} - {err}")
                self.assertFalse(True)
        self.assertTrue(exists(self.image))

        username = os.environ.get("LIBVIRT_REMOTE_USERNAME", "mountuser")
        password = os.environ.get("LIBVIRT_REMOTE_PASSWORD", "Passw0rd!")

        private_key_file = os.environ.get(
            "LIBVIRT_REMOTE_PRIVATE_KEY_FILE",
            None,
        )
        public_key_file = os.environ.get(
            "LIBVIRT_REMOTE_PUBLIC_KEY_FILE",
            None,
        )
        if not public_key_file and private_key_file:
            public_key_file = f"{private_key_file}.pub"
        hostname = os.environ.get("LIBVIRT_REMOTE_HOSTNAME", "127.0.0.1")
        port = os.environ.get("LIBVIRT_REMOTE_PORT", 2222)

        self.datastore = SFTPStore(
            host=hostname,
            port=port,
            authenticator=SSHAuthenticator(
                username=username,
                password=password,
                private_key_file=private_key_file,
                public_key_file=public_key_file,
            ),
        )
        self.assertTrue(self.datastore.mkdir(self.images_dir, recursive=True))
        if not self.datastore.exists(self.image):
            self.assertTrue(self.datastore.upload(self.image, self.image))
        # TODO, lookup the remote node uid/gid for the self.libvirt_user
        remote_qemu_uid, remote_qemu_gid = 107, 107
        for i in range(2):
            test_image = join(self.images_dir, f"{self.name}-Rocky-9-{i}.qcow2")
            if not self.datastore.exists(test_image):
                self.assertTrue(self.datastore.copy(self.image, test_image))
            self.assertTrue(self.datastore.exists(test_image))
            test_image_stats = self.datastore.stat(test_image)
            self.assertNotEqual(test_image_stats, False)
            test_image_stats.uid = remote_qemu_uid
            test_image_stats.gid = remote_qemu_gid
            self.assertTrue(self.datastore.setstat(test_image, test_image_stats))

        remote_uri = f"qemu+ssh://{username}@{hostname}/session"
        self.client = new_client(LIBVIRT, open_uri=remote_uri)

    async def asyncTearDown(self):
        await self.context.tearDown()
        for i in range(2):
            test_image = join(self.images_dir, f"{self.name}-Rocky-9-{i}.qcow2")
            self.assertTrue(self.datastore.remove(test_image))
            self.assertFalse(self.datastore.exists(test_image))
        self.client.close()

    async def test_create_node(self):
        test_image = self.datastore.realpath(
            join(self.images_dir, f"{self.name}-Rocky-9-0.qcow2")
        )
        # Load architecture node_options
        node_options_path = join(
            "tests", "res", "node_options", f"{self.architecture}.json"
        )
        loaded_node_options = load_json(node_options_path)
        self.assertIsInstance(loaded_node_options, dict)
        node_options = {
            "name": "test-1",
            "disk_image_path": test_image,
            "memory_size": "1024MiB",
            **loaded_node_options,
        }

        node = await create(self.client, **node_options)
        self.assertIsNotNone(node)
        self.assertIsInstance(node, Node)
        self.assertTrue(await remove(self.client, node.id))

    async def test_stop_node(self):
        test_image = self.datastore.realpath(
            join(self.images_dir, f"{self.name}-Rocky-9-1.qcow2")
        )
        # Load architecture node_options
        node_options_path = join(
            "tests", "res", "node_options", f"{self.architecture}.json"
        )
        loaded_node_options = load_json(node_options_path)
        self.assertIsInstance(loaded_node_options, dict)
        node_options = {
            "name": "test-2",
            "disk_image_path": test_image,
            "memory_size": "1024MiB",
            **loaded_node_options,
        }

        new_node = await create(self.client, **node_options)
        self.assertIsNotNone(new_node)
        self.assertIsInstance(new_node, Node)

        node = await get(self.client, new_node.id)
        self.assertIsNotNone(node)
        self.assertIsInstance(node, Node)
        self.assertEqual(node.id, new_node.id)
        self.assertTrue(await stop(self.client, node.id))

        node_state = await state(self.client, node.id)
        self.assertIsNot(node_state, False)
        # TODO, check that the state is actually running
        self.assertTrue(await remove(self.client, node.id))
        node = await get(self.client, node.id)
        self.assertFalse(node)


if __name__ == "__main__":
    unittest.main()
