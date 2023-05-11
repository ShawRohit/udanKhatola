from database.db_connection import Base, engine
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, and_, func
import datetime
from database.db_session import session


class Language(Base):
    __tablename__ = "language"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    language_id = Column(Text)
    language_name = Column(Text)
    created_by = Column(Text)
    regional_language_id = Column(Text)
    language_icon_path = Column(Text)
    region = Column(Text)
    language_status = Column(Text)
    status = Column(Boolean)
    deleted = Column(Boolean)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, language_id=None, language_name=None, created_by=None, regional_language_id=None,
                 language_icon_path=None, region=None, language_status=None, status=None, deleted=None):
        self.language_id = language_id
        self.language_name = language_name
        self.created_by = created_by
        self.regional_language_id = regional_language_id
        self.language_icon_path = language_icon_path
        self.region = region
        self.language_status = language_status
        self.status = status
        self.deleted = deleted

    @property
    def serialize(self):
        return {
            "id": self.id,
            "language_id": self.language_id,
            "language_name": self.language_name,
            "created_by": self.created_by,
            "regional_language_id": self.regional_language_id,
            "language_icon_path": self.language_icon_path,
            "region": self.region,
            "language_status": self.language_status,
            "status": self.status,
            "deleted": self.deleted,
            "created": self.created,
            "updated": self.updated,
        }


# function to create languages in db
def create_language(language_id, language_name, created_by, regional_language_id, language_icon_path,region):
    try:
        language = Language(language_id=language_id,
                            language_name=language_name,
                            created_by=created_by,
                            regional_language_id=regional_language_id,
                            language_icon_path=language_icon_path,
                            region=region,
                            language_status="Active",
                            status=1,
                            deleted=0)
        session.add(language)
        session.commit()
        session.refresh(language)
        return language.serialize if language is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def edit_language_by_language_id(language_id, language_name, regional_language_id,language_icon_path, region):
    try:
        result = session.query(Language).filter(Language.language_id == language_id) \
                 .filter(func.lower(Language.language_name) != 'english') \
                 .filter(Language.deleted == 0).first()
        if result is not None:
            result.language_name = language_name
            result.regional_language_id = regional_language_id
            if language_icon_path != "" and language_icon_path is not None:
                result.language_icon_path = language_icon_path
            result.region = region
            result.updated = datetime.datetime.utcnow()
            session.add(result)
            session.commit()
            session.refresh(result)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def is_language_exist_by_name(language_name):
    try:
        language = session.query(Language).filter(Language.language_name == language_name)\
            .filter(Language.deleted == 0).count()
        return False if language == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def is_language_exist_by_name_diff_id(language_id, language_name):
    try:
        language = session.query(Language).filter(Language.language_name == language_name)\
            .filter(Language.language_id != language_id)\
            .filter(Language.deleted == 0).count()
        return False if language == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def delete_language_by_language_id(language_id):
    try:
        result = session.query(Language).filter(Language.language_id == language_id)\
                 .filter(func.lower(Language.language_name) != 'english')\
                 .filter(Language.deleted == 0).first()
        if result is not None:
            result.deleted = 1
            result.updated = datetime.datetime.utcnow()
            session.add(result)
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def get_all_languages():
    try:
        language = session.query(Language).filter(Language.language_status == "Active").filter(Language.deleted == 0).order_by(Language.id.desc()).all()
        return [res.serialize for res in language] if len(language) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_all_languages_in_web():
    try:
        language = session.query(Language).filter(Language.deleted == 0).order_by(Language.id.desc()).all()
        return [res.serialize for res in language] if len(language) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_language_by_language_id(language_id):
    try:
        language = session.query(Language).filter(Language.language_id == language_id)\
            .filter(Language.deleted == 0).first()
        return language.serialize if language is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def get_language_name_by_language_id(language_id):
    try:
        language = session.query(Language).filter(Language.language_id == language_id)\
            .filter(Language.deleted == 0).first()
        return language.serialize["language_name"] if language is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def is_language_exist(language_id):
    try:
        language = session.query(Language).filter(Language.language_id == language_id)\
            .filter(Language.deleted == 0).count()
        return False if language == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def is_language_english(language_id):
    try:
        language = session.query(Language).filter(Language.language_id == language_id)\
            .filter(func.lower(Language.language_name) == 'english').count()
        return False if language == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def update_language_status(language_status,language_id):
    try:
        result = session.query(Language).filter(Language.language_id == language_id) \
                 .filter(Language.deleted == 0).first()
        if result is not None:
            result.language_status = language_status
            result.updated = datetime.datetime.utcnow()
            session.add(result)
            session.commit()
            session.refresh(result)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


Base.metadata.create_all(engine)
