# class ApiMessage:
#     SOMETHING_WENT_WRONG = "Something went wrong"
#     LOGIN_SUCCESS = 'Login successful'
#     INVALID_LOGIN_CREDENTIALS = "The email or password is incorrect"

class ApiMessage:
    SUCCESS = 'Success'
    BLANK_EMAIL = 'Please enter an email address'
    BLANK_LOGIN_TYPE = 'Login Type can not be blank. Please select valid login type'
    BLANK_PASSWORD = 'Password can not be blank, please enter your password'
    BLANK_NAME = 'Name can not be blank. Please enter valid name'
    BLANK_PHONE = 'Phone No can not be blank. Please enter valid phone no'
    INVALID_PHONE = 'Phone number must contain 10 digits'
    INVALID_PASSWORD_LENGTH = 'Password length must be at least 6 characters'
    INVALID_EMAIL = "Please enter valid email id"
    SOMETHING_WENT_WRONG = 'Something went wrong. Try again later'
    EXCEPTION_MSG = 'Exception! Something went wrong. Try again later'
    # EMAIL_ALREADY_EXIST = 'Email already exist'
    PHONE_ALREADY_EXIST = 'Phone Number already exist'
    FIRST_NAME_CAN_NOT_BE_BLANK = 'First Name Can Not Be Blank'
    LAST_NAME_CAN_NOT_BE_BLANK = 'LAST Name Can Not Be Blank'
    ENTER_FIRST_NAME = 'Enter your First Name'
    ENTER_LAST_NAME = 'Enter your Last Name'
    ENTER_GENDER = 'Enter your Gender'
    ENTER_VALID_GENDER = 'Enter your Valid Gender'
    ENTER_DOB = 'Put DOB'
    VALID_DOB = 'Enter valid Date format(%m/%d/%Y)'
    ENTER_CITY = 'Enter City Name'
    INVALID_CITY = 'Invalid City id'
    INVALID_SPORTS = 'Invalid Sports id'
    SELECT_SPORTS_INTEREST = 'Select kid sports interest'
    ACCOUNT_DEACTIVATE = 'Your account is Deactivate'
    NO_USER_FOUND = 'No user found'
    NO_DATA_FOUND = 'No data found'
    EMAIL_NOT_EXIST = 'The email does not match our records'
    EMAIL_ALREADY_EXIST = 'This Email is already in use '
    KID_NAME_EXIST = 'Kid name already exist'
    USER_ID_BLANK = 'User id can not be blank. Please enter valid User id'
    USER_NAME_BLANK = 'User name can not be blank. Please enter valid User name'
    KID_ID_BLANK = 'Kid id can not be blank. Please enter valid Kid id'
    INVALID_USER_ID = 'Invalid User id'
    INVALID_USER_NAME = 'Invalid User Name'
    ADD_KID = 'Successfully add Player'
    UNABLE_ADD = 'Unable to add'
    UNABLE_UPDATE = 'Unable to Update'
    INPUT_FILE_NOT_FOUND = 'kindly upload image'
    INVALID_EXT = 'Kindly upload valid image'
    MAX_IMAGE_FILE_SIZE = "File size can not exceed 8 mb"
    NO_KID = "Kid not found"
    NO_ACCESS = "You Dont have add/update access"
    SUCCESS_UPDATE = 'Successfully Updated'
    NAME_ALREADY_EXIST = 'Name already exist'
    INVALID_LEAGUE_ID = 'Invalid league id'
    NO_LEAGUE_FOUND = 'No league data found'
    INVALID_KID_ID = 'Invalid kid id'
    INVALID_USER_ID_FOR_KID = 'Invalid user id for this kid'
    INPUT_PDF_FILE_NOT_FOUND = 'kindly upload PDF file'
    INPUT_PDF_EXT = 'kindly upload valid PDF file'
    INVALID_OTP = 'Invalid OTP'
    BLANK_OTP = 'Kindly put OTP'
    EXPIRED_OTP = 'OTP expired. Pls. try again.'
    TEAM_SHOULD_POWER_2 = 'Team number should be power of 2.'
    BLANK_FASTNAME = 'First Name can not be blank, please enter first name'
    BLANK_LASTNAME = 'Last Name can not be blank, please enter last name'
    INVALID_LOGIN = 'Please check user username or password or login type '
    OLD_PASSWORD_BLANK = 'Old password can not be blank, please enter your old password'
    NEW_PASSWORD_BLANK = 'New password can not be blank, please enter a new password in proper format'
    SAME_PASSWORD = ' New Password should not match with previous password'
    USER_ID_NOT_EXIST = 'This userid is not exist'
    USER_DELETED = 'User deleted successfully'
    UNABLE_TO_DELETE = 'Unable to delete the user'
    BLANK_GENDER = 'Gender Field can not be blank. Please select a valid gender'
    INVALID_GENDER = 'Please Choose a valid gender option'
    BLANK_LANGUAGE_NAME = 'Please enter the language name'
    BLANK_REGION = 'Please select a region'
    BLANK_LANGUAGE_ID = """Language id can't be blank"""
    BLANK_LANGUAGE_KEYWORDS = """Language keywords can't be blank"""
    INVALID_LANGUAGE_NAME = 'Please enter a valid language name'
    INVALID_REGION = 'Please select a valid region'
    SESSION_EXPIRED = 'Session expired!'
    INVALID_SESSION = 'Invalid session!'









