import math
import os
import time
# import cv2
import cv2
from flask import session

from app_session.user_session import get_current_user_gen_id
from model.episode import create_episode, update_epiosde
from model.episode_language import add_edit_language
from model.language import get_all_languages
from model.series import create_series
from util.message import LanguageMessages, ApiMessage
from util.utility import generate_alphanumeric_string, get_response, is_image_file, generate_master_episode_id, \
    generate_episode_id
import boto3
from config_env.conf_env import config
from boto3.s3.transfer import TransferConfig


S3_REGION_NAME = config.S3_REGION_NAME
S3_IMAGE_FOLDER = config.S3_EPISODE_IMAGE_FOLDER
S3_BUCKET_NAME = config.S3_BUCKET_NAME


def create_episode_db(series_id, series_name,episode_name, episode_thumbnail, episode_position, episode_tags, title, decription, audio,video):
    if episode_thumbnail != "":
        print("-------1--------")
        if episode_thumbnail.filename != '':
            if not is_image_file(episode_thumbnail.filename):
                return get_response(False, "Please select proper image file (.jpg, .jpeg, .png)", {})
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            dynamic_file_name = str(timestamp) + '_' + str(episode_thumbnail.filename).strip().replace(" ","")
            cv2_file_name = 'cv2_' + str(episode_thumbnail.filename)
            f_path = os.path.join(temp_folder, dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, cv2_file_name)
            print()
            episode_thumbnail.save(cv2_f_path)
            image = cv2.imread(cv2_f_path)
            w, h, c = image.shape
            percentage = 0.6
            resized_image = cv2.resize(image,
                                       (int(h * percentage), int(w * percentage)),
                                       # interpolation=cv2.INTER_AREA
                                       )
            cv2.imwrite(f_path, resized_image)
            os.remove(cv2_f_path)
        else:
            dynamic_file_name = None
            f_path = None
    else:
        dynamic_file_name = None
        f_path = None

    #Video upload
    if video != "":
        print("-------1--------")
        if video.filename != '':
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            video_dynamic_file_name = str(timestamp) + '_' + str(video.filename).strip().replace(" ","")
            video_f_path = os.path.join(temp_folder, video_dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, video_dynamic_file_name)
            video.save(cv2_f_path)
        else:
            video_dynamic_file_name = None
            video_f_path = None
    else:
        video_dynamic_file_name = None
        video_f_path = None

    # Dubbed audio upload function
    if audio != "":
        print("-------1--------")
        if audio.filename != '':
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            audio_dynamic_file_name = str(timestamp) + '_' + str(audio.filename).strip().replace(" ","")
            # cv2_file_name = 'cv2_' + str(episode_audio.filename)
            audio_f_path = os.path.join(temp_folder, audio_dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, audio_dynamic_file_name)
            print()
            audio.save(cv2_f_path)

        else:
            audio_dynamic_file_name = None
            audio_f_path = None
    else:
        audio_dynamic_file_name = None
        audio_f_path = None

    if dynamic_file_name is not None:
        series_thumbnail, is_file_uploaded = upload_episode_image_into_bucket(f_path, dynamic_file_name)
        os.remove(f_path)
    else:
        series_thumbnail, is_file_uploaded = None,None

    if video_dynamic_file_name is not None:
        episode_video_path, is_file_uploaded = upload_episode_video_into_bucket(video_f_path, video_dynamic_file_name)
        os.remove(video_f_path)
    else:
        episode_video_path, is_file_uploaded = None, None
    if audio_dynamic_file_name is not None:
        episode_audio_path, is_file_uploaded = upload_episode_image_into_bucket(audio_f_path, audio_dynamic_file_name)
        os.remove(audio_f_path)
    else:
        episode_audio_path, is_file_uploaded = None, None

    res = create_episode("",generate_master_episode_id(),generate_episode_id(),series_id,series_name,"lang_tifew",episode_name, episode_position, episode_tags,
                         title,decription,episode_video_path,episode_audio_path, 1,str(get_current_user_gen_id()), series_thumbnail)

    if res is not None:
        return get_response(True, "Episode created successfully", {})
    else:
        return get_response(False, "Episode creation failed", {})


