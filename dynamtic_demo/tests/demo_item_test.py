from dynamtic.models.dynamtic_item import DynamticKey

from models.demo_item import DemoItem


def test_get_person_table_definition():
    expected_pk_definition = ("tenant_id", "STRING",)
    expected_sk_definition = ("user_id", "NUMBER",)

    pk_definition = DemoItem.get_table_definition(DynamticKey.PARTITION_KEY)
    sk_definition = DemoItem.get_table_definition(DynamticKey.SORT_KEY)

    assert pk_definition == expected_pk_definition
    assert sk_definition == expected_sk_definition
