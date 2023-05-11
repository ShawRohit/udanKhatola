import json

from model.language import is_language_exist_by_name, is_language_exist_by_name_diff_id
from util.message import LanguageMessages, ApiMessage
from util.response import get_response
from util.utility import empty_param_check, is_region_valid, is_name_valid, num_validation, is_num_validation, \
    is_id_valid, is_valid_thumbnail


def create_language_input_validation(request):
    input_form = request.form
    input_file = request.files
    if "regional_language_id" not in input_form:
        return get_response(False, LanguageMessages.regionalLanguageIdMissing, {})

    if 'language_icon' not in input_file:
        return get_response(False, "Language icon is missing", {})

    if "language_name" not in input_form:
        return get_response(False, LanguageMessages.languageNameMissing, {})

    if "region" not in input_form:
        return get_response(False, LanguageMessages.regionMissing, {})

    regional_language_id = str(input_form.get('regional_language_id')).strip()
    language_name = str(input_form.get('language_name')).strip()
    region = str(input_form.get('region')).strip()
    language_icon = input_file["language_icon"]

    try:
        # if empty_param_check(regional_language_id):
        #     data = get_response(False, ApiMessage.BLANK_REGIONAL_LANGUAGE_ID, {})
        if empty_param_check(language_name):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_NAME, {})
        elif empty_param_check(region):
            data = get_response(False, ApiMessage.BLANK_REGION, {})

        # elif not is_name_valid(language_name):
        #     data = get_response(False, ApiMessage.INVALID_LANGUAGE_NAME, {})
        elif is_language_exist_by_name(language_name):
            data = get_response(False, "Language already exist with this name", {})
        elif not is_valid_thumbnail(language_icon):
            data = get_response(False, "Please upload a valid language icon file", {})
        elif not is_region_valid(region):
            data = get_response(False, ApiMessage.INVALID_REGION, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'regional_language_id': regional_language_id,
                                                           'language_name': language_name,
                                                           'language_icon': language_icon,
                                                           'region': region})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def edit_language_input_validation(request):
    input_form = request.form
    input_file = request.files
    if "language_id" not in input_form:
        return get_response(False, LanguageMessages.languageIdMissing, {})

    if "regional_language_id" not in input_form:
        return get_response(False, LanguageMessages.regionalLanguageIdMissing, {})

    if "language_name" not in input_form:
        return get_response(False, LanguageMessages.languageNameMissing, {})

    if "region" not in input_form:
        return get_response(False, LanguageMessages.regionMissing, {})

    if "language_icon" in input_file:
        language_icon = input_file['language_icon']
    else:
        language_icon = str(input_form.get('language_icon')).strip()

    language_id = str(input_form.get('language_id')).strip()
    regional_language_id = str(input_form.get('regional_language_id')).strip()
    language_name = str(input_form.get('language_name')).strip()
    region = str(input_form.get('region')).strip()

    try:
        # if empty_param_check(regional_language_id):
        #     data = get_response(False, ApiMessage.BLANK_REGIONAL_LANGUAGE_ID, {})
        if empty_param_check(language_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        elif empty_param_check(language_name):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_NAME, {})
        elif empty_param_check(region):
            data = get_response(False, ApiMessage.BLANK_REGION, {})

        # elif not is_name_valid(language_name):
        #     data = get_response(False, ApiMessage.INVALID_LANGUAGE_NAME, {})
        elif is_language_exist_by_name_diff_id(language_id, language_name):
            data = get_response(False, "Another language already exist with this name", {})

        elif language_icon != '' and not is_valid_thumbnail(language_icon):
            data = get_response(False, "Please upload a valid image file", {})
        elif not is_region_valid(region):
            data = get_response(False, ApiMessage.INVALID_REGION, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language_id': language_id,
                                                           'regional_language_id': regional_language_id,
                                                           'language_name': language_name,
                                                           'language_icon': language_icon,
                                                           'region': region})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def delete_language_input_validation(request):
    input_form = request.form
    if "language_id" not in input_form:
        return get_response(False, LanguageMessages.languageIdMissing, {})

    language_id = str(input_form.get('language_id')).strip()

    try:
        if empty_param_check(language_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language_id': language_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def language_details_input_validation(request):
    input_form = request.form
    if "language_id" not in input_form:
        return get_response(False, LanguageMessages.languageIdMissing, {})

    language_id = str(input_form.get('language_id')).strip()

    try:
        if empty_param_check(language_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language_id': language_id})
    except Exception as e:
        print(e)
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def add_keywords_input_validation(request):
    input_form = request.form
    if "language_id" not in input_form:
        return get_response(False, LanguageMessages.languageIdMissing, {})

    language_id = str(input_form.get('language_id')).strip()

    try:
        if empty_param_check(language_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language_id': language_id})
    except Exception as e:
        print(e)
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def update_keywords_input_validation(request):
    input_form = request.form
    if "language_keywords" not in input_form:
        return get_response(False, LanguageMessages.languageKeywordsMissing, {})

    language_keywords = json.dumps(json.loads(input_form.get('language_keywords')))
    print("---------11-----")
    print(language_keywords)
    print(is_num_validation(language_keywords))
    print("----222-----")
    try:
        if empty_param_check(language_keywords):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_KEYWORDS, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language_keywords': language_keywords})
    except Exception as e:
        print(e)
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def language_affix_input_validation(request):
    input_form = request.form
    if "language_id" not in input_form:
        return get_response(False, LanguageMessages.languageIdMissing, {})

    language_id = str(input_form.get('language_id')).strip()

    try:
        if empty_param_check(language_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language_id': language_id})
    except Exception as e:
        print(e)
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def update_language_status_input_validation(request):
    input_form = request.form
    if "language_status" not in input_form:
        return get_response(False, "language status is missing", {})
    elif "language_id" not in input_form:
        return get_response(False, "language id is missing", {})
    language_status = str(input_form.get('language_status')).strip()
    language_id = str(input_form.get('language_id')).strip()

    try:
        if empty_param_check(language_status):
            data = get_response(False, "Please enter the language status", {})
        elif language_status not in ["Active", "Inactive"]:
            data = get_response(False, "Please enter a valid language status", {})
        elif empty_param_check(language_id):
            data = get_response(False, "Please enter the language id", {})
        # elif not is_id_valid(language_id):
        #     data = get_response(False, "Please enter a valid language id", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS,
                                {'language_status': language_status, 'language_id': language_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data