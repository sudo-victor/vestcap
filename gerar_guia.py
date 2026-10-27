#!/usr/bin/env python3
"""Gera o guia de contatos da VestCap.

Tudo o que aparece no PDF vem de CONTATOS, VIDEOS e TEXTOS, logo abaixo.
Edite os dados e rode:
    python3 gerar_guia.py

Regras do modelo:
- Cada contato pode ter um ou mais catálogos. Cada catálogo vira uma página.
  Com mais de 10 itens, o catálogo continua na página seguinte.
- "aba" é o nome curto do catálogo na barra de etapas do topo da página.
- "botao" no catálogo é opcional: muda o texto do botão que abre o link.
- "video" no contato é opcional: aparece ao lado do botão do passo a passo.
- MOSTRAR_VIDEOS = False esconde a página de vídeos e todos os botões de vídeo.
- MOSTRAR_PRINTS = False esconde as imagens dos passos. Os caminhos em "print"
  continuam salvos para voltar quando os arquivos certos estiverem na pasta.
- "tabela_unica": True junta todos os catálogos do contato numa página só de
  preços, com um botão para abrir cada catálogo. Cabem até 13 itens no total.
- "so_links": True junta os catálogos numa lista de links, sem preço.
  Nesse caso os catálogos não precisam de "itens". A lista continua
  na página seguinte quando não cabe.
- Preços, adicionais e frete são texto livre: escreva do jeito que deve aparecer.
- Listas vazias (adicionais ou frete) não aparecem no PDF.
- "passos" vira a seção Passo a passo: uma página por passo. Cada passo pode
  ser (título, descrição, print) ou um dicionário com "titulo", "texto",
  "print" e, se precisar, "lista" (passos numerados), "exemplo" (título, dica
  e texto de uma mensagem pronta), "modelos" (quadros de mensagem, até 2 lado
  a lado), "notas" (avisos em destaque), "acao" ("catalogos" ou "whatsapp")
  e "mensagens" (True abre o botão da etapa Mensagens). O print é um PNG ou JPG, de preferência
  um print de celular em pé, salvo na pasta prints/ ao lado deste arquivo.
  Sem o arquivo, a página mostra um quadro indicando qual print falta.
- "mensagens" no contato vira a etapa Mensagens: templates para copiar e
  colar. Cada item é (título, dica, texto da mensagem).
- "checklist" no contato vira a última etapa: uma página para marcar na hora
  do pedido. Sem a lista, a etapa não aparece.
"""

import os
import re

from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

# ---------------------------------------------------------------- DADOS --

TEXTOS = {
    "capa_edicao": "ARQUIVO 01 · USO INTERNO",
    "capa_carimbo": "CONFIDENCIAL",
    "capa_titulo": ["ACESSO"],
    "capa_destaque": "RESTRITO",
    "capa_texto": "Os contatos que a gente usa pra comprar. Não estão em site nem em post. Ficam só aqui.",
    "capa_categorias": ["CAMISA DE TIME", "TÊNIS", "ÓCULOS E BOLSAS"],
    "capa_info": [
        ("ARQUIVO", "Contatos e catálogos"),
        ("ACESSO", "Só quem recebeu"),
        ("REGRA", "Não encaminhar"),
    ],
    "sumario_texto": "Leia o Antes de comprar uma vez. Depois, em cada contato: catálogo, frete, passo a passo e a checklist na hora do pedido.",
    "antes": [
        ("PRAZO", "A entrega leva de 20 a 40 dias depois do envio. O código de rastreio vem do fornecedor, na mesma conversa."),
        ("TAXA DE IMPORTAÇÃO", "Compra internacional pode ser taxada pela Receita Federal. Se for, a cobrança chega pelos Correios e é paga por quem recebe. Na próxima página: como pagar menos."),
        ("PAGAMENTO EM DÓLAR", "Os preços estão em dólar. Cada contato aceita um método, que está na etapa Frete e pagamento. A conversão para real acontece na hora de pagar."),
        ("SE DER PROBLEMA", "Guarde o comprovante e os prints da conversa. Se vier errado ou não chegar, fale com o fornecedor na mesma conversa, mostrando o print do pedido."),
    ],
    "imposto": {
        "link": "https://apps.correios.com.br/portalimportador/",
        "intro": "Quando a encomenda chega no Brasil, vincule seu CPF a ela no Portal do Importador dos Correios. Assim a taxa sai com o valor certo, sem cobrança a mais.",
        "passos": [
            ("AGUARDE", "o nome do objeto postado aparecer no rastreio, no aplicativo dos Correios."),
            ("ACESSE", "o Portal do Importador, no site dos Correios. O botão abaixo abre o portal."),
            ("DIGITE", "o código de rastreio na barra de pesquisa e encontre a sua encomenda."),
            ("PREENCHA", "o campo Identificação do Importador com o seu CPF."),
            ("AGUARDE A ATUALIZAÇÃO", "da página. Quando aparecer Documento vinculado, está feito."),
        ],
        "fim": "Agora é só acompanhar o rastreio e esperar a taxa, com o valor certo.",
        "regra": "O cadastro no site dos Correios tem que estar no mesmo nome de quem vai receber a encomenda.",
        "exemplo": "Se o pacote está no nome da Raimunda, o login usado no Portal do Importador também tem que ser da Raimunda.",
        "riscos": [
            ("BARRADO", "Se alguém entra na conta do José e vincula uma encomenda da Raimunda, ou de qualquer outra pessoa, o pacote pode ser barrado por divergência de informações."),
            ("PERDIDO", "Se isso acontecer, a encomenda pode ser perdida, sem reembolso e sem reenvio, mesmo com seguro."),
        ],
        "dica": "Cada pessoa faz no próprio login, com o próprio CPF. Nunca use o login ou o CPF de outra pessoa.",
    },
    "tamanhos": [("P", "S"), ("M", "M"), ("G", "L"), ("GG", "XL"), ("XGG", "XXL")],
    "tamanhos_texto": "Nas mensagens, use sempre o tamanho internacional. As medidas em cm da camisa estão no contato da camisa. No tênis, a numeração europeia (EU), que costuma ser um número acima da brasileira.",
}

