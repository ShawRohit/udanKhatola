import json

from flask import session

from model.episode import is_episode_exist_by_name, is_position_exist_by_series, is_episode_exists_by_id, \
    is_episode_exist_by_language_id, if_episode_position_exist, is_episode_exist_by_title, if_episode_name_exist, \
    if_episode_title_exist
from model.language import is_language_exist_by_name, is_language_exist_by_name_diff_id
from model.series import is_series_exist_by_name
from util.message import ApiMessage
from util.response import get_response
from util.utility import empty_param_check, is_region_valid, is_name_valid, is_id_valid, is_download_status_valid, \
    is_valid_thumbnail, is_valid_video, is_valid_audio


def create_episode_input_validation(request):
    input_form = request.form
    input_file = request.files
    if "episode_name" not in input_form:
        return get_response(False, "Episode name is missing", {})
    if "episode_position" not in input_form:
        return get_response(False, "Episode position is missing", {})
    if "episodeTitle" not in input_form:
        return get_response(False, "Episode title is missing", {})
    if "episodetags" not in input_form:
        return get_response(False, "Episode tags is missing", {})
    # if 'episode_thumbnail' not in input_file:
    #     return get_response(False, "Episode thumbnail is missing", {})
    # if 'addepisodeVideo' not in input_file:
    #     return get_response(False, "Episode video is missing", {})
    if 'series_id' not in input_form:
        return get_response(False, "series_id is missing", {})
    if "episodeDescription" not in input_form:
        return get_response(False, "Episode description  is missing", {})

    episode_name = str(input_form.get('episode_name')).strip()
    episode_title = str(input_form.get('episodeTitle')).strip()
    episode_description = str(input_form.get('episodeDescription')).strip()
    episode_position = str(input_form.get('episode_position')).strip()
    episodetags = str(input_form.get('episodetags')).strip()
    series_id = str(input_form.get('series_id')).strip()
    if 'episode_thumbnail' not in input_form:
        episode_thumbnail = input_file["episode_thumbnail"]
    else:
        episode_thumbnail = str(input_form["episode_thumbnail"]).strip()

    if 'addepisodeAudio' not in input_form:
        episode_audio = input_file["addepisodeAudio"]
    else:
        episode_audio = str(input_form["addepisodeAudio"]).strip()
    if 'addepisodeVideo' not in input_form:
        episode_video = input_file["addepisodeVideo"]
    else:
        episode_video = str(input_form["addepisodeVideo"]).strip()

    try:
        if empty_param_check(episode_name):
            data = get_response(False, "Please enter the episode name", {})
        # elif is_episode_exist_by_name(episode_name):
        #     data = get_response(False, "Episode already exists", {})
        elif is_episode_exist_by_name(episode_name):
            data = get_response(False, "Episode already exist with this name", {})
        elif empty_param_check(episode_position):
            data = get_response(False, "Please enter the episode position", {})
        elif empty_param_check(episode_title):
            data = get_response(False, "Please enter the episode title", {})
        elif is_episode_exist_by_title(episode_title):
            data = get_response(False, "Episode already exist with this title", {})
        elif not episode_position.isnumeric():
            data = get_response(False, "You must enter a non negative numeric value in episode position", {})
        elif is_position_exist_by_series(series_id, episode_position):
            data = get_response(False, "This position already exists", {})
        elif empty_param_check(episodetags):
            data = get_response(False, "Please enter the episode tags", {})
        elif empty_param_check(episode_description):
            data = get_response(False, "Please enter the episode description", {})
        elif empty_param_check(series_id):
            data = get_response(False, "Please enter the series id", {})
        elif not is_id_valid(series_id):
            data = get_response(False, "Please enter a valid series id", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'episode_name': episode_name,
                                                           'episode_title': episode_title,
                                                           'episode_description': episode_description,
                                                           'episode_thumbnail': episode_thumbnail,
                                                           'episode_video': episode_video,
                                                           'episode_audio': episode_audio,
                                                           'episodetags': episodetags,
                                                           'episode_position': episode_position,
                                                           'series_id': series_id
                                                           })
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data


