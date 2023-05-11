from model.web_user import is_admin_user_email_exist
from util.message import InputFormValidation, ApiMessage
from util.utility import get_response, empty_param_check, is_email_valid, password_validation


def forgot_password_otp_input_validation(request):
    input_form = request.form
    if "email" not in input_form:
        return get_response(False, InputFormValidation.emailMission, {})

    email = str(input_form.get('email')).strip()
    try:
        if empty_param_check(email):
            data = get_response(False, ApiMessage.BLANK_EMAIL, {})
        elif not is_email_valid(email):
            data = get_response(False, ApiMessage.INVALID_EMAIL, {})
        elif not is_admin_user_email_exist(email):
            data = get_response(False, ApiMessage.EMAIL_NOT_EXIST, {})
        else:
            data = get_response(True, 'success', {'email': email})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data


def change_forgot_password_input_validation(request):
    input_form = request.form
    if "email" not in input_form:
        return get_response(False, InputFormValidation.emailMission, {})
    if "conf_code" not in input_form:
        return get_response(False, "Conf Code field Is Missing", {})
    if "password" not in input_form:
        return get_response(False, InputFormValidation.passwordMission, {})
    if "conf_password" not in input_form:
        return get_response(False, "Conf Password field Is Missing", {})

    email = str(input_form.get('email')).strip()
    conf_code = str(input_form.get('conf_code')).strip()
    password = str(input_form.get('password')).strip()
    conf_password = str(input_form.get('conf_password')).strip()

    try:
        if empty_param_check(email):
            data = get_response(False, ApiMessage.BLANK_EMAIL, {})
        elif empty_param_check(conf_code):
            data = get_response(False, 'Please enter the confirmation code', {})
        elif empty_param_check(password):
            data = get_response(False, ApiMessage.BLANK_PASSWORD, {})
        elif empty_param_check(conf_password):
            data = get_response(False, 'Please enter the confirm password', {})
        elif not is_email_valid(email):
            data = get_response(False, ApiMessage.INVALID_EMAIL, {})
        elif not conf_code.isnumeric() or len(conf_code) != 6:
            data = get_response(False, "Confirmation code must be a 6 digit numeric value", {})
        elif not password_validation(password):
            data = get_response(False, "Your password didn't match our criteria", {})
        elif not (password == conf_password):
            data = get_response(False, "Password and confirm password didn't match", {})
        elif not is_admin_user_email_exist(email):
            data = get_response(False, ApiMessage.EMAIL_NOT_EXIST, {})
        else:
            data = get_response(True, 'success', {'email': email, 'conf_code': conf_code,
                                                  'password': password})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data