def create_language_support_episode_db(episode_id, data_episode_id, language, title, tags, decription, episode_thumbnail,
                                       episode_video, episode_audio):
    if episode_thumbnail != "":
        print("-------1-2-------")
        if episode_thumbnail.filename != '':
            if not is_image_file(episode_thumbnail.filename):
                return get_response(False, "Please select proper image file (.jpg, .jpeg, .png)", {})
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            dynamic_file_name = str(timestamp) + '_' + str(episode_thumbnail.filename).strip().replace(" ","")
            cv2_file_name = 'cv2_' + str(episode_thumbnail.filename)
            f_path = os.path.join(temp_folder, dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, cv2_file_name)
            print()
            episode_thumbnail.save(cv2_f_path)
            image = cv2.imread(cv2_f_path)
            w, h, c = image.shape
            percentage = 0.6
            resized_image = cv2.resize(image,
                                       (int(h * percentage), int(w * percentage)),
                                       # interpolation=cv2.INTER_AREA
                                       )
            cv2.imwrite(f_path, resized_image)
            os.remove(cv2_f_path)
        else:
            dynamic_file_name = None
            f_path = None
    else:
        dynamic_file_name = None
        f_path = None

    # Dubbed video upload function
    if episode_video != "":
        print("-------1--------")
        if episode_video.filename != '':
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            video_dynamic_file_name = str(timestamp) + '_' + str(episode_video.filename).strip().replace(" ","")
            # cv2_file_name = 'cv2_' + str(episode_video.filename)
            video_f_path = os.path.join(temp_folder, video_dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, video_dynamic_file_name)
            # print()
            episode_video.save(cv2_f_path)
            # video = cv2.imread(cv2_f_path)
            # w, h, c = image.shape
            # percentage = 0.6
            # resized_image = cv2.resize(image,
            #                            (int(h * percentage), int(w * percentage)),
            #                            # interpolation=cv2.INTER_AREA
            #                            )
            # cv2.imwrite(f_path, resized_image)
            # cv2.imwrite(video_f_path, video)
            # os.remove(cv2_f_path)
        else:
            video_dynamic_file_name = None
            video_f_path = None
    else:
        video_dynamic_file_name = None
        video_f_path = None

    # Dubbed audio upload function
    if episode_audio != "":
        print("-------1--------")
        if episode_audio.filename != '':
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            audio_dynamic_file_name = str(timestamp) + '_' + str(episode_audio.filename).strip().replace(" ","")
            # cv2_file_name = 'cv2_' + str(episode_audio.filename)
            audio_f_path = os.path.join(temp_folder, audio_dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, audio_dynamic_file_name)
            print()
            episode_audio.save(cv2_f_path)
        else:
            audio_dynamic_file_name = None
            audio_f_path = None
    else:
        audio_dynamic_file_name = None
        audio_f_path = None

    if dynamic_file_name is not None:
        episode_thumbnail, is_file_uploaded = upload_episode_image_into_bucket(f_path, dynamic_file_name)
        os.remove(f_path)
    else:
        episode_thumbnail, is_file_uploaded=None,None
    if video_dynamic_file_name is not None:
        episode_video_path, is_file_uploaded = upload_episode_video_into_bucket(video_f_path, video_dynamic_file_name)
        os.remove(video_f_path)
    else:
        episode_video_path, is_file_uploaded = None, None
    if audio_dynamic_file_name is not None:
        episode_audio_path, is_file_uploaded = upload_episode_image_into_bucket(audio_f_path, audio_dynamic_file_name)
        os.remove(audio_f_path)
    else:
        episode_audio_path, is_file_uploaded=None,None

    # res = add_edit_language(language_id, language, episode_thumbnail, episode_audio_path, episode_video_path, title, tags, decription, "",
    #                   episode_id, str(get_current_user_gen_id()))

    res = create_episode(data_episode_id,session["episode_details"]["masterEpisodeId"], generate_episode_id(), session["episode_details"]["series_id"],session["series_name"],language,session["episode_details"]["episode_name"],
                         session["episode_details"]["episode_position"], tags,
                         title, decription, episode_video_path, episode_audio_path, 0,str(get_current_user_gen_id()),
                         episode_thumbnail)

    if res is not None:
        return get_response(True, "Language support added successfully", {})
    else:
        return get_response(False, "Language support creation failed", {})


