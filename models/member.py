from pydantic import BaseModel, Field, constr, conint
from datetime import datetime, date
from typing import List,Optional

class Member(BaseModel):
    id: int
    timestamp_daftar: datetime = Field(default_factory=datetime.now)
    email: str
    password: str
    nama_lengkap: constr(max_length=255)
    provinsi: constr(max_length=255)
    kota: constr(max_length=255)
    kecamatan: Optional[constr(max_length=255)] = None
    kelurahan: Optional[constr(max_length=255)] = None
    alamat_lengkap: str
    nomor_whatsapp: constr(max_length=20)
    jenis_kelamin: str = Field(..., max_length=1, pattern='^(L|P)$')
    tanggal_lahir: date
    pendidikan_terakhir: int = Field(..., ge=0, le=9)
    profesi: Optional[constr(max_length=255)] = None
    referensi: Optional[str] = None
    harapan: Optional[str] = None
    is_verified: bool = False
    is_active: bool = False
    is_admin: bool = False

class MemberResponse(BaseModel):
    id: int
    nama_lengkap: str
    email: str
    nomor_whatsapp: str

class PaginatedMembersResponse(BaseModel):
    members: List[MemberResponse]
    total: int