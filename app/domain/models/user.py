from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    document: str = ""
    name: str = ""
    lastname: str = ""
    phone: Optional[str] = None
    email: str = ""
    created_at: Optional[datetime] = None
    is_active: bool = True