def update_episode_db(episode_id, episode_name, current_thumbnail, prev_thumbnail, position, tags,title,description,episode_audio,episode_video):
    if episode_audio != "":
        print("-------1--------")
        if episode_audio.filename != '':
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            audio_dynamic_file_name = str(timestamp) + '_' + str(episode_audio.filename).strip().replace(" ","")
            # cv2_file_name = 'cv2_' + str(episode_audio.filename)
            audio_f_path = os.path.join(temp_folder, audio_dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, audio_dynamic_file_name)
            print()
            episode_audio.save(cv2_f_path)
        else:
            audio_dynamic_file_name = None
            audio_f_path = None
    else:
        audio_dynamic_file_name = None
        audio_f_path = None

    if episode_video != "":
        print("-------1--------")
        if episode_video.filename != '':
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            video_dynamic_file_name = str(timestamp) + '_' + str(episode_video.filename).strip().replace(" ","")
            # cv2_file_name = 'cv2_' + str(episode_video.filename)
            video_f_path = os.path.join(temp_folder, video_dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, video_dynamic_file_name)
            # print()
            episode_video.save(cv2_f_path)
        else:
            video_dynamic_file_name = None
            video_f_path = None
    else:
        video_dynamic_file_name = None
        video_f_path = None

    if current_thumbnail != "":
        print("-------1--------")
        if current_thumbnail.filename != '':
            if not is_image_file(current_thumbnail.filename):
                return get_response(False, "Please select proper image file (.jpg, .jpeg, .png)", {})
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            dynamic_file_name = str(timestamp) + '_' + str(current_thumbnail.filename).replace(" ", "")
            cv2_file_name = 'cv2_' + str(current_thumbnail.filename)
            f_path = os.path.join(temp_folder, dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, cv2_file_name)
            print()
            current_thumbnail.save(cv2_f_path)
            image = cv2.imread(cv2_f_path)
            w, h, c = image.shape
            percentage = 0.6
            resized_image = cv2.resize(image,
                                       (int(h * percentage), int(w * percentage)),
                                       # interpolation=cv2.INTER_AREA
                                       )
            cv2.imwrite(f_path, resized_image)
            os.remove(cv2_f_path)
        else:
            dynamic_file_name = None
            f_path = None
    else:
        dynamic_file_name = None
        f_path = None

    if dynamic_file_name is not None:
        episode_thumbnail, is_file_uploaded = upload_episode_image_into_bucket(f_path, dynamic_file_name)
        os.remove(f_path)
    else:
        episode_thumbnail, is_file_uploaded = None, None
    if video_dynamic_file_name is not None:
        episode_video_path, is_file_uploaded = upload_episode_video_into_bucket(video_f_path, video_dynamic_file_name)
        os.remove(video_f_path)
    else:
        episode_video_path, is_file_uploaded = None, None
    if audio_dynamic_file_name is not None:
        episode_audio_path, is_file_uploaded = upload_episode_image_into_bucket(audio_f_path, audio_dynamic_file_name)
        os.remove(audio_f_path)
    else:
        episode_audio_path, is_file_uploaded=None,None


    res = update_epiosde(episode_name, episode_thumbnail, episode_id, position, tags, title, description,episode_audio_path,episode_video_path)
    if res is not None:
        return get_response(True, "Episode Updated successfully", {})
    else:
        return get_response(False, "Episode Update failed", {})


    # if dynamic_file_name is None:
    #     res = update_epiosde(episode_name, prev_thumbnail, episode_id, position, tags)
    #     if res is not None:
    #         return get_response(True, "Episode Updated successfully", {})
    #     else:
    #         return get_response(False, "Episode Update failed", {})
    # else:
    #     res = update_epiosde(episode_name, episode_thumbnail, episode_id, position, tags)
    #     if res is not None:
    #         return get_response(True, "Episode Updated successfully", {})
    #     else:
    #         return get_response(False, "Episode Update failed", {})


# def set_language_affix(language_id):
#     if not is_language_exist(language_id):
#         return get_response(False, LanguageMessages.languageNotExist, {})
#     else:
#         session['current_language_id'] = language_id
#         return get_response(True, ApiMessage.SUCCESS, {'language_id': language_id})


# Function for creating a boto3 session
def aws_session(region):
    return boto3.session.Session(region_name=region,aws_access_key_id=config.aws_access_key_id,aws_secret_access_key=config.aws_secret_access_key)


# Function for uploading image files in s3 bucket
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
    # except Exception as e:
    #     print(e)
    #     return None, False


def upload_episode_video_into_bucket(video_file, new_file_name):
    try:
        video_config = TransferConfig(multipart_threshold=1024 * 20, max_concurrency=10,
                                multipart_chunksize=1024 * 25, use_threads=True)
        bucket_name = config.S3_BUCKET_NAME
        region = config.S3_REGION_NAME
        session = aws_session(region)
        s3_resource = session.resource('s3')
        aws_file_path = f"{S3_IMAGE_FOLDER}/{new_file_name}"
        bucket = s3_resource.Bucket(bucket_name)
        bucket.upload_file(
            Filename=video_file,
            Key=aws_file_path,
            Config=video_config,
            ExtraArgs={'ContentType': 'video/mp4'},
        )
        s3_profile_pic_name = f"https://{bucket_name}.s3.amazonaws.com/episode/{new_file_name}"
        return s3_profile_pic_name, True
    except Exception as e:
        print(e)
        return None, False


def get_all_language_id():
    all_language =[]
    languages = get_all_languages()
    for language in languages:
        if language["language_name"] == "English":
            continue
        language_details = {"language_id":language["language_id"], "language_name":language["language_name"]}
        all_language.append(language_details)
    return all_language
