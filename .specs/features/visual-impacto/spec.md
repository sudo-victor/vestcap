# Visual de impacto Specification

## Problem Statement

A página abre e funciona, mas a primeira tela é um formulário simples. Quem recebe o link no celular não sente que entrou num guia fechado da VestCap. O impacto tem que aparecer antes de qualquer contato, e o pedido em si tem que continuar fácil de ler, copiar e tocar.

## Goals

- [ ] A tela de entrada ocupa o celular inteiro, no verde escuro da marca, com o fundo Silk do React Bits e o nome VestCap em brilho lima
- [ ] Depois do código, os catálogos ganham o Spotlight Card. Tabelas, passos e mensagens ficam parados, para ler e copiar
- [ ] O HTML de quem não entrou continua sem catálogo, WhatsApp e mensagem
- [ ] Quem pediu menos movimento no celular vê o fundo parado

## Out of Scope

| Feature | Reason |
| --- | --- |
| React Bits Pro | Biblioteca paga, com licença. O plano usa só o registro gratuito |
| Tailwind | O app já está em CSS. A variante é TypeScript + CSS |
| Fundo 3D de brinquedo (Ballpit, Hyperspeed, Glitch, terminal, cursor de tinta) | Pesa no celular e atrapalha o pedido |
| Animar preço, tabela de tamanho ou texto da mensagem | O número e a mensagem têm que aparecer inteiros na hora |
| Mudar o PDF | O visual novo é só da página |
| Trocar a paleta | Continuam `#10280A`, `#145C38`, `#DCFF00` e `#FBF6E4` |

---

## User Stories

### P1: A porta de entrada ⭐ MVP

**User Story**: Como lojista, quero abrir o link e ver uma tela de marca antes do formulário, para sentir que o guia é fechado e feito para mim.

**Why P1**: É a primeira coisa que aparece. Sem isso, o resto do guia continua com cara de rascunho.

**Acceptance Criteria**:

1. WHEN a pessoa abre a página sem sessão THEN a tela SHALL ocupar a altura da janela, com fundo `#10280A` e o componente Silk nas cores `#145C38` e `#DCFF00`
2. WHEN a tela de entrada aparece THEN o título VestCap SHALL usar ShinyText, com a cor de base `#DCFF00` e o brilho `#FBF6E4`
3. WHEN a tela de entrada aparece THEN o campo de código e o botão Entrar SHALL continuar utilizáveis por cima do fundo
4. WHEN o sistema pede menos movimento THEN o Silk SHALL ficar parado (`paused`)
5. WHEN a pessoa ainda não entrou THEN o HTML SHALL continuar sem `wa.me`, sem link de catálogo e sem número de contato

**Independent Test**: Abrir `/` sem cookie. A tela é escura, o nome brilha, o formulário envia. O HTML dessa resposta não contém contato.

---

### P2: Catálogo com luz

**User Story**: Como lojista já dentro do guia, quero que cada catálogo pareça um cartão, para achar o que vou abrir sem perder o passo a passo.

**Why P2**: O impacto da porta já vende a entrada. O cartão ajuda a percorrer a lista sem mexer no que precisa ser copiado.

**Acceptance Criteria**:

1. WHEN o guia autenticado lista um catálogo THEN esse bloco SHALL estar dentro de um SpotlightCard no tema claro, com a luz `#DCFF00`
2. WHEN o guia mostra tabela de tamanho, passo ou mensagem pronta THEN esses blocos SHALL permanecer texto estático, fora do SpotlightCard
3. WHEN a pessoa toca em Abrir catálogo ou Chamar no WhatsApp THEN o destino SHALL ser o mesmo link de hoje

**Independent Test**: Entrar com um código ativo, ver o cartão no catálogo e o bloco branco da mensagem sem animação. O link de WhatsApp segue `https://wa.me/` mais os dígitos.

---

## Edge Cases

- WHEN o celular não tem WebGL2 THEN o Silk SHALL falhar em silêncio e a tela SHALL continuar legível no verde `#10280A`, com o formulário no lugar
- WHEN `prefers-reduced-motion: reduce` THEN o ShinyText SHALL deixar o título estático na cor lima e o Silk SHALL receber `paused`
- WHEN a lista de catálogos é longa THEN só o cartão visível SHALL animar a luz. O restante da página SHALL rolar como hoje
- WHEN o código é recusado THEN a frase "Código não entra." SHALL continuar visível sobre o fundo

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| VIS-01 | P1: A porta de entrada | Tasks | Pending |
| VIS-02 | P1: A porta de entrada | Tasks | Pending |
| VIS-03 | P1: A porta de entrada | Tasks | Pending |
| VIS-04 | P1: A porta de entrada | Tasks | Pending |
| VIS-05 | P2: Catálogo com luz | Tasks | Pending |
| VIS-06 | P2: Catálogo com luz | Tasks | Pending |

**Coverage:** 6 total, 6 mapped to tasks, 0 unmapped

---

## Success Criteria

- [ ] No celular, a primeira tela parece um convite da marca e o formulário continua óbvio
- [ ] Uma pessoa consegue copiar a mensagem e abrir o catálogo sem a animação cobrir o texto
- [ ] O teste de entrada sem contato continua passando
- [ ] `npx next build` em `web/` passa
