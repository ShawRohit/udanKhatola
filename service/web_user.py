from flask import session

from app_session.user_session import create_user_session
from model.web_user import get_web_user_by_email, get_admin_user_details_by_cognito_id, \
    update_forget_password_email_otp, get_user_obj_by_email
from service.cognito import app_user_login, cognito_set_password
from util.message import ApiMessage, Login
from util.send_email import email_forgot_password_otp
from util.utility import get_six_digit_number, get_current_time_milli_sec, get_response


def login_user(email, password):
    web_user = get_web_user_by_email(email)
    if web_user is not None:
        if not web_user:
            return {"status": False,
                    "message": "No user found"}
        else:
            return {"status": False,
                    "message": "No user found", "web_user": web_user}

    else:
        return {"status": False, "message": "No such profile found"}


def web_user_login(email, password):
    cognito_res = app_user_login(email, password)
    if cognito_res['status']:
        data = get_admin_user_details_by_cognito_id(cognito_res['cognito_id'])
        if data is None:
            return {'status': False, 'error_type': '', 'message': ApiMessage.INVALID_LOGIN}
        else:
            data['access_token'] = cognito_res['access_token']
            data['message'] = Login.L_success
            data['refresh_token'] = cognito_res['refresh_token']
            create_user_session(data)
            session.permanent = True
    else:
        data = cognito_res
    return data


def send_forgot_password_otp(email):
    forgot_password_email_otp = get_six_digit_number()
    forgot_password_email_otp_timestamp = get_current_time_milli_sec()
    db_res = update_forget_password_email_otp(email, forgot_password_email_otp,
                                              forgot_password_email_otp_timestamp)
    if db_res is not None:
        email_res = email_forgot_password_otp(forgot_password_email_otp, email)
        if email_res:
            return get_response(True, "Please check your email for a confirmation code", {})
        else:
            return get_response(False, "Failed to send the confirmation code, Please try again", {})
    else:
        return get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})


def change_forgot_password_by_otp(email, conf_code, password):
    user_obj = get_user_obj_by_email(email)
    current_time_stamp = get_current_time_milli_sec()
    if user_obj.forgot_password_otp_timestamp and user_obj.forgot_password_otp:
        otp_expire_time = int(user_obj.forgot_password_otp_timestamp) + 600000
        if int(user_obj.forgot_password_otp) == int(conf_code):
            if not int(current_time_stamp) > otp_expire_time:
                update_res = cognito_set_password(email, password)
                if update_res['status']:
                    res = get_response(True, "You’ve updated your password, please log in again", {})
                else:
                    res = get_response(False, "Unable to update your password", {})
            else:
                res = get_response(False, "Confirmation code expired, please try again", {})
        else:
            res = get_response(False, "Please enter the correct confirmation code", {})
    else:
        res = get_response(False, "Please request a confirmation code to change your password", {})
    return res
