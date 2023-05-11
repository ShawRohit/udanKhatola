import traceback

from flask import Blueprint, request, json

from app_session.user_session import is_user_active
from model.episode import get_episode_by_episode_id, get_episode_by_id,get_episode_by_episodeId, \
    get_all_episode, update_download_state, get_all_master_episode, get_all_dubbed_episode, \
    get_filtered_episode, update_episode_view_count, get_episodes_by_language_id
from model.language import get_language_name_by_language_id, get_all_languages
from model.language_details import get_language_details_by_language_id
from model.series import update_series_view_count,if_series_status_active
from util.message import ApiMessage
from util.utility import get_response
from validation.episode_validation import episode_details_input_validation, episode_language_support_details_input_validation, \
    update_episode_download_input_validation

appUser = Blueprint('app_user_controller', __name__)


@appUser.route('/update-download-status', methods=['POST'])
def update_download_status_api():
    try:
        update_download_status_validation = update_episode_download_input_validation(request)
        if not update_download_status_validation['status']:
            data = update_download_status_validation
        else:
            res = update_download_state(update_download_status_validation['data']['episode_id'],
                                        update_download_status_validation['data']['download_status']
                                        )
            if res:
                data = get_response(True, "Download status updated successfully", res)
            else:
                data = get_response(False, "Download status updated failed", {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@appUser.route('/episode-language-details', methods=['POST'])
def episode_language_details():
    try:
        if is_user_active():
            language_support_for_episode_status_validation = episode_language_support_details_input_validation(request)
            if not language_support_for_episode_status_validation['status']:
                data = language_support_for_episode_status_validation
            else:
                data = get_episode_by_id(
                    language_support_for_episode_status_validation['data']['episode_id']
                )[0]
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@appUser.route('/details', methods=['POST'])
def episode_details():
    try:
        if is_user_active():
            episode_details_validation = episode_details_input_validation(request)
            if not episode_details_validation['status']:
                data = episode_details_validation
            else:
                data = get_episode_by_episode_id(episode_details_validation['data']['episode_id'])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@appUser.route('/get-all-episodes', methods=['POST', 'GET'])
def get_all_episode_api():
    try:
        res = get_all_episode()
        final_episode = []
        if res is not None:
            for episode in res:
                is_episode_active = if_series_status_active(episode["series_id"])
                print("=============")
                print(episode["series_id"])
                print(is_episode_active)

                print("=========")

                if is_episode_active:
                    final_episode.append(episode)
            if len(final_episode) > 0:
                data = get_response(True, "Episode fetched successfully", final_episode)
            else:
                data = get_response(True, "No episodes found", [])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@appUser.route('/get-all-master-episodes', methods=['POST', 'GET'])
def get_all_master_episodes():
    try:
        res = get_all_master_episode()
        final_episodes_array = []
        for episodes in res:
            is_episode_active = if_series_status_active(episodes["series_id"])
            if is_episode_active:
                episodes_res = get_all_dubbed_episode(episodes["masterEpisodeId"])
                language_details = []
                if len(episodes_res) > 0 :
                    for episode in episodes_res:
                        temp_language_details = {"language_name":get_language_name_by_language_id(episode["language_id"]),"episode_title":episode["episode_title"]}
                        language_details.append(temp_language_details)

                episodes["language_details"] = language_details

                final_episodes_array.append(episodes)
        data = get_response(True, "Episode fetched successfully", final_episodes_array)
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@appUser.route('/get-all-filtered', methods=['POST', 'GET'])
def get_all_filtered_episode_api():
    try:
        res = get_filtered_episode(request.get_json()["query"])
        data = get_response(True, "Episode fetched successfully", res)
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@appUser.route('/view-episode-counter', methods=['POST', 'GET'])
def update_views_of_episode():
    try:
        episode = get_episode_by_episodeId(request.get_json()["episode_id"])
        print("---------------")
        print(episode)
        print("------------")
        if episode is not None:
            res = update_episode_view_count(request.get_json()["episode_id"])
            if res:
                series_view_update_response = update_series_view_count(episode["series_id"])
                if series_view_update_response:
                    data = get_response(True, "Views updated successfully", res)
                else:
                    data = get_response(False, "Series not found ", res)
            else:
                data = get_response(False, "Episode not found ", {})
        else:
            data = get_response(False, "Episode not found ", {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@appUser.route('/get-all-languages', methods=['POST', 'GET'])
def get_languages():
    try:
        languages = get_all_languages()
        if len(languages) > 0:
            data = get_response(True, "Languages fetched successfully", languages)
        else:
            data = get_response(False, "Languages not found ", [])
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@appUser.route('/get-language-details-by-id', methods=['POST'])
def get_language_detail_by_id():
    try:
        languages = get_language_details_by_language_id(request.get_json()["language_id"])
        if languages is not None:
            languages["language_keywords"] = json.loads(languages["language_keywords"])
            if len(languages) > 0:
                data = get_response(True, "Languages details fetched successfully", languages)
            else:
                data = get_response(False, "Languages details not found ", [])
        else:
            data = get_response(False, "Languages details not found ", [])

    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)


@appUser.route('/get-episode-by-language-id', methods=['POST','GET'])
def get_episode_by_language_id():
    try:
        res = get_episodes_by_language_id(request.get_json()["language_id"])
        final_episode = []
        if res is not None:
            for episode in res:
                is_episode_active = if_series_status_active(episode["series_id"])
                if is_episode_active:
                    final_episode.append(episode)
            if len(final_episode) > 0:
                data = get_response(True, "Episode fetched successfully", final_episode)
            else:
                data = get_response(True, "No episodes found", [])
        else:
            data = get_response(False, ApiMessage.INVALID_SESSION, {})
    except Exception as e:
        print(traceback.format_exc())
        data = get_response(False, str(e), {})
    return json.dumps(data)