import hashlib
from dataclasses import dataclass

from domain.values.user import Password


@dataclass
class PasswordService:

    def hash_password(self, plain_password: str) -> str:
        hashed = hashlib.sha256(plain_password.encode()).hexdigest()
        return hashed

    def check_password(self, plain_password: str, password: Password) -> bool:
        return self.hash_password(plain_password) == password.as_generic_type()
