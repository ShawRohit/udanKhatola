import json

from database.db_connection import Base, engine
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, and_, func
import datetime
from database.db_session import session


class Episode(Base):
    __tablename__ = "episode"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    masterEpisodeId = Column(Text)
    episodeId = Column(Text)
    series_id = Column(Text)
    series_name = Column(Text)
    language_id = Column(Text)
    episode_name = Column(Text)
    episode_position = Column(Text)
    episode_tags = Column(Text)
    episode_views = Column(Text)
    episode_title = Column(Text)
    episode_description = Column(Text)
    episode_thumbnail = Column(Text)
    episode_video = Column(Text)
    episode_audio = Column(Text)
    episode_status = Column(Text)
    download_state = Column(Text)
    is_master_episode = Column(Boolean)
    created_by = Column(Text)
    status = Column(Boolean)
    deleted = Column(Boolean)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, masterEpisodeId=None, episodeId=None, series_id=None, series_name=None, language_id=None,
                 episode_name=None,
                 episode_position=None, episode_tags=None, episode_views=None, episode_title=None,
                 episode_description=None, episode_video=None, episode_audio=None, created_by=None,
                 episode_thumbnail=None,
                 episode_status=None, download_state=None, is_master_episode=None, status=None, deleted=None):
        self.masterEpisodeId = masterEpisodeId
        self.episodeId = episodeId
        self.series_id = series_id
        self.series_name = series_name
        self.language_id = language_id
        self.episode_name = episode_name
        self.episode_position = episode_position
        self.episode_tags = episode_tags
        self.episode_views = episode_views
        self.episode_title = episode_title
        self.episode_description = episode_description
        self.episode_video = episode_video
        self.episode_audio = episode_audio
        self.created_by = created_by
        self.episode_thumbnail = episode_thumbnail
        self.episode_status = episode_status
        self.download_state = download_state
        self.is_master_episode = is_master_episode
        self.status = status
        self.deleted = deleted

    @property
    def serialize(self):
        return {
            "id": self.id,
            "masterEpisodeId": self.masterEpisodeId,
            "episodeId": self.episodeId,
            "series_id": self.series_id,
            "series_name": self.series_name,
            "language_id": self.language_id,
            "episode_name": self.episode_name,
            "episode_position": self.episode_position,
            "episode_tags": self.episode_tags,
            "episode_views": self.episode_views,
            "episode_title": self.episode_title,
            "episode_description": self.episode_description,
            "episode_thumbnail": self.episode_thumbnail,
            "episode_video": self.episode_video,
            "episode_audio": self.episode_audio,
            "episode_status": self.episode_status,
            "download_state": self.download_state,
            "is_master_episode": self.is_master_episode,
            "created_by": self.created_by,
            "status": self.status,
            "deleted": self.deleted,
            "created": self.created,
            "updated": self.updated,
        }


# function to create master series in db
def create_episode(data_episode_id, masterEpisodeId, episodeId, series_id, series_name, language_id, episode_name,
                   episode_position,
                   episode_tags,
                   episode_title, episode_description, episode_video, episode_audio, is_master_episode, created_by,
                   episode_thumbnail):
    try:
        if data_episode_id == "" or data_episode_id is None or data_episode_id == "undefined":
            episode = Episode(masterEpisodeId=masterEpisodeId,
                              episodeId=episodeId,
                              series_id=series_id,
                              series_name=series_name,
                              language_id=language_id,
                              episode_name=episode_name,
                              episode_position=episode_position,
                              episode_tags=episode_tags,
                              episode_title=episode_title,
                              episode_description=episode_description,
                              episode_video=episode_video,
                              episode_audio=episode_audio,
                              episode_views=1,
                              created_by=created_by,
                              episode_thumbnail=episode_thumbnail,
                              episode_status="Active",
                              download_state="",
                              is_master_episode=is_master_episode,
                              status=1,
                              deleted=0)
            session.add(episode)
            session.commit()
            session.refresh(episode)
            return episode.serialize if episode is not None else None
        else:
            result = session.query(Episode).filter(Episode.id == data_episode_id) \
                .filter(Episode.deleted == 0).first()
            if result is not None:
                result.language_id = language_id
                # result.title = episode_title
                if episode_thumbnail is not None and episode_thumbnail != "":
                    result.episode_thumbnail = episode_thumbnail
                if episode_audio is not None and episode_audio != "":
                    result.episode_audio = episode_audio
                if episode_video is not None and episode_video != "":
                    result.episode_video = episode_video

                result.episode_title = episode_title
                result.episode_tags = episode_tags
                result.episode_description = episode_description
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


