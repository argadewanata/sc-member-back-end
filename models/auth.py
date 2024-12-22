from pydantic import BaseModel

class PasswordChangeRequest(BaseModel):
    newPassword: str