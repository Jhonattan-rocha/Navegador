import os.path

from PySide6.QtWebEngineWidgets import QWebEngineView


def save_cookies(webView: QWebEngineView, cook):
    try:
        cookies_file = os.path.abspath(os.path.join("configs", "cookies.json"))

        with open(cookies_file, 'r') as file:
            dados = file.read()
            file_for_save = {}

            if not bool(dados):
                file_for_save = {"cookies": [{'dominio': cook['dominio'], 'cooks': cook['cooks']}]}
    except Exception as e:
        print(e)
