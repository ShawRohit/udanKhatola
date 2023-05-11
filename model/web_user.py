from database.db_connection import Base, engine
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, and_
import datetime
from database.db_session import session


class WebUser(Base):
    __tablename__ = "web_users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    cognito_user_id = Column(Text)
    web_user_id = Column(Text)
    username = Column(Text)
    email = Column(Text)
    role = Column(Text)
    created_by = Column(Text)
    is_email_valid = Column(Boolean)
    status = Column(Boolean)
    deleted = Column(Boolean)
    account_otp = Column(Text)
    account_otp_timestamp = Column(Text)
    forgot_password_otp = Column(Text)
    forgot_password_otp_timestamp = Column(Text)

    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, cognito_user_id=None, web_user_id=None, username=None, email=None, role=None,
                 created_by=None, is_email_valid=None, status=None, deleted=None, account_otp=None,
                 account_otp_timestamp=None, forgot_password_otp=None, forgot_password_otp_timestamp=None):
        self.cognito_user_id = cognito_user_id
        self.web_user_id = web_user_id
        self.username = username
        self.email = email
        self.role = role
        self.created_by = created_by
        self.is_email_valid = is_email_valid
        self.status = status
        self.deleted = deleted
        self.account_otp = account_otp
        self.account_otp_timestamp = account_otp_timestamp
        self.forgot_password_otp = forgot_password_otp
        self.forgot_password_otp_timestamp = forgot_password_otp_timestamp

    @property
    def serialize(self):
        return {
            "id": self.id,
            "cognito_user_id": self.cognito_user_id,
            "web_user_id": self.web_user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_by": self.created_by,
            "is_email_valid": self.is_email_valid,
            "status": self.status,
            "deleted": self.deleted,
            "created": self.created,
            "updated": self.updated,
        }


# function to create web_users in db
def create_web_user(cognito_user_id, web_user_id, username, email, role, created_by, is_email_valid,
                    account_otp, account_otp_timestamp, status=1, deleted=0
                    ):
    try:
        web_user = WebUser(cognito_user_id=cognito_user_id, web_user_id=web_user_id, username=username, email=email,
                           role=role, created_by=created_by, is_email_valid=is_email_valid,
                           status=status, deleted=deleted, account_otp=account_otp,
                           account_otp_timestamp=account_otp_timestamp)
        session.add(web_user)
        session.commit()
        session.refresh(web_user)
        return web_user.serialize if web_user is not None else None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


# function to get web user details by email
def get_web_user_by_email(email):
    try:
        web_user = session.query(WebUser).filter(WebUser.email == email).filter(
            WebUser.deleted == 0).first()
        if web_user is not None:
            return web_user.serialize
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


def is_admin_user_email_exist(email):
    try:
        count = session.query(WebUser).filter(
            and_(WebUser.email == email, WebUser.deleted == 0)).count()
        print(count)
        return False if count == 0 else True
    except Exception as e:
        session.roleback()
        return False
    finally:
        session.remove()


def get_admin_user_details_by_cognito_id(cognitoid):
    try:
        user = session.query(WebUser).filter(
            and_(WebUser.cognito_user_id == cognitoid, WebUser.deleted == 0)).first()
        if user is not None:
            return user.serialize
        else:
            return None
    except Exception as e:
        return None
    finally:
        session.remove()


def update_forget_password_email_otp(email, forgot_password_otp,
                                     forgot_password_otp_timestamp):
    try:
        user = session.query(WebUser).filter(
            and_(WebUser.email == email, WebUser.deleted == 0)).first()
        if user is not None:
            user.forgot_password_otp = forgot_password_otp
            user.forgot_password_otp_timestamp = forgot_password_otp_timestamp
            user.updated = datetime.datetime.utcnow()
            session.add(user)
            session.commit()
            return user.serialize
        else:
            return None
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


# Fetching user details using email id
def get_user_obj_by_email(email):
    try:
        user = session.query(WebUser).filter(WebUser.email == email)\
            .filter(WebUser.deleted == 0).filter(WebUser.status == 1).first()
        return user
    except Exception as e:
        print(e)
        return None
    finally:
        session.remove()


Base.metadata.create_all(engine)