CONTATOS = [
    {
        "key": "chen",
        "nome": "Chen",
        "linha": "Camisa de Time",
        "resumo": "Catálogo geral, de conjuntos e de calças. Pedido por print.",
        "tabela_unica": True,
        "tabela_texto": "Os três catálogos numa tabela só. Adicionais, frete e pagamento vêm na próxima etapa.",
        "catalogos": [
            {
                "titulo": "Geral",
                "aba": "Geral",
                "botao": "ABRIR CATÁLOGO GERAL",
                "descricao": "Camisa, short e meia. Na página de pedido estão os adicionais e o frete.",
                "link": "https://chen13690323804.x.yupoo.com/",
                "itens": [
                    ("Camisa torcedor", "US$ 9"),
                    ("Camisa torcedor manga longa", "US$ 13"),
                    ("Camisa player", "US$ 14"),
                    ("Camisa retrô", "US$ 15"),
                    ("Short", "US$ 8"),
                    ("Short player", "US$ 10"),
                    ("Meia", "US$ 4"),
                ],
            },
            {
                "titulo": "Conjuntos (suit)",
                "aba": "Conjuntos",
                "botao": "ABRIR CATÁLOGO DE CONJUNTOS",
                "descricao": "Agasalho e corta-vento. Pede junto com o catálogo geral.",
                "link": "http://huang456852.x.yupoo.com/albums?_wv=1",
                "itens": [
                    ("Corta-vento", "US$ 28"),
                    ("Kit agasalho", "US$ 42"),
                    ("Conjunto de treino", "US$ 35"),
                ],
            },
            {
                "titulo": "Calças (pants)",
                "aba": "Calças",
                "botao": "ABRIR CATÁLOGO DE CALÇAS",
                "descricao": "Calças de treino e de passeio. Pede junto com o catálogo geral.",
                "link": "https://ty-guoji2.x.yupoo.com/",
                "itens": [
                    ("Calça de treino", "US$ 18"),
                    ("Calça jogger", "US$ 20"),
                    ("Calça de moletom", "US$ 22"),
                ],
            },
        ],
        "pedido_titulo": "POR PRINT",
        "pedido_intro": "O que soma no valor do pedido e como pagar. O link vem dele, depois da confirmação. O frete da tabela vale para camisa. Conjunto e calça: pergunte o frete na conversa.",
        "medidas_intro": "Na mensagem, escreva o código da esquerda. P vira S, G vira L, XG vira XL, 2XG vira XXL e 3XL vira XXXL. 4XL continua 4XL. Comprimento e largura são da camisa, em cm. Altura é da pessoa, em cm. Peso é em kg. No limite entre dois, pegue o maior. Player usa a tabela justa.",
        "medidas": [
            [
                (
                    "TORCEDOR",
                    "Versão larga.",
                    ["ESCREVA", "COMP.", "LARG.", "ALTURA", "PESO"],
                    [
                        ("S · P", "69–71", "53–55", "162–170", "50–62"),
                        ("M · M", "71–73", "55–57", "170–176", "62–78"),
                        ("L · G", "73–75", "57–58", "176–182", "78–83"),
                        ("XL · XG", "75–78", "58–60", "182–190", "83–90"),
                        ("XXL · 2XG", "78–81", "60–62", "190–195", "90–97"),
                        ("XXXL · 3XL", "81–83", "62–64", "192–197", "97–104"),
                        ("4XL", "83–85", "64–65", "197–200", "104–110"),
                    ],
                ),
                (
                    "JOGADOR",
                    "Versão justa. A camisa já é mais curta.",
                    ["ESCREVA", "COMP.", "LARG.", "ALTURA", "PESO"],
                    [
                        ("S · P", "67–69", "49–51", "162–170", "50–62"),
                        ("M · M", "69–71", "51–53", "170–175", "62–75"),
                        ("L · G", "71–73", "53–55", "175–180", "75–80"),
                        ("XL · XG", "73–76", "55–57", "180–185", "80–85"),
                        ("XXL · 2XG", "76–78", "57–60", "185–190", "85–90"),
                        ("XXXL · 3XL", "78–79", "60–63", "190–195", "90–95"),
                    ],
                ),
            ],
            [
                (
                    "FEMININA",
                    "Sem peso nesta tabela.",
                    ["ESCREVA", "COMP.", "LARG.", "ALTURA"],
                    [
                        ("S · P", "61–63", "40–41", "150–160"),
                        ("M · M", "63–66", "41–44", "160–165"),
                        ("L · G", "66–69", "44–47", "165–170"),
                        ("XL · XG", "69–71", "47–50", "170–175"),
                    ],
                ),
                (
                    "INFANTIL",
                    "Escreva o número, não a letra. Idade em anos. Cintura e altura em cm.",
                    ["Nº", "IDADE", "COMP.", "LARG.", "CINT.", "ALTURA"],
                    [
                        ("16", "3–4", "44–47", "35–37", "20–37", "95–105"),
                        ("18", "4–5", "47–50", "37–39", "21–39", "105–115"),
                        ("20", "5–6", "50–53", "39–41", "22–41", "115–125"),
                        ("22", "6–7", "53–56", "41–43", "23–42", "125–135"),
                        ("24", "8–9", "56–59", "43–45", "24–44", "135–145"),
                        ("26", "10–11", "59–62", "45–47", "25–47", "145–155"),
                        ("28", "12–13", "62–65", "47–49", "26–50", "155–165"),
                    ],
                ),
            ],
        ],
        "passos": [
            {
                "titulo": "Ache e tire print",
                "texto": "Um print por produto. A imagem tem que aparecer inteira.",
                "acao": "catalogos",
                "lista": [
                    "Abra o catálogo",
                    "Busque o produto",
                    "Tire o print da imagem",
                    "Vários produtos: um print de cada",
                ],
                "print": "prints/chen-1.png",
            },
            {
                "titulo": "Pergunte se tem",
                "texto": "Mande o print com a mensagem abaixo. Espere a resposta antes de montar o pedido.",
                "acao": "whatsapp",
                "exemplo": (
                    "PERGUNTAR SE TEM",
                    "Copie e cole junto com o print:",
                    "Olá, tudo bem?\nTem este produto abaixo?",
                ),
                "notas": [
                    ("IMPORTANTE", "Ele é chinês e traduz tudo no Google. Nada de abreviação ou palavra com duplo sentido. Seja rápido e direto."),
                ],
                "print": "prints/chen-2.png",
            },
            {
                "titulo": "Mande o pedido",
                "texto": "Com todos os produtos confirmados, mande a mensagem neste padrão. Casaco e o resto: só o print.",
                "mensagens": True,
                "modelos": [
                    ("SEM PERSONALIZAÇÃO", [
                        "O print",
                        "Tipo de camisa: torcedor ou player",
                        "Os tamanhos",
                    ]),
                    ("COM PERSONALIZAÇÃO", [
                        "O print",
                        "Tipo de camisa, se precisar",
                        "Os patrocínios",
                        "Os tamanhos",
                        "O número",
                    ]),
                ],
                "notas": [
                    ("TAMANHOS", "Escreva o código da tabela de tamanhos. Torcedor: versão larga. Player: versão justa. No limite entre dois, pegue o maior. Infantil: o número, de 16 a 28."),
                    ("PATROCÍNIO", "Se o print tem patrocínio e você não quer, risque os patrocínios na imagem e escreva: SEM OS PATROCÍNIOS."),
                ],
                "print": "prints/chen-3.png",
            },
            {
                "titulo": "Envio e pagamento",
                "texto": "Só pague depois que ele confirmar. O link de pagamento vem dele, na mesma conversa.",
                "lista": [
                    "Ele pede os dados de envio",
                    "Você responde no formato abaixo",
                    "Paga pelo link e guarda o comprovante",
                    "Quando o rastreio aparecer, vincula o CPF no Portal do Importador",
                ],
                "exemplo": (
                    "DADOS DE ENVIO",
                    "Quando ele pedir, copie e preencha depois do igual:",
                    "to this address pls\nname=\nStreet=\nCountry=\ncity=\nstate=\nzip code=\nphone=\nCPF=",
                ),
                "print": "prints/chen-4.png",
            },
        ],
        "adicionais": [
            ("Personalização", "+ US$ 3"),
            ("Tamanho XXL", "+ US$ 1"),
            ("Tamanho XXXL", "+ US$ 2"),
            ("Patch", "+ US$ 1"),
        ],
        "frete": [
            ("1 camisa", "+ US$ 5"),
            ("2 camisas", "+ US$ 4"),
            ("3 camisas", "+ US$ 2"),
            ("4 camisas ou mais", "Frete grátis"),
        ],
        "pagamento": "XTransfer",
        "whatsapp": "+86 136 9032 3804",
        "video": "https://www.youtube.com/watch?v=pedido-camisa",
        "mensagens": [
            (
                "PERGUNTAR SE TEM",
                "Mande o print e esta mensagem:",
                "Olá, tudo bem?\nTem este produto abaixo?",
            ),
            (
                "SEM PERSONALIZAÇÃO",
                "Depois da confirmação, mande o print e preencha:",
                "Camisa torcedor\nTamanho L",
            ),
            (
                "COM PERSONALIZAÇÃO",
                "Se quiser número ou patrocínio. Player: um tamanho a mais.",
                "Camisa player\nTamanho XL\nNúmero 10\nPatrocínio: [nome do patrocínio]",
            ),
            (
                "SEM OS PATROCÍNIOS",
                "Se o print tem patrocínio e você não quer, risque na foto e mande:",
                "Camisa player\nSEM OS PATROCÍNIOS\nTamanho XL\nNúmero 10",
            ),
            (
                "DADOS DE ENVIO",
                "Quando ele pedir, copie e preencha depois do igual:",
                "to this address pls\nname=\nStreet=\nCountry=\ncity=\nstate=\nzip code=\nphone=\nCPF=",
            ),
        ],
        "checklist": [
            "Abri o catálogo e tirei print de cada peça",
            "Perguntei se tem e esperei a confirmação",
            "Se for camisa, marquei torcedor ou player. Casaco e o resto: só o print",
            "Se for camisa, escrevi o tamanho da tabela. Infantil: o número, de 16 a 28",
            "Se não quiser patrocínio: risquei e escrevi SEM OS PATROCÍNIOS",
            "Se for personalizado: mandei patrocínios e número",
            "Enviei o endereço com name, Street, Country, city, state, zip code, phone e CPF",
            "Paguei pelo link, guardei o comprovante e vinculei o CPF no Portal",
        ],
    },
    {
        "key": "cris",
        "nome": "Cris",
        "linha": "X Super Factory",
        "resumo": "Vários catálogos. Cada um pede separado.",
        "so_links": True,
        "links_texto": "Sem tabela de preço. Cada catálogo é um pedido separado. O valor você confirma com o contato.",
        "catalogos": [
            {
                "titulo": "Tudo",
                "descricao": "Catálogo completo.",
                "link": "https://xingtu521.x.yupoo.com/categories/",
            },
            {
                "titulo": "Tênis Adidas",
                "descricao": "Catálogo de tênis Adidas.",
                "link": "https://xingtu521.x.yupoo.com/categories/5010674",
            },
            {
                "titulo": "Tênis Nike",
                "descricao": "Catálogo de tênis Nike.",
                "link": "https://xingtu521.x.yupoo.com/categories/5010658",
            },
            {
                "titulo": "Tênis Air Jordan",
                "descricao": "Catálogo de tênis Air Jordan.",
                "link": "https://xingtu521.x.yupoo.com/categories/4972194",
            },
            {
                "titulo": "Tênis Corrida",
                "descricao": "Catálogo de tênis de corrida.",
                "link": "https://xingtu521.x.yupoo.com/categories/5010657",
            },
            {
                "titulo": "Tênis Hoka",
                "descricao": "Catálogo de tênis Hoka.",
                "link": "https://xingtu521.x.yupoo.com/categories/5010664",
            },
            {
                "titulo": "Tênis New Balance",
                "descricao": "Catálogo de tênis New Balance.",
                "link": "https://xingtu521.x.yupoo.com/categories/5010659",
            },
            {
                "titulo": "Tênis Asics",
                "descricao": "Catálogo de tênis Asics.",
                "link": "https://xingtu521.x.yupoo.com/categories/5010670",
            },
            {
                "titulo": "Tênis Puma",
                "descricao": "Catálogo de tênis Puma.",
                "link": "https://xingtu521.x.yupoo.com/categories/5010656",
            },
            {
                "titulo": "Tênis Mizuno",
                "descricao": "Catálogo de tênis Mizuno.",
                "link": "https://xingtu521.x.yupoo.com/categories/5010660",
            },
            {
                "titulo": "Tênis Brooks",
                "descricao": "Catálogo de tênis Brooks.",
                "link": "https://xingtu521.x.yupoo.com/categories/5010667",
            },
            {
                "titulo": "Óculos de sol",
                "descricao": "Catálogo de óculos de sol.",
                "link": "https://shangmei168.x.yupoo.com/albums",
            },
            {
                "titulo": "Bolsas",
                "descricao": "Catálogo de bolsas.",
                "link": "https://legent.x.yupoo.com/categories/",
            },
        ],
        "pedido_titulo": "EM SEPARADO",
        "pedido_intro": "O que soma no valor do pedido e como pagar. Cada catálogo sai num pedido separado.",
        "passos": [
            {
                "titulo": "Escolhe o catálogo",
                "texto": "Abra só o catálogo da peça. Catálogos diferentes não vão na mesma mensagem.",
                "acao": "catalogos",
                "lista": [
                    "Ache o catálogo na lista",
                    "Abra só esse",
                    "Tire um print da imagem inteira",
                ],
                "print": "prints/cris-1.png",
            },
            {
                "titulo": "Escreve a mensagem",
                "texto": "A primeira linha é o nome do catálogo. Embaixo, o modelo e a quantidade. No tênis, a numeração europeia (EU).",
                "acao": "whatsapp",
                "mensagens": True,
                "exemplo": (
                    "PEDIDO",
                    "Troque o nome do catálogo. Se não for tênis, apague a linha da numeração.",
                    "[nome do catálogo]\nModelo da foto\nQuantidade: 1\nNumeração: 42 EU",
                ),
                "print": "prints/cris-2.png",
            },
            {
                "titulo": "Espera a confirmação",
                "texto": "Ele confere o estoque e responde. Sem essa resposta, não pague.",
                "lista": [
                    "Se não tiver, o pedido para aqui",
                    "Se tiver, confira o preço que ele passou",
                    "Só então siga para o pagamento",
                ],
                "print": "prints/cris-3.png",
            },
            {
                "titulo": "Pagamento",
                "texto": "O prazo de envio começa depois que o pagamento é confirmado.",
                "lista": [
                    "Pague pelo método da etapa Frete e pagamento",
                    "Guarde o comprovante",
                    "Quando o rastreio aparecer, vincule o CPF no Portal do Importador",
                ],
                "exemplo": (
                    "DADOS DE ENVIO",
                    "Quando ele pedir, copie e preencha depois dos dois pontos:",
                    "Nome:\nEndereço:\nCidade:\nEstado:\nPaís:\nCEP:\nTelefone:\nCPF:\nE-mail:",
                ),
                "print": "prints/cris-4.png",
            },
        ],
        "adicionais": [
            ("Embalagem para presente", "+ US$ 3"),
        ],
        "frete": [
            ("1 item", "+ US$ 12"),
            ("2 itens", "+ US$ 8"),
            ("3 itens ou mais", "Grátis"),
        ],
        "pagamento": "Transferência ou carteira digital",
        "whatsapp": "+86 156 0501 5136",
        "video": "https://www.youtube.com/watch?v=pedido-tenis-luxo",
        "mensagens": [
            (
                "PEDIDO",
                "A primeira linha é o nome do catálogo. Se não for tênis, apague a numeração.",
                "[nome do catálogo]\nModelo da foto\nQuantidade: 1\nNumeração: 42 EU",
            ),
            (
                "DADOS DE ENVIO",
                "Quando ele pedir, copie e preencha depois dos dois pontos:",
                "Nome:\nEndereço:\nCidade:\nEstado:\nPaís:\nCEP:\nTelefone:\nCPF:\nE-mail:",
            ),
        ],
        "checklist": [
            "Escolhi um catálogo só, na lista",
            "Mandei uma mensagem só para aquele catálogo",
            "A primeira linha é o nome do catálogo. Anotei o modelo e a quantidade",
            "Se for tênis: confirmei a numeração europeia (EU)",
            "Esperei a confirmação do estoque antes de pagar",
            "Enviei nome, endereço, cidade, estado, país, CEP, telefone, CPF e e-mail",
            "Paguei e guardei o comprovante",
            "Quando o rastreio aparecer: vinculei o CPF no Portal do Importador",
        ],
    },
]

