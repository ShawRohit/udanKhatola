from flask import session

# This app name will show in browser title bar
app_name = "Scripture Videos"


# After user login when user access page, this time it will return in page for show
def user_obj():
    return {
        "email": session['email'],
        "role": session['role'],
        "username": session['username'],
        "user_id": session['user_id']
    }


# For individual page all static details
def get_page_details(page_name):
    if page_name == "admin-login":
        return admin_login_page()
    if page_name == "super-admin-login":
        return super_admin_login_page()
    if page_name == "verify-email":
        return verify_email()
    if page_name == "register":
        return register_page()
    if page_name == "forgot-password":
        return forgot_password()
    if page_name == "change-password":
        return change_password()
    if page_name == "password-reset":
        return password_reset()
    if page_name == "verify-otp":
        return verify_otp()
    if page_name == "confirm-otp":
        return confirm_otp()

    if page_name == "dubbing-management":
        return dubbing_management()
    if page_name == "language-management":
        return language_management()
    if page_name == "admin-list":
        return admin_list()
    if page_name == "outlet_list":
        return outlet_list()
    if page_name == "outlet-add":
        return outlet_add()
    if page_name == "outlet-edit":
        return outlet_edit()
    if page_name == "outlet-details":
        return outlet_details()
    if page_name == "restaurant":
        return restaurant()
    if page_name == "restaurant-details":
        return restaurant_details()
    if page_name == "language-details":
        return language_details()


def admin_login_page():
    return {
        "title": "Login | " + app_name
    }


def super_admin_login_page():
    return {
        "title": "Super Admin Login | " + app_name
    }


def verify_email():
    return {
        "title": "Verify Email | " + app_name
    }


def register_page():
    return {
        "title": "Register | " + app_name
    }


def forgot_password():
    return {
        "title": "Forgot Password | " + app_name
    }


def change_password():
    return {
        "title": "Change Password | " + app_name
    }


def password_reset():
    return {
        "title": "Password Reset | " + app_name
    }


def verify_otp():
    return {
        "title": "Verify OTP | " + app_name
    }


def confirm_otp():
    return {
        "title": "Confirm OTP | " + app_name
    }


def dubbing_management():
    return {
        "title": "Dubbing Management | " + app_name
    }

    # page_name = "Dubbing Management"
    # return {
    #     "title": page_name + " | " + app_name,
    #     "page_title": page_name,
    #     "user_details": user_obj(),
    #     "breadcrumb": [
    #         {"url": "/dubbing-management", "name": page_name}
    #     ]
    # }


def language_management():
    return {
        "title": "Language Management | " + app_name
    }


def admin_list():
    page_name = "Admin List"
    return {
        "title": page_name + " | " + app_name,
        "page_title": page_name,
        "user_details": user_obj(),
        "breadcrumb": [
            {"url": "/dashboard", "name": page_name}
        ]
    }


def outlet_list():
    page_name = "Outlets"
    return {
        "title": page_name + " | " + app_name,
        "page_title": page_name,
        "user_details": user_obj(),
        "breadcrumb": [
            {"url": "/dashboard", "name": page_name}
        ]
    }


def outlet_add():
    page_name = "Outlet Add"
    return {
        "title": page_name + " | " + app_name,
        "page_title": page_name,
        "user_details": user_obj(),
        "breadcrumb": [
            {"url": "/dashboard", "name": page_name}
        ]
    }


def outlet_edit():
    page_name = "Outlet Edit"
    return {
        "title": page_name + " | " + app_name,
        "page_title": page_name,
        "user_details": user_obj(),
        "breadcrumb": [
            {"url": "/dashboard", "name": page_name}
        ]
    }


def outlet_details():
    page_name = "Outlet Details"
    return {
        "title": page_name + " | " + app_name,
        "page_title": page_name,
        "user_details": user_obj(),
        "breadcrumb": [
            {"url": "/dashboard", "name": page_name}
        ]
    }


def restaurant():
    page_name = "Restaurant"
    return {
        "title": page_name + " | " + app_name,
        "page_title": page_name,
        "user_details": user_obj(),
        "breadcrumb": [
            {"url": "/dashboard", "name": page_name}
        ]
    }


def restaurant_details():
    page_name = "Restaurant Details"
    return {
        "title": page_name + " | " + app_name,
        "page_title": page_name,
        "user_details": user_obj(),
        "breadcrumb": [
            {"url": "/dashboard", "name": page_name}
        ]
    }


def language_details():
    return {
        "title": "Language Details | " + app_name,
    }
