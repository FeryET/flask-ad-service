from flask_security.models import fsqla_v3 as fsqla
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=BaseModel, disable_autonaming=True)
fsqla.FsModels.set_db_info(db)
