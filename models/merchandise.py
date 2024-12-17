from pydantic import BaseModel, constr, condecimal

class Merchandise(BaseModel):
    id: int
    nama_paket: constr(max_length=255)
    tshirt: bool = False
    hoodie: bool = False
    jaket: bool = False
    harga: condecimal(max_digits=10, decimal_places=2, ge=0)