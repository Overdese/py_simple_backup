#!/usr/bin/env python3

import config
import os
import shutil
from datetime import datetime

import re

home_pattern = re.compile(r'^~')


def get_backup_sets():
    """
    Get backup sets from config.py file
    """

    result = dict()
    for e in dir(config):
        if e.startswith('SET_'):
            result[e.replace('SET_', '')] = getattr(config, e)
    return result
            

def backup_set(name, data):
    """
    Backup files path from set
    """
    src = os.path.join(name, datetime.now().strftime(config.TIMESTAMP_DIR))
    if os.path.exists(src):
        shutil.rmtree(src)
    for src in data:
        src = home_pattern.sub(os.path.expanduser('~'), src)
        dst = os.path.join(name, datetime.now().strftime(config.TIMESTAMP_DIR), *src.split(os.sep))
        copy_data(src, dst)


def copy_data(src, dst):    
    """
    Copy file or folder from src to dst
    """

    if os.path.isdir(src):
        shutil.copytree(src, dst)
    elif os.path.isfile(src):
        try:
            os.makedirs(os.path.split(dst)[0])
        except:
            pass
        shutil.copyfile(src, dst)


if __name__ == '__main__':
    for e in get_backup_sets():
        backup_set(e, get_backup_sets()[e])
