from database.db_connection import Base, engine
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, and_, func
import datetime
from database.db_session import session


class EpisodeLanguage(Base):
    __tablename__ = "episode_language"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    language_name = Column(Text)
    episode_thumbnail = Column(Text)
    episode_video = Column(Text)
    episode_audio = Column(Text)
    title = Column(Text)
    tags = Column(Text)
    description = Column(Text)
    series_id = Column(Text)
    series_name = Column(Text)
    episode_id = Column(Text)
    created_by = Column(Text)
    language_status = Column(Text)
    status = Column(Boolean)
    deleted = Column(Boolean)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, language_name=None, episode_thumbnail=None, episode_video=None, episode_audio=None, title=None,
                 tags=None, description=None, series_id=None, series_name=None,
                 episode_id=None, created_by=None,
                 language_status=None, status=None, deleted=None):
        self.language_name = language_name
        self.episode_thumbnail = episode_thumbnail
        self.episode_video = episode_video
        self.episode_audio = episode_audio
        self.title = title
        self.tags = tags
        self.description = description
        self.series_id = series_id
        self.series_name = series_name
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
            "episode_thumbnail": self.episode_thumbnail,
            "episode_video": self.episode_video,
            "episode_audio": self.episode_audio,
            "title": self.title,
            "tags": self.tags,
            "description": self.description,
            "series_id": self.series_id,
            "series_name": self.series_name,
            "episode_id": self.episode_id,
            "created_by": self.created_by,
            "language_status": self.language_status,
            "status": self.status,
            "deleted": self.deleted,
            "created": self.created,
            "updated": self.updated,
        }


# function to create languages in db
def add_edit_language(language_id, language_name, thumbnail, audio, video, title, tags, description, series_id,
                      series_name, episode_id, created_by):
    try:

        if language_id == "" or language_id == "undefined":
            print("here---------")
            language = EpisodeLanguage(language_name=language_name,
                                       episode_thumbnail=thumbnail,
                                       episode_video=video,
                                       episode_audio=audio,
                                       created_by=created_by,
                                       title=title,
                                       tags=tags,
                                       description=description,
                                       series_id=series_id,
                                       series_name=series_name,
                                       episode_id=episode_id,
                                       language_status="Active",
                                       status=1,
                                       deleted=0)
            session.add(language)
            session.commit()
            session.refresh(language)
            return language.serialize if language is not None else None
        else:
            result = session.query(EpisodeLanguage).filter(EpisodeLanguage.id == language_id) \
                .filter(EpisodeLanguage.deleted == 0).first()
            if result is not None:
                result.language_name = language_name
                result.title = title
                if thumbnail is not None and thumbnail != "":
                    result.thumbnail = thumbnail
                if audio is not None and audio != "":
                    result.episode_audio = audio
                if audio is not None and audio != "":
                    result.episode_audio = audio

                result.title = title
                result.tags = tags
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


def update_episode_language_status(language_status, id):
    try:
        result = session.query(EpisodeLanguage).filter(EpisodeLanguage.id == id) \
            .filter(EpisodeLanguage.deleted == 0).first()
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


def is_episode_language_exist(language_id):
    try:
        language = session.query(EpisodeLanguage).filter(EpisodeLanguage.id == language_id) \
            .filter(EpisodeLanguage.deleted == 0).count()
        return False if language == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def delete_episode_language_support_by_id(language_id):
    try:
        result = session.query(EpisodeLanguage).filter(EpisodeLanguage.id == language_id) \
            .filter(EpisodeLanguage.deleted == 0).first()
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


def update_episode_language_support_status(language_status, id):
    print("print after update")
    print(language_status)
    result = session.query(EpisodeLanguage).filter(EpisodeLanguage.id == id) \
        .filter(EpisodeLanguage.deleted == 0).first()
    if result is not None:
        result.language_status = language_status
        result.updated = datetime.datetime.utcnow()
        session.add(result)
        session.commit()
        session.refresh(result)
        return True
    else:
        return False


def get_language_by_episode_id(episode_id):
    try:
        language = session.query(EpisodeLanguage).filter(EpisodeLanguage.episode_id == episode_id) \
            .filter(EpisodeLanguage.deleted == 0).all()
        return [x.serialize for x in language]
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def get_episode_language_by_language_id(language_id):
    try:
        language = session.query(EpisodeLanguage).filter(EpisodeLanguage.id == language_id) \
            .filter(EpisodeLanguage.deleted == 0).first()
        return language.serialize if language is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


Base.metadata.create_all(engine)
