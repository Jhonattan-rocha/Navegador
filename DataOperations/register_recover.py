import datetime
import json
import os

from PySide6.QtWidgets import QWidget, QLayout


def register_download_historic(suggested_file_name: str, folder_path: str, status: str,
                               download_time: datetime.datetime, file_saved_main: str = 'download_history.json'):
    with open(os.path.abspath(os.path.join('configs', file_saved_main)), 'rb') as file:
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

        with open(os.path.abspath(os.path.join('configs', file_saved_main)), 'wb') as file2:
            file2.write(str(json_file).replace("'", '"').encode('utf8'))


def recover_download_historic(file_saved: str = 'download_history.json', f: str = "") -> dict:
    with open(os.path.join('configs', file_saved), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)

            if bool(f):
                f_list = [his for his in js['Files'] if f in his['path'] or f in his['name']]
                return {"Files": f_list}
            return js
        return {}


def remove_download_historic_item(download_data: dict, remove_view: bool = False, widget: QWidget = None,
                                  layout: QLayout = None, file_saved_main: str = 'download_history.json') -> bool:
    with open(os.path.join('configs', file_saved_main), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)
            js_copy = {'Files': []}
            for file_saved in js['Files']:
                if file_saved['name'] != download_data['name']:
                    js_copy['Files'].insert(0, file_saved)

            with open(os.path.abspath(os.path.join('configs', file_saved_main)), 'wb') as file2:
                file2.write(str(js_copy).replace("'", '"').encode('utf8'))
        else:
            return False
    if remove_view:
        layout.removeWidget(widget)
        widget.deleteLater()
        layout.update()
    return True


# ------------------

def register_historic(site: str, cookies: list,
                      download_time: datetime.datetime, file_saved_main: str = 'historic.json'):
    with open(os.path.abspath(os.path.join('configs', file_saved_main)), 'rb+') as file:
        file_read = file.read()
        json_file = {}
        if not file_read:
            json_file = {"Sites": [{"id": 0, "name": f"{site}", "cookies": cookies, "date_time": f"{download_time}"}]}
        else:
            json_file = json.loads(file_read)
            json_file = dict(json_file)
            json_file["Sites"].insert(0, {"id": len(json_file["Sites"]), "name": f"{site}", "cookies": cookies,
                                          "date_time": f"{download_time}"})

        with open(os.path.abspath(os.path.join('configs', file_saved_main)), 'wb') as file2:
            file2.write(str(json_file).replace("'", '"').encode('utf8'))

        return len(json_file["Sites"])


def recover_historic(file_saved: str = 'historic.json', f: str = "") -> dict:
    with open(os.path.join('configs', file_saved), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)
            if bool(f):
                f_list = [his for his in js['Sites'] if f in his['name']]
                return {'Sites': f_list}
            return js
        return {}


def remove_historic_item(id: int,
                         file_saved_main: str = 'historic.json',
                         widget: QWidget = None,
                         layout: QLayout = None,
                         remove_view=True) -> bool:
    with open(os.path.join('configs', file_saved_main), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)
            js_copy = {'Sites': []}
            for file_saved in js['Sites']:
                if file_saved['id'] != id:
                    js_copy['Sites'].insert(0, file_saved)

            with open(os.path.abspath(os.path.join('configs', file_saved_main)), 'wb') as file2:
                file2.write(str(js_copy).replace("'", '"').encode('utf8'))
        else:
            return False
    if remove_view:
        layout.removeWidget(widget)
        widget.deleteLater()
        layout.update()
    return True


