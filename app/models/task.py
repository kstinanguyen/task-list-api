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

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data.get("title"),
            description=task_data.get("description"),
            is_complete=task_data.get("is_complete")
        )
