#!python3
# -*- coding: UTF-8 -*-

import ctypes
import datetime
import glob
import hashlib
import json
import os
import shutil

def get_volume_information(volume):
    result = config['DRIVE_LABELS'].get(volume.replace(":\\", "").upper())
    if result is None:
        volume_name_buffer = ctypes.create_unicode_buffer(1024)
        ctypes.windll.kernel32.GetVolumeInformationW(ctypes.c_wchar_p(volume), volume_name_buffer, ctypes.sizeof(volume_name_buffer))
        result = volume_name_buffer.value if volume_name_buffer.value != "" else None
    return result

def get_destination_directory(source_file_full_path):
    source_directory = os.path.dirname(source_file_full_path)
    drive, directory = os.path.splitdrive(source_directory)
    sub_dir = "{} - {}".format(drive.replace(":", "").upper(), get_volume_information(drive + "\\"))
    return os.path.abspath(os.path.join(config['BACKUP_DIRECTORY'], sub_dir, "." + directory))

def get_source_file_hash(source_file_full_path):
    result = None
    with open(source_file_full_path, 'rb') as content_file:
        content = content_file.read()
        new_hash = hashlib.sha512()
        new_hash.update(content)
        result = new_hash.hexdigest()
    return result[:10]

def get_destination_filename(source_file_full_path, filehash = None, modification_time = False):
    if filehash is None:
        filehash = get_source_file_hash(source_file_full_path)
    filename = os.path.basename(source_file_full_path)
    if modification_time:
        file_datetime = datetime.datetime.fromtimestamp(int(os.stat(source_file_full_path).st_mtime)).strftime("%Y%m%d%H%M%S")
    else:
        file_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return "{}.{}.{}.backup".format(filename, file_datetime, filehash)

def get_destination_file_full_path(source_file_full_path, filehash = None, modification_time = False):
    return os.path.abspath(os.path.join(get_destination_directory(source_file_full_path), get_destination_filename(source_file_full_path, filehash, modification_time)))

def twinner():
    for item in config['file_list']:
        if os.path.isfile(item):
            filehash = get_source_file_hash(item)
            print("Copying {} to {}...".format(item, get_destination_file_full_path(item, filehash)))
            try:
                destination_file_full_path = get_destination_file_full_path(item)
                search_string = "{}{}*{}.backup".format(os.path.dirname(destination_file_full_path), os.sep, filehash)
                if len(glob.glob(search_string)) == 0:
                    shutil.copyfile(item, destination_file_full_path)
                else:
                    print("{} is already saved".format(item))
            except FileNotFoundError as fnfe:
                if fnfe.args[1] == 'No such file or directory' and fnfe.filename == destination_file_full_path:
                    os.makedirs(os.path.dirname(destination_file_full_path))
                    shutil.copyfile(item, destination_file_full_path)

if __name__ == '__main__':
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    config = json.load(open(os.path.join(PROJECT_PATH, 'config.json')))

    twinner()