def create_language_support_input_validation(request):
    input_form = request.form
    input_file = request.files
    if 'data_episode_id' not in input_form:
        return get_response(False, "Episode id is missing", {})
    data_episode_id = str(input_form.get('data_episode_id')).strip()
    if "language" not in input_form:
        return get_response(False, "Language  is missing", {})
    if "title" not in input_form:
        return get_response(False, "Title is missing", {})

    # if data_episode_id =="" or data_episode_id=="undefined" or data_episode_id is None:
    #     if 'episode_thumbnail' not in input_file:
    #         return get_response(False, "Episode thumbnail is missing", {})
    #     if 'episodeVideo' not in input_file:
    #         return get_response(False, "Episode Video is missing", {})
        # if 'episodeAudio' not in input_file:
        #     return get_response(False, "Episode Audio is missing", {})
    if "episode_tags" not in input_form:
        return get_response(False, "Episode tags is missing", {})
    if 'episode_language_description' not in input_form:
        return get_response(False, "Episode description is missing", {})
    if 'episode_id' not in input_form:
        return get_response(False, "episode id is missing", {})

    language = str(input_form.get('language')).strip()
    title = str(input_form.get('title')).strip()
    episode_tags = str(input_form.get('episode_tags')).strip()
    episode_language_description = str(input_form.get('episode_language_description')).strip()
    episode_id = str(input_form.get('episode_id')).strip()
    data_episode_id = str(input_form.get('data_episode_id')).strip()
    if 'episode_thumbnail' not in input_form:
        episode_thumbnail = input_file["episode_thumbnail"]
    else:
        episode_thumbnail = str(input_form["episode_thumbnail"]).strip()
    if 'episodeVideo' not in input_form:
        episodeVideo = input_file["episodeVideo"]
    else:
        episodeVideo = str(input_form["episodeVideo"]).strip()
    if 'episodeAudio' not in input_form:
        episodeAudio = input_file["episodeAudio"]
    else:
        episodeAudio = str(input_form["episodeAudio"]).strip()
    try:
        if empty_param_check(language):
            data = get_response(False, "Please enter the language name", {})
        elif data_episode_id == "" and is_episode_exist_by_language_id(session["episode_details"]["masterEpisodeId"], language):
            print("Herer-------------")
            data = get_response(False, "Episode already exist in this language", {})
        elif empty_param_check(title):
            data = get_response(False, "Please enter the episode title", {})
        elif empty_param_check(title):
            data = get_response(False, "Please enter the episode title", {})
        elif episode_thumbnail !="" and not is_valid_thumbnail(episode_thumbnail):
            data = get_response(False, "Please upload a valid image file", {})
        elif episodeVideo!="" and  not is_valid_video(episodeVideo):
            data = get_response(False, "Please upload a valid video file", {})
        elif episodeAudio !="" and not is_valid_audio(episodeAudio):
            data = get_response(False, "Please upload a valid audio file", {})
        elif empty_param_check(episode_tags):
            data = get_response(False, "Please enter the episode tags", {})
        elif empty_param_check(episode_language_description):
            data = get_response(False, "Please enter the episode description", {})
        elif empty_param_check(episode_id):
            data = get_response(False, "Please enter the episode id", {})
        elif not is_id_valid(episode_id):
            data = get_response(False, "Please enter a valid episode id", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language': language,
                                                           'title': title,
                                                           'episode_tags': episode_tags,
                                                           'episode_language_description': episode_language_description,
                                                           'episode_id': episode_id,
                                                           'data_episode_id': data_episode_id,
                                                           'episode_thumbnail': episode_thumbnail,
                                                           'episodeVideo': episodeVideo,
                                                           'episodeAudio': episodeAudio
                                                           })
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data


def episode_details_input_validation(request):
    input_form = request.form
    if "episode_id" not in input_form:
        return get_response(False, "Episode id is missing", {})
    episode_id = str(input_form.get('episode_id')).strip()
    try:
        if empty_param_check(episode_id):
            data = get_response(False, "Episode id cannot be empty", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'episode_id': episode_id})
    except Exception as e:
        print(e)
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data


