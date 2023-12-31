import json
import os.path
import threading

semaphoro = threading.Semaphore(1)


def save_cookies(cook):
    try:
        semaphoro.acquire()
        cookies_file = os.path.abspath(os.path.join("configs", "cookies.json"))

        cookies_data = {"Cookies": []}
        # Tenta ler o arquivo de cookies
        if os.path.exists(cookies_file):
            with open(cookies_file, 'rb') as file:
                dado = file.read()
                if bool(dado):
                    cookies_data = json.loads(dado)
                    cookies_data = dict(cookies_data)

        # Verifica se já existe um cookie com o mesmo nome
        existing_cookie = next((c for c in cookies_data["Cookies"] if c["name"] == cook["name"]), None)
        if existing_cookie:
            # Atualiza o valor do cookie existente
            existing_cookie["cookie"] = cook["cookie"]
        else:
            # Adiciona um novo cookie se não existir um com o mesmo nome
            cookies_data["Cookies"].append({'domain': cook['domain'], 'cookie': cook['cookie'], 'name': cook['name']})

        # Salva os cookies de volta no arquivo
        with open(cookies_file, 'w', encoding='utf-8') as file:
            json.dump(cookies_data, file, indent=2)
    except Exception as e:
        print(e)
    finally:
        semaphoro.release()


def recover_cookies(file_saved: str = 'cookies.json') -> dict:
    with open(os.path.join('configs', file_saved), 'rb') as file:
        file_read = file.read()
        if bool(file_read):
            js = json.loads(file_read.decode('utf8'))
            js = dict(js)
            return js
        return {}


def remove_cookie(cookie_name, cookie_value):
    try:
        semaphoro.acquire()
        cookies_file = os.path.abspath(os.path.join("configs", "cookies.json"))

        cookies_data = {"Cookies": []}
        # Tenta ler o arquivo de cookies
        if os.path.exists(cookies_file):
            with open(cookies_file, 'rb') as file:
                dado = file.read()
                if bool(dado):
                    cookies_data = json.loads(dado)
                    cookies_data = dict(cookies_data)

        # Procura o cookie pelo nome e o remove, se existir
        if "Cookies" in cookies_data and len(cookies_data["Cookies"]) > 0:
            cookies_data["Cookies"] = [c for c in cookies_data["Cookies"] if
                                       c["name"] != cookie_name and c['cookie'] != cookie_value]

        # Salva os cookies atualizados de volta no arquivo
        with open(cookies_file, 'w', encoding='utf-8') as file:
            json.dump(cookies_data, file, indent=2)
    except Exception as e:
        print(e)
    finally:
        semaphoro.release()