def is_episode_exist_by_name(episode_name):
    try:
        series = session.query(Episode).filter(Episode.episode_name == episode_name) \
            .filter(Episode.deleted == 0).count()
        return False if series == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def is_episode_exist_by_title(episode_title):
    try:
        series = session.query(Episode).filter(Episode.episode_title == episode_title) \
            .filter(Episode.deleted == 0).count()
        return False if series == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def update_episode_language_support_status(language_status, id):
    try:
        result = session.query(Episode).filter(Episode.id == id) \
            .filter(Episode.deleted == 0).first()
        if result is not None:
            result.episode_status = language_status
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


def update_download_state(episode_id, download_state):
    try:
        result = session.query(Episode).filter(Episode.episodeId == episode_id) \
            .filter(Episode.deleted == 0).first()
        print(result)
        if result is not None:
            result.download_state = download_state
            result.updated = datetime.datetime.utcnow()
            session.add(result)
            session.commit()
            session.refresh(result)
            return result.serialize
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def is_position_exist_by_series(series_id, position):
    try:
        series = session.query(Episode).filter(Episode.episode_position == position).filter(
            Episode.series_id == series_id) \
            .filter(Episode.deleted == 0).count()
        return False if series == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def is_episode_name_exist_by_series(series_id, episode_name):
    try:
        series = session.query(Episode).filter(Episode.episode_name == episode_name).filter(
            Episode.series_id == series_id) \
            .filter(Episode.deleted == 0).count()
        return False if series == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def is_episode_title_exist_by_series(series_id, episode_title):
    try:
        series = session.query(Episode).filter(Episode.episode_title == episode_title).filter(
            Episode.series_id == series_id) \
            .filter(Episode.deleted == 0).count()
        return False if series == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def get_episode_by_series_id(series_id):
    try:
        series = session.query(Episode).filter(Episode.deleted == 0).filter(Episode.series_id == series_id).filter(
            Episode.is_master_episode == 1).order_by(
            Episode.episode_position).all()
        return [res.serialize for res in series] if len(series) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_episode_count_for_language(masterEpisodeId):
    try:
        series = session.query(Episode).filter(Episode.deleted == 0).filter(
            Episode.masterEpisodeId == masterEpisodeId).filter(
            Episode.is_master_episode == 0).count()
        return series
    except Exception as e:
        print(e)
        return 0
    finally:
        session.remove()


def get_episode_by_id(episode_id):
    try:
        print(episode_id)
        episode = session.query(Episode).filter(Episode.deleted == 0).filter(Episode.id == episode_id).order_by(
            Episode.id.desc()).first()
        return episode.serialize
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_episode_by_episodeId(episode_id):
    try:
        episode = session.query(Episode).filter(Episode.deleted == 0).filter(Episode.episodeId == episode_id).order_by(
            Episode.id.desc()).first()
        if episode is not None:
            return episode.serialize
        return []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_episode_by_master_episode_id(episode_id):
    # try:
    episode = session.query(Episode).filter(Episode.deleted == 0).filter(
        Episode.masterEpisodeId == episode_id).first()
    if episode is not None:
        return episode.serialize
    else:
        return []
    # except Exception as e:
    #     print(e)
    #     return []
    # finally:
    #     session.remove()


def get_all_episode_by_master_episode_id(episode_id):
    try:
        series = session.query(Episode).filter(Episode.deleted == 0).filter(
            Episode.masterEpisodeId == episode_id).order_by(
            Episode.id.desc()).all()
        return [res.serialize for res in series] if len(series) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_all_master_episode():
    try:
        series = session.query(Episode).filter(Episode.deleted == 0).filter(Episode.is_master_episode == 1).order_by(
            Episode.id.desc()).all()
        return [res.serialize for res in series] if len(series) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_episodes_by_language_id(language_id):
    try:
        episodes = session.query(Episode).filter(Episode.deleted == 0).filter(Episode.episode_status == "Active").filter(
            Episode.language_id == language_id).order_by(
            Episode.id.desc()).all()
        return [res.serialize for res in episodes] if len(episodes) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_all_dubbed_episode(master_episode):
    try:
        series = session.query(Episode).filter(Episode.deleted == 0).filter(
            Episode.masterEpisodeId == master_episode).filter(Episode.is_master_episode == 0).order_by(
            Episode.id.desc()).all()
        return [res.serialize for res in series] if len(series) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_all_episode_count_by_master_episode_id(episode_id):
    try:
        series = session.query(Episode).filter(Episode.deleted == 0).filter(
            Episode.masterEpisodeId == episode_id).filter(Episode.is_master_episode == 0).count()
        return series
    except Exception as e:
        print(e)
        return 0
    finally:
        session.remove()


