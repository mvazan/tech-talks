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