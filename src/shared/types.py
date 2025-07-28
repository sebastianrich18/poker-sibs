from typing import NewType
from uuid import UUID

PlayerId = NewType('PlayerId', UUID)
TableId = NewType('TableId', UUID)
WalletId = NewType('WalletId', UUID)