def update_epiose_status(episode_status, id):
    try:
        result = session.query(Episode).filter(Episode.id == id) \
            .filter(Episode.deleted == 0).first()
        if result is not None:
            result.episode_status = episode_status
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


def update_epiose_positions(update_positions, initial_rows):
    try:
        all_updated_positions = json.loads(update_positions)
        initial_position = json.loads(initial_rows)
        error_flag = 1
        for episode_position in range(len(all_updated_positions)):
            result = session.query(Episode).filter(Episode.id == all_updated_positions[episode_position]["episode_id"]) \
                .filter(Episode.deleted == 0).first()
            if result is not None:
                result.episode_position = initial_position[episode_position]["position"]
                result.updated = datetime.datetime.utcnow()
                session.add(result)
                session.commit()
                session.refresh(result)
            else:
                error_flag = 0
                break
        if error_flag == 1:
            return True
        return False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def get_episode_by_episode_id(episode_id):
    print(episode_id)
    try:
        episode = session.query(Episode).filter(Episode.id == episode_id) \
            .filter(Episode.deleted == 0).first()
        return episode.serialize if episode is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def is_episode_exists_by_id(episode_id):
    try:
        episode = session.query(Episode).filter(Episode.episodeId == episode_id) \
            .filter(Episode.deleted == 0).first()
        return True if episode is not None else False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def get_all_episode():
    try:
        episode = session.query(Episode).filter(Episode.deleted == 0).filter(Episode.episode_status == "Active").all()
        return [res.serialize for res in episode] if len(episode) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def is_episode_exist_by_language_id(masterEpisodeId, language_id):
    try:
        series = session.query(Episode).filter(Episode.deleted == 0).filter(
            Episode.masterEpisodeId == masterEpisodeId).filter(Episode.language_id == language_id).count()
        return True if series > 0 else False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def get_filtered_episode(query):
    try:
        search = "%{}%".format(query.lower())
        results = session.query(Episode).filter(func.lower(Episode.episode_title).like(search)).filter(
            Episode.deleted == 0).all()
        if results is not None:
            return [res.serialize for res in results]
        else:
            return []
    except Exception as e:
        return []
    finally:
        session.remove()


def update_epiosde(episode_name, thumbnail, id, position, tags, title, description, episode_audio_path,
                   episode_video_path):
    try:
        result = session.query(Episode).filter(Episode.id == id) \
            .filter(Episode.deleted == 0).first()
        if result is not None:
            result.episode_name = episode_name
            if thumbnail != "undefined" and thumbnail is not None:
                result.episode_thumbnail = thumbnail
            if episode_audio_path is not None:
                result.episode_audio = episode_audio_path
            if episode_video_path is not None:
                result.episode_video = episode_video_path
            result.episode_position = position
            result.episode_title = title
            result.episode_description = description
            result.episode_tags = tags
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


def update_episode_status(episode_status, id):
    try:
        result = session.query(Episode).filter(Episode.id == id) \
            .filter(Episode.deleted == 0).first()
        if result is not None:
            result.episode_status = episode_status
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


def update_episode_view_count(episode_id):
    try:
        result = session.query(Episode).filter(Episode.episodeId == episode_id) \
            .filter(Episode.deleted == 0).first()
        if result is not None:
            result.episode_views = int(result.episode_views) + 1
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


def delete_episode_by_id(episode_id):
    try:
        result = session.query(Episode).filter(Episode.id == episode_id) \
            .filter(Episode.deleted == 0).first()
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


def delete_episode_by_seriees_id(series_id):
    try:
        session.query(Episode).filter(Episode.series_id == series_id).update({Episode.deleted: 1})
        session.commit()
        session.remove()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def if_episode_position_exist(episode_id, position, series_id):
    try:
        result = session.query(Episode).filter(Episode.id == episode_id) \
            .filter(Episode.deleted == 0).first()
        if result is not None:
            if result.episode_position == position:
                return False
            else:
                return is_position_exist_by_series(series_id, position)
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def if_episode_name_exist(episode_id, episode_name, series_id):
    try:
        result = session.query(Episode).filter(Episode.id == episode_id) \
            .filter(Episode.deleted == 0).first()
        if result is not None:
            if result.episode_name == episode_name:
                return False
            else:
                return is_episode_name_exist_by_series(series_id, episode_name)
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def if_episode_title_exist(episode_id, episode_title, series_id):
    try:
        result = session.query(Episode).filter(Episode.id == episode_id) \
            .filter(Episode.deleted == 0).first()
        if result is not None:
            if result.episode_title == episode_title:
                return False
            else:
                return is_episode_title_exist_by_series(series_id, episode_title)
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


Base.metadata.create_all(engine)
