from elemental_tools.config import config_initializer
from elemental_tools.db import text

from elemental_tools.logger import Logger

config = config_initializer()


class Declarative:

    @classmethod
    def get(cls) -> dict:
        return {key: item for key, item in cls.__dict__.items() if not key.startswith("_")}


class DDL(Declarative):
    ___logger__ = Logger(app_name=config.app_name, owner='installation', origin='ddl').log
    _session = None

    class Domains(Declarative):
        email = text("""DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.domains WHERE domain_name = 'email') THEN
                    CREATE DOMAIN email AS citext CHECK ( value ~ '^[a-zA-Z0-9.!#$%%&''*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$' );
                END IF;
            END $$;""")

    def __init__(self, session):
        self._session = session

    def __call__(self, *args, **kwargs):
        with self._session() as session:
            for subclass_name in self.get():
                for _name, raw in self.__getattribute__(subclass_name).get().items():
                    self.___logger__('info', f"Installing {_name} with DDL: {raw}", origin=_name)
                    session.execute(raw)
                    session.commit()

