from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.schema import Table
from datetime import datetime
from sqlalchemy.orm.attributes import QueryableAttribute

def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
Base = automap_base()
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:pass@localhost/smart_lock"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 'base' reflects the tables in the Database
Base.prepare(engine, reflect=True)
#mapped classes are now created with names by default matching that of table name
user = Base.classes.user
session_factory = sessionmaker(bind=engine)
session = session_factory()
#query data test
Users = session.query(user).all()
for Pin_Code in Users:
    print(Pin_Code)



