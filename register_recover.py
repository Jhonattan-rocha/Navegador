import datetime
import json
import os

from PySide6.QtWidgets import QWidget, QLayout


def register_download_history(suggested_file_name: str, folder_path: str, status: str,
                              download_time: datetime.datetime, file_saved_main: str = 'download_history.json'):
    with open(os.path.abspath(os.path.join('.', 'configs', file_saved_main)), 'rb') as file:
        file_read = file.read()
        json_file = {}
        if not file_read:
            json_file = {"Files": [{"name": f"{suggested_file_name}", "path": f"{folder_path}",
                                    "download_time": f"{download_time}", "status": f"{status}"}]}
        else:
            json_file = json.loads(file_read)
            json_file = dict(json_file)
            json_file["Files"].insert(0,
                                      {"name": f"{suggested_file_name}", "path": f"{folder_path}",
                                       "download_time": f"{download_time}", "status": f"{status}"})

        with open(os.path.abspath(os.path.join('.', 'configs', file_saved_main)), 'wb') as file2:
            file2.write(str(json_file).replace("'", '"').encode('utf8'))


def recover_download_history(file_saved: str = 'download_history.json') -> dict:
    with open(os.path.join('.', 'configs', file_saved), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)
            return js
        return {}


def remove_download_history_item(download_data: dict, remove_view: bool = False, widget: QWidget = None,
                                 layout: QLayout = None, file_saved_main: str = 'download_history.json') -> bool:
    with open(os.path.join('.', 'configs', file_saved_main), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)
            js_copy = {'Files': []}
            for file_saved in js['Files']:
                if file_saved['name'] != download_data['name']:
                    js_copy['Files'].insert(0, file_saved)

            with open(os.path.abspath(os.path.join('.', 'configs', file_saved_main)), 'wb') as file2:
                file2.write(str(js_copy).replace("'", '"').encode('utf8'))
        else:
            return False
    if remove_view:
        layout.removeWidget(widget)
        layout.update()
    return True

# ------------------
