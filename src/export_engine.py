import json
import os
import shutil

def export_workspace(user_dir, export_path):
    shutil.make_archive(export_path, 'zip', user_dir)

def import_workspace(zip_path, target_dir):
    shutil.unpack_archive(zip_path, target_dir)
