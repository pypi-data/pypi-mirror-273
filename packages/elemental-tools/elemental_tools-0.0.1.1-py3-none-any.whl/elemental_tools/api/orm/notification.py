
from sqlalchemy import LargeBinary, CheckConstraint

from elemental_tools.pydantic import UserRoles
from elemental_tools.api.orm.user import TableUser
from elemental_tools.api.orm.smtp import TableSMTP
from elemental_tools.api.orm.template import TableTemplate

from elemental_tools.db.orm import SQLModel, relationship, AppendableTableArgs
from elemental_tools.db.constraints import constraint_notification_content
from elemental_tools.db import Column, Boolean, String, ForeignKey, JSONColumn, List, Dict, Mapped, \
    SQLEnum


class TableNotification(SQLModel):
    __tablename__ = 'notification'
    __table_args__ = AppendableTableArgs(
        CheckConstraint(
            "((content IS NULL or content = '') AND smtp_ref IS NOT NULL AND template_ref IS NOT NULL) or (content IS NOT NULL)",
            name="check_content_or_template"
        ),
    )

    sub: Mapped[str] = Column(String, ForeignKey(TableUser.ref), default=None)

    customer_ref: Mapped[str] = Column(String, ForeignKey(TableUser.ref), default=None)
    smtp_ref: Mapped[str] = Column(String, ForeignKey(TableSMTP.ref), nullable=True)
    template_ref: Mapped[str] = Column(String, ForeignKey(TableTemplate.ref), nullable=True)

    last_response_execution: Mapped[str] = Column(String, default=None)

    content: Mapped[str] = Column(String, nullable=True, default=None)

    status_wpp: Mapped[bool] = Column(Boolean, nullable=False, server_default="false")
    status_email: Mapped[bool] = Column(Boolean, nullable=False, server_default="false")

    role: List = JSONColumn(SQLEnum(UserRoles), default=[])
    modifiers: List = JSONColumn(default=None)
    variables: Dict = JSONColumn(default=None)

    customer = relationship("TableUser", foreign_keys=[customer_ref])
    smtp = relationship("TableSMTP", foreign_keys=[smtp_ref])
    template = relationship("TableTemplate", foreign_keys=[template_ref])

    # __table_args__ = AppendableTableArgs(CheckConstraint("((content IS NULL or content == "") AND smtp_ref IS NOT NULL AND template_ref IS NOT NULL) or (content IS NOT NULL)", name="check_content_or_template"))

