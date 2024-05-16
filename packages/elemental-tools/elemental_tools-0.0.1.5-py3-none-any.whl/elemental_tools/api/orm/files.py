from elemental_tools.db.constraints import constraint_unique
from elemental_tools.db.orm import SQLModel, AppendableTableArgs
from elemental_tools.db import String, Mapped, Column



class TableFiles(SQLModel):
    __tablename__ = "files"

    sub: Mapped[str] = Column(String, name="sub", nullable=False)
    institution_ref: Mapped[str] = Column(String, name="institution_ref", nullable=False)
    filename: Mapped[str] = Column(String, name="filename", nullable=False)

    __table_args__ = AppendableTableArgs(constraint_unique(filename, sub, institution_ref))

