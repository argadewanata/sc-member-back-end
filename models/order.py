from pydantic import BaseModel, Field, condecimal, constr
from datetime import datetime
from typing import Optional

class Order(BaseModel):
    id: int
    member_id: int
    paket_id: int
    tshirt_size: Optional[constr(max_length=10)] = None
    hoodie_size: Optional[constr(max_length=10)] = None
    jaket_size: Optional[constr(max_length=10)] = None
    ongkos_kirim: condecimal(max_digits=10, decimal_places=2, ge=0)
    total_harga: condecimal(max_digits=10, decimal_places=2, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
    status: constr(max_length=50) = "pending"