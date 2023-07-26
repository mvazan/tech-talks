from typing import Annotated, Optional

from dynamtic.models import DynamticItem, DynamticKey

from models.color import Color


class DemoItem(DynamticItem):
    tenant_id: Annotated[str, DynamticKey.PARTITION_KEY]
    user_id: Annotated[int, DynamticKey.SORT_KEY]
    value1: Optional[str] = None
    value2: Optional[int] = None
    shoe_color: Optional[Color] = None
