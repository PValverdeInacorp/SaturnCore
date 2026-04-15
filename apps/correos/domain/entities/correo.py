from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Correo:
    destinatarios: List[str]
    asunto: str
    contenido_html: str
    cc: List[str] = field(default_factory=list)
    bcc: List[str] = field(default_factory=list)
    attachments: Optional[list] = field(default_factory=list)