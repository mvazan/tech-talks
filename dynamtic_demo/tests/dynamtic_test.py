import unittest

from dynamtic import Dynamtic
from moto import mock_dynamodb

from dynamtic_demo.models.demo_item import DemoItem


@mock_dynamodb
class TestDynamtic(unittest.TestCase):
    def setUp(self):
        table_name = "demo"
        self.dynamodb = Dynamtic(DemoItem, table_name)
        self.dynamodb.client.create_table(
            TableName=table_name,
            **DemoItem._get_table_definition(),
            BillingMode="PAY_PER_REQUEST",
        )

    def test_crud_dynamtic(self):
        # Create a Dog object to pass to the function
        item = DemoItem(tenant_id="i123", user_id=123)

        # Call the function with the moto DynamoDB client and item
        self.dynamodb.put(item)

        # Get the item from the table and assert that it matches the expected data
        response = self.dynamodb.get(partition_key_value="i123", sort_key_value=123)

        self.assertIsInstance(response, DemoItem)
        self.assertEqual(response.tenant_id, "i123")
        self.assertEqual(response.user_id, 123)
