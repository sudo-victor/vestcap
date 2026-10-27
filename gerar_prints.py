#!/usr/bin/env python3
"""Gera prints simulados de conversa de WhatsApp para o passo a passo.

As conversas ficam em CONVERSAS, logo abaixo. Cada uma vira um PNG na pasta
prints/ com o nome indicado, no tamanho de um print de iPhone. Rode:
    python3 gerar_prints.py
e depois:
    python3 gerar_guia.py

A foto de perfil vem de avatares/<contato>.png (ex.: avatares/chen.png).
Sem o arquivo, aparece um círculo com a inicial do contato.

Tipos de mensagem:
- ("out" | "in", "texto")            mensagem de texto, enviada ou recebida
- ("out" | "in", "img", [peças])     foto; peça = ("camisa", cor, detalhe, riscada)
                                     ou ("tenis", cor) ou ("comprovante", valor)
- ("out" | "in", "resp", peça, "texto")  resposta citando uma foto
- ("in", "pagamento", titulo, valor)     cartão de link de pagamento
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1170, 2532
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prints")
AVATARES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avatares")

BG = "#0B141A"
BARRA = "#1F2C34"
SAIDA = "#005C4B"
ENTRADA = "#1F2C34"
TEXTO = "#E9EDEF"
CINZA = "#8696A0"
AZUL = "#53BDEB"
VERDE = "#00A884"
CITA = "#06CF9C"

FONTE = "/System/Library/Fonts/Helvetica.ttc"
F_MSG = ImageFont.truetype(FONTE, 46)
F_HORA = ImageFont.truetype(FONTE, 30)
F_NOME = ImageFont.truetype(FONTE, 50, index=1)
F_SUB = ImageFont.truetype(FONTE, 34)
F_BOLD = ImageFont.truetype(FONTE, 46, index=1)
F_STATUS = ImageFont.truetype(FONTE, 44, index=1)

CONVERSAS = [
    {
        "arquivo": "chen-2.png",
        "contato": "Chen",
        "hora": "21:33",
        "mensagens": [
            ("out", "Olá, tudo bem? Tem essas camisas abaixo?"),
            ("out", "img", [("camisa", "#7A3FB8", "#E3B23C", False), ("camisa", "#D62828", "#FFFFFF", False)]),
            ("in", "Olá. Sim, tenho as duas camisas."),
            ("in", "Quais tamanhos você quer?"),
        ],
    },
    {
        "arquivo": "chen-3.png",
        "contato": "Chen",
        "hora": "21:41",
        "mensagens": [
            ("out", "resp", ("camisa", "#7A3FB8", "#E3B23C", False), "Camisa torcedor\nTamanho L"),
            ("out", "img", [("camisa", "#D62828", "#FFFFFF", True)]),
            ("out", "Camisa player\nSEM OS PATROCÍNIOS\nTamanho XL\nNúmero 10"),
            ("in", "Ok. Confirmado."),
        ],
    },
    {
        "arquivo": "chen-4.png",
        "contato": "Chen",
        "hora": "21:52",
        "mensagens": [
            ("in", "Pedido confirmado. Envie nome completo, endereço com CEP, CPF e telefone para o envio."),
            ("out", "Nome: João da Silva\nEndereço: Rua das Flores, 123, São Paulo, SP\nCEP: 01000-000\nCPF: 000.000.000-00\nTelefone: (11) 90000-0000"),
            ("in", "pagamento", "Pedido de 2 camisas", "US$ 30"),
            ("out", "img", [("comprovante", "US$ 30,00")]),
            ("out", "Pagamento feito. Segue o comprovante."),
            ("in", "Recebido. Envio o rastreio quando postar."),
        ],
    },
    {
        "arquivo": "cris-2.png",
        "contato": "Cris",
        "hora": "18:05",
        "mensagens": [
            ("out", "img", [("tenis", "#F2F2F2")]),
            ("out", "Tênis\nModelo da foto\nQuantidade: 1\nNumeração: 42 EU"),
        ],
    },
    {
        "arquivo": "cris-3.png",
        "contato": "Cris",
        "hora": "18:12",
        "mensagens": [
            ("out", "resp", ("tenis", "#F2F2F2"), "Tênis\nNumeração: 42 EU"),
            ("in", "Tem em estoque. Numeração 42 EU disponível."),
            ("out", "Fechado. Pode separar."),
        ],
    },
    {
        "arquivo": "cris-4.png",
        "contato": "Cris",
        "hora": "18:20",
        "mensagens": [
            ("in", "pagamento", "Tênis numeração 42 EU", "US$ 52"),
            ("out", "img", [("comprovante", "US$ 52,00")]),
            ("out", "Pago. Segue o comprovante."),
            ("in", "Pagamento confirmado. Envio em até 5 dias."),
        ],
    },
]


# ---------------------------------------------------------------- PEÇAS --

def camisa(tam, cor, detalhe, riscada):
    img = Image.new("RGB", (tam, tam), "#D9D9D6")
    d = ImageDraw.Draw(img)
    for x in range(0, tam, 46):
        d.line([(x, 0), (x, tam)], fill="#CFCFCB", width=3)
    for y in range(0, tam, 46):
        d.line([(0, y), (tam, y)], fill="#CFCFCB", width=3)
    p = lambda pts: [(x * tam, y * tam) for x, y in pts]
    d.polygon(p([(0.40, 0.12), (0.25, 0.17), (0.07, 0.36), (0.18, 0.47), (0.28, 0.39), (0.28, 0.90),
                 (0.72, 0.90), (0.72, 0.39), (0.82, 0.47), (0.93, 0.36), (0.75, 0.17), (0.60, 0.12),
                 (0.50, 0.19)]), fill=cor)
    d.line(p([(0.40, 0.12), (0.50, 0.19), (0.60, 0.12)]), fill=detalhe, width=int(tam * 0.02))
    d.line(p([(0.10, 0.39), (0.19, 0.46)]), fill=detalhe, width=int(tam * 0.02))
    d.line(p([(0.90, 0.39), (0.81, 0.46)]), fill=detalhe, width=int(tam * 0.02))
    d.ellipse(p([(0.58, 0.27), (0.65, 0.34)]), fill=detalhe)
    box = p([(0.36, 0.44), (0.64, 0.56)])
    d.rounded_rectangle(box, radius=int(tam * 0.02), fill=detalhe)
    if riscada:
        w = int(tam * 0.025)
        d.line(p([(0.32, 0.41), (0.68, 0.59)]), fill="#FF2D2D", width=w)
        d.line(p([(0.32, 0.59), (0.68, 0.41)]), fill="#FF2D2D", width=w)
        for k in range(3):
            y = 0.43 + k * 0.06
            d.line(p([(0.33, y), (0.67, y + 0.02)]), fill="#FF2D2D", width=w // 2)
    return img


def tenis(tam, cor):
    img = Image.new("RGB", (tam, tam), "#E6E2DA")
    d = ImageDraw.Draw(img)
    p = lambda pts: [(x * tam, y * tam) for x, y in pts]
    d.rounded_rectangle(p([(0.08, 0.62), (0.92, 0.70)]), radius=int(tam * 0.03), fill="#FFFFFF", outline="#BDB7AC", width=4)
    d.polygon(p([(0.10, 0.62), (0.12, 0.48), (0.30, 0.44), (0.46, 0.30), (0.58, 0.32), (0.66, 0.46),
                 (0.88, 0.52), (0.91, 0.62)]), fill=cor, outline="#BDB7AC")
    d.line(p([(0.30, 0.50), (0.62, 0.58)]), fill="#2B2B2B", width=int(tam * 0.02))
    for k in range(4):
        x = 0.47 + k * 0.04
        d.line(p([(x, 0.35 + k * 0.02), (x + 0.05, 0.37 + k * 0.02)]), fill="#9A948A", width=6)
    return img


def comprovante(tam, valor):
    img = Image.new("RGB", (tam, tam), "#F4F4F2")
    d = ImageDraw.Draw(img)
    f_t = ImageFont.truetype(FONTE, int(tam * 0.06), index=1)
    f_v = ImageFont.truetype(FONTE, int(tam * 0.11), index=1)
    f_s = ImageFont.truetype(FONTE, int(tam * 0.045))
    d.ellipse((tam * 0.42, tam * 0.10, tam * 0.58, tam * 0.26), fill="#1FAF5C")
    d.line([(tam * 0.46, tam * 0.18), (tam * 0.49, tam * 0.21), (tam * 0.55, tam * 0.14)], fill="#FFFFFF", width=int(tam * 0.02))
    d.text((tam / 2, tam * 0.33), "Pagamento concluído", font=f_t, fill="#1D1D1D", anchor="mm")
    d.text((tam / 2, tam * 0.46), valor, font=f_v, fill="#1D1D1D", anchor="mm")
    for k, (a, b) in enumerate([("Status", "Pago"), ("Método", "Transferência"), ("Data", "Hoje")]):
        y = tam * (0.62 + k * 0.10)
        d.line([(tam * 0.10, y - tam * 0.04), (tam * 0.90, y - tam * 0.04)], fill="#E0E0DC", width=3)
        d.text((tam * 0.10, y), a, font=f_s, fill="#777777", anchor="lm")
        d.text((tam * 0.90, y), b, font=f_s, fill="#1D1D1D", anchor="rm")
    return img


def peca(spec, tam):
    tipo = spec[0]
    if tipo == "camisa":
        return camisa(tam, *spec[1:])
    if tipo == "tenis":
        return tenis(tam, *spec[1:])
    return comprovante(tam, *spec[1:])


# ---------------------------------------------------------------- TELA --

def quebrar(texto, fonte, largura):
    linhas = []
    for par in texto.split("\n"):
        atual = ""
        for palavra in par.split():
            teste = palavra if not atual else f"{atual} {palavra}"
            if fonte.getlength(teste) <= largura:
                atual = teste
            else:
                linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def checks(d, x, y):
    for dx in (0, 14):
        d.line([(x + dx, y + 2), (x + dx + 8, y + 10), (x + dx + 22, y - 6)], fill=AZUL, width=4)


def rodape_bolha(d, direita, base, hora, saida):
    larg = F_HORA.getlength(hora) + (44 if saida else 0)
    x = direita - 22 - larg
    d.text((x, base), hora, font=F_HORA, fill="#A8C7BF" if saida else CINZA, anchor="ls")
    if saida:
        checks(d, direita - 58, base - 10)


def bolha(d, x0, y, x1, h, cor):
    d.rounded_rectangle((x0, y, x1, y + h), radius=22, fill=cor)


def tela(conversa):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, W, 300), fill=BARRA)
    d.text((110, 78), conversa["hora"], font=F_STATUS, fill=TEXTO, anchor="lm")
    for k in range(4):
        d.rounded_rectangle((900 + k * 22, 92 - k * 10, 914 + k * 22, 102), radius=3, fill=TEXTO)
    d.rounded_rectangle((1010, 62, 1086, 98), radius=10, outline=TEXTO, width=4)
    d.rounded_rectangle((1016, 68, 1068, 92), radius=6, fill=TEXTO)
    d.line([(70, 190), (46, 216), (70, 242)], fill=TEXTO, width=7)
    avatar = os.path.join(AVATARES, conversa["contato"].lower() + ".png")
    if os.path.exists(avatar):
        foto = Image.open(avatar).convert("RGB").resize((110, 110), Image.LANCZOS)
        mask = Image.new("L", (110, 110), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 110, 110), fill=255)
        img.paste(foto, (100, 160), mask)
    else:
        d.ellipse((100, 160, 210, 270), fill="#6B7C85")
        d.text((155, 215), conversa["contato"][0], font=F_NOME, fill=TEXTO, anchor="mm")
    d.text((238, 196), conversa["contato"], font=F_NOME, fill=TEXTO, anchor="lm")
    d.text((238, 246), "online", font=F_SUB, fill=CINZA, anchor="lm")
    for k in range(3):
        d.ellipse((1100, 186 + k * 22, 1112, 198 + k * 22), fill=TEXTO)
    d.rounded_rectangle((900, 194, 960, 236), radius=10, outline=TEXTO, width=5)
    d.polygon([(962, 215), (990, 196), (990, 234)], outline=TEXTO, fill=None, width=5)

    chip = "Hoje"
    cw = F_SUB.getlength(chip) + 50
    d.rounded_rectangle((W / 2 - cw / 2, 340, W / 2 + cw / 2, 400), radius=16, fill="#182229")
    d.text((W / 2, 370), chip, font=F_SUB, fill=CINZA, anchor="mm")

    y = 440
    max_txt = 780
    hora = conversa["hora"]
    for msg in conversa["mensagens"]:
        lado, tipo = msg[0], msg[1]
        saida = lado == "out"
        cor = SAIDA if saida else ENTRADA

        if tipo == "img":
            pecas = msg[2]
            if len(pecas) == 1:
                tam = 460 if pecas[0][0] == "comprovante" else 620
                bw, bh = tam + 16, tam + 16
            else:
                tam = 380
                bw, bh = tam * 2 + 24, tam + 16
            x0 = W - 30 - bw if saida else 30
            bolha(d, x0, y, x0 + bw, bh, cor)
            for k, spec in enumerate(pecas):
                im = peca(spec, tam)
                mask = Image.new("L", (tam, tam), 0)
                ImageDraw.Draw(mask).rounded_rectangle((0, 0, tam, tam), radius=16, fill=255)
                img.paste(im, (int(x0 + 8 + k * (tam + 8)), int(y + 8)), mask)
            sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(sombra).rounded_rectangle((x0 + bw - 190, y + bh - 64, x0 + bw - 16, y + bh - 18), radius=20, fill=(0, 0, 0, 110))
            img.paste(Image.alpha_composite(img.convert("RGBA"), sombra).convert("RGB"))
            d = ImageDraw.Draw(img)
            rodape_bolha(d, x0 + bw, y + bh - 30, hora, saida)
            y += bh + 24
            continue

        if tipo == "pagamento":
            titulo, valor = msg[2], msg[3]
            bw, bh = 760, 330
            x0 = 30
            bolha(d, x0, y, x0 + bw, bh, cor)
            d.rounded_rectangle((x0 + 14, y + 14, x0 + bw - 14, y + 200), radius=16, fill="#18252D")
            d.rounded_rectangle((x0 + 40, y + 46, x0 + 140, y + 146), radius=18, fill="#1677FF")
            d.text((x0 + 90, y + 96), "$", font=F_NOME, fill="#FFFFFF", anchor="mm")
            d.text((x0 + 170, y + 76), "Link de pagamento", font=F_BOLD, fill=TEXTO, anchor="lm")
            d.text((x0 + 170, y + 132), f"{titulo} · {valor}", font=F_SUB, fill=CINZA, anchor="lm")
            d.line([(x0, y + 246), (x0 + bw, y + 246)], fill="#2A3942", width=2)
            d.text((x0 + bw / 2, y + 290), "Pagar", font=F_BOLD, fill=AZUL, anchor="mm")
            d.text((x0 + 30, y + 226), "Toque em Pagar para concluir.", font=F_HORA, fill=CINZA, anchor="lm")
            rodape_bolha(d, x0 + bw, y + 234, hora, False)
            y += bh + 24
            continue

        cita = tipo == "resp"
        texto = msg[3] if cita else tipo
        linhas = quebrar(texto, F_MSG, max_txt)
        larg_linhas = max(F_MSG.getlength(l) for l in linhas)
        larg_hora = F_HORA.getlength(hora) + (66 if saida else 22)
        extra = F_MSG.getlength(linhas[-1]) + larg_hora + 20 > max(larg_linhas, 560 if cita else 0)
        bw = max(larg_linhas, 560 if cita else 0) + 56
        if not extra:
            bw = max(bw, F_MSG.getlength(linhas[-1]) + larg_hora + 76)
        bw = min(bw, max_txt + 56)
        topo_txt = 22 + (176 if cita else 0)
        bh = topo_txt + len(linhas) * 58 + (44 if extra else 6) + 14
        x0 = W - 30 - bw if saida else 30
        bolha(d, x0, y, x0 + bw, bh, cor)
        if cita:
            d.rounded_rectangle((x0 + 12, y + 12, x0 + bw - 12, y + 172), radius=14, fill="#025144" if saida else "#18252D")
            d.rectangle((x0 + 12, y + 12, x0 + 22, y + 172), fill=CITA)
            d.text((x0 + 46, y + 58), "Você", font=F_BOLD, fill=CITA, anchor="lm")
            d.rounded_rectangle((x0 + 46, y + 100, x0 + 84, y + 128), radius=6, outline=CINZA, width=4)
            d.text((x0 + 98, y + 114), "Foto", font=F_SUB, fill="#A8C7BF", anchor="lm")
            th = 148
            im = peca(msg[2], th)
            img.paste(im, (int(x0 + bw - 22 - th), int(y + 18)))
        ty = y + topo_txt + 40
        for linha in linhas:
            d.text((x0 + 28, ty), linha, font=F_MSG, fill=TEXTO, anchor="ls")
            ty += 58
        rodape_bolha(d, x0 + bw, y + bh - 20, hora, saida)
        y += bh + 14

    h = min(max(int(y) + 240, 1500), H)
    img = img.crop((0, 0, W, h))
    d = ImageDraw.Draw(img)
    d.rectangle((0, h - 200, W, h), fill=BG)
    d.rounded_rectangle((110, h - 176, 960, h - 70), radius=53, fill=BARRA)
    d.text((160, h - 123), "Mensagem", font=F_MSG, fill=CINZA, anchor="lm")
    d.line([(40, h - 123), (84, h - 123)], fill=TEXTO, width=6)
    d.line([(62, h - 145), (62, h - 101)], fill=TEXTO, width=6)
    d.ellipse((990, h - 176, 1096, h - 70), fill=VERDE)
    d.rounded_rectangle((1031, h - 152, 1055, h - 112), radius=12, fill="#FFFFFF")
    d.arc((1021, h - 134, 1065, h - 98), 0, 180, fill="#FFFFFF", width=5)
    return img


def main():
    os.makedirs(PASTA, exist_ok=True)
    for conversa in CONVERSAS:
        destino = os.path.join(PASTA, conversa["arquivo"])
        tela(conversa).save(destino)
        print("prints/" + conversa["arquivo"])


if __name__ == "__main__":
    main()
