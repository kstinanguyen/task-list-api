from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    is_complete: Mapped[bool] = mapped_column(default=False)

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete
        )