def episode_language_support_details_input_validation(request):
    input_form = request.form
    if "episode_id" not in input_form:
        return get_response(False, "Episode id is missing", {})
    episode_id = str(input_form.get('episode_id')).strip()
    try:
        if empty_param_check(episode_id):
            data = get_response(False, "Episode id cannot be empty", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'episode_id': episode_id})
    except Exception as e:
        print(e)
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data


def update_episode_status_input_validation(request):
    input_form = request.form
    print(input_form)
    if "episode_status" not in input_form:
        return get_response(False, "Episode status is missing", {})
    elif "episode_id" not in input_form:
        return get_response(False, "Episode id is missing", {})
    episode_status = str(input_form.get('episode_status')).strip()
    episode_id = str(input_form.get('episode_id')).strip()

    try:
        if empty_param_check(episode_status):
            data = get_response(False, "Please enter the episode status", {})

        elif not is_name_valid(episode_status):
            data = get_response(False, "Please enter a valid episode status", {})

        elif episode_status not in ["Active", "Deactivated", "In Progress"]:
            data = get_response(False, "Please enter a valid episode status", {})
        elif empty_param_check(episode_id):
            data = get_response(False, "Please enter the episode id", {})

        elif not is_id_valid(episode_id):
            data = get_response(False, "Please enter a valid episode id", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'episode_status': episode_status, 'episode_id': episode_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data

# formdata.append("language_status", language_status);
#         formdata.append("language_id", language_id);

def update_episode_download_input_validation(request):
    input_form = request.get_json()
    print(json.dumps(input_form))
    if "download_status" not in input_form:
        return get_response(False, "Download status is missing", {})
    elif "episode_id" not in input_form:
        return get_response(False, "Episode id is missing", {})
    download_status = str(input_form.get('download_status')).strip()
    episode_id = str(input_form.get('episode_id')).strip()

    try:
        if empty_param_check(download_status):
            data = get_response(False, "Download status can not be blank", {})
        elif not is_episode_exists_by_id(episode_id):
            data = get_response(False, "Episode does not exist", {})
        elif not is_download_status_valid(download_status):
            data = get_response(False, "Please enter a valid download status", {})
        elif empty_param_check(episode_id):
            data = get_response(False, "Please enter the episode id", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'download_status': download_status, 'episode_id': episode_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def update_language_support_status_input_validation(request):
    input_form = request.form
    print(input_form)
    if "language_status" not in input_form:
        return get_response(False, "Language status is missing", {})
    elif "language_id" not in input_form:
        return get_response(False, "Language id is missing", {})
    language_status = str(input_form.get('language_status')).strip()
    language_id = str(input_form.get('language_id')).strip()

    try:
        if empty_param_check(language_status):
            data = get_response(False, "Please enter the episode status", {})

        elif not is_name_valid(language_status):
            data = get_response(False, "Please enter a valid episode status", {})

        elif language_status not in ["Active", "Deactivated", "In Progress"]:
            data = get_response(False, "Please enter a valid episode status", {})
        elif empty_param_check(language_id):
            data = get_response(False, "Please enter the language id", {})

        elif not is_id_valid(language_id):
            data = get_response(False, "Please enter a valid language id", {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'language_status': language_status, 'language_id': language_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def edit_episode_input_validation(request):
    input_form = request.form
    input_file = request.files
    current_episode_thumnail = ''
    current_episode_video = ''
    current_episode_audio = ''
    if "episode_id" not in input_form:
        return get_response(False, "Episode id is missing", {})
    if "episode_name" not in input_form:
        return get_response(False, "Episode name is missing", {})
    if "episode_position" not in input_form:
        return get_response(False, "Episode position is missing", {})
    if "episode_title" not in input_form:
        return get_response(False, "Episode title is missing", {})
    if "episode_tags" not in input_form:
        return get_response(False, "Episode tags is missing", {})
    if "current_episode_thumbnail" in input_file:
        current_episode_thumnail = input_file['current_episode_thumbnail']

    if "episode_video" in input_file:
        current_episode_video = input_file['episode_video']
    else:
        current_episode_video = str(input_form.get('episode_video')).strip()

    if "episode_audio" in input_file:
        current_episode_audio = input_file['episode_audio']
    else:
        current_episode_audio = str(input_form.get('episode_audio')).strip()

    if "episode_description" not in input_form:
        return get_response(False, "Episode description is missing", {})
    episode_name = str(input_form.get('episode_name')).strip()
    episode_title = str(input_form.get('episode_title')).strip()
    episode_description = str(input_form.get('episode_description')).strip()
    episode_position = str(input_form.get('episode_position')).strip()
    episode_tags = str(input_form.get('episode_tags')).strip()
    episode_id = str(input_form.get('episode_id')).strip()
    prev_episode_thumbnail = str(input_form.get('prev_episode_thumbnail')).strip()
    # try:
    if empty_param_check(episode_name):
        data = get_response(False, "Please enter the episode name", {})
    elif if_episode_name_exist(episode_id, episode_name, session["series_id"]):
        data = get_response(False, "Episode name already exists", {})
    elif empty_param_check(episode_position):
        data = get_response(False, "Please enter the episode position", {})
    elif if_episode_position_exist(episode_id, episode_position, session["series_id"]):
        data = get_response(False, "Episode position already exists", {})

    elif not episode_position.isnumeric():
        data = get_response(False, "You must enter a non negative numeric value in episode position", {})
    elif empty_param_check(episode_title):
        data = get_response(False, "Please enter the episode title", {})
    elif if_episode_title_exist(episode_id, episode_title, session["series_id"]):
        data = get_response(False, "Episode title already exists", {})

    elif empty_param_check(episode_tags):
        data = get_response(False, "Please enter the episode tags", {})
    elif current_episode_thumnail!='' and not is_valid_thumbnail(current_episode_thumnail):
        data = get_response(False, "Please upload a valid image file", {})
    elif  current_episode_video!='' and not is_valid_video(current_episode_video):
        data = get_response(False, "Please upload a valid video file", {})
    elif current_episode_audio!='' and  not is_valid_audio(current_episode_audio):
        data = get_response(False, "Please upload a valid audio file", {})

    elif empty_param_check(episode_description):
        data = get_response(False, "Please enter the episode description", {})
    elif empty_param_check(episode_id):
        data = get_response(False, "Please enter the episode id", {})

    # elif not is_name_valid(episode_name):
    #     data = get_response(False, "Please enter a valid episode name", {})
    elif not episode_id.isnumeric():
        data = get_response(False, "You must enter a non negative numeric value in episode id", {})

    else:
        data = get_response(True, ApiMessage.SUCCESS, {'episode_name': episode_name,
                                                       'episode_id': episode_id,
                                                       'episode_position': episode_position,
                                                       'episode_title': episode_title,
                                                       'episode_description': episode_description,
                                                       'current_episode_audio': current_episode_audio,
                                                       'current_episode_video': current_episode_video,
                                                       'episode_tags': episode_tags,
                                                       'prev_episode_thumbnail': prev_episode_thumbnail,
                                                       'current_episode_thumnail': current_episode_thumnail
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

        elif series_status not in ["Active", "Deactivated", "Paused","In Progress"]:
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


def delete_episode_input_validation(request):
    input_form = request.form
    if "episode_id" not in input_form:
        return get_response(False, "episode id is missing", {})

    episode_id = str(input_form.get('episode_id')).strip()

    try:
        if empty_param_check(episode_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'episode_id': episode_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})

    return data


def delete_language_support_input_validation(request):
    input_form = request.form
    if "episode_id" not in input_form:
        return get_response(False, "episode id is missing", {})
    episode_id = str(input_form.get('episode_id')).strip()
    try:
        if empty_param_check(episode_id):
            data = get_response(False, ApiMessage.BLANK_LANGUAGE_ID, {})
        else:
            data = get_response(True, ApiMessage.SUCCESS, {'episode_id': episode_id})
    except Exception as e:
        data = get_response(False, ApiMessage.SOMETHING_WENT_WRONG, {})
    return data
