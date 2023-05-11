import json
import math
import os
import time
import traceback

import boto3
import cv2
from flask import session

from app_session.user_session import get_current_user_gen_id
from config_env.conf_env import config
from constant.language_keys_map import language_keys
from model.episode import get_episodes_by_language_id
from model.language import create_language, edit_language_by_language_id, is_language_english, is_language_exist, \
    delete_language_by_language_id, get_language_by_language_id
from model.language_details import is_language_details_exist, update_language_details, create_language_details, \
    get_language_details_by_language_id
from service.episode import S3_IMAGE_FOLDER
from util.message import LanguageMessages, ApiMessage
from util.utility import generate_alphanumeric_string, get_response, is_image_file




def aws_session(region):
    return boto3.session.Session(region_name=region,aws_access_key_id=config.aws_access_key_id,aws_secret_access_key=config.aws_secret_access_key)

def create_language_db(regional_language_id, language_name, language_icon, region):
    if not is_image_file(language_icon.filename):
        return get_response(False, "Please select proper image file (.jpg, .jpeg, .png)", {})
    temp_folder = 'uploads'
    ts = time.time()
    timestamp = math.trunc(ts)
    dynamic_file_name = str(timestamp) + '_' + str(language_icon.filename).strip().replace(" ","")
    cv2_file_name = 'cv2_' + str(language_icon.filename)
    f_path = os.path.join(temp_folder, dynamic_file_name)
    cv2_f_path = os.path.join(temp_folder, cv2_file_name)
    print()
    language_icon.save(cv2_f_path)
    image = cv2.imread(cv2_f_path)
    w, h, c = image.shape
    percentage = 0.6
    resized_image = cv2.resize(image,
                               (int(h * percentage), int(w * percentage)),
                               # interpolation=cv2.INTER_AREA
                               )
    cv2.imwrite(f_path, resized_image)
    os.remove(cv2_f_path)

    language_icon_path, is_file_uploaded = upload_episode_image_into_bucket(f_path, dynamic_file_name)
    os.remove(f_path)
    res = create_language("lang_" + generate_alphanumeric_string(5), language_name, str(get_current_user_gen_id()),
                          regional_language_id, language_icon_path,region)
    if res is not None:
        return get_response(True, LanguageMessages.languageCreateSuccess, {})
    else:
        return get_response(False, LanguageMessages.languageCreateFail, {})


def upload_episode_image_into_bucket(image, new_file_name):
    # try:
    bucket_name = config.S3_BUCKET_NAME
    region = config.S3_REGION_NAME
    session = aws_session(region)
    s3_resource = session.resource('s3')
    aws_file_path = f"{S3_IMAGE_FOLDER}/{new_file_name}"
    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(
        Filename=image,
        Key=aws_file_path
        # ExtraArgs={"ContentType": "image/jpeg"}
    )
    s3_profile_pic_name = f"https://{bucket_name}.s3.amazonaws.com/episode/{new_file_name}"
    return s3_profile_pic_name, True


def edit_language_db(language_id, regional_language_id, language_name, language_icon, region):

    if language_icon !="":
        temp_folder = 'uploads'
        ts = time.time()
        timestamp = math.trunc(ts)
        dynamic_file_name = str(timestamp) + '_' + str(language_icon.filename).strip().replace(" ","")
        cv2_file_name = 'cv2_' + str(language_icon.filename)
        f_path = os.path.join(temp_folder, dynamic_file_name)
        cv2_f_path = os.path.join(temp_folder, cv2_file_name)
        print()
        language_icon.save(cv2_f_path)
        image = cv2.imread(cv2_f_path)
        w, h, c = image.shape
        percentage = 0.6
        resized_image = cv2.resize(image,
                                   (int(h * percentage), int(w * percentage)),
                                   # interpolation=cv2.INTER_AREA
                                   )
        cv2.imwrite(f_path, resized_image)
        os.remove(cv2_f_path)

        language_icon_path, is_file_uploaded = upload_episode_image_into_bucket(f_path, dynamic_file_name)
        os.remove(f_path)
    else:
        language_icon_path, is_file_uploaded = None, None




    if not is_language_exist(language_id):
        return get_response(False, LanguageMessages.languageNotExist, {})
    if is_language_english(language_id):
        return get_response(False, LanguageMessages.englishNonEditable, {})
    else:
        res = edit_language_by_language_id(language_id, language_name, regional_language_id, language_icon_path,region)
        if res:
            return get_response(True, LanguageMessages.languageEditSuccess, {})
        else:
            return get_response(False, LanguageMessages.languageEditFail, {})


def delete_language_db(language_id):
    episodes = get_episodes_by_language_id(language_id)

    if not is_language_exist(language_id):
        return get_response(False, LanguageMessages.languageNotExist, {})
    if is_language_english(language_id):
        return get_response(False, LanguageMessages.englishNonDeletable, {})
    if len(episodes) > 0:
        return get_response(False, LanguageMessages.languageContainsContent, {})

    else:
        res = delete_language_by_language_id(language_id)
        if res:
            return get_response(True, LanguageMessages.languageDeleteSuccess, {})
        else:
            return get_response(False, LanguageMessages.languageDeleteFail, {})


def get_language_details(language_id):
    if not is_language_exist(language_id):
        return get_response(False, LanguageMessages.languageNotExist, {})
    else:
        res = get_language_by_language_id(language_id)
        if res is not None:
            return get_response(True, LanguageMessages.getLanguageSuccess, res)
        else:
            return get_response(False, LanguageMessages.getLanguageFail, {})


def add_keywords_db(language_id):
    if not is_language_exist(language_id):
        return get_response(False, LanguageMessages.languageNotExist, {})
    else:
        res = create_language_details(language_id, json.dumps(language_keys))
        if res is not None:
            return get_response(True, LanguageMessages.addLanguageKeywordsSuccess, res)
        else:
            return get_response(False, LanguageMessages.addLanguageKeywordsFail, {})


def update_keywords_db(language_keywords):
    language_id = session["current_language_id"]
    if not is_language_exist(language_id):
        return get_response(False, LanguageMessages.languageNotExist, {})
    else:
        if is_language_details_exist(language_id):
            res = update_language_details(language_id, language_keywords)
        else:
            res = create_language_details(language_id, language_keywords)
        if res:
            return get_response(True, LanguageMessages.updateLanguageKeywordsSuccess, res)
        else:
            return get_response(False, LanguageMessages.updateLanguageKeywordsFail, {})


def get_all_language_keywords():
    try:
        language_id = session["current_language_id"]
        if is_language_details_exist(language_id):
            res = get_language_details_by_language_id(language_id)
            if res is not None:
                return json.loads(res["language_keywords"])
            else:
                return {}
        else:
            return language_keys
    except Exception as e:
        print(traceback.format_exc())
        return {}


def set_language_affix(language_id):
    if not is_language_exist(language_id):
        return get_response(False, LanguageMessages.languageNotExist, {})
    else:
        session['current_language_id'] = language_id
        return get_response(True, ApiMessage.SUCCESS, {'language_id': language_id})


def get_language_data():
    try:
        language_id = session["current_language_id"]
        if is_language_exist(language_id):
            res = get_language_by_language_id(language_id)
            if res is not None:
                return res
            else:
                return {}
        else:
            return {}
    except Exception as e:
        print(traceback.format_exc())
        return {}


def get_languages_by_language_id(language_data):
    try:
        data = language_data['languages']['data']
        all_languages = []
        for language in data:
            res = get_language_details(language['id'])
            all_languages.append(res)
        return all_languages
    except Exception as e:
        return []
