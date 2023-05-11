import json
import os

from model.language import is_language_exist_by_name, is_language_exist_by_name_diff_id
from model.series import is_series_exist_by_name, is_series_position_exists, if_series_position_exist
from model.series_episode_language import is_series_language_exist_by_name
from util.message import ApiMessage
from util.response import get_response
from util.utility import empty_param_check, is_region_valid, is_name_valid, is_id_valid, is_position_valid, \
    is_valid_thumbnail


def create_series_input_validation(request):
    input_form = request.form
    input_file = request.files

    if "series_name" not in input_form:
        return get_response(False, "Series name is missing", {})
    if "series_tags" not in input_form:
        return get_response(False, "Series tags is missing", {})

    if "series_position" not in input_form:
        return get_response(False, "Series position is missing", {})

    series_name = str(input_form.get('series_name')).strip()
    series_tags = str(input_form.get('series_tags')).strip()
    series_position = str(input_form.get('series_position')).strip()
    if 'series_thumbnail' not in input_form:
        series_thumbnail = input_file["series_thumbnail"]
    else:
        series_thumbnail = str(input_form["series_thumbnail"]).strip()
    try:
        if empty_param_check(series_name):
            data = get_response(False, "Please enter the series name", {})
        elif empty_param_check(series_position):
            data = get_response(False, "Please enter the position of the series", {})
        elif empty_param_check(series_tags):
            data = get_response(False, "Please enter the series tags", {})
        elif is_series_exist_by_name(series_name):
            data = get_response(False, "Series already exist with this name", {})
        elif not series_position.isnumeric():
            data = get_response(False, "You must enter a non negative numeric value in series position", {})
        elif not is_position_valid(series_position):
            data = get_response(False, "Position must be greater than zero", {})
        elif is_series_exist_by_name(series_name):
            data = get_response(False, "Series already exist with this name", {})

        else:
            data = get_response(True, ApiMessage.SUCCESS, {'series_name': series_name,
                                                           'series_position': series_position,
                                                           'series_thumbnail': series_thumbnail,
                                                           'series_tags': series_tags
                                                           })
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def edit_series_input_validation(request):
    input_form = request.form
    input_file = request.files
    current_series_thumnail = ''
    if "series_id" not in input_form:
        return get_response(False, "Series id is missing", {})

    if "series_name" not in input_form:
        return get_response(False, "Series name is missing", {})

    # if "series_position" not in input_form:
    #     return get_response(False, "Series position is missing", {})

    if "editseriestags" not in input_form:
        return get_response(False, "Series tag is missing position is missing", {})

    if "editThumbnail" in input_file:
        current_series_thumnail = input_file['editThumbnail']

    series_name = str(input_form.get('series_name')).strip()
    series_position = str(input_form.get('series_position')).strip()
    editseriestags = str(input_form.get('editseriestags')).strip()
    series_id = str(input_form.get('series_id')).strip()
    prev_series_thumbnail = str(input_form.get('series_thumbnail')).strip()
    # try:
    if empty_param_check(series_name):
        data = get_response(False, "Please enter the series name", {})
    # elif empty_param_check(series_position):
    #     data = get_response(False, "Please enter the position of the series", {})
    elif empty_param_check(editseriestags):
        data = get_response(False, "Please enter the tags of the series", {})
    elif empty_param_check(series_id):
        data = get_response(False, "Please enter the series id", {})
    # elif if_series_position_exist(series_id, series_position):
    #     data = get_response(False, "Series position already exists", {})
    # elif not series_position.isnumeric():
    #     data = get_response(False, "You must enter a non negative numeric value in series position", {})
    elif not series_id.isnumeric():
        data = get_response(False, "You must enter a non negative numeric value in series id", {})
    elif current_series_thumnail != '' and  not is_valid_thumbnail(current_series_thumnail):
        data = get_response(False, "Please enter a valid thumbnail", {})
    else:
        data = get_response(True, ApiMessage.SUCCESS, {'series_name': series_name,

                                                       'series_id': series_id,
                                                       'series_thumbnail': prev_series_thumbnail,
                                                       'editThumbnail': current_series_thumnail,
                                                       'editseriestags': editseriestags,
                                                       })
    # except Exception as e:
    #     data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def update_series_status_input_validation(request):
    input_form = request.form
    print(input_form)
    if "series_status" not in input_form:
        return get_response(False, "Series status is missing", {})
    elif "series_id" not in input_form:
        return get_response(False, "Series id is missing", {})
    series_status = str(input_form.get('series_status')).strip()
    series_id = str(input_form.get('series_id')).strip()

    try:
        if empty_param_check(series_status):
            data = get_response(False, "Please enter the series status", {})

        elif not is_name_valid(series_status):
            data = get_response(False, "Please enter a valid series status", {})

        elif series_status not in ["Active", "Deactivated", "In Progress"]:
            data = get_response(False, "Please enter a valid series status", {})
        elif empty_param_check(series_id):
            data = get_response(False, "Please enter the series id", {})

        elif not is_id_valid(series_id):
            data = get_response(False, "Please enter a valid series id", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'series_status': series_status, 'series_id': series_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def update_series_language_status_input_validation(request):
    input_form = request.form
    print(input_form)
    if "language_status" not in input_form:
        return get_response(False, "language status is missing", {})
    elif "language_id" not in input_form:
        return get_response(False, "language id is missing", {})
    language_status = str(input_form.get('language_status')).strip()
    language_id = str(input_form.get('language_id')).strip()

    try:
        if empty_param_check(language_status):
            data = get_response(False, "Please enter the language status", {})

        elif language_status not in ["Active", "Deactivated", "In Progress"]:
            data = get_response(False, "Please enter a valid language status", {})
        elif empty_param_check(language_id):
            data = get_response(False, "Please enter the language id", {})

        elif not is_id_valid(language_id):
            data = get_response(False, "Please enter a valid language id", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS,
                                {'language_status': language_status, 'language_id': language_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def series_details_input_validation(request):
    input_form = request.form
    if "series_id" not in input_form:
        return get_response(False, "Series id is missing", {})
    series_id = str(input_form.get('series_id')).strip()
    try:
        if empty_param_check(series_id):
            data = get_response(False, "Series id cannot be empty", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'series_id': series_id})
    except Exception as e:
        print(e)
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data


def delete_series_input_validation(request):
    input_form = request.form
    if "series_id" not in input_form:
        return get_response(False, "Series id is missing", {})

    series_id = str(input_form.get('series_id')).strip()

    try:
        if empty_param_check(series_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'series_id': series_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def delete_language_support_for_series_input_validation(request):
    input_form = request.form
    if "language_id" not in input_form:
        return get_response(False, "Language id is missing", {})

    language_id = str(input_form.get('language_id')).strip()

    try:
        if empty_param_check(language_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language_id': language_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def series_language_input_validation(request):
    input_form = request.form
    if "language_id" not in input_form:
        return get_response(False, "Language id is missing", {})
    language_id = str(input_form.get('language_id')).strip()
    try:
        if empty_param_check(language_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language_id': language_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data


def add_language_input_validation(request):
    input_form = request.form
    input_file = request.files
    if "language_id" not in input_form:
        return get_response(False, "Language id is missing", {})
    language_id = str(input_form.get('language_id')).strip()
    if "series_id" not in input_form:
        return get_response(False, "Series id is missing", {})
    if "language_name" not in input_form:
        return get_response(False, "Language name is missing", {})
    if "title" not in input_form:
        return get_response(False, "Language title is missing", {})
    if 'description' not in input_form:
        return get_response(False, "Language description is missing", {})
    series_id = str(input_form.get('series_id')).strip()
    language_id = str(input_form.get('language_id')).strip()
    languageID = str(input_form.get('languageId')).strip()
    language_name = str(input_form.get('language_name')).strip()
    title = str(input_form.get('title')).strip()
    description = str(input_form.get('description')).strip()
    if empty_param_check(series_id):
        data = get_response(False, "Please enter the series id", {})
    elif not series_id.isnumeric():
        data = get_response(False, "You must enter a non negative numeric value in series id", {})
    elif empty_param_check(language_name):
        data = get_response(False, "Please enter language name", {})
    elif empty_param_check(title):
        data = get_response(False, "Please enter language title", {})
    elif empty_param_check(description):
        data = get_response(False, "Please enter a valid description", {})
    # elif not is_name_valid(title):
    #     data = get_response(False, "Please enter a valid title", {})
    elif language_id == "" and is_series_language_exist_by_name(language_name, series_id):
        data = get_response(False, "Language already exist for series", {})
    else:
        print("----------------1---------------")
        data = get_response(True, ApiMessage.SUCCESS, {'series_id': series_id,
                                                       'language_id': language_id,
                                                       'languageID': languageID,
                                                       'language_name': language_name,
                                                       'title': title,
                                                       'description': description,
                                                       })

    # except Exception as e:
    #     data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data
