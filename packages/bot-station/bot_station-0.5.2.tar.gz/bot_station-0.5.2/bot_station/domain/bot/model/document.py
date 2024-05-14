from dataclasses import dataclass, field


@dataclass
class Document:
    id: str = field()
    data: str = field()
    source_link: str | None = field(default=None)
    metadata: dict | None = field(default_factory=dict)
