import traceback

from flask import Blueprint, request, json

from app_session.user_session import is_user_active
from model.language import update_language_status
from service.language import create_language_db, edit_language_db, delete_language_db, get_language_details, \
    set_language_affix, update_keywords_db, add_keywords_db
from util.message import ApiMessage
from util.utility import get_response
from validation.language_validation import create_language_input_validation, edit_language_input_validation, \
    delete_language_input_validation, language_details_input_validation, language_affix_input_validation, \
    update_keywords_input_validation, add_keywords_input_validation, update_language_status_input_validation

language = Blueprint('language_controller', __name__)


@language.route('/create', methods=['POST'])
def create_language():
    try:
        if is_user_active():
            create_language_validation = create_language_input_validation(request)
            if not create_language_validation['status']:
                data = create_language_validation
            else:
                data = create_language_db(create_language_validation['data']['regional_language_id'],
                                          create_language_validation['data']['language_name'],
                                          create_language_validation['data']['language_icon'],
                                          create_language_validation['data']['region'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@language.route('/details', methods=['POST'])
def language_details():
    try:
        if is_user_active():
            language_details_validation = language_details_input_validation(request)
            if not language_details_validation['status']:
                data = language_details_validation
            else:
                data = get_language_details(language_details_validation['data']['language_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@language.route('/edit', methods=['POST'])
def edit_language():
    try:
        if is_user_active():
            edit_language_validation = edit_language_input_validation(request)
            if not edit_language_validation['status']:
                data = edit_language_validation
            else:
                data = edit_language_db(edit_language_validation['data']['language_id'],
                                        edit_language_validation['data']['regional_language_id'],
                                        edit_language_validation['data']['language_name'],
                                        edit_language_validation['data']['language_icon'],
                                        edit_language_validation['data']['region'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@language.route('/delete', methods=['POST'])
def delete_language():
    try:
        if is_user_active():
            delete_language_validation = delete_language_input_validation(request)
            if not delete_language_validation['status']:
                data = delete_language_validation
            else:
                data = delete_language_db(delete_language_validation['data']['language_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@language.route('/add_keywords', methods=['POST'])
def add_keywords():
    try:
        if is_user_active():
            add_keywords_validation = add_keywords_input_validation(request)
            if not add_keywords_validation['status']:
                data = add_keywords_validation
            else:
                data = add_keywords_db(add_keywords_validation['data']['language_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@language.route('/update_keywords', methods=['POST'])
def update_keywords():
    try:
        if is_user_active():
            update_keywords_validation = update_keywords_input_validation(request)
            if not update_keywords_validation['status']:
                data = update_keywords_validation
            else:
                data = update_keywords_db(update_keywords_validation['data']['language_keywords'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


# API for set language id for access in another page or another API
@language.route('/affix_id', methods=['POST'])
def api_restaurant_affix_id():
    try:
        if is_user_active():
            language_affix_validation = language_affix_input_validation(request)
            if language_affix_validation['status']:
                data = set_language_affix(language_affix_validation['data']['language_id'])
            else:
                data = language_affix_validation
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@language.route('/update-language-status', methods=['POST'])
def update_status():
    try:
        if is_user_active():
            update_language_status_validation = update_language_status_input_validation(request)
            if not update_language_status_validation['status']:
                data = update_language_status_validation
            else:
                data = update_language_status(update_language_status_validation['data']['language_status'],update_language_status_validation['data']['language_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)
