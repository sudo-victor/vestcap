# VestCap Guia

**Vision:** O guia de contatos da VestCap vira uma página de celular que só abre com o código de cada cliente.
**For:** Lojistas que receberam acesso, na hora de fazer o pedido. Quem opera é a VestCap.
**Solves:** No PDF, o link falha dentro do WhatsApp e copiar a mensagem é ruim. Um link solto, sem trava, entrega os contatos para qualquer pessoa.

## Goals

- Quem não tem código válido não vê catálogo, WhatsApp nem mensagem pronta
- Quem tem código abre o catálogo, cai no WhatsApp e copia a mensagem com um toque, no celular
- Apagar o código de uma pessoa trava só essa pessoa
- O mesmo dado de contato alimenta o PDF e a página

## Tech Stack

**Core:**

- Página: Next.js 16 (App Router), na pasta `web/`, raiz do projeto na Vercel
- Language: TypeScript na página. Python 3 só no gerador do PDF
- Acesso: variável `VESTCAP_ACESSOS` e segredo `VESTCAP_SEGREDO`, lidos no servidor
- Conteúdo: `gerar_guia.py` exporta `web/dados/guia.json`. A página lê esse JSON no servidor

**Key dependencies:** next, react, server-only. reportlab continua só no PDF.

## Scope

**v1 includes:**

- Página no formato do celular com o guia que já existe: Chen, Cris, tamanhos, frete, passos, mensagens e checklist
- Código individual para entrar
- Desligar um código sem afetar os outros
- Botão que copia a mensagem inteira e links que abrem catálogo e WhatsApp
- O PDF continua sendo gerado

**Explicitly out of scope:**

- Impedir print ou encaminhamento depois que a pessoa viu a tela
- Site público, loja ou página de venda
- Uma senha só para todo mundo, ou um link secreto como única trava
- Página de vídeos
- Cobrança automática do acesso

## Constraints

- Timeline: não definida
- Technical: os contatos não podem ir no HTML de quem ainda não entrou. O leitor de PDF do WhatsApp não é o destino
- Resources: uma pessoa opera os códigos. O conteúdo em português segue o tom do guia atual
