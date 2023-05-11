import json

from database.db_connection import Base, engine
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, and_, func
import datetime
from database.db_session import session


class Series(Base):
    __tablename__ = "series"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    series_id = Column(Text)
    series_name = Column(Text)
    series_tags = Column(Text)
    series_views = Column(Text)
    series_languages = Column(Text)
    created_by = Column(Text)
    series_thumbnail = Column(Text)
    series_position = Column(Text)
    series_status = Column(Text)
    status = Column(Boolean)
    deleted = Column(Boolean)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, series_id=None, series_name=None, series_tags=None, series_views=None, series_languages=None,
                 created_by=None, series_thumbnail=None, series_position=None,
                 series_status=None, status=None, deleted=None):
        self.series_id = series_id
        self.series_name = series_name
        self.series_tags = series_tags
        self.series_views = series_views
        self.series_languages = series_languages
        self.created_by = created_by
        self.series_thumbnail = series_thumbnail
        self.series_position = series_position
        self.series_status = series_status
        self.status = status
        self.deleted = deleted

    @property
    def serialize(self):
        return {
            "id": self.id,
            "series_id": self.series_id,
            "series_name": self.series_name,
            "series_tags": self.series_tags,
            "series_views": self.series_views,
            "series_languages": self.series_languages,
            "created_by": self.created_by,
            "series_thumbnail": self.series_thumbnail,
            "series_position": self.series_position,
            "series_status": self.series_status,
            "status": self.status,
            "deleted": self.deleted,
            "created": self.created,
            "updated": self.updated,
        }


# function to create master series in db
def create_series(series_id, series_name, series_tags, created_by, series_thumbnail, series_position):

    # code to shift all previos position
    array = get_all_series_postion()
    array.sort()
    array = [int(x) for x in array]

    array.append(1)
    print(array)
    postion = series_position

    if postion in array:
        index_of_position = array.index(postion)
        for i in range(index_of_position, len(array)):
            if i == len(array) - 1:
                break
            else:
                temp = array[i]
                increment_series_position(array[i])
                array[i] = array[i] + 1
                if array[i + 1] - temp > 1:
                    break
    else:
        pass

    try:
        langauges = {
            "languages": {
                "data": [
                    {
                        "id": "lang_tifew",
                        "name": "English"
                    }
                ]
            }
        }
        # count = series_position

        series = Series(series_id=series_id,
                        series_name=series_name,
                        series_tags=series_tags,
                        series_views=0,
                        series_languages=json.dumps(langauges),
                        created_by=created_by,
                        series_thumbnail=series_thumbnail,
                        series_position=series_position,
                        series_status="Active",
                        status=1,
                        deleted=0)
        session.add(series)
        session.commit()
        session.refresh(series)

        return series.serialize if series is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def is_series_exist_by_name(series_name):
    try:
        series = session.query(Series).filter(Series.series_name == series_name) \
            .filter(Series.deleted == 0).count()
        return False if series == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()



def get_all_series_postion():
    try:
        series = session.query(Series).filter(Series.deleted == 0).all()
        return [res.serialize["series_position"] for res in series]
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def is_series_position_exists(position):
    try:
        series = session.query(Series).filter(Series.series_position == position) \
            .filter(Series.deleted == 0).count()
        return False if series == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def delete_series_by_id(series_id):
    try:
        result = session.query(Series).filter(Series.id == series_id) \
            .filter(Series.deleted == 0).first()
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


#
def increment_series_position(position):
    try:
        result = session.query(Series).filter(Series.series_position == position) \
            .filter(Series.deleted == 0).first()
        if result is not None:
            result.series_position = position + 1
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


def get_all_series():
    try:
        series = session.query(Series).filter(Series.deleted == 0).order_by(Series.series_position.desc()).all()
        return [res.serialize for res in series] if len(series) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def is_series_exist_by_language():
    try:
        series = session.query(Series).filter(Series.deleted == 0).order_by(Series.series_position.desc()).all()
        return [res.serialize for res in series] if len(series) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def get_filtered_series(title, tag, status):
    try:
        search_title = "%{}%".format(title)
        search_tag = "%{}%".format(tag)
        search_status = "%{}%".format(status)
        results = session.query(Series).filter(Series.series_name.like(search_title)).filter(
            Series.series_status.like(search_status)).filter(
            Series.deleted == 0).all()
        return [res.serialize for res in results] if len(results) != 0 else []
    except Exception as e:
        print(e)
        return []
    finally:
        session.remove()


def update_series_status(series_status, id):
    try:
        result = session.query(Series).filter(Series.id == id) \
            .filter(Series.deleted == 0).first()
        if result is not None:
            result.series_status = series_status
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


def update_series(series_name,  thumbnail, id, editseriestags):
    try:
        result = session.query(Series).filter(Series.id == id) \
            .filter(Series.deleted == 0).first()
        if result is not None:
            result.series_name = series_name
            result.series_tags = editseriestags
            # result.series_position = position
            if thumbnail != "undefined":
                result.series_thumbnail = thumbnail
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


def get_series_by_series_id(series_id):
    try:
        series = session.query(Series).filter(Series.id == series_id) \
            .filter(Series.deleted == 0).first()
        return series.serialize if series is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()

#
#
def is_series_exist(series_id):
    try:
        series = session.query(Series).filter(Series.id == series_id) \
            .filter(Series.deleted == 0).count()
        return False if series == 0 else True
    except Exception as e:
        print(e)
        return False
    finally:
        session.remove()


def update_series_view_count(series_id):
    try:
        result = session.query(Series).filter(Series.id == series_id) \
            .filter(Series.deleted == 0).first()
        if result is not None:
            result.series_views = int(result.series_views) + 1
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


def if_series_position_exist(series_id, position):
    # try:
    result = session.query(Series).filter(Series.id == series_id) \
        .filter(Series.deleted == 0).first()
    if result is not None:
        if result.series_position == position:
            return False
        else:
            return is_series_position_exists(position)
    else:
        return False
    # except Exception as e:
    #     print(e)
    #     return False
    # finally:
    #     session.remove()


def if_series_status_active(series_id):
    try:
        result = session.query(Series).filter(Series.id == series_id) \
            .filter(Series.deleted == 0).filter(Series.series_status == "Active").first()
        if result is not None:
            return True
        else:
            return False
    except Exception as e:

        print(e)
        return False
    finally:
        session.remove()


def move_series_position(position):
    array = get_all_series_postion()
    array.sort()
    array = [int(x) for x in array]
    array.append(1)
    if position in array:
        index_of_position = array.index(position)
        for i in range(index_of_position, len(array)):
            if i == len(array) - 1:
                break
            else:
                temp = array[i]
                increment_series_position(array[i])
                array[i] = array[i] + 1
                if array[i + 1] - temp > 1:
                    break
        return
    else:
        return


def updated_series_positions(update_positions, initial_rows):
    try:
        all_updated_positions = json.loads(update_positions)[::-1]
        initial_position = json.loads(initial_rows)
        error_flag = 1
        for series_position in range(len(all_updated_positions)):
            result = session.query(Series).filter(Series.id == all_updated_positions[series_position]["series_id"]) \
                .filter(Series.deleted == 0).first()
            if result is not None:
                print("-------------1------------")
                print(initial_position[series_position]["position"])
                print("----------1----------------")

                result.series_position = initial_position[series_position]["position"]
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


Base.metadata.create_all(engine)
