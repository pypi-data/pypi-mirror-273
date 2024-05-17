import unittest
from dotenv import load_dotenv
from msfabricpysdkcore import FabricClientAdmin

load_dotenv()

class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        self.fca = FabricClientAdmin()
                  
    def test_admin_api(self):
        fca = self.fca

        user_id = 'b4f4e299-e6e1-4667-886c-57e4a8dde1c2'

        # List workspaces
        ws = fca.list_workspaces(name="testworkspace")[0]

        self.assertEqual(ws.name, "testworkspace")

        # Get workspace
        ws_clone = fca.get_workspace(workspace_id=ws.id)

        self.assertEqual(ws.id, ws_clone.id)

        # Get workspace access details

        ws_access = fca.list_workspace_access_details(ws.id)
        principials = ws_access["accessDetails"]
        principials_ids = [p["principal"]["id"] for p in principials]
        self.assertIn(user_id, principials_ids)

        # Get access entities

        access_entities = fca.list_access_entities(user_id, type="Notebook")
        self.assertGreater(len(access_entities), 0)

        # Get tenant settings

        tenant_settings = fca.list_tenant_settings()
        self.assertGreater(len(tenant_settings["tenantSettings"]), 0)

        # Get capacity tenant settings overrides

        overrides = fca.list_capacities_tenant_settings_overrides()
        self.assertGreater(len(overrides), -1)

        # List items

        item_list = fca.list_items(workspace_id=ws.id)
        self.assertGreater(len(item_list), 0)

        # Get item

        item = fca.get_item(workspace_id=ws.id, item_id=item_list[0].id)
        self.assertEqual(item.id, item_list[0].id)

        # Get item access details

        item_access = fca.list_item_access_details(workspace_id=ws.id, item_id=item_list[0].id)
        principials = item_access["accessDetails"]

        principials_ids = [p["principal"]["id"] for p in principials]

        self.assertIn(user_id, principials_ids)


    def test_labels(self):

        fca = self.fca

        items = [{"id": "d417b834-d381-454c-9cf0-c491f69508de", "type": "Lakehouse"}]
        label_id = "defa4170-0d19-0005-000a-bc88714345d2"
        resp = fca.bulk_set_labels(items=items, label_id=label_id)
        self.assertEqual(resp["itemsChangeLabelStatus"][0]["status"], "Succeeded")
        resp = fca.bulk_remove_labels(items=items)
        self.assertEqual(resp["itemsChangeLabelStatus"][0]["status"], "Succeeded")
