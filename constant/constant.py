import os

from config_env.conf_env import config


def default_files_dir_created():
    if not os.path.isdir(config.upload_folder):
        print("entered")
        os.mkdir(config.upload_folder)
