from database.db_connection import Base, engine
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, and_, func
import datetime
from database.db_session import session


class SeriesEpisodeLanguage(Base):
    __tablename__ = "series_episode_language"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    language_name = Column(Text)
    languageId = Column(Text)
    thumbnail = Column(Text)
    title = Column(Text)
    tags = Column(Text)
    description = Column(Text)
    series_id = Column(Text)
    episode_id = Column(Text)
    created_by = Column(Text)
    language_status = Column(Text)
    status = Column(Boolean)
    deleted = Column(Boolean)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, language_name=None,languageId=None, thumbnail=None, title=None, tags=None, description=None, series_id=None,
                 episode_id=None, created_by=None,
                 language_status=None, status=None, deleted=None):
        self.language_name = language_name
        self.languageId = languageId
        self.thumbnail = thumbnail
        self.title = title
        self.tags = tags
        self.description = description
        self.series_id = series_id
        self.episode_id = episode_id
        self.created_by = created_by
        self.language_status = language_status
        self.status = status
        self.deleted = deleted

    @property
    def serialize(self):
        return {
            "id": self.id,
            "language_name": self.language_name,
            "languageId": self.languageId,
            "thumbnail": self.thumbnail,
            "title": self.title,
            "tags": self.tags,
            "description": self.description,
            "series_id": self.series_id,
            "episode_id": self.episode_id,
            "created_by": self.created_by,
            "language_status": self.language_status,
            "status": self.status,
            "deleted": self.deleted,
            "created": self.created,
            "updated": self.updated,
        }


# function to create languages in db
def insert_language(language_id, language_name,languageId,  title, description, series_id, episode_id, created_by):
    try:

        if language_id == "" or language_id == "undefined":
            language = SeriesEpisodeLanguage(language_name=language_name,
                                             thumbnail="thumbnail",
                                             created_by=created_by,
                                             title=title,
                                             tags="tags",
                                             description=description,
                                             series_id=series_id,
                                             languageId=languageId,
                                             episode_id=episode_id,
                                             language_status="Active",
                                             status=1,
                                             deleted=0)
            session.add(language)
            session.commit()
            session.refresh(language)
            return language.serialize if language is not None else None
        else:
            print("--okay------")
            result = session.query(SeriesEpisodeLanguage).filter(SeriesEpisodeLanguage.id == language_id) \
                .filter(SeriesEpisodeLanguage.deleted == 0).first()
            if result is not None:
                result.language_name = language_name
                result.title = title
                result.description = description
                result.updated = datetime.datetime.utcnow()
                session.add(result)
                session.commit()
                session.refresh(result)
                return True
            else:
                return False
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def update_series_language_status(language_status,id):
    try:
        result = session.query(SeriesEpisodeLanguage).filter(SeriesEpisodeLanguage.id == id) \
                 .filter(SeriesEpisodeLanguage.deleted == 0).first()
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


def is_series_language_exist(language_id):
    try:
        language = session.query(SeriesEpisodeLanguage).filter(SeriesEpisodeLanguage.id == language_id)\
            .filter(SeriesEpisodeLanguage.deleted == 0).count()
        return False if language == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def is_series_languageName_exist(language_name):
    try:
        language = session.query(SeriesEpisodeLanguage).filter(SeriesEpisodeLanguage.language_name == language_name)\
            .filter(SeriesEpisodeLanguage.deleted == 0).count()
        return False if language == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def get_language_count_by_series_id(series_id):
    try:
        language = session.query(SeriesEpisodeLanguage).filter(SeriesEpisodeLanguage.series_id == series_id) \
            .filter(SeriesEpisodeLanguage.deleted == 0).count()
        return language
    except Exception as e:
        print(e)
        return 0
    finally:
        session.remove()


def is_series_language_exist_by_name(language_name, series_id):
    try:
        language = session.query(SeriesEpisodeLanguage).filter(SeriesEpisodeLanguage.series_id == series_id).filter(SeriesEpisodeLanguage.language_name == language_name)\
            .filter(SeriesEpisodeLanguage.deleted == 0).count()
        return False if language == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()

def delete_series_language_support_by_id(language_id):
    try:
        result = session.query(SeriesEpisodeLanguage).filter(SeriesEpisodeLanguage.id == language_id)\
                 .filter(SeriesEpisodeLanguage.deleted == 0).first()
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

def get_language_by_series_id(series_id):
    try:
        language = session.query(SeriesEpisodeLanguage).filter(SeriesEpisodeLanguage.series_id == series_id) \
            .filter(SeriesEpisodeLanguage.deleted == 0).all()
        return [x.serialize for x in language]
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def get_series_language_by_language_id(language_id):
    try:
        language = session.query(SeriesEpisodeLanguage).filter(SeriesEpisodeLanguage.id == language_id) \
            .filter(SeriesEpisodeLanguage.deleted == 0).first()
        return language.serialize if language is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


Base.metadata.create_all(engine)
