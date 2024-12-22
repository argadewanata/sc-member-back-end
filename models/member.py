from pydantic import BaseModel, Field, constr, conint
from datetime import datetime, date
from typing import List,Optional

class Member(BaseModel):
    id: int
    timestamp_daftar: datetime = Field(default_factory=datetime.now)
    email: str
    password: str
    nama_lengkap: constr(max_length=255)
    provinsi: Optional[constr(max_length=255)] = None
    kota: Optional[constr(max_length=255)] = None
    kecamatan: Optional[constr(max_length=255)] = None
    kelurahan: Optional[constr(max_length=255)] = None
    alamat_lengkap: Optional[str] = None
    nomor_whatsapp: constr(max_length=20)
    jenis_kelamin: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    pendidikan_terakhir: Optional[int] = None
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
    is_verified: bool
    is_active: bool
    is_admin: bool

class PaginatedMembersResponse(BaseModel):
    members: List[MemberResponse]
    total: int

class MemberCreate(BaseModel):
    nama_lengkap: constr(max_length=255)
    email: str
    nomor_whatsapp: constr(max_length=20)