from icecream import ic
import inspect

from sqlalchemy import CheckConstraint, UniqueConstraint, text, Column

from elemental_tools.constants import ref_length


def constraint_unique(*fields, postgresql_nulls_not_distinct: bool = True) -> UniqueConstraint:
    name = f"unique_{'+'.join([str(f) for f in fields])}"
    return UniqueConstraint(*fields, name=name, postgresql_nulls_not_distinct=postgresql_nulls_not_distinct)


def constraint_email():
    return CheckConstraint("email ~* '^[a-zA-Z0-9]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\.]+$'", name='check_valid_email'),


def constraint_object_id(column_name: str):
    return CheckConstraint(f"LENGTH({column_name}) = {str(ref_length)} or {column_name} IS NULL", name=f"check_{column_name}_object_id")


constraint_password_length = CheckConstraint("LENGTH(password) >= 6 OR password IS NULL", name="check_password_length")
constraint_notification_content = CheckConstraint("((content IS NULL or content = "") AND smtp_ref IS NOT NULL AND template_ref IS NOT NULL) or (content IS NOT NULL)", name="check_content_or_template")

constraint_setting_name = CheckConstraint("""((name = 'root_ref' and sub IS NULL) or (name != 'root_ref'))""", name="root_ref_allow_only_null_sub")
constraint_cnpj = CheckConstraint("tax_number ~ '^[0-9]{2}\.[0-9]{3}\.[0-9]{3}\/[0-9]{4}\-[0-9]{2}$'")
constraint_cpf = CheckConstraint("doc_number ~ '^[0-9]{3}\.[0-9]{3}\.[0-9]{3}\-[0-9]{2}$'")

