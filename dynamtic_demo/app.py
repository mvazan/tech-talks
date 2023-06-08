from typing import Annotated, Optional

from dynamtic import Dynamtic
from dynamtic.dynamtic_item import DynamticItem, DynamticKey

from models.color import Color
from models.demo_item import DemoItem

# Dynamtic is an initiative to combine the DynamoDB boto3 client with the Pydantic model.

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

item = NoPKItem(tenant_id="tenant1", user_id=1)

class MultiplePKsItem(DynamticItem):
    tenant_id: Annotated[str, DynamticKey.PARTITION_KEY]
    user_id: Annotated[int, DynamticKey.SORT_KEY]
    value1: Annotated[str, DynamticKey.PARTITION_KEY]
    value2: Optional[int] = None
    shoe_color: Optional[Color] = None

item = MultiplePKsItem(tenant_id="tenant1", user_id=1, value1="value1")

# Is not annotated with multiple sort keys
class MultipleSKsItem(DynamticItem):
    tenant_id: Annotated[str, DynamticKey.PARTITION_KEY]
    user_id: Annotated[int, DynamticKey.SORT_KEY]
    value1: Annotated[str, DynamticKey.SORT_KEY]
    value2: Optional[int] = None
    shoe_color: Optional[Color] = None

item = MultipleSKsItem(tenant_id="tenant1", user_id=1, value1="value1")

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
print(dynamodb.query_by_partition_key(partition_key_value="tenant1"))

# SCAN the entire DynamoDB table and return all items as a list.
print(dynamodb.scan())

# Paging - shown in unit tests in dynamtic library

# CDK
# get table definition
pk_name, pk_type = DemoItem.get_table_definition(DynamticKey.PARTITION_KEY)
sk_name, sk_type = DemoItem.get_table_definition(DynamticKey.SORT_KEY)

user_activity_table = Table(
    self,
    "Table",
    # partition_key=aws_dynamodb.Attribute(
    #     name="tenant_id", type=aws_dynamodb.AttributeType.STRING
    # ),
    partition_key=Attribute(name=pk_name, type=AttributeType(pk_type)),
    sort_key=Attribute(name=sk_name, type=AttributeType(sk_type)),
)

# TODOs:
# - documentation
#   - which set of privileges is needed by ie lambda to fully utilize all features of this module, ie.: dynamodb::GetItem, dynamodb::PutItem etc...so that users don't run into issues when they did not expect that this privilege had to be granted to their lambda because they are just users of this wrapper
# - make the library first version available to use
# - use generics to improve the GET function signature
# - add more optional attributes to CRUD functions
# - add support for "private" parameters (ignoring DB IO operations)
# - add index support
# - dynamtic's region: remove this or make the default None, boto3 should be aware on what region you are based on which region the lambda's deployed to
# - dynamtic's attributes: mark those as protected/private if they're not supposed to be used from outside the class please
# - instead of root validators, it would make sense to trigger those checks during class creation (metaclass __new__ i believe)
# otherwise this runs during every instance creationpip install twine