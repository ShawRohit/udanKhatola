import os
import boto3, base64, hmac, hashlib

from util.message import cognito_resp_msg
from util.response import get_response

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
USER_POOL_ID = os.environ['USER_POOL_ID']
REGION_NAME = os.environ['REGION_NAME']
aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key']

client = boto3.client('cognito-idp', aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key, region_name=REGION_NAME)


# Get secret hash in cognito
def get_secret_hash(email):
    msg = email + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def cognito_user_sign_up(email, password):
    client = boto3.client('cognito-idp', region_name='us-west-2', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(email),
            Username=email,
            Password=password
        )

    except client.exceptions.InvalidParameterException as e:
        return {"status": False, "message": str(e)}
    except client.exceptions.UsernameExistsException as e:
        return {"status": False, "message": "This email already exists"}
    except client.exceptions.InvalidPasswordException as e:
        return {"status": False, "message": "Invalid password format"}
    except client.exceptions.LimitExceededException:
        return {"status": False, "message": "Limit exceeded"}
    except Exception as e:
        print(e)
        return {"status": False, "message": "Something went wrong"}
    return {"status": True, "data": resp, "message": "User registration is successful"}


# Initiate auth in cognito with username and password
def initiate_auth(client, username, password):
    secret_hash = get_secret_hash(username)
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret_hash,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password,
            })

    except client.exceptions.NotAuthorizedException:
        return None, cognito_resp_msg.cognito_incorrect_username_password

    except client.exceptions.UserNotConfirmedException:
        return None, cognito_resp_msg.cognito_user_not_confirmed

    except client.exceptions.UserNotFoundException as e:
        return None, cognito_resp_msg.UserNotFoundException
        # return {"status": False, "message": "User Not Found"}

    except client.exceptions.InvalidParameterException as e:
        print("Invalid")
        return None, cognito_resp_msg.InvalidParameterException
        # return {"status": False, "message": "Invalid parameters"}

    except client.exceptions.ResourceNotFoundException as e:
        return None, cognito_resp_msg.ResourceNotFoundException

    except Exception as e:
        return None, e.__str__()

    return resp, None


def get_user_details_by_access_token(access_token):
    try:
        response = client.get_user(
            AccessToken=access_token
        )
        # print(response)
    except client.exceptions.NotAuthorizedException:
        return {"status": False, "message": cognito_resp_msg.NotAuthorizedExceptionAccessToken}
    except client.exceptions.UserNotFoundException as e:
        return {"status": False, "message": cognito_resp_msg.UserNotFoundException}
    except client.exceptions.InvalidParameterException as e:
        return {"status": False, "message": cognito_resp_msg.InvalidParameterException}
    except client.exceptions.ResourceNotFoundException as e:
        return {"status": False, "message": cognito_resp_msg.ResourceNotFoundException}
    except Exception as e:
        return {"status": False, "message": str(e)}

    return {"status": True, "data": response}


def app_user_login(email, password):
    resp, msg = initiate_auth(client, email, password)
    if msg != None:
        if msg == 'User is not confirmed':
            return {'status': False, 'isAccountConfirmed': False,
                    'message': cognito_resp_msg.cognito_user_not_confirmed}

        print("=============not-confirmed=======")
        print("=============not-confirmed======="+str(msg))

        return {'status': False, 'message': str(msg)}

    if resp.get("AuthenticationResult"):
        if resp.get("AuthenticationResult"):
            user_details = get_user_details_by_access_token(resp["AuthenticationResult"]["AccessToken"])
            user_attributes = user_details['data']['UserAttributes']
            email = user_details['data']['Username']

            user_dict = {}
            for user_attribute in user_attributes:
                if user_attribute['Name'] == 'sub':
                    user_dict['cognito_id'] = user_attribute['Value']

        return {"status": True, "message": "Login successful",
                "access_token": resp["AuthenticationResult"]["AccessToken"],
                "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                "Idtoken": resp["AuthenticationResult"]["IdToken"],
                "cognito_id": user_dict['cognito_id'],
                "email": email
                }


# Admin set app user's password in cognito
def cognito_set_password(username, password):
    try:
        resp = client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=username,
            Password=password,
            Permanent=True
        )
        # print(resp)
        data = get_response(True, "Password set successfully", {})

    except client.exceptions.InvalidParameterException as e:
        data = get_response(False, "Invalid parameter", {})
    except client.exceptions.UserNotFoundException as e:
        data = get_response(False, "This email does not exist", {})
    except client.exceptions.InvalidPasswordException as e:
        data = get_response(False, "Your password must contain at least one lower case letter, one upper case letter, "
                                   "one number, one special character, and be at least 8 characters long", {})
    except client.exceptions.ResourceNotFoundException as e:
        data = get_response(False, "Resource not found", {})
    except client.exceptions.TooManyRequestsException as e:
        data = get_response(False, "Too many request please try again later", {})
    except client.exceptions.NotAuthorizedException as e:
        data = get_response(False, "User is not authorized", {})
    except Exception as e:
        data = get_response(False, str(e), {})
    return data