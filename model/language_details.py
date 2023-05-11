from database.db_connection import Base, engine
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, and_, func
import datetime
from database.db_session import session


class LanguageDetails(Base):
    __tablename__ = "language_details"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    language_id = Column(Text)
    language_keywords = Column(Text)
    status = Column(Boolean)
    deleted = Column(Boolean)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, language_id=None, language_keywords=None, status=None, deleted=None):
        self.language_id = language_id
        self.language_keywords = language_keywords
        self.status = status
        self.deleted = deleted

    @property
    def serialize(self):
        return {
            "id": self.id,
            "language_id": self.language_id,
            "language_keywords": self.language_keywords,
            "status": self.status,
            "deleted": self.deleted,
            "created": self.created,
            "updated": self.updated,
        }


# function to store language details in db
def create_language_details(language_id, language_keywords):
    try:
        language_details = LanguageDetails(language_id=language_id,
                                           language_keywords=language_keywords,
                                           status=1,
                                           deleted=0)
        session.add(language_details)
        session.commit()
        session.refresh(language_details)
        return language_details.serialize if language_details is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def update_language_details(language_id, language_keywords):
    try:
        result = session.query(LanguageDetails).filter(LanguageDetails.language_id == language_id) \
                 .filter(LanguageDetails.deleted == 0).first()
        if result is not None:
            result.language_keywords = language_keywords
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


def get_language_details_by_language_id(language_id):
    try:
        language = session.query(LanguageDetails).filter(LanguageDetails.language_id == language_id)\
            .filter(LanguageDetails.deleted == 0).first()
        return language.serialize if language is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def is_language_details_exist(language_id):
    try:
        language = session.query(LanguageDetails).filter(LanguageDetails.language_id == language_id)\
                   .filter(LanguageDetails.deleted == 0).count()
        return False if language == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


Base.metadata.create_all(engine)
