"""Imprime o payload real do endpoint consultaAluno da GVDASA.

Uso: python3 scripts/check_gvdasa_consulta_aluno.py <matricula_do_aluno>
"""
import json
import sys

import requests
from decouple import config

if len(sys.argv) != 2:
    print("Uso: python3 scripts/check_gvdasa_consulta_aluno.py <matricula_do_aluno>")
    sys.exit(1)

base_url = config("GVDASA_BASE_URL").rstrip("/")
headers = {"Authorization": f"Bearer {config('GVDASA_API_KEY')}"}
url = f"{base_url}/consultaAluno/{sys.argv[1]}"

response = requests.get(url, headers=headers)
print(f"GET {url} -> {response.status_code}\n")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
