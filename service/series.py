import math
import os
import time
# import cv2
import cv2

from app_session.user_session import get_current_user_gen_id
from model.episode import delete_episode_by_seriees_id
from model.series import create_series, is_series_exist, get_series_by_series_id, update_series, delete_series_by_id
from model.series_episode_language import insert_language, is_series_language_exist, \
    delete_series_language_support_by_id, get_language_by_series_id
from util.message import LanguageMessages, ApiMessage
from util.utility import generate_alphanumeric_string, get_response, is_image_file
import boto3
from config_env.conf_env import config

S3_REGION_NAME = config.S3_REGION_NAME
S3_IMAGE_FOLDER = config.S3_IMAGE_FOLDER
S3_BUCKET_NAME = config.S3_BUCKET_NAME


def create_series_db(series_name, series_thumbnail, series_position,series_tags):
    if series_thumbnail != "":
        if series_thumbnail.filename != '':
            if not is_image_file(series_thumbnail.filename):
                return get_response(False, "Please select proper image file (.jpg, .jpeg, .png)", {})
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            dynamic_file_name = str(timestamp) + '_' + str(series_thumbnail.filename).strip().replace(" ","")
            cv2_file_name = 'cv2_' + str(series_thumbnail.filename)
            f_path = os.path.join(temp_folder, dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, cv2_file_name)
            series_thumbnail.save(cv2_f_path)
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
        series_thumbnail, is_file_uploaded = upload_image_into_bucket(f_path, dynamic_file_name)
        os.remove(f_path)
    res = create_series("msr_" + generate_alphanumeric_string(5), series_name,series_tags,
                        str(get_current_user_gen_id()), series_thumbnail, int(series_position))
    if res is not None:
        return get_response(True, "Series created successfully", {})
    else:
        return get_response(False, "Series creation failed", {})


def add_language_for_series(series_id, language_name,language_id,languageId, title, description):

    series_thumbnail, is_file_uploaded = None, None

    res = insert_language(language_id,language_name,languageId,  title, description,series_id,"", str(get_current_user_gen_id()))
    if language_id == "" or language_id is None :

        if res is not None:
            return get_response(True, "Language created successfully", res)
        else:
            return get_response(False, "Language creation failed", {})
    else:
        if res is not None:
            return get_response(True, "Language edited successfully", {})
        else:
            return get_response(False, "Language edit failed", {})



def update_series_db(series_id,series_name, series_thumbnail,  prev_thumbnail,editseriestags):
    if series_thumbnail != "":
        if series_thumbnail.filename != '':
            if not is_image_file(series_thumbnail.filename):
                return get_response(False, "Please select proper image file (.jpg, .jpeg, .png)", {})
            temp_folder = 'uploads'
            ts = time.time()
            timestamp = math.trunc(ts)
            dynamic_file_name = str(timestamp) + '_' + str(series_thumbnail.filename).strip().replace(" ","")
            cv2_file_name = 'cv2_' + str(series_thumbnail.filename)
            f_path = os.path.join(temp_folder, dynamic_file_name)
            cv2_f_path = os.path.join(temp_folder, cv2_file_name)
            series_thumbnail.save(cv2_f_path)
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
        series_thumbnail, is_file_uploaded = upload_image_into_bucket(f_path, dynamic_file_name)
        os.remove(f_path)

    if dynamic_file_name is None:
        res = update_series(series_name,prev_thumbnail,series_id,editseriestags)
        # res = create_series("msr_" + generate_alphanumeric_string(5), series_name,
        #                     str(get_current_user_gen_id()), prev_thumbnail, int(series_position))
        if res is not None:
            return get_response(True, "Series Updated successfully", {})
        else:
            return get_response(False, "Series Update failed", {})
    else:
        res = update_series(series_name,  series_thumbnail, series_id,editseriestags)
        if res is not None:
            return get_response(True, "Series Updated successfully", {})
        else:
            return get_response(False, "Series Update failed", {})



# def set_language_affix(language_id):
#     if not is_language_exist(language_id):
#         return get_response(False, LanguageMessages.languageNotExist, {})
#     else:
#         session['current_language_id'] = language_id
#         return get_response(True, ApiMessage.SUCCESS, {'language_id': language_id})


# Function for creating a boto3 session
def aws_session(region):
    return boto3.session.Session(region_name=region)


# Function for uploading image files in s3 bucket
def upload_image_into_bucket(image, new_file_name):
    # try:
    bucket_name = config.S3_BUCKET_NAME
    region = config.S3_REGION_NAME
    session = aws_session(region)
    s3_resource = session.resource('s3',aws_access_key_id=config.aws_access_key_id,aws_secret_access_key= config.aws_secret_access_key)
    aws_file_path = f"{S3_IMAGE_FOLDER}/{new_file_name}"
    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(
        Filename=image,
        Key=aws_file_path,
        ExtraArgs={"ContentType": "image/jpeg"}
    )

    s3_profile_pic_name = f"https://{bucket_name}.s3.amazonaws.com/series/{new_file_name}"
        # s3_profile_pic_name = new_file_name
    return s3_profile_pic_name, True
    # except Exception as e:
    #     print(e)
    #     return None, False


def get_series_details(series_id):
    if not is_series_exist(series_id):
        return get_response(False, "Series not exists", {})
    else:
        res = get_series_by_series_id(series_id)
        if res is not None:
            return get_response(True, "Series fetched successfully", res)
        else:
            return get_response(False, "Fetched to fail series", {})


def delete_series_db(series_id):
    if not is_series_exist(series_id):
        return get_response(False, "Series does not exists", {})
    else:
        res = delete_series_by_id(series_id)
        if res:
            delete_episode_res = delete_episode_by_seriees_id(series_id)
            if delete_episode_res:
                return get_response(True, "Series deleted successfully", {})
            else:
                return get_response(True, "Series deleted successfully but failed to delete underlying episodes", {})
        else:
            return get_response(False, "Failed to delete series", {})


def delete_series_language_support_db(language_id):
    if not is_series_language_exist(language_id):
        return get_response(False, "Language does not exists", {})
    else:
        res = delete_series_language_support_by_id(language_id)
        if res:
            return get_response(True, "Language deleted successfully", {})
        else:
            return get_response(False, "Failed to delete Language", {})



def get_all_language_by_series_id(series_id):
    all_language =[]
    languages = get_language_by_series_id(series_id)
    for language in languages:
        if language["language_name"] == "English":
            continue
        language_details = {"language_id":language["languageId"],"language_name":language["language_name"]}
        all_language.append(language_details)
    return all_language