import unittest
from datetime import datetime
from dotenv import load_dotenv
from time import sleep
from msfabricpysdkcore.coreapi import FabricClientCore

load_dotenv()

class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        #load_dotenv()
        self.fc = FabricClientCore()
        self.workspace_id = "d8a5abe0-9eed-406d-ab46-343bc57ddbe5"

        
    def test_environments(self):
        fc = self.fc
        workspace_id = self.workspace_id

        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        envname = "testitem" + datetime_str
        env1 = fc.create_environment(workspace_id, envname, "testenv description")

        env2 = fc.get_environment(workspace_id, environment_name=envname)

        self.assertEqual(env1.id, env2.id)

        env_list = fc.list_environments(workspace_id, with_properties=True)
        env_names = [env.display_name for env in env_list]

        self.assertIn(envname, env_names)

        env3 = fc.update_environment(workspace_id, env1.id, envname + "name", "testenv description updated")

        env4 = fc.get_environment(workspace_id, environment_name=env3.display_name)

        self.assertEqual(env1.id, env4.id)

        fc.delete_environment(workspace_id, env4.id)

        env_list = fc.list_environments(workspace_id, with_properties=True)
        env_names = [env.display_name for env in env_list]

        self.assertNotIn(env4.display_name, env_names)

        