MOSTRAR_VIDEOS = False
MOSTRAR_PRINTS = False

VIDEOS = {
    "link": "https://www.youtube.com/@vestcap/videos",
    "texto": "Primeiro o catálogo e o pedido da camisa. Depois o tênis, os óculos e a bolsa.",
    "lista": [
        ("01", "7 min", "Como ler o catálogo de camisa"),
        ("02", "8 min", "Como mandar o pedido por print"),
        ("03", "9 min", "Pedido de tênis, óculos e bolsa"),
    ],
}

OUT = "VestCap-Guia-do-Lojista.pdf"

# ---------------------------------------------------------------- LAYOUT --

W, H = 810, 1440
ML, MR = 56, 56
CW = W - ML - MR
MAX_ITENS = 10

PRIMARIO_TOPO = 200

CREAM = HexColor("#FBF6E4")
GREEN = HexColor("#145C38")
GREEN_DEEP = HexColor("#10280A")
LIME = HexColor("#DCFF00")
YELLOW = HexColor("#FFF3B0")
WHITE = HexColor("#F7F4EA")
MUTED = HexColor("#3E6A52")
LINE = HexColor("#D5E0C8")
SOFT = HexColor("#D5E8C4")
DOTS = HexColor("#8FB56A")
DARK_CARD = HexColor("#1A3A12")

FUTURA = "/System/Library/Fonts/Supplemental/Futura.ttc"
AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
pdfmetrics.registerFont(TTFont("FuB", FUTURA, subfontIndex=2))
pdfmetrics.registerFont(TTFont("FuX", FUTURA, subfontIndex=4))
pdfmetrics.registerFont(TTFont("Av", AVENIR, subfontIndex=7))
pdfmetrics.registerFont(TTFont("AvI", AVENIR, subfontIndex=4))
pdfmetrics.registerFont(TTFont("AvB", AVENIR, subfontIndex=0))


def wrap(text, font, size, width):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else f"{cur} {word}"
        if stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(c, text, x, y, font, size, width, leading, color):
    c.setFillColor(color)
    c.setFont(font, size)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def fit(text, font, size, width):
    while size > 8 and stringWidth(text, font, size) > width:
        size -= 1
    return size


def rule(c, x1, x2, y, color=LINE, weight=1):
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.line(x1, y, x2, y)


def goto(c, key, tooltip, rect):
    c.linkAbsolute(tooltip, key, rect, thickness=0, Border="[0 0 0]")


def uri(c, url, rect):
    c.linkURL(url, rect, relative=0, thickness=0, Border="[0 0 0]")


def mark(c, key, title):
    c.bookmarkPage(key, fit="Fit")
    c.addOutlineEntry(title, key, level=0)


def fundo(c, cor):
    c.setFillColor(cor)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def brand(c, color):
    c.setFillColor(color)
    c.setFont("FuX", 20)
    c.drawRightString(W - MR, H - 52, "VESTCAP")
    c.setFont("Av", 11)
    c.drawString(ML, H - 50, "guia interno")


_MARCA = None


def _criar_marca(texto):
    import io

    from PIL import Image, ImageDraw, ImageFont

    escala = 2
    fonte = ImageFont.truetype(FUTURA, 52 * escala, index=4)
    margem = 700 * escala
    largura = W * escala + margem * 2
    altura = H * escala + margem * 2
    camada = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    desenho = ImageDraw.Draw(camada)
    caixa = desenho.textbbox((0, 0), texto, font=fonte)
    tw, th = caixa[2] - caixa[0], caixa[3] - caixa[1]
    cx, cy = largura / 2, altura / 2
    for i in range(-2, 3):
        x = cx - tw / 2 - caixa[0]
        y = cy - i * 220 * escala - th / 2 - caixa[1]
        desenho.text((x, y), texto, font=fonte, fill=(0x10, 0x28, 0x0A, 18))
    camada = camada.rotate(38, resample=Image.Resampling.BICUBIC, center=(cx, cy))
    esquerda = int(cx - W * escala / 2)
    topo = int(cy - H * escala / 2)
    recorte = camada.crop((esquerda, topo, esquerda + W * escala, topo + H * escala))
    buf = io.BytesIO()
    recorte.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def marca_dagua(c, texto="TIME INTERNO VESTCAP"):
    global _MARCA
    if _MARCA is None:
        _MARCA = _criar_marca(texto)
    c.drawImage(_MARCA, 0, 0, W, H, mask="auto")


