import traceback

from flask import Blueprint, request, json, session

from app_session.user_session import is_user_active
from model.episode import get_episode_by_episode_id, update_episode_status, delete_episode_by_id, get_episode_by_id, \
    update_epiose_positions, get_all_episode, update_download_state,update_episode_language_support_status
from model.episode_language import  delete_episode_language_support_by_id
from service.episode import create_episode_db, update_episode_db, create_language_support_episode_db
from util.message import ApiMessage
from util.utility import get_response
from validation.episode_validation import create_episode_input_validation, episode_details_input_validation, \
    edit_episode_input_validation, update_episode_status_input_validation, delete_episode_input_validation, \
    create_language_support_input_validation, episode_language_support_details_input_validation, \
    delete_language_support_input_validation, update_language_support_status_input_validation, \
    update_episode_download_input_validation

episode = Blueprint('episode_controller', __name__)


@episode.route('/create', methods=['POST'])
def create_episode():
    try:
        if is_user_active():
            create_episode_validation = create_episode_input_validation(request)
            if not create_episode_validation['status']:
                data = create_episode_validation
            else:
                data = create_episode_db(create_episode_validation['data']['series_id'],
                                         session["series_name"],
                                         create_episode_validation['data']['episode_name'],
                                         create_episode_validation['data']['episode_thumbnail'],
                                         create_episode_validation['data']['episode_position'],
                                         create_episode_validation['data']['episodetags'],
                                         create_episode_validation['data']['episode_title'],
                                         create_episode_validation['data']['episode_description'],
                                         create_episode_validation['data']['episode_audio'],
                                         create_episode_validation['data']['episode_video'],
                                         )
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/edit', methods=['POST'])
def edit_episode():
    try:
        if is_user_active():
            edit_episode_validation = edit_episode_input_validation(request)
            if not edit_episode_validation['status']:
                data = edit_episode_validation
            else:
                data = update_episode_db(edit_episode_validation['data']['episode_id'],
                                         edit_episode_validation['data']['episode_name'],
                                         edit_episode_validation['data']['current_episode_thumnail'],
                                         edit_episode_validation['data']['prev_episode_thumbnail'],
                                         edit_episode_validation['data']['episode_position'],
                                         edit_episode_validation['data']['episode_tags'],
                                         edit_episode_validation['data']['episode_title'],
                                         edit_episode_validation['data']['episode_description'],
                                         edit_episode_validation['data']['current_episode_audio'],
                                         edit_episode_validation['data']['current_episode_video'],
                                         )

        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return data


@episode.route('/add-edit-language-support', methods=['POST'])
def add_edit_language_support():
    try:
        if is_user_active():
            language_support_input_validation = create_language_support_input_validation(request)
            if not language_support_input_validation['status']:
                data = language_support_input_validation
            else:
                data = create_language_support_episode_db(language_support_input_validation['data']['episode_id'],
                                                          language_support_input_validation['data']['data_episode_id'],
                                                          language_support_input_validation['data']['language'],
                                                          language_support_input_validation['data']['title'],
                                                          language_support_input_validation['data']['episode_tags'],
                                                          language_support_input_validation['data'][
                                                              'episode_language_description'],
                                                          language_support_input_validation['data'][
                                                              'episode_thumbnail'],
                                                          language_support_input_validation['data']['episodeVideo'],
                                                          language_support_input_validation['data']['episodeAudio'],
                                                          )
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/update-download-status', methods=['POST'])
def update_download_status_api():
    try:
        # if is_user_active():
        update_download_status_validation = update_episode_download_input_validation(request)
        if not update_download_status_validation['status']:
            data = update_download_status_validation
        else:
            res = update_download_state(update_download_status_validation['data']['episode_id'],update_download_status_validation['data']['download_status']
                                         )
            if res:
                data = get_response(True, "Download status updated successfully", res)
            else:
                data = get_response(False, "Download status updated failed", {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/update-episode-status', methods=['POST'])
def update_episode_status_api():
    try:
        if is_user_active():
            update_episode_status_validation = update_episode_status_input_validation(request)
            if not update_episode_status_validation['status']:
                data = update_episode_status_validation
            else:
                data = update_episode_status(update_episode_status_validation['data']['episode_status'],
                                             update_episode_status_validation['data']['episode_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/episode-language-details', methods=['POST'])
def episode_language_details():
    # try:
    if is_user_active():
        language_support_for_episode_status_validation = episode_language_support_details_input_validation(request)
        if not language_support_for_episode_status_validation['status']:
            data = language_support_for_episode_status_validation
        else:
            data = get_episode_by_id(language_support_for_episode_status_validation['data']['episode_id'])
    else:
        data = get_response(False, ApiMessage.INVALID_SESSION, {})
    # except Exception as e:
    #     data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/update-episode-positions', methods=['POST'])
def update_episode_positions():
    try:
        if is_user_active():
            updated_rows = request.form.get("updated_rows")
            initial_rows = request.form.get("initial_rows")
            print(updated_rows)
            print(initial_rows)
            response = update_epiose_positions(updated_rows,initial_rows)
            if response:
                data = get_response(True, "Episode update successfully", {})
            else:
                data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/delete', methods=['POST'])
def episode_delete():
    try:
        if is_user_active():
            delete_episode_validation = delete_episode_input_validation(request)
            if not delete_episode_validation['status']:
                data = delete_episode_validation
            else:
                data = delete_episode_by_id(delete_episode_validation['data']['episode_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/delete-language-support', methods=['POST'])
def delete_language_support():
    try:
        if is_user_active():
            delete_episode_validation = delete_language_support_input_validation(request)
            if not delete_episode_validation['status']:
                data = delete_episode_validation
            else:
                data = delete_episode_by_id(delete_episode_validation['data']['episode_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/update-episode-language-status', methods=['POST'])
def update_episode_language_status_api():
    try:
        if is_user_active():
            update_episode_status_validation = update_language_support_status_input_validation(request)
            if not update_episode_status_validation['status']:
                data = update_episode_status_validation
            else:
                data = update_episode_language_support_status(update_episode_status_validation['data']['language_status'],
                                             update_episode_status_validation['data']['language_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/details', methods=['POST'])
def episode_details():
    try:
        if is_user_active():
            episode_details_validation = episode_details_input_validation(request)
            if not episode_details_validation['status']:
                data = episode_details_validation
            else:
                data = get_episode_by_episode_id(episode_details_validation['data']['episode_id'])
                print(data)
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)


@episode.route('/get-all-episodes', methods=['POST','GET'])
def get_all_episode_api():
    try:
        res = get_all_episode()
        if len(res) > 0:
            data = get_response(True, "Episode fetched successfully", res)
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return json.dumps(data)
