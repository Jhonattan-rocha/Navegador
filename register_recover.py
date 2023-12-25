import datetime
import json
import os

from PySide6.QtWidgets import QWidget, QLayout


def register_download_historic(suggested_file_name: str, folder_path: str, status: str,
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


def recover_download_historic(file_saved: str = 'download_history.json') -> dict:
    with open(os.path.join('.', 'configs', file_saved), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)
            return js
        return {}


def remove_download_historic_item(download_data: dict, remove_view: bool = False, widget: QWidget = None,
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
        widget.deleteLater()
        layout.update()
    return True


# ------------------

def register_historic(site: str, cookies: list,
                      download_time: datetime.datetime, file_saved_main: str = 'historic.json'):
    with open(os.path.abspath(os.path.join('.', 'configs', file_saved_main)), 'rb') as file:
        file_read = file.read()
        json_file = {}
        if not file_read:
            json_file = {"Sites": [{"name": f"{site}", "cookies": cookies, "date_time": f"{download_time}"}]}
        else:
            json_file = json.loads(file_read)
            json_file = dict(json_file)
            json_file["Sites"].insert(0, {"name": f"{site}", "cookies": cookies, "date_time": f"{download_time}"})

        with open(os.path.abspath(os.path.join('.', 'configs', file_saved_main)), 'wb') as file2:
            file2.write(str(json_file).replace("'", '"').encode('utf8'))


def recover_historic(file_saved: str = 'historic.json') -> dict:
    with open(os.path.join('.', 'configs', file_saved), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)
            return js
        return {}


def remove_historic_item(site: str, date_time: datetime.datetime,
                         file_saved_main: str = 'historic.json',
                         widget: QWidget = None,
                         layout: QLayout = None,
                         remove_view=True) -> bool:
    with open(os.path.join('.', 'configs', file_saved_main), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)
            js_copy = {'Sites': []}
            for file_saved in js['Sites']:
                if file_saved['name'] != site and file_saved['date_time'] != date_time:
                    js_copy['Sites'].insert(0, file_saved)

            with open(os.path.abspath(os.path.join('.', 'configs', file_saved_main)), 'wb') as file2:
                file2.write(str(js_copy).replace("'", '"').encode('utf8'))
        else:
            return False
    if remove_view:
        layout.removeWidget(widget)
        widget.deleteLater()
        layout.update()
    return True


def recover_adjacent_historic(site: str, date_time: str, direction: str, file_saved: str = 'historic.json') -> dict:
    path = os.path.join('.', 'configs', file_saved)

    if os.path.exists(path):
        with open(path, 'r') as file:
            js = json.load(file)

            for idx, h in enumerate(js['Sites']):
                if site == h['name'] and date_time == h['date_time']:
                    if direction == 'ant' and idx > 0:
                        print(h['name'], site, h['date_time'], date_time)
                        return js['Sites'][idx - 1]  # Retorna o site anterior
                    elif direction == 'prox' and idx + 1 < len(js['Sites']):
                        return js['Sites'][idx + 1]  # Retorna o próximo site
                    else:
                        return {}  # Se estiver no primeiro e pedir o anterior ou no último e pedir o próximo, retorna um dicionário vazio
    return {}
