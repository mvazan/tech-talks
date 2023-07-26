import logging
from typing import Annotated, Optional

from dynamtic import Dynamtic
from dynamtic.models import DynamticItem, DynamticKey

from models.color import Color
from models.demo_item import DemoItem

# Dynamtic is an initiative to combine the DynamoDB boto3 client with the Pydantic model.
logging.basicConfig(level=logging.INFO)

# Model validation:
# Can't instantiate base DynamticItem class
DynamticItem()


# Is annotated with a single partition key
class NoPKItem(DynamticItem):
    tenant_id: str
    user_id: Annotated[int, DynamticKey.SORT_KEY]
    value1: Optional[str] = None
    value2: Optional[int] = None
    shoe_color: Optional[Color] = None


class MultiplePKsItem(DynamticItem):
    tenant_id: Annotated[str, DynamticKey.PARTITION_KEY]
    user_id: Annotated[int, DynamticKey.SORT_KEY]
    value1: Annotated[str, DynamticKey.PARTITION_KEY]
    value2: Optional[int] = None
    shoe_color: Optional[Color] = None


# Is not annotated with multiple sort keys
class MultipleSKsItem(DynamticItem):
    tenant_id: Annotated[str, DynamticKey.PARTITION_KEY]
    user_id: Annotated[int, DynamticKey.SORT_KEY]
    value1: Annotated[str, DynamticKey.SORT_KEY]
    value2: Optional[int] = None
    shoe_color: Optional[Color] = None


# Database actions:
dynamodb = Dynamtic(DemoItem, "mvazan-dynamtic-demo")

# PUT an item into the DynamoDB table.
item_tenant1_user1 = DemoItem(tenant_id="tenant1", user_id=1, value1="value1", value2=2, shoe_color=Color.RED)
dynamodb.put(item_tenant1_user1)

# GET an item from the DynamoDB table using partition key and optional sort key.
print(dynamodb.get(partition_key_value="tenant1", sort_key_value=1))

# UPDATE an item in the DynamoDB table.
item_tenant1_user1.value1 = "updated value1"
dynamodb.update(item_tenant1_user1)

# DELETE an item from the DynamoDB table using partition key and optional sort key.
dynamodb.delete(partition_key_value="tenant1", sort_key_value=1)

# QUERY items from the DynamoDB table using partition key and optional sort key.
item_tenant1_user_2 = DemoItem(tenant_id="tenant1", user_id=2, value1="value1", value2=2, shoe_color=Color.RED)
dynamodb.put(item_tenant1_user_2)
item_tenant2_user_1 = DemoItem(tenant_id="tenant2", user_id=1, value1="value1", value2=2, shoe_color=Color.RED)
dynamodb.put(item_tenant2_user_1)
print(dynamodb.query(partition_key_value="tenant1"))

# SCAN the entire DynamoDB table and return all items as a list.
print(dynamodb.scan())

# Paging - shown in unit tests in dynamtic library

# CDK
# get table definition - look in the CDK folder

# TODOs: https://github.com/blackboard-foundations/dynamtic-lib/tree/v0.3.5#future-improvements
