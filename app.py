import os
from datetime import timedelta

from flask import Flask, redirect, url_for
from flask_cors import CORS

from constant.constant import default_files_dir_created
from controller.api import appUser
from controller.episode_controller import episode
from controller.language_controller import language
from controller.page_view import page_view
from controller.web_user import web_user
from controller.series_controller import series


app = Flask(__name__)

app.config['SECRET_KEY'] = 'dZwwMGShspJPSCjuwty4nbGOQPlzhXcA#^b03h&y%S|2>vGyVr=e*@Z_b1<{'
app.register_blueprint(page_view)
app.register_blueprint(web_user, url_prefix='/api/v1/web-user')
app.register_blueprint(language, url_prefix='/api/v1/language')
app.register_blueprint(series, url_prefix='/api/v1/series')
app.register_blueprint(episode, url_prefix='/api/v1/episode')
app.register_blueprint(appUser, url_prefix='/api/v1/appUser')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
CORS(app)
default_files_dir_created()


@app.route("/")
def index():
    return redirect(url_for('page_view_controller.page_view_login'))


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', debug=True)
    # if os.environ['ENV'] == "prod":
    #     app.run(host='0.0.0.0', debug=True)  # local webserver : app.run()
    # else:
    #     app.run(host='0.0.0.0', port=5000, debug=True)

