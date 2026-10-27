#!/usr/bin/env python3
"""Copia CONTATOS e TEXTOS para o JSON que a página lê no servidor."""

import json
import os

from gerar_guia import CONTATOS, TEXTOS

destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web", "dados", "guia.json")
os.makedirs(os.path.dirname(destino), exist_ok=True)
with open(destino, "w", encoding="utf-8") as arquivo:
    json.dump({"contatos": CONTATOS, "textos": TEXTOS}, arquivo, ensure_ascii=False, indent=2)
    arquivo.write("\n")
print(destino)
