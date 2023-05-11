from model.web_user import is_admin_user_email_exist
from util.message import InputFormValidation, ApiMessage
from util.utility import get_response, empty_param_check, is_email_valid


def admin_user_login_input_validation(request):
    input_form = request.form
    if "email" not in input_form:
        return get_response(False, InputFormValidation.emailMission, {})

    if "password" not in input_form:
        return get_response(False, InputFormValidation.passwordMission, {})

    email = str(input_form.get('email')).strip()
    password = str(input_form.get('password')).strip()
    try:
        if empty_param_check(email):
            data = get_response(False, ApiMessage.BLANK_EMAIL, {})
        elif empty_param_check(password):
            data = get_response(False, ApiMessage.BLANK_PASSWORD, {})

        elif not is_email_valid(email):
            data = get_response(False, ApiMessage.INVALID_EMAIL, {})
        elif not is_admin_user_email_exist(email):
            data = get_response(False, ApiMessage.EMAIL_NOT_EXIST, '')
        else:
            data = get_response(True, 'success', {'email': email, 'password': password})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, '')
    return data
