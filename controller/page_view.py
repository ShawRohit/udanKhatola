import json

from flask import (Blueprint, render_template, redirect, url_for, session,render_template_string)

from app_session.user_session import destroy_user_session
from constant.page_view import get_page_details
from constant.region_map import regions
from model.episode import get_episode_by_series_id, get_episode_by_id, get_episode_by_master_episode_id, \
    get_all_episode_by_master_episode_id, get_episode_count_for_language, get_all_episode_count_by_master_episode_id
from model.episode_language import get_language_by_episode_id
from model.language import get_all_languages, get_language_by_language_id,get_all_languages_in_web
from model.series import get_all_series, get_series_by_series_id, get_all_series_postion
from model.series_episode_language import get_language_by_series_id, get_language_count_by_series_id
from service.episode import get_all_language_id
from service.language import get_all_language_keywords, get_language_data, get_languages_by_language_id
from service.series import get_all_language_by_series_id
from util.utility import is_session_active, get_all_avaialbale_languages

page_view = Blueprint('page_view_controller', __name__)


@page_view.route("/login")
def page_view_login():
    if is_session_active():
        return redirect(url_for('page_view_controller.page_view_language_management'))
    return render_template('login.html', page_details=get_page_details("admin-login"))


@page_view.route("/forgot-password")
def page_view_forgot_password():
    return render_template('forgot_password.html', page_details=get_page_details("forgot-password"))


@page_view.route("/change-password")
def page_view_change_password():
    return render_template('change-password.html', page_details=get_page_details("change-password"))


@page_view.route("/password-reset")
def page_view_password_reset():
    return render_template('password-reset.html', page_details=get_page_details("password-reset"))


@page_view.route("/dubbing-management")
def page_view_dubbing_management():
    if is_session_active():
        series = get_all_series()
        final_series_data = []
        all_postions = get_all_series_postion()
        all_postions.sort()
        for series_details in series:
            series_details["language_count"] = get_language_count_by_series_id(series_details["id"])
            final_series_data.append(series_details)
        return render_template('dubbing_management.html', page_details=get_page_details("dubbing-management"),
                               all_series=final_series_data)
    return redirect(url_for('page_view_controller.page_view_login'))


@page_view.route("/language-management")
def page_view_language_management():
    if is_session_active():
        return render_template('language-management.html', page_details=get_page_details("language-management"),
                               region_list=regions, language_list=get_all_languages_in_web(),
                               active_language_management="active")
    return redirect(url_for('page_view_controller.page_view_login'))


@page_view.route("/episode-management/<episode_id>")
def page_view_episode_management(episode_id):
    if is_session_active():
        # languages = get_all_language_id()
        episode_details = get_episode_by_master_episode_id(episode_id)
        print("==================")
        print(episode_details)
        print(episode_details["series_id"])
        print(episode_details["episode_thumbnail"])
        languages = get_all_language_by_series_id(episode_details["series_id"])
        print("=================")
        session["episode_details"] = episode_details
        print(session["episode_details"])
        all_dubbed_episodes = get_all_episode_by_master_episode_id(episode_id)
        print(all_dubbed_episodes)
        for i in range(len(all_dubbed_episodes)):
            print("===============")
            print(all_dubbed_episodes[i]["language_id"])
            print("===================")
            language = get_language_by_language_id(all_dubbed_episodes[i]["language_id"])
            if language is not None:
                all_dubbed_episodes[i]["language_name"] = language["language_name"]
        return render_template('episode-management-updated.html', page_details=get_page_details("language-management"),
                               episode_details=episode_details, episodes=all_dubbed_episodes, languages=languages)
    return redirect(url_for('page_view_controller.page_view_login'))


@page_view.route("/language-management/language")
def page_view_language_details():
    if is_session_active():
        return render_template('language.html', page_details=get_page_details("language-details"),
                               language_keyword_list=get_all_language_keywords(),
                               language_data=get_language_data(), active_language_management="active")
    return redirect(url_for('page_view_controller.page_view_login'))


@page_view.route("/series-management/<series_id>")
def page_view_series_management(series_id):
    if is_session_active():
        series_details = get_series_by_series_id(series_id)
        if series_details is not None:
            session["series_name"] = series_details['series_name']
            session["series_id"] = series_details['id']
            episodes = get_episode_by_series_id(series_id)
            final_episodes = []
            series_languages = get_language_by_series_id(series_id)
            languages = get_all_languages()
            available_languages = get_all_avaialbale_languages(languages, json.loads(series_details['series_languages']))
            for episode in episodes:
                episode["language_count"] = get_all_episode_count_by_master_episode_id(episode["masterEpisodeId"])
                final_episodes.append(episode)
            return render_template('series-management.html', page_details=get_page_details("dubbing-management"),
                                   active_series_management="active", series_details=series_details,
                                   episodes=final_episodes,
                                   languages=series_languages, available_languages=available_languages)
        else:
            return render_template_string('PageNotFound {{ errorCode }}', errorCode='404'), 404
    return redirect(url_for('page_view_controller.page_view_login'))


@page_view.route("/logout")
def user_logout():
    destroy_user_session()
    return redirect(url_for('page_view_controller.page_view_login'))