class Signup:
    S_90 = 'User added successfully'
    S_91 = 'Successfully add User in Cognito'
    S_100 = 'This username already exists'
    S_101 = 'Invalid password format. Password should have Caps,Small, Special chars, Numbers and minimum length 8'
    S_102 = 'Email already exists'
    S_103 = 'Please confirm your signup, check Email for validation code'
    S_104 = 'Username doesnt exists'
    S_105 = 'Invalid Verification code'
    S_106 = 'User is already confirmed'
    S_107 = 'User Verified Successfully'
    S_108 = 'Username is not confirmed yet'
    S_109 = 'Please check your Registered email id for validation code'
    S_110 = 'Password has been changed successfully'
    S_111 = 'Password failed to changed'
    S_112 = 'Unable to signup'
    S_113 = 'Password changed successfully'
    S_114 = 'Unable to change user password '
    S_115 = 'User deleted successfully'


class Login:
    L_success = "Logged in successfully"
    L_failed = "Failed to login"


class cognito_resp_msg:
    cognito_incorrect_username_password = "The username or password is incorrect"
    cognito_user_not_confirmed = "User is not confirmed"
    UserNotFoundException = "User Not Found"
    InvalidParameterException = "Invalid parameters"
    ResourceNotFoundException = "Resource Not Found"
    NotAuthorizedExceptionAccessToken = "Invalid or expired access token"
    NotAuthorizedException = "Uer is not authorized"
    UserNotConfirmedException = "User not confirmed yet"
    InvalidPasswordException = " Invalid password"




class InputFormValidation:
    emailMission = "Email field Is Missing"
    passwordMission = "Password field Is Missing"
    loginTypeMissing = "Login Type field  Is Missing"
    firstNameMissing = "First name field  is missing"
    lastNameMissing = "Last name field  is missing"
    phoneNumberMissing = "Phone Number field  is missing"
    oldPasswordMissing = "Old Password field  is missing"
    newPasswordMissing = "New Password field is missing"
    userIdMissing = "User Id field is Missing"
    genderMissing = "Gender field  is Missing"


class LanguageMessages:
    languageNotExist = """Language does not exist"""
    englishNonDeletable = """Can't delete english language"""
    englishNonEditable = """Can't edit english language"""
    languageCreateSuccess = """Language created successfully"""
    languageCreateFail = """Language creation failed"""
    languageEditSuccess = """Language updated successfully"""
    languageEditFail = """Language update failed"""
    languageDeleteSuccess = """Language deleted successfully"""
    languageDeleteFail = """Language delete failed"""
    addLanguageKeywordsSuccess = """Language keywords added successfully"""
    addLanguageKeywordsFail = """Language keywords add failed"""
    updateLanguageKeywordsSuccess = """Language keywords updated successfully"""
    updateLanguageKeywordsFail = """Language keywords update failed"""
    getLanguageSuccess = """Language details fetched successfully"""
    getLanguageFail = """Language details fetch failed"""
    languageIdMissing = """Language id is missing"""
    regionalLanguageIdMissing = """Regional language id is missing"""
    languageNameMissing = """Language name is missing"""
    regionMissing = """Region is missing"""
    languageKeywordsMissing = """Language keywords is missing"""
    languageContainsContent = """This language cannot be deleted , please clear contents of language before deleting"""


class ForgotPassword:
    pass



