#!/home/ryba/rbpi_qemu/python_project/venv/bin/python

import os
import jwt
import time


# remote gpio nie jest w żaden sposób szyfrowane, dlatego nie jest bezpieczną metodą na przesył gpio
# projekt to trochę proof of concept ale metoda działa

def main(args):
    gpio_ins = "/home/ryba/rbpi_qemu/python_project/test"

    ins_names: list = []

    for i in args[0].split(','):
        print(i)
        ins_names.append(gpio_ins + str(i))

    while True:
        read_arr: str = ''
        for i in ins_names:
            read_arr += str(os.popen(f"cat {i}").read())

        read_arr = read_arr.replace('\n', '')

        print(read_arr)
        secret = os.popen("cat ./secret").read().replace('\n', '')
        rbpname = os.popen("cat ./rbpname").read().replace('\n', '')

        # json web token jest dosyć elastyczny w implementacji, łatwo zmienić algorytm szyfrowania,
        # normalnie użyłbym asymetrycznego szyfrowania typu EdDSA ale HS256 na vmce szybciej działa
        # dodatkowo jako plus widzę możliwość łatwiejszej konfiguracji kluczy dla osobnych urządzeń

        encoded_read = jwt.encode({rbpname: read_arr}, secret, algorithm="HS256")

        print(encoded_read)

        # metoda na odkodowanie gpio
        # decode_test = jwt.decode(encoded_read, secret, algorithms="HS256")
        # print(decode_test)

        # protokół http użyty dlatego że dane nie są duże a skrypt ma tylko raportować.
        # do pobierania większej ilości danych użyłbym czegoś w stylu wysyłania na serwera sftp
        request = f"curl -X POST http://0.0.0.0:8000/ -H 'Content-Type: text/plain' -d {encoded_read}"

        print(request)
        os.popen(request)
        time.sleep(10)
        # skrypt może być wywoływany przez system zarządzania serwisami systemctl na starcie rbpi
        # może też się sam reaktywować jeśli się scrashuje

    return

import sys
if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)

# TODO: SEND ALL PINS
