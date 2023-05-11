import traceback

from flask import Blueprint, request, json

from app_session.user_session import is_user_active
from model.series import update_series_status, get_series_by_series_id, get_filtered_series, updated_series_positions
from model.series_episode_language import get_series_language_by_language_id, update_series_language_status
from service.language import create_language_db, edit_language_db, delete_language_db, get_language_details, \
    set_language_affix, update_keywords_db, add_keywords_db
from service.series import create_series_db, update_series_db, delete_series_db, add_language_for_series, \
    delete_series_language_support_db
from util.message import ApiMessage
from util.utility import get_response
from validation.language_validation import create_language_input_validation, edit_language_input_validation, \
    delete_language_input_validation, language_details_input_validation, language_affix_input_validation, \
    update_keywords_input_validation, add_keywords_input_validation
from validation.series_validation import create_series_input_validation, update_series_status_input_validation, \
    series_details_input_validation, edit_series_input_validation, delete_series_input_validation, \
    add_language_input_validation, series_language_input_validation, update_series_language_status_input_validation, \
    delete_language_support_for_series_input_validation

series = Blueprint('series_controller', __name__)


@series.route('/create', methods=['POST'])
def create_series():
    try:
        if is_user_active():
            create_series_validation = create_series_input_validation(request)
            if not create_series_validation['status']:
                data = create_series_validation
            else:
                data = create_series_db(create_series_validation['data']['series_name'],
                                        create_series_validation['data']['series_thumbnail'],
                                        create_series_validation['data']['series_position'],
                                        create_series_validation['data']['series_tags'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@series.route('/edit', methods=['POST'])
def edit_series():
    try:
        if is_user_active():
            edit_series_validation = edit_series_input_validation(request)
            if not edit_series_validation['status']:
                data = edit_series_validation
            else:
                data = update_series_db(edit_series_validation['data']['series_id'],
                                        edit_series_validation['data']['series_name'],
                                        edit_series_validation['data']['editThumbnail'],

                                        edit_series_validation['data']['series_thumbnail'],
                                        edit_series_validation['data']['editseriestags'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return data


@series.route('/update-series-status', methods=['POST'])
def update_series_status_api():
    try:
        if is_user_active():
            update_series_status_validation = update_series_status_input_validation(request)
            if not update_series_status_validation['status']:
                data = update_series_status_validation
            else:
                data = update_series_status(update_series_status_validation['data']['series_status'],
                                            update_series_status_validation['data']['series_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@series.route('/update-series-language-status', methods=['POST'])
def update_series_language_api():
    try:
        if is_user_active():
            update_series_language_status_validation = update_series_language_status_input_validation(request)
            if not update_series_language_status_validation['status']:
                data = update_series_language_status_validation
            else:
                data = update_series_language_status(update_series_language_status_validation['data']['language_status'],
                                            update_series_language_status_validation['data']['language_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@series.route('/details', methods=['POST'])
def series_details():
    try:
        if is_user_active():
            series_details_validation = series_details_input_validation(request)
            if not series_details_validation['status']:
                data = series_details_validation
            else:
                data = get_series_by_series_id(series_details_validation['data']['series_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@series.route('/series-language-details', methods=['POST'])
def series_language_details():
    try:
        if is_user_active():
            series_language_validation_resposnse= series_language_input_validation(request)
            if not series_language_validation_resposnse['status']:
                data = series_language_validation_resposnse
            else:
                data = get_series_language_by_language_id(series_language_validation_resposnse['data']['language_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@series.route('/delete', methods=['POST'])
def delete_language():
    try:
        if is_user_active():
            delete_series_validation = delete_series_input_validation(request)
            if not delete_series_validation['status']:
                data = delete_series_validation
            else:
                data = delete_series_db(delete_series_validation['data']['series_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@series.route('/get-filtered-data', methods=['POST'])
def get_filtered_data():
    try:
        if is_user_active():
            request_obj = request.form
            data = get_filtered_series(request_obj['title'],request_obj['tag'],request_obj['status'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@series.route('/delete-language-support', methods=['POST'])
def delete_language_support():
    try:
        if is_user_active():
            delete_series_language_validation = delete_language_support_for_series_input_validation(request)
            if not delete_series_language_validation['status']:
                data = delete_series_language_validation
            else:
                data = delete_series_language_support_db(delete_series_language_validation['data']['language_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@series.route('/add-language', methods=['POST'])
def add_language():
    # try:
    if is_user_active():
        add_language_for_series_validation = add_language_input_validation(request)
        if not add_language_for_series_validation['status']:
            data= add_language_for_series_validation
        else:
            print(add_language_for_series_validation)
            data = add_language_for_series(add_language_for_series_validation['data']['series_id'],
                                           add_language_for_series_validation['data']['language_name'],
                                           add_language_for_series_validation['data']['language_id'],
                                           add_language_for_series_validation['data']['languageID'],
                                           add_language_for_series_validation['data']['title'],
                                           add_language_for_series_validation['data']['description']
                                           )
    else:
        data = get_response(False, ApiMessage.INVALID_SESSION, {})
    # except Exception as e:
    #     print(traceback.format_exc())
    #     data = get_response(False, str(e), {})
    return json.dumps(data)


@series.route('/update-series-positions', methods=['POST'])
def update_series_positions():
    try:
        if is_user_active():
            updated_rows = request.form.get("updated_rows")
            initial_rows = request.form.get("initial_rows")
            print(updated_rows)
            print(initial_rows)
            response = updated_series_positions(updated_rows, initial_rows)
            if response:
                data = get_response(True, "Series update successfully", {})
            else:
                data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)