def foot(c, page, color):
    c.setFillColor(color)
    c.setFont("Av", 13)
    c.drawString(ML, 40, "Voltar ao sumário")
    lw = stringWidth("Voltar ao sumário", "Av", 13)
    rule(c, ML, ML + lw, 36, color, 0.8)
    goto(c, "sumario", "Sumário", (ML, 30, ML + lw, 56))
    c.setFont("FuX", 14)
    c.drawRightString(W - MR, 38, f"{page:02d}")


def lime_line(c, text, x, y, size=54, text_color=GREEN_DEEP):
    size = fit(text, "FuX", size, CW - 24)
    w = stringWidth(text, "FuX", size)
    c.setFillColor(LIME)
    c.roundRect(x - 12, y - 10, w + 24, size * 0.98 + 10, 4, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont("FuX", size)
    c.drawString(x, y, text)
    return y - size - 8


def botao(c, x, y, w, label, url=None, key=None, h=64, cheio=True, cor=GREEN):
    if cheio:
        c.setFillColor(LIME)
        c.roundRect(x, y - h, w, h, h / 2, fill=1, stroke=0)
        c.setFillColor(GREEN_DEEP)
    else:
        c.setStrokeColor(cor)
        c.setLineWidth(2)
        c.roundRect(x + 1, y - h + 1, w - 2, h - 2, (h - 2) / 2, fill=0, stroke=1)
        c.setFillColor(cor)
    size = fit(label, "FuB", 17, w - 40)
    c.setFont("FuB", size)
    c.drawCentredString(x + w / 2, y - h / 2 - size * 0.35, label)
    rect = (x, y - h, x + w, y)
    if url:
        uri(c, url, rect)
    if key:
        goto(c, key, label, rect)
    return y - h


def kicker(c, text, y, color=GREEN, size=16):
    c.setFillColor(color)
    c.setFont("FuX", fit(text, "FuX", size, CW))
    c.drawString(ML, y, text)


def big(c, text, y, size, color=GREEN):
    size = fit(text, "FuX", size, CW)
    c.setFillColor(color)
    c.setFont("FuX", size)
    c.drawString(ML, y, text)


def etapas(c, y, itens, atual, r=19):
    keys = [k for k, _ in itens]
    pos = keys.index(atual)
    apagado = HexColor("#9DB291")
    col = CW / len(itens)
    centros = [ML + col * (i + 0.5) for i in range(len(itens))]

    c.setLineCap(1)
    for i in range(len(itens) - 1):
        feito = i < pos
        c.setStrokeColor(GREEN if feito else LINE)
        c.setLineWidth(3 if feito else 2)
        c.line(centros[i] + r + 10, y, centros[i + 1] - r - 10, y)

    for i, (key, label) in enumerate(itens):
        cx = centros[i]
        if i < pos:
            c.setFillColor(GREEN)
            c.circle(cx, y, r, fill=1, stroke=0)
            c.setStrokeColor(LIME)
            c.setLineWidth(3)
            c.setLineJoin(1)
            p = c.beginPath()
            p.moveTo(cx - 7, y)
            p.lineTo(cx - 2, y - 5)
            p.lineTo(cx + 8, y + 6)
            c.drawPath(p, stroke=1, fill=0)
            cor = GREEN
        elif i == pos:
            c.saveState()
            c.setFillColor(LIME)
            c.setFillAlpha(0.35)
            c.circle(cx, y, r + 8, fill=1, stroke=0)
            c.restoreState()
            c.setFillColor(LIME)
            c.setStrokeColor(GREEN_DEEP)
            c.setLineWidth(2)
            c.circle(cx, y, r, fill=1, stroke=1)
            c.setFillColor(GREEN_DEEP)
            c.setFont("FuX", 16)
            c.drawCentredString(cx, y - 6, str(i + 1))
            cor = GREEN_DEEP
        else:
            c.setFillColor(CREAM)
            c.setStrokeColor(apagado)
            c.setLineWidth(2)
            c.circle(cx, y, r, fill=1, stroke=1)
            c.setFillColor(apagado)
            c.setFont("FuX", 16)
            c.drawCentredString(cx, y - 6, str(i + 1))
            cor = apagado
        texto = label.upper()
        c.setFillColor(cor)
        c.setFont("FuX", fit(texto, "FuX", 14, col - 16))
        c.drawCentredString(cx, y - r - 28, texto)
        goto(c, key, label, (cx - col / 2, y - r - 40, cx + col / 2, y + r + 10))


def whatsapp_url(numero):
    return "https://wa.me/" + re.sub(r"\D", "", numero)


# ---------------------------------------------------------------- PÁGINAS --

def capa(c, n, ctx):
    mark(c, "capa", "Capa")
    fundo(c, GREEN_DEEP)

    c.setStrokeColor(HexColor("#1F3D16"))
    c.setLineWidth(1.5)
    for r in range(110, 560, 64):
        c.circle(W + 30, H - 330, r, fill=0, stroke=1)

    c.setFillColor(LIME)
    c.setFont("FuX", 28)
    c.drawString(ML, H - 72, "VESTCAP")
    c.setFillColor(SOFT)
    c.setFont("FuB", 13)
    c.drawRightString(W - MR, H - 68, TEXTOS["capa_edicao"])
    rule(c, ML, W - MR, H - 100, HexColor("#2C4A22"), 1)

    carimbo = TEXTOS["capa_carimbo"]
    c.saveState()
    c.translate(W - MR - 120, 1160)
    c.rotate(-12)
    sw = stringWidth(carimbo, "FuX", 22) + 52
    c.setStrokeColor(LIME)
    c.setLineWidth(2.5)
    c.rect(-sw / 2, -20, sw, 48, fill=0, stroke=1)
    c.setLineWidth(1)
    c.rect(-sw / 2 + 5, -15, sw - 10, 38, fill=0, stroke=1)
    c.setFillColor(LIME)
    c.setFont("FuX", 22)
    c.drawCentredString(0, -4, carimbo)
    c.restoreState()

    c.setFillColor(WHITE)
    y = 686 + 172 * len(TEXTOS["capa_titulo"])
    for palavra in TEXTOS["capa_titulo"]:
        c.setFont("FuX", fit(palavra, "FuX", 200, CW))
        c.drawString(ML - 6, y, palavra)
        y -= 172
    size = fit(TEXTOS["capa_destaque"], "FuX", 200, CW)
    w = stringWidth(TEXTOS["capa_destaque"], "FuX", size)
    c.setFillColor(LIME)
    c.rect(0, y - 22, ML + w + 22, size * 0.8 + 22, fill=1, stroke=0)
    c.setFillColor(GREEN_DEEP)
    c.setFont("FuX", size)
    c.drawString(ML - 6, y, TEXTOS["capa_destaque"])

    y = block(c, TEXTOS["capa_texto"], ML, y - 100, "Av", 25, 560, 36, WHITE) - 34

    x = ML
    c.setFont("FuB", 15)
    for i, cat in enumerate(TEXTOS["capa_categorias"]):
        if i:
            c.setFillColor(LIME)
            c.rect(x, y + 4, 6, 6, fill=1, stroke=0)
            x += 20
        c.setFillColor(SOFT)
        c.drawString(x, y, cat)
        x += stringWidth(cat, "FuB", 15) + 20

    rule(c, ML, W - MR, 360, HexColor("#2C4A22"), 1)
    col = CW / len(TEXTOS["capa_info"])
    for i, (rotulo, valor) in enumerate(TEXTOS["capa_info"]):
        x = ML + i * col
        c.setFillColor(LIME)
        c.setFont("FuX", 12)
        c.drawString(x, 326, rotulo)
        c.setFillColor(WHITE)
        c.setFont("Av", fit(valor, "Av", 16, col - 16))
        c.drawString(x, 300, valor)

    botao(c, ML, 200, CW, "ABRIR O GUIA", key="sumario")


def sumario(c, n, ctx):
    mark(c, "sumario", "Sumário")
    fundo(c, GREEN_DEEP)
    brand(c, LIME)
    kicker(c, "ONDE ESTÁ CADA COISA", 1270, WHITE, 20)
    lime_line(c, "SUMÁRIO", ML, 1180, 64, GREEN_DEEP)
    block(c, TEXTOS["sumario_texto"], ML, 1086, "Av", 20, CW, 28, WHITE)

    def linha(key, label, y, x0):
        num = ctx["num"][key]
        goto(c, key, label, (ML, y - 14, W - MR, y + 30))
        size = fit(label, "FuB", 19, CW - 120)
        c.setFillColor(WHITE)
        c.setFont("FuB", size)
        c.drawString(x0, y, label)
        c.setFont("FuX", 20)
        c.drawRightString(W - MR, y - 2, f"{num:02d}")
        c.setFillColor(DOTS)
        c.setFont("Av", 14)
        x = x0 + stringWidth(label, "FuB", size) + 12
        while x < W - MR - 48:
            c.drawString(x, y + 2, ".")
            x += 8

    y = 980
    primeiro = [("antes", "Antes de comprar"), ("imposto", "Como pagar menos imposto")]
    h = 64 + 48 * len(primeiro)
    c.setFillColor(LIME)
    c.roundRect(ML - 16, y - h + 30, CW + 32, h, 16, fill=1, stroke=0)
    c.setFillColor(GREEN_DEEP)
    c.setFont("FuX", 14)
    c.drawString(ML, y, "LEIA PRIMEIRO")
    ly = y - 44
    for key, label in primeiro:
        goto(c, key, label, (ML, ly - 14, W - MR, ly + 30))
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuB", 19)
        c.drawString(ML + 22, ly, label)
        c.setFont("FuX", 20)
        c.drawRightString(W - MR, ly - 2, f"{ctx['num'][key]:02d}")
        c.setFillColor(GREEN)
        c.setFont("Av", 14)
        x = ML + 22 + stringWidth(label, "FuB", 19) + 12
        while x < W - MR - 48:
            c.drawString(x, ly + 2, ".")
            x += 8
        ly -= 48
    y -= h + 30
    for idx, contato in enumerate(CONTATOS, start=1):
        c.setFillColor(DARK_CARD)
        secoes = ctx["secoes"][contato["key"]]
        h = 70 + len(secoes) * 52 + 10
        c.roundRect(ML - 16, y - h + 30, CW + 32, h, 16, fill=1, stroke=0)
        c.setFillColor(LIME)
        c.setFont("FuX", 14)
        c.drawString(ML, y, f"CONTATO {idx}")
        c.setFillColor(WHITE)
        c.setFont("FuB", 24)
        c.drawString(ML, y - 32, f"{contato['nome']} — {contato['linha']}")
        y -= 84
        for key, label in secoes:
            linha(key, label, y, ML + 22)
            y -= 52
        y -= 34
    if MOSTRAR_VIDEOS:
        linha("videos", "Todos os vídeos", y - 6, ML)


def antes_de_comprar(c, n, ctx):
    mark(c, "antes", "Antes de comprar")
    fundo(c, CREAM)
    brand(c, GREEN)
    foot(c, n, GREEN)
    kicker(c, "LEIA PRIMEIRO", 1300, GREEN, 18)
    big(c, "ANTES DE COMPRAR", 1220, 64, GREEN_DEEP)
    rule(c, ML, ML + 64, 1194, LIME, 8)
    y = 1140

    for i, (rotulo, texto) in enumerate(TEXTOS["antes"], start=1):
        c.setFillColor(LIME)
        c.circle(ML + 20, y - 8, 20, fill=1, stroke=0)
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuX", 16)
        c.drawCentredString(ML + 20, y - 14, f"{i:02d}")
        c.setFillColor(GREEN)
        c.setFont("FuX", 16)
        c.drawString(ML + 58, y - 2, rotulo)
        y = block(c, texto, ML + 58, y - 30, "Av", 18, CW - 58, 26, GREEN_DEEP) - 22
        rule(c, ML + 58, W - MR, y + 8, LINE, 1)
        y -= 14

    pares = TEXTOS["tamanhos"]
    linhas = wrap(TEXTOS["tamanhos_texto"], "Av", 17, CW - 48)
    h = 214 + 24 * len(linhas)
    bottom = y - h
    c.setFillColor(GREEN_DEEP)
    c.roundRect(ML, bottom, CW, h, 18, fill=1, stroke=0)
    c.setFillColor(LIME)
    c.setFont("FuX", 16)
    c.drawString(ML + 24, y - 36, "TAMANHOS")
    block(c, TEXTOS["tamanhos_texto"], ML + 24, y - 64, "Av", 17, CW - 48, 24, WHITE)
    gap = 10
    bw = (CW - 48 - gap * (len(pares) - 1)) / len(pares)
    by = bottom + 26
    for k, (br, intl) in enumerate(pares):
        x = ML + 24 + k * (bw + gap)
        c.setFillColor(DARK_CARD)
        c.roundRect(x, by, bw, 104, 12, fill=1, stroke=0)
        c.setFillColor(SOFT)
        c.setFont("FuB", 15)
        c.drawCentredString(x + bw / 2, by + 74, f"BR  {br}")
        c.setFillColor(LIME)
        c.setFont("FuX", 30)
        c.drawCentredString(x + bw / 2, by + 24, intl)


ETAPAS_IMPOSTO = [("imposto", "Passo a passo"), ("imposto-atencao", "Atenção")]
ALERTA = HexColor("#E5484D")


def topo_imposto(c, n, key):
    mark(c, key, "Imposto · " + dict(ETAPAS_IMPOSTO)[key])
    fundo(c, CREAM)
    brand(c, GREEN)
    foot(c, n, GREEN)
    c.setFillColor(GREEN)
    c.setFont("FuX", 16)
    c.drawString(ML, 1338, "IMPOSTO DE IMPORTAÇÃO")
    rule(c, ML, W - MR, 1320, LINE, 1)
    etapas(c, 1282, ETAPAS_IMPOSTO, key)


def imposto_passos(c, n, ctx):
    dados = TEXTOS["imposto"]
    topo_imposto(c, n, "imposto")
    big(c, "COMO PAGAR", 1150, 60, GREEN_DEEP)
    lime_line(c, "MENOS IMPOSTO", ML, 1070, 54)
    y = block(c, dados["intro"], ML, 1000, "Av", 19, CW, 27, GREEN) - 26

    for i, (verbo, texto) in enumerate(dados["passos"], start=1):
        c.setFillColor(LIME)
        c.circle(ML + 20, y - 8, 20, fill=1, stroke=0)
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuX", 16)
        c.drawCentredString(ML + 20, y - 14, str(i))
        c.setFont("FuX", 18)
        c.drawString(ML + 58, y - 2, verbo)
        y = block(c, texto, ML + 58, y - 30, "Av", 18, CW - 58, 25, GREEN) - 20

    y = botao(c, ML, y - 4, CW, "ABRIR O PORTAL DO IMPORTADOR", url=dados["link"], h=60) - 22
    linhas = wrap(dados["fim"], "FuB", 18, CW - 48)
    h = 40 + 26 * len(linhas)
    c.setFillColor(GREEN_DEEP)
    c.roundRect(ML, y - h, CW, h, 14, fill=1, stroke=0)
    block(c, dados["fim"], ML + 24, y - 32, "FuB", 18, CW - 48, 26, WHITE)


def imposto_atencao(c, n, ctx):
    dados = TEXTOS["imposto"]
    topo_imposto(c, n, "imposto-atencao")
    c.setFillColor(ALERTA)
    p = c.beginPath()
    p.moveTo(ML + 30, 1196)
    p.lineTo(ML, 1144)
    p.lineTo(ML + 60, 1144)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("FuX", 30)
    c.drawCentredString(ML + 30, 1150, "!")
    c.setFillColor(GREEN_DEEP)
    c.setFont("FuX", 64)
    c.drawString(ML + 80, 1146, "ATENÇÃO")
    rule(c, ML, ML + 64, 1120, LIME, 8)

    y = block(c, dados["regra"], ML, 1066, "FuB", 26, CW, 36, GREEN_DEEP) - 20

    linhas = wrap(dados["exemplo"], "Av", 18, CW - 48)
    h = 62 + 26 * len(linhas)
    c.setFillColor(YELLOW)
    c.roundRect(ML, y - h, CW, h, 14, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("FuX", 14)
    c.drawString(ML + 24, y - 30, "EXEMPLO")
    block(c, dados["exemplo"], ML + 24, y - 58, "Av", 18, CW - 48, 26, GREEN_DEEP)
    y -= h + 34

    for rotulo, texto in dados["riscos"]:
        c.setFillColor(ALERTA)
        c.circle(ML + 24, y - 14, 24, fill=1, stroke=0)
        c.setStrokeColor(WHITE)
        c.setLineWidth(4)
        c.setLineCap(1)
        c.line(ML + 15, y - 23, ML + 33, y - 5)
        c.line(ML + 15, y - 5, ML + 33, y - 23)
        c.setFillColor(ALERTA)
        c.setFont("FuX", 18)
        c.drawString(ML + 66, y - 6, rotulo)
        y = block(c, texto, ML + 66, y - 34, "Av", 18, CW - 66, 26, GREEN_DEEP) - 26

    linhas = wrap(dados["dica"], "FuB", 22, CW - 48)
    h = 74 + 30 * len(linhas)
    y -= 6
    c.setFillColor(GREEN_DEEP)
    c.roundRect(ML, y - h, CW, h, 16, fill=1, stroke=0)
    c.setFillColor(LIME)
    c.setFont("FuX", 14)
    c.drawString(ML + 24, y - 32, "A DICA")
    block(c, dados["dica"], ML + 24, y - 64, "FuB", 22, CW - 48, 30, WHITE)


def topo_contato(c, n, ctx, contato, idx, atual):
    fundo(c, CREAM)
    brand(c, GREEN)
    foot(c, n, GREEN)
    c.setFillColor(GREEN)
    c.setFont("FuX", 16)
    c.drawString(ML, 1338, f"CONTATO {idx}  ·  {contato['nome']} — {contato['linha']}".upper())
    rule(c, ML, W - MR, 1320, LINE, 1)
    etapas(c, 1282, ctx["secoes"][contato["key"]], atual)


def pagina_catalogo(c, n, ctx, contato, idx, cat, itens, cont, aba):
    mark(c, ctx["key"], f"{contato['nome']} · {cat['titulo']}" + (" (cont.)" if cont else ""))
    topo_contato(c, n, ctx, contato, idx, aba)
    big(c, cat["titulo"].upper(), 1150, 64)
    rule(c, ML, ML + 64, 1124, LIME, 8)
    texto = "Continuação do catálogo." if cont else cat["descricao"]
    y = block(c, texto, ML, 1074, "Av", 21, CW, 30, GREEN) - 18

    c.setFillColor(MUTED)
    c.setFont("FuX", 13)
    c.drawString(ML, y, "PEÇA")
    c.drawRightString(W - MR, y, "PREÇO")
    y -= 12
    rule(c, ML, W - MR, y, GREEN, 1.4)
    for nome, preco in itens:
        y -= 52
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuB", fit(nome, "FuB", 20, CW - 160))
        c.drawString(ML, y + 8, nome)
        c.setFillColor(GREEN)
        c.setFont("FuB", 20)
        c.drawRightString(W - MR, y + 8, preco)
        rule(c, ML, W - MR, y - 8, LINE, 1)

    y = botao(c, ML, PRIMARIO_TOPO, CW, cat.get("botao", f"ABRIR CATÁLOGO DE {cat['titulo'].upper()}"), url=cat["link"])
    c.setFillColor(MUTED)
    c.setFont("Av", 13)
    c.drawCentredString(W / 2, y - 24, cat["link"])
    uri(c, cat["link"], (ML, y - 34, ML + CW, y - 10))

def tabela_medidas(c, y, titulo, texto, cols, rows):
    c.setFillColor(GREEN)
    c.setFont("FuX", 18)
    c.drawString(ML, y, titulo)
    y = block(c, texto, ML, y - 24, "Av", 14, CW, 18, MUTED) - 8
    n = len(cols)
    cw = CW / n
    hh, rh = 28, 30
    c.setFillColor(GREEN_DEEP)
    c.rect(ML, y - hh, CW, hh, fill=1, stroke=0)
    c.setFillColor(LIME)
    c.setFont("FuX", 10)
    for i, col in enumerate(cols):
        c.drawCentredString(ML + cw * (i + 0.5), y - 18, col)
    y -= hh
    for r, row in enumerate(rows):
        if r % 2 == 0:
            c.setFillColor(WHITE)
            c.rect(ML, y - rh, CW, rh, fill=1, stroke=0)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(ML, y - rh, ML + CW, y - rh)
        c.setFillColor(GREEN_DEEP)
        c.setFont("AvB", 12)
        c.drawCentredString(ML + cw * 0.5, y - 20, row[0])
        c.setFillColor(GREEN)
        c.setFont("Av", 12)
        for i, cel in enumerate(row[1:], start=1):
            c.drawCentredString(ML + cw * (i + 0.5), y - 20, cel)
        y -= rh
    return y - 18


def pagina_medidas(c, n, ctx, contato, idx, tabelas, cont, aba):
    mark(c, ctx["key"], f"{contato['nome']} · Tamanhos" + (" (cont.)" if cont else ""))
    topo_contato(c, n, ctx, contato, idx, aba)
    big(c, "TAMANHOS", 1150, 64)
    rule(c, ML, ML + 64, 1124, LIME, 8)
    intro = "Continuação." if cont else contato.get("medidas_intro", "")
    y = block(c, intro, ML, 1080, "Av", 16, CW, 22, GREEN) - 16
    for titulo, texto, cols, rows in tabelas:
        y = tabela_medidas(c, y, titulo, texto, cols, rows)


def pagina_tabela(c, n, ctx, contato, idx):
    mark(c, ctx["key"], f"{contato['nome']} · Tabela de preços")
    topo_contato(c, n, ctx, contato, idx, ctx["key"])
    big(c, "TABELA DE PREÇOS", 1150, 64)
    rule(c, ML, ML + 64, 1124, LIME, 8)
    y = block(c, contato.get("tabela_texto", ""), ML, 1080, "Av", 19, CW, 27, GREEN) - 22

    for cat in contato["catalogos"]:
        c.setFillColor(GREEN)
        c.setFont("FuX", 17)
        c.drawString(ML, y, cat["titulo"].upper())
        pw, ph = 186, 32
        px = W - MR - pw
        c.setFillColor(LIME)
        c.roundRect(px, y - 9, pw, ph, ph / 2, fill=1, stroke=0)
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuB", 12)
        c.drawCentredString(px + pw / 2, y + 2, "ABRIR CATÁLOGO")
        uri(c, cat["link"], (px, y - 9, px + pw, y - 9 + ph))
        y -= 20
        rule(c, ML, W - MR, y, GREEN, 1.4)
        for nome, preco in cat["itens"]:
            y -= 38
            c.setFillColor(GREEN_DEEP)
            c.setFont("FuB", fit(nome, "FuB", 18, CW - 160))
            c.drawString(ML, y + 8, nome)
            c.setFillColor(GREEN)
            c.setFont("FuB", 18)
            c.drawRightString(W - MR, y + 8, preco)
            rule(c, ML, W - MR, y - 6, LINE, 1)
        y -= 44


def altura_link(cat):
    linhas = wrap(cat.get("descricao", ""), "Av", 15, CW - 250)[:2] if cat.get("descricao") else []
    return 64 + 20 * len(linhas), linhas


def pagina_links(c, n, ctx, contato, idx, catalogos, cont, numero, proxima):
    mark(c, ctx["key"], f"{contato['nome']} · Catálogos" + (" (cont.)" if cont else ""))
    topo_contato(c, n, ctx, contato, idx, f"{contato['key']}-links")
    big(c, "CATÁLOGOS", 1150, 64)
    rule(c, ML, ML + 64, 1124, LIME, 8)
    intro = "Continuação da lista." if cont else contato.get("links_texto", "")
    y = block(c, intro, ML, 1080, "Av", 19, CW, 27, GREEN) - 18

    for i, cat in enumerate(catalogos, start=numero):
        h, _ = altura_link(cat)
        bottom = y - h
        c.setFillColor(WHITE)
        c.setStrokeColor(LINE)
        c.setLineWidth(1.5)
        c.roundRect(ML, bottom, CW, h, 14, fill=1, stroke=1)
        c.setFillColor(LIME)
        c.circle(ML + 34, bottom + h / 2, 16, fill=1, stroke=0)
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuB", 12)
        c.drawCentredString(ML + 34, bottom + h / 2 - 4, f"{i:02d}")
        linhas = wrap(cat.get("descricao", ""), "Av", 15, CW - 250)[:2] if cat.get("descricao") else []
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuX", fit(cat["titulo"].upper(), "FuX", 22, CW - 280))
        titulo_y = bottom + h - 30 if linhas else bottom + h / 2 - 8
        c.drawString(ML + 64, titulo_y, cat["titulo"].upper())
        ly = titulo_y - 24
        for linha in linhas:
            c.setFillColor(MUTED)
            c.setFont("Av", 15)
            c.drawString(ML + 64, ly, linha)
            ly -= 20
        pw, ph = 132, 36
        px, py = W - MR - 18 - pw, bottom + (h - ph) / 2
        c.setFillColor(LIME)
        c.roundRect(px, py, pw, ph, ph / 2, fill=1, stroke=0)
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuB", 12)
        c.drawCentredString(px + pw / 2, py + 12, "ABRIR")
        uri(c, cat["link"], (ML, bottom, ML + CW, bottom + h))
        y = bottom - 12

    if proxima:
        botao(c, ML, y, CW, "VER O RESTO DOS CATÁLOGOS", key=proxima, h=56)


def desenhar_print(c, caminho, cx, top, max_w, max_h, rotulo):
    arquivo = None
    if caminho:
        base = os.path.splitext(os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho))[0]
        arquivo = next((base + ext for ext in (".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG") if os.path.exists(base + ext)), None)
    if arquivo:
        img = ImageReader(arquivo)
        iw, ih = img.getSize()
        escala = min(max_w / iw, max_h / ih)
        w, h = iw * escala, ih * escala
    else:
        img = None
        w, h = min(max_w, max_h * 0.46), max_h
    x, y = cx - w / 2, top - h
    raio = 26

    c.setFillColor(LIME)
    c.roundRect(x + 14, y - 14, w, h, raio, fill=1, stroke=0)
    if img:
        c.saveState()
        p = c.beginPath()
        p.roundRect(x, y, w, h, raio)
        c.clipPath(p, stroke=0, fill=0)
        c.drawImage(img, x, y, w, h, mask="auto")
        c.restoreState()
        c.setStrokeColor(GREEN_DEEP)
        c.setLineWidth(6)
        c.roundRect(x, y, w, h, raio, fill=0, stroke=1)
    else:
        c.setFillColor(WHITE)
        c.roundRect(x, y, w, h, raio, fill=1, stroke=0)
        c.setStrokeColor(GREEN)
        c.setLineWidth(2)
        c.setDash(10, 8)
        c.roundRect(x + 1, y + 1, w - 2, h - 2, raio, fill=0, stroke=1)
        c.setDash()
        c.setFillColor(GREEN)
        c.setFont("FuX", fit(rotulo, "FuX", 22, w - 28))
        c.drawCentredString(cx, y + h / 2 + 10, rotulo)
        c.setFillColor(MUTED)
        c.setFont("Av", fit(caminho or "sem arquivo", "Av", 14, w - 28))
        c.drawCentredString(cx, y + h / 2 - 20, caminho or "sem arquivo")


def modelos_mensagem(c, y, modelos):
    gap = 16
    col_w = (CW - gap * (len(modelos) - 1)) / len(modelos)
    tw = col_w - 76
    alturas = [56 + sum(len(wrap(item, "Av", 16, tw)) * 22 + 14 for item in itens) for _, itens in modelos]
    h = max(alturas) + 6
    bottom = y - h
    for j, (titulo, itens) in enumerate(modelos):
        x = ML + j * (col_w + gap)
        c.setFillColor(YELLOW)
        c.roundRect(x, bottom, col_w, h, 14, fill=1, stroke=0)
        c.setFillColor(GREEN)
        c.setFont("FuX", fit(titulo, "FuX", 14, col_w - 40))
        c.drawString(x + 20, y - 30, titulo)
        ly = y - 62
        for k, item in enumerate(itens, start=1):
            c.setFillColor(LIME)
            c.circle(x + 32, ly + 5, 12, fill=1, stroke=0)
            c.setFillColor(GREEN_DEEP)
            c.setFont("FuB", 12)
            c.drawCentredString(x + 32, ly + 1, str(k))
            ly = block(c, item, x + 56, ly, "Av", 16, tw, 22, GREEN_DEEP) - 14
    return bottom - 16


def nota(c, y, rotulo, texto):
    linhas = wrap(texto, "Av", 17, CW - 48)
    h = 52 + 24 * len(linhas)
    bottom = y - h
    c.setFillColor(GREEN_DEEP)
    c.roundRect(ML, bottom, CW, h, 14, fill=1, stroke=0)
    c.setFillColor(LIME)
    c.setFont("FuX", 13)
    c.drawString(ML + 24, y - 28, rotulo)
    block(c, texto, ML + 24, y - 54, "Av", 17, CW - 48, 24, WHITE)
    return bottom - 12


def lista_curta(c, y, itens):
    blocos = [wrap(item, "Av", 18, CW - 108) for item in itens]
    h = 28 + sum(18 + 24 * len(linhas) for linhas in blocos)
    bottom = y - h
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.setLineWidth(1.5)
    c.roundRect(ML, bottom, CW, h, 16, fill=1, stroke=1)
    ly = y - 34
    for i, linhas in enumerate(blocos, start=1):
        c.setFillColor(LIME)
        c.circle(ML + 36, ly + 6, 14, fill=1, stroke=0)
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuB", 13)
        c.drawCentredString(ML + 36, ly + 1, str(i))
        for linha in linhas:
            c.setFillColor(GREEN_DEEP)
            c.setFont("Av", 18)
            c.drawString(ML + 64, ly, linha)
            ly -= 24
        ly -= 18
    return bottom - 16


def cartao_mensagem(c, y, titulo, dica, texto):
    linhas = texto.split("\n")
    dicas = wrap(dica, "Av", 15, CW - 52)
    msg_h = 20 + 30 * len(linhas)
    h = 52 + 22 * len(dicas) + msg_h
    bottom = y - h
    c.setFillColor(YELLOW)
    c.roundRect(ML, bottom, CW, h, 16, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("FuX", 14)
    c.drawString(ML + 24, y - 28, titulo)
    block(c, dica, ML + 24, y - 52, "Av", 15, CW - 52, 22, MUTED)
    box_top = bottom + 14 + msg_h
    c.setFillColor(WHITE)
    c.roundRect(ML + 16, bottom + 14, CW - 32, msg_h, 10, fill=1, stroke=0)
    c.setFillColor(LIME)
    c.roundRect(ML + 28, bottom + 26, 5, msg_h - 24, 2, fill=1, stroke=0)
    texto_msg = c.beginText(ML + 48, box_top - 26)
    texto_msg.setFont("AvB", 18)
    texto_msg.setFillColor(GREEN_DEEP)
    texto_msg.setLeading(30)
    for linha in linhas:
        texto_msg.textLine(linha)
    c.drawText(texto_msg)
    return bottom - 14


def pagina_passo(c, n, ctx, contato, idx, i, passo, aba):
    if not isinstance(passo, dict):
        passo = {"titulo": passo[0], "texto": passo[1], "print": passo[2] if len(passo) > 2 else None}
    total = len(contato["passos"])
    mark(c, ctx["key"], f"{contato['nome']} · Passo {i}")
    topo_contato(c, n, ctx, contato, idx, aba)

    c.setFillColor(GREEN)
    c.setFont("FuX", 18)
    c.drawString(ML, 1176, f"PASSO {i:02d} DE {total:02d}")
    big(c, passo["titulo"].upper(), 1110, 56, GREEN_DEEP)
    y = block(c, passo["texto"], ML, 1058, "Av", 21, CW, 30, GREEN) - 18

    if passo.get("acao") == "whatsapp":
        y = botao(c, ML, y, CW, "CHAMAR NO WHATSAPP", url=whatsapp_url(contato["whatsapp"]), h=56) - 18
    elif passo.get("acao") == "catalogos":
        y = botao(c, ML, y, CW, "VER OS CATÁLOGOS", key=ctx["inicio"][contato["key"]], h=56) - 18

    if passo.get("lista"):
        y = lista_curta(c, y, passo["lista"])
    if passo.get("exemplo"):
        y = cartao_mensagem(c, y, *passo["exemplo"])
    if passo.get("modelos"):
        y = modelos_mensagem(c, y, passo["modelos"])
    for rotulo, texto in passo.get("notas", []):
        y = nota(c, y, rotulo, texto)
    if passo.get("mensagens"):
        y = botao(c, ML, y, CW, "VER AS MENSAGENS PRONTAS", key=f"{contato['key']}-mensagens", h=56) - 18

    if MOSTRAR_PRINTS:
        desenhar_print(c, passo.get("print"), W / 2 - 7, y - 12, CW - 120, y - 132, f"PRINT DO PASSO {i:02d}")


def pagina_mensagens(c, n, ctx, contato, idx, mensagens, cont):
    mark(c, ctx["key"], f"{contato['nome']} · Mensagens" + (" (cont.)" if cont else ""))
    topo_contato(c, n, ctx, contato, idx, f"{contato['key']}-mensagens")
    big(c, "MENSAGENS PRONTAS", 1150, 56)
    rule(c, ML, ML + 64, 1124, LIME, 8)
    intro = "O restante das mensagens." if cont else "Selecione só o bloco branco, copie e cole no WhatsApp. Troque o que está entre [ ]."
    y = block(c, intro, ML, 1080, "Av", 19, CW, 27, GREEN) - 20

    for titulo, dica, texto in mensagens:
        y = cartao_mensagem(c, y, titulo, dica, texto)

    botao(c, ML, 200, CW, "CHAMAR NO WHATSAPP", url=whatsapp_url(contato["whatsapp"]))


def pagina_checklist(c, n, ctx, contato, idx):
    mark(c, ctx["key"], f"{contato['nome']} · Checklist")
    topo_contato(c, n, ctx, contato, idx, ctx["key"])
    big(c, "CHECKLIST", 1150, 64)
    rule(c, ML, ML + 64, 1124, LIME, 8)
    y = block(
        c,
        "Marque na hora do pedido. Se faltar algum item, volta na etapa certa antes de pagar.",
        ML, 1080, "Av", 20, CW, 28, GREEN,
    ) - 28

    itens = contato["checklist"]
    for i, texto in enumerate(itens, start=1):
        linhas = wrap(texto, "Av", 20, CW - 100)
        h = max(64, 28 + 28 * len(linhas))
        bottom = y - h
        c.setFillColor(WHITE)
        c.setStrokeColor(LINE)
        c.setLineWidth(1.5)
        c.roundRect(ML, bottom, CW, h, 14, fill=1, stroke=1)
        c.setStrokeColor(GREEN)
        c.setLineWidth(2.5)
        c.roundRect(ML + 22, bottom + h / 2 - 16, 32, 32, 6, fill=0, stroke=1)
        c.setFillColor(MUTED)
        c.setFont("FuX", 14)
        c.drawString(ML + 70, bottom + h - 24, f"{i:02d}")
        block(c, texto, ML + 70, bottom + h - 48, "Av", 20, CW - 100, 28, GREEN_DEEP)
        y = bottom - 12

    botao(c, ML, 200, CW, "CHAMAR NO WHATSAPP", url=whatsapp_url(contato["whatsapp"]))


def pagina_pedido(c, n, ctx, contato, idx):
    mark(c, ctx["key"], f"{contato['nome']} · Frete e pagamento")
    topo_contato(c, n, ctx, contato, idx, ctx["key"])
    big(c, "FRETE E PAGAMENTO", 1150, 64)
    rule(c, ML, ML + 64, 1124, LIME, 8)
    y = block(c, contato["pedido_intro"], ML, 1080, "Av", 21, CW, 30, GREEN) - 24

    tabelas = [t for t in (("ADICIONAIS", contato["adicionais"]), ("FRETE", contato["frete"])) if t[1]]
    if tabelas:
        gap = 16
        col_w = (CW - gap * (len(tabelas) - 1)) / len(tabelas)
        rows = max(len(t[1]) for t in tabelas)
        h = 50 + rows * 28
        bottom = y - h
        for j, (titulo, linhas) in enumerate(tabelas):
            x = ML + j * (col_w + gap)
            c.setFillColor(YELLOW)
            c.roundRect(x, bottom, col_w, h, 14, fill=1, stroke=0)
            c.setFillColor(GREEN)
            c.setFont("FuX", 13)
            c.drawString(x + 18, bottom + h - 26, titulo)
            ly = bottom + h - 54
            for esq, dir_ in linhas:
                c.setFillColor(GREEN_DEEP)
                c.setFont("Av", fit(esq, "Av", 15, col_w - 130))
                c.drawString(x + 18, ly, esq)
                c.setFont("AvB", 15)
                c.drawRightString(x + col_w - 18, ly, dir_)
                ly -= 28
        y = bottom - 14

    h = 76
    bottom = y - h
    c.setStrokeColor(GREEN)
    c.setLineWidth(1.4)
    c.roundRect(ML + 0.7, bottom + 0.7, CW - 1.4, h - 1.4, 14, fill=0, stroke=1)
    c.setFillColor(GREEN)
    c.setFont("FuX", 12)
    c.drawString(ML + 18, bottom + h - 24, "PAGAMENTO")
    c.drawString(ML + CW / 2, bottom + h - 24, "WHATSAPP")
    c.setFillColor(GREEN_DEEP)
    c.setFont("FuB", fit(contato["pagamento"], "FuB", 16, CW / 2 - 30))
    c.drawString(ML + 18, bottom + 20, contato["pagamento"])
    c.setFont("FuB", 16)
    c.drawString(ML + CW / 2, bottom + 20, contato["whatsapp"])

    topo = bottom - 40
    passo = f"{contato['key']}-passo"
    if MOSTRAR_VIDEOS and contato.get("video"):
        w1 = CW * 0.62
        botao(c, ML, topo, w1, "COMEÇAR O PASSO A PASSO", key=passo)
        botao(c, ML + w1 + 14, topo, CW - w1 - 14, "VER O VÍDEO", url=contato["video"], cheio=False)
    else:
        botao(c, ML, topo, CW, "COMEÇAR O PASSO A PASSO", key=passo)

def videos(c, n, ctx):
    mark(c, "videos", "Vídeos")
    fundo(c, GREEN_DEEP)
    brand(c, LIME)
    foot(c, n, WHITE)
    kicker(c, "TODOS EM UM LUGAR", 1270, WHITE, 20)
    lime_line(c, "VÍDEOS", ML, 1170, 60, GREEN_DEEP)
    y = block(c, VIDEOS["texto"], ML, 1070, "Av", 22, 640, 32, WHITE) - 20
    for num, tempo, titulo in VIDEOS["lista"]:
        h = 130
        bottom = y - h
        c.setFillColor(DARK_CARD)
        c.roundRect(ML, bottom, CW, h, 16, fill=1, stroke=0)
        c.setFillColor(LIME)
        c.setFont("FuX", 22)
        c.drawString(ML + 24, bottom + h - 42, num)
        c.setFillColor(WHITE)
        c.setFont("FuB", fit(titulo, "FuB", 22, CW - 120))
        c.drawString(ML + 80, bottom + h - 42, titulo)
        c.setFillColor(SOFT)
        c.setFont("Av", 16)
        c.drawString(ML + 80, bottom + 36, tempo)
        c.setFillColor(LIME)
        c.roundRect(ML + CW - 180, bottom + 30, 150, 40, 20, fill=1, stroke=0)
        c.setFillColor(GREEN_DEEP)
        c.setFont("FuB", 13)
        c.drawCentredString(ML + CW - 105, bottom + 45, "ASSISTIR")
        uri(c, VIDEOS["link"], (ML, bottom, ML + CW, y))
        y = bottom - 16
    botao(c, ML, y - 14, CW, "ABRIR OS VÍDEOS NO YOUTUBE", url=VIDEOS["link"])
    c.setFillColor(SOFT)
    c.setFont("Av", 14)
    c.drawCentredString(W / 2, y - 110, VIDEOS["link"])


# ---------------------------------------------------------------- MONTAGEM --

def montar():
    pages = [
        {"key": "capa", "draw": capa},
        {"key": "sumario", "draw": sumario},
        {"key": "antes", "draw": antes_de_comprar},
        {"key": "imposto", "draw": imposto_passos},
        {"key": "imposto-atencao", "draw": imposto_atencao},
    ]
    inicio, secoes = {}, {}
    for idx, contato in enumerate(CONTATOS, start=1):
        secoes[contato["key"]] = []
        if contato.get("medidas"):
            mkey = f"{contato['key']}-medidas"
            secoes[contato["key"]].append((mkey, "Tamanhos"))
            for k, parte in enumerate(contato["medidas"]):
                pages.append({
                    "key": mkey if k == 0 else f"{mkey}-{k + 1}",
                    "draw": pagina_medidas,
                    "args": (contato, idx, parte, k > 0, mkey),
                    "contato": contato["key"],
                })
        unica = contato.get("tabela_unica") or contato.get("so_links")
        if unica:
            if contato.get("so_links"):
                key = f"{contato['key']}-links"
                secoes[contato["key"]].append((key, "Catálogos"))
                inicio[contato["key"]] = key
                partes, atual, altura = [], [], 0
                for cat in contato["catalogos"]:
                    h, _ = altura_link(cat)
                    if atual and altura + h + 12 > 760:
                        partes.append(atual)
                        atual, altura = [], 0
                    atual.append(cat)
                    altura += h + 12
                if atual:
                    partes.append(atual)
                numero = 1
                for k, parte in enumerate(partes):
                    pages.append({
                        "key": key if k == 0 else f"{key}-{k + 1}",
                        "draw": pagina_links,
                        "args": (
                            contato,
                            idx,
                            parte,
                            k > 0,
                            numero,
                            f"{key}-{k + 2}" if k + 1 < len(partes) else None,
                        ),
                        "contato": contato["key"],
                    })
                    numero += len(parte)
            else:
                key = f"{contato['key']}-precos"
                secoes[contato["key"]].append((key, "Tabela de preços"))
                inicio[contato["key"]] = key
                pages.append({
                    "key": key,
                    "draw": pagina_tabela,
                    "args": (contato, idx),
                    "contato": contato["key"],
                })
        for num, cat in enumerate([] if unica else contato["catalogos"], start=1):
            itens = cat["itens"]
            partes = [itens[i:i + MAX_ITENS] for i in range(0, len(itens), MAX_ITENS)] or [[]]
            aba = f"{contato['key']}-catalogo-{num}"
            secoes[contato["key"]].append((aba, cat.get("aba", cat["titulo"])))
            inicio.setdefault(contato["key"], aba)
            for k, parte in enumerate(partes):
                pages.append({
                    "key": aba + (f"-{k + 1}" if k else ""),
                    "draw": pagina_catalogo,
                    "args": (contato, idx, cat, parte, k > 0, aba),
                    "aba": cat.get("aba", cat["titulo"]),
                    "contato": contato["key"],
                })
        pedido = f"{contato['key']}-pedido"
        secoes[contato["key"]].append((pedido, "Frete e pagamento"))
        pages.append({
            "key": pedido,
            "draw": pagina_pedido,
            "args": (contato, idx),
            "contato": contato["key"],
            "pedido": True,
        })
        passo_aba = f"{contato['key']}-passo"
        if contato["passos"]:
            secoes[contato["key"]].append((passo_aba, "Passo a passo"))
        for i, passo in enumerate(contato["passos"], start=1):
            pages.append({
                "key": passo_aba if i == 1 else f"{passo_aba}-{i}",
                "draw": pagina_passo,
                "args": (contato, idx, i, passo, passo_aba),
                "contato": contato["key"],
            })
        if contato.get("mensagens"):
            msg_aba = f"{contato['key']}-mensagens"
            secoes[contato["key"]].append((msg_aba, "Mensagens"))
            bloco = 3
            partes = [contato["mensagens"][i:i + bloco] for i in range(0, len(contato["mensagens"]), bloco)]
            for k, parte in enumerate(partes):
                pages.append({
                    "key": msg_aba if k == 0 else f"{msg_aba}-{k + 1}",
                    "draw": pagina_mensagens,
                    "args": (contato, idx, parte, k > 0),
                    "contato": contato["key"],
                })
        if contato.get("checklist"):
            check = f"{contato['key']}-checklist"
            secoes[contato["key"]].append((check, "Checklist"))
            pages.append({
                "key": check,
                "draw": pagina_checklist,
                "args": (contato, idx),
                "contato": contato["key"],
            })
    if MOSTRAR_VIDEOS:
        pages.append({"key": "videos", "draw": videos})
    return pages, inicio, secoes


def main():
    pages, inicio, secoes = montar()
    num = {p["key"]: i + 1 for i, p in enumerate(pages)}
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle("VestCap — Guia de contatos")
    c.setAuthor("VestCap")
    for i, p in enumerate(pages):
        ctx = {"key": p["key"], "num": num, "inicio": inicio, "secoes": secoes}
        n = i + 1
        if "args" in p:
            p["draw"](c, n, ctx, *p["args"])
        else:
            p["draw"](c, n, ctx)
        marca_dagua(c)
        c.showPage()
    c.save()
    print(OUT, len(pages), "páginas")


if __name__ == "__main__":
    main()

