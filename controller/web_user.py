from flask import Blueprint, request, json, session

from service.web_user import web_user_login, send_forgot_password_otp, change_forgot_password_by_otp
from validation.forgot_password_validation import forgot_password_otp_input_validation, \
    change_forgot_password_input_validation
from validation.user_login_validation import admin_user_login_input_validation

web_user = Blueprint('web_user_controller', __name__)


@web_user.route("/login", methods=["POST"])
def login_user():
    admin_user_login_validation = admin_user_login_input_validation(request)
    if not admin_user_login_validation['status']:
        data = admin_user_login_validation
    else:
        data = web_user_login(admin_user_login_validation['data']['email'],
                              admin_user_login_validation['data']['password'])
    return json.dumps(data)


@web_user.route("/forgot-password-otp", methods=["POST"])
def forgot_password_otp():
    forgot_password_otp_validation = forgot_password_otp_input_validation(request)
    print(forgot_password_otp_validation)
    if not forgot_password_otp_validation['status']:
        data = forgot_password_otp_validation
    else:
        data = send_forgot_password_otp(forgot_password_otp_validation['data']['email'])
    return json.dumps(data)


@web_user.route("/change-forgot-password", methods=["POST"])
def change_forgot_password():
    change_forgot_password_validation = change_forgot_password_input_validation(request)
    if not change_forgot_password_validation['status']:
        data = change_forgot_password_validation
    else:
        data = change_forgot_password_by_otp(change_forgot_password_validation['data']['email'],
                                             change_forgot_password_validation['data']['conf_code'],
                                             change_forgot_password_validation['data']['password'])
    return json.dumps(data)
