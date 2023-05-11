import re
import random
import string
import hashlib
from datetime import datetime
from constant.region_map import regions
import string
import calendar
import time

regex_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
regex_name = r"^[a-zA-Z\s]+$"
allowed_image_extentions = ['jpg', 'jpeg', 'png']


def generate_alphanumeric_string(length=5):
    x = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))
    return str(x.lower())


def encryption(str):
    result = hashlib.sha256(str.encode())
    return result.hexdigest()


def is_email_valid(email):
    if re.search(regex_email, email):
        return True
    else:
        return False


def datetime_to_string(datetime_obj):
    return datetime_obj.strftime("%b %d %Y, %H:%M")


def is_valid_date_string_format(datetime_str):
    try:
        datetime.strptime(datetime_str, '%m-%d-%Y')
        return True
    except  Exception:
        return False


def string_to_date(datetime_str):
    return datetime.strptime(datetime_str, '%m-%d-%Y')


def string_to_date_for_slot_create(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d')


def string_to_time_for_slot_create(time_str):
    return datetime.strptime(time_str, "%H:%M")


def date_to_string_for_slot(datetime_obj):
    return datetime_obj.strftime('%Y-%m-%d')


def time_to_string_for_slot(time_obj):
    return time_obj.strftime("%H:%M")



#############################################################3
import uuid

from flask import render_template, session
import hashlib
import re
import random
import time, datetime




regex_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
regex_phone_no = r"^\+?(44)?(0|7)\d{9,13}$"


def create_md5(string):
    return hashlib.md5(string.encode("utf-8")).hexdigest()

def is_position_valid(position):
    try:
        valid_position = int(position)
        if valid_position > 0 :
            return True
        else:
            return False
    except Exception as e:
        return False


def is_id_valid(number):
    try:
        val = int(number)
        return True
    except ValueError:
       return False


def is_email_valid(email):
    if re.search(regex_email, email):
        return True
    else:
        return False


def get_six_digit_number():
    number = random.randint(100000, 999999)
    print(number)
    return number


def get_current_time_milli_sec():
    return round(time.time() * 1000)


def is_special_character_exists(string):
    regex = re.compile('[@_!."#$%^&*()<>?/\|}{~:]')
    if (regex.search(string) == None):
        print("String is accepted")
        if "'" in string:
            return False
        else:
            return True
    else:
        print("String is not accepted.")
        return False


def name_validation(name):
    regex_name = re.compile('([a-z]+)( [a-z]+)*( [a-z]+)*$', re.IGNORECASE)
    name_obj = regex_name.search(name)
    if name_obj is not None:
        return True
    else:
        return False


def int_validation(phone_number):
    try:
        if phone_number is not None:
            regex_number = re.compile(r'^[-+]?[0-9]+$')
            num_obj = regex_number.match(phone_number)
        else:
            num_obj = None
        if num_obj is not None:
            return True
        else:
            return False
    except Exception as error:
        print(error)
        return False


def num_validation(number):
    try:
        if number is not None:
            regex_number = re.compile(r'^[-+]?[0-9]+$')
            num_obj = regex_number.match(number)
        else:
            num_obj = None
        if num_obj is not None:
            return True
        else:
            print("else false")
            return False
    except Exception as error:
        print(error)
        print("else Exception")
        return False



def is_num_validation(number):
    try:
       number_m = int(number)
       return True
    except Exception as error:
        return False


def email_validation(email):
    if email is not None:
        regex_email = re.compile('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        email_object = regex_email.match(email)
    else:
        email_object = None
    if email_object is not None:
        return True
    else:
        return False


def user_name_validation(user_name):
    regex_name = re.compile('^[a-zA-Z0-9]+([_]?[a-zA-Z0-9]+)*$', re.IGNORECASE)
    user_name_obj = regex_name.search(user_name)
    if user_name_obj is not None:
        return True
    else:
        return False


def user_otp_validation(user_name):
    regex_name = re.compile('^[0-9]{4}$', re.IGNORECASE)
    user_name_obj = regex_name.search(user_name)
    if user_name_obj is not None:
        return True
    else:
        return False


def password_validation(password):
    regex_password = re.compile('^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', re.IGNORECASE)
    user_password_obj = regex_password.search(password)
    if user_password_obj is not None:
        return True
    else:
        return False


# def phone_number_validation(phone_number):
#     regex_phone_number = re.compile('((\+*)((0[ -]+)*|(91 )*)(\d{12}+|\d{10}+))|\d{5}([- ]*)\d{6}', re.IGNORECASE)
#     user_phone_number_obj = regex_phone_number.search(phone_number)
#     if user_phone_number_obj is not None:
#         return True
#     else:
#         return False


def phone_number_validation(phone_number):
    regex_phone_number = re.compile('^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', re.IGNORECASE)
    user_phone_number_obj = regex_phone_number.search(phone_number)
    print(user_phone_number_obj)
    if user_phone_number_obj is not None:
        if len(phone_number) == 10:
            return True
        else:
            return False
    else:
        return False


# check if input parameters are empty or not
def empty_param_check(param):
    if param is not None and param != "":
        return False
    else:
        return True


def valid_gender_type_check(gender):
    accepted_gender = ["Male", "Female", "Transgender", "Others"]
    try:
        if gender in accepted_gender:
            return True
        else:
            return False
    except Exception as error:
        print("Exception valid_gender_type_check")
        print(error)
        return False


def valid_dob_format_check(date_of_birth):
    try:
        dob = datetime.datetime.strptime(date_of_birth, "%m/%d/%Y").date()
        return True
    except Exception as error:
        print("Exception valid_dob_format_check")
        print(error)
        return False


def valid_date_format_check_mm_dd_yy(date_str):
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        print(dt)
        return True
    except Exception as error:
        print("Exception valid_dob_format_check")
        print(error)
        return False


def covert_str_to_date(str_date):
    try:
        dob = datetime.datetime.strptime(str_date, "%m/%d/%Y").date()
        return dob
    except Exception as error:
        print("Exception covert_str_to_date")
        print(error)
        return None


# V1
def string_to_date(str_date):
    return datetime.datetime.strptime(str_date, "%Y-%m-%d").date()


# V1
def number_of_days(d1, d2):
    return (d1 - d2).days


# V1 this code for add/update admin youth league check date range
def is_valid_date_range(r_s_d, r_e_d):
    res = number_of_days(r_s_d, r_e_d)
    return True if res < 0 else False


# get current time in milli sec
def get_current_time_milli_sec():
    return round(time.time() * 1000)


def get_time_in_milli_sec(minute):
    current_time = datetime.datetime.now()
    ten_minutes_ago = current_time + datetime.timedelta(minutes=minute)
    return int(ten_minutes_ago.timestamp() * 1000)


# V1
# convert normal response data into json
def get_response(status, message, result):
    data = {'status': status, 'message': message, 'data': result}
    return data


# check for valid token
def is_token_valid(token):
    try:
        token = token.split(' ')
        token_bytes = bytes(token[1], 'utf-8')
        jwt_decode = jwt.decode(token_bytes, jwt_key, algorithms='HS256')
        print(jwt_decode)
        if jwt_decode['app_jwt_key'] == api_jwt_key:
            return True
        else:
            return False
    except Exception as error:
        print(error)
        return False


def verify_token(token):
    try:
        token_bytes = bytes(token, 'utf-8')
        jwt_decode = jwt.decode(token_bytes, jwt_key, algorithms='HS256')
        print(jwt_decode)
        if jwt_decode['app_jwt_key'] == api_jwt_key:
            return True
        else:
            return False
    except Exception as error:
        print(error)
        return False


# create jwt token
# def create_jwt_token(user_id, name, email):
#     payload = {'id': user_id, 'name': name, 'email': email}
#     encoded_token = jwt.encode(payload, jwt_key, algorithm='HS256')
#     return encoded_token


# get app user id from jwt token
# def get_app_user_id_jwt_token(token):
#     try:
#         token = token.split(' ')
#         token_bytes = bytes(token[1], 'utf-8')
#         payload = jwt.decode(token_bytes, jwt_key, algorithms='HS256')
#         app_user_id = payload['id']
#         return int(app_user_id)
#     except Exception as error:
#         print(error)
#         return 0


# # create jwt token with time
# def create_jwt_token_with_time(user_id, first_name, last_name, email):
#     add_time = get_time_in_milli_sec(1)
#     payload = {'id': user_id, 'first_name': first_name, 'last_name': last_name, 'email': email, 'exp': add_time}
#     encoded_token = jwt.encode(payload, jwt_key, algorithm='HS256')
#     print(encoded_token)
#     return encoded_token.decode('utf-8')


# check for valid jwt token
# def is_valid_jwt_token(token):
#     data = {}
#     try:
#         print(token)
#         token = token.split(' ')
#         token_bytes = bytes(token[1], 'utf-8')
#         raw = jwt.decode(token_bytes, jwt_key, algorithms='HS256')
#         exp_time = raw['exp']
#         dt_current = get_current_time_milli_sec()
#         if exp_time > dt_current:
#             print('valid')
#             data['status'] = True
#             data['message'] = 'Valid auth token'
#         else:
#             print('Exp')
#             data['status'] = True
#             data['message'] = 'Token Expired'
#     except Exception as error:
#         print(error)
#         data['status'] = False
#         data['message'] = 'Invalid Token'
#     return data




# def get_demo_email_temp(name):
#     return render_template('email/demo_email_temp.html', name=name)
#
#
# def get_admin_email_verification_otp_temp(email_otp):
#     return render_template('email/admin_email_verification_otp_temp.html', email_otp=email_otp)
#
#
# def get_admin_forgot_password_email_temp(link):
#     return render_template('email/admin_forgot_password_email_temp.html', link=link)


# For check authority whether login admin can edit and delete only login admin contents
def is_admin_access_edit_delete(role, admin_id, login_admin_id):
    if role == '0':
        return True
    elif role == '1':
        if admin_id == login_admin_id:
            return True
        else:
            return False
    else:
        return False


def get_payment_hash_token():
    # hash = hashlib.md5(get_four_digit_number()).digest().encode("base64")
    hash = hashlib.md5(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    alnum_hash = re.sub(r'[^a-zA-Z0-9]', "", hash)
    return alnum_hash[:16]


def amount_with_tax(amount):
    tax = (amount * tax_rate) / 100
    tax_float_number = "{:.2f}".format(tax)
    amount = amount + float(tax_float_number)
    return amount


def amount_in_cent(amount):
    amount_cent = amount * 100
    return int(amount_cent)


def sms_body_for_first_time_player_join(user_name, password, link):
    body = ' User Name ' + user_name + ' Password  ' + password + ' Link: ' + link
    return body


def failure_response(msg):
    print("failure_response")
    print(msg)
    return {'status': False, 'message': msg, 'data': None}


def success_response(msg, data):
    return {'status': True, 'message': msg, 'data': data}


def formatted_date(d):
    date = d.strftime("%Y-%m-%d %H:%M:%S")
    return date


ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


ALLOWED_PDF_EXTENSIONS = {'pdf', 'jpg', 'jpeg'}


def allowed_pdf_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_PDF_EXTENSIONS


def get_input_file_size(file_input_req):
    source_file_size = len(file_input_req.read())
    # source_file_size_mb = source_file_size / 1000000
    print("file size")
    print(source_file_size)
    file_input_req.seek(0)
    return source_file_size


def save_image_file_dir(source_image_pil, upload_dir, final_image):
    try:
        source_image_pil.save(upload_dir + final_image)
        return True
    except Exception as error:
        print(error)
        return False


def check_str_ids_are_number(ids):
    is_number = False
    try:
        ids_arr = ids.split(',')
        for id in ids_arr:
            if num_validation(id):
                is_number = True
            else:
                is_number = False
                break
    except Exception as e:
        print("Exception check_ids_are_number")
        is_number = False
    return is_number


# Function to check if number is power of 2 or not
def isPowerOfTwo(n):
    if n == 0:
        return False
    while n != 1:
        if n % 2 != 0:
            return False
        n = n // 2

    return True


def valid_gender_check(param):
    if param.lower() in ['male', 'female', 'others']:
        return True
    else:
        return False


# create default jwt token
def create_default_jwt_token(api_jwt_key):
    payload = {'app_jwt_key': api_jwt_key}
    encoded_token = jwt.encode(payload, jwt_key, algorithm='HS256')
    return encoded_token


# for generating random user id
def gen_user_id():
    id = uuid.uuid4()
    id = "user_" + str(id)[:32].replace("-", "")
    return id


def is_session_active():
    try:
        if session.get('active'):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        session['active'] = False
        return False




# def get_superadmin_email_verification_temp(email, password, name, url):
#     return render_template('email/superadmin_email_verification_temp.html', email=email, password=password, name=name,
#                            url=url)


# check validation of password
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%', '^', '*', '!', '%', '&', '-']
    res = {'status': True, 'error': None}

    if len(passwd) < 8:
        res = {'status': False, 'error': 'Length Should Be At Least 8'}

    elif not any(char.isdigit() for char in passwd):
        res = {'status': False, 'error': 'Your password should have at least one number'}

    elif not any(char.isupper() for char in passwd):
        res = {'status': False, 'error': 'Password Should Have At Least One Uppercase Letter'}

    elif not any(char.islower() for char in passwd):
        res = {'status': False, 'error': 'Password Should Have At Least One Lowercase Letter'}

    elif not any(char in SpecialSym for char in passwd):
        res = {'status': False, 'error': 'Password should have at least one symbol. Example: Test123!'}

    return res


def is_region_valid(region):
    for reg_key, reg_val in regions.items():
        if reg_key == region:
            return True
    return False


def is_name_valid(name):
    print(name)
    pattern = re.compile(regex_name)
    is_format_valid = bool(pattern.match(name))
    return is_format_valid


def is_download_status_valid(status):
  try:
      if status in ["downloaded","paused","in_progress"]:
          return True
      else:
          return False
  except Exception as e:
      return False


# Checking whether image format is correct or not
def is_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_image_extentions


def generate_master_episode_id():
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    random_str = ''.join(random.choices(string.ascii_lowercase, k=5))
    prefx = "mepi"
    master_episode_id = prefx + "-" + str(time_stamp)[:5] + "-" + random_str + "-" + str(time_stamp)[5:]
    return master_episode_id


def generate_episode_id():
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    random_str = ''.join(random.choices(string.ascii_lowercase, k=5))
    prefx = "epis"
    master_episode_id = prefx + "-" + str(time_stamp)[:5] + "-" + random_str + "-" + str(time_stamp)[5:]
    return master_episode_id


def get_all_avaialbale_languages(languages,languages_already_exixts):
    final_arr = []

    for l in languages:
        print("=====================")
        if l["language_name"] =="English":
            continue
        else:
            final_arr.append({"id": l["language_id"], "name": l["language_name"]})
    return final_arr


def is_valid_thumbnail(file):
    try:
        print(file.filename.split(".")[1])
        extension = file.filename.split(".")[-1]
        if extension in ["jpg","png","jpeg","PNG","JPG","JPEG"]:
            print("here-------")
            return True
        else:
            print("there--------")
            return False
    except Exception as e:
        return False


def is_valid_video(file):
    try:
        extension = file.filename.split(".")[-1]
        if extension in ["mp4","mov","avi","mkv","webm","MP4","MOV","AVI","MKV","WEBM"]:
            return True
        else:
            return False
    except Exception as e:
        return False


def is_valid_audio(file):
    try:
        extension = file.filename.split(".")[-1]
        if extension in ["mp3","wav","MP3","WAV"]:
            return True
        else:
            return False
    except Exception as e:
        return False





