from pydantic import BaseModel, Field, constr, conint
from datetime import datetime, date
from typing import Optional

class Member(BaseModel):
    id: int
    timestamp_daftar: datetime = Field(default_factory=datetime.now)
    email: str
    nama_lengkap: constr(max_length=255)
    provinsi: constr(max_length=255)
    kota: constr(max_length=255)
    kecamatan: Optional[constr(max_length=255)] = None
    kelurahan: Optional[constr(max_length=255)] = None
    alamat_lengkap: str
    nomor_whatsapp: constr(max_length=20)
    jenis_kelamin: constr(max_length=1, regex='^(L|P)$')
    tanggal_lahir: date
    pendidikan_terakhir: conint(ge=0, le=9)
    profesi: Optional[constr(max_length=255)] = None
    referensi: Optional[str] = None
    harapan: Optional[str] = None
    is_verified: bool = False
    is_active: bool = False