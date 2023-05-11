from flask import session


def create_user_session(user_details):
    session.permanent = True
    session['active'] = True
    session['data'] = user_details


def destroy_user_session():
    session.permanent = False
    session['active'] = False
    session['data'] = {}
    session.clear()


def is_user_active():
    try:
        return True if session['active'] else False
    except Exception as e:
        session['active'] = False
        return False


def get_current_user_gen_id():
    return session['data']['web_user_id']
