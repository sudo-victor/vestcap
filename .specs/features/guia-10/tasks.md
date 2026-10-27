# Guia 10 Tasks

**Design**: pulado. A mudança cabe em `gerar_guia.py`, no desenho que já existe.
**Spec**: `.specs/features/guia-10/spec.md`
**Status**: Draft

T5–T8 não começam sem as respostas do context.md.

---

## Execution Plan

### Phase 1: O que já dá para fazer

T1 → T2 → T3 → T4

### Phase 2: Dados reais

Depende das respostas. Podem rodar em paralelo entre si.

T5, T6, T7, T8

### Phase 3: Fechamento

T4 e T5–T8 completos, então T9

---

## Task Breakdown

### T1: Tirar a legenda que repete o título

**What**: Apagar a descrição dos catálogos da Cris cujo texto só repete o nome. Não mexer na linha "Tudo" nesta tarefa.
**Where**: `gerar_guia.py` (`catalogos` da Cris)
**Depends on**: None
**Reuses**: `pagina_links` já omite a segunda linha quando não há descrição
**Requirement**: LISTA-01

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Tênis Adidas até Bolsas ficam só com título, link e botão Abrir
- [ ] "Tudo" continua com a descrição atual
- [ ] `python3 gerar_guia.py` gera o PDF sem erro

**Verify**:

Abrir as páginas de catálogo da Cris. A linha "Tênis Nike" não tem "Catálogo de tênis Nike" embaixo.

---

### T2: Conferir a lista com linhas curtas

**What**: Gerar o PDF e ver se os 13 catálogos cabem melhor, e se o botão de continuação só aparece quando há próxima página.
**Where**: páginas de catálogo da Cris em `VestCap-Guia-do-Lojista.pdf`
**Depends on**: T1
**Reuses**: `altura_link` e o fatiamento em `montar`
**Requirement**: LISTA-02

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Nenhuma linha corta o título
- [ ] "VER O RESTO DOS CATÁLOGOS" não aparece na última página da lista
- [ ] O botão Abrir não encosta no título

**Verify**:

Render das páginas de catálogo. A última não contém o texto "VER O RESTO DOS CATÁLOGOS".

---

### T3: Fechar cada passo com "Acabou quando"

**What**: Em cada um dos oito passos, desenhar um cartão escuro de uma frase dizendo quando o passo terminou.
**Where**: `gerar_guia.py`, campo novo no passo e `pagina_passo`
**Depends on**: None
**Reuses**: `nota`
**Requirement**: PASSO-01, PASSO-02

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Os quatro passos do Chen e os quatro da Cris têm o aviso
- [ ] O aviso fica acima do rodapé e não cobre botão
- [ ] `MOSTRAR_PRINTS` continua falso e nenhum quadro de print aparece

**Verify**:

Render dos oito passos. Cada página contém "Acabou quando" e não contém "PRINT DO PASSO".

**Commit**: `feat(guia): fecha cada passo com o critério de pronto`

---

### T4: Garantir a cópia dos endereços

**What**: Selecionar os blocos brancos de endereço do Chen e da Cris e comparar com o texto combinado.
**Where**: páginas de mensagem e o passo de pagamento de cada um
**Depends on**: T3
**Reuses**: marca d'água em imagem, `cartao_mensagem`
**Requirement**: COPY-01

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Chen cola `to this address pls` até `CPF=` em linhas separadas
- [ ] Cris cola `Nome:` até `E-mail:` em linhas separadas
- [ ] A seleção não inclui "TIME INTERNO"

**Verify**:

`PDFPage.selection(for:)` no retângulo do bloco branco. A string é igual ao template do arquivo.

---

### T5: WhatsApp real [bloqueada]

**What**: Trocar os placeholders e só então mostrar número e botão.
**Where**: `whatsapp` de Chen e Cris, e o desenho do botão
**Depends on**: resposta do context.md
**Reuses**: `whatsapp_url`, `botao`
**Requirement**: DADO-01

**Done when**:

- [ ] O PDF não contém `90000-0001` nem `90000-0002`
- [ ] Com número real, o botão abre `https://wa.me/` com os dígitos certos

**Verify**:

Extrair o texto do PDF e buscar `90000-000`. Com o número novo no arquivo, o link do botão usa esse número.

---

### T6: Frete e pagamento da Cris [bloqueada]

**What**: Publicar só frete, adicional e pagamento que forem confirmados. Omitir o resto.
**Where**: `adicionais`, `frete`, `pagamento` da Cris e `pagina_pedido`
**Depends on**: resposta do context.md
**Reuses**: `pagina_pedido` já esconde lista vazia
**Requirement**: DADO-02

**Done when**:

- [ ] Valor não confirmado não aparece na página Frete e pagamento
- [ ] Valor confirmado aparece com o texto exato informado

**Verify**:

Ler a página Frete e pagamento da Cris e comparar com a lista confirmada no context.md.

---

### T7: Regra do catálogo "Tudo" [bloqueada]

**What**: Escrever na linha "Tudo" quando esse catálogo deve ser usado.
**Where**: descrição do catálogo "Tudo"
**Depends on**: resposta do context.md
**Reuses**: segunda linha de `pagina_links`
**Requirement**: LISTA-03

**Done when**:

- [ ] A linha "Tudo" tem uma frase que diferencia esse catálogo dos de marca
- [ ] As outras linhas continuam sem descrição repetida

**Verify**:

Na primeira página de catálogos, "Tudo" tem a frase do context.md e "Tênis Nike" não tem segunda linha.

---

### T8: Óculos e bolsas [bloqueada]

**What**: Se forem outro atendimento, o passo e o botão não mandam esses catálogos para o WhatsApp dos tênis.
**Where**: passos, mensagens e catálogos da Cris
**Depends on**: resposta do context.md
**Reuses**: `acao: whatsapp`
**Requirement**: DADO-03, DADO-04

**Done when**:

- [ ] Se for o mesmo contato, o PDF diz isso numa frase na lista
- [ ] Se for outro, óculos e bolsas não usam o WhatsApp dos tênis

**Verify**:

Ler o passo "Escreve a mensagem" e a linha de óculos e de bolsas. O destino bate com o context.md.

---

### T9: Revisão visual do PDF inteiro

**What**: Renderizar todas as páginas e checar sobreposição, stepper e rodapé.
**Where**: `VestCap-Guia-do-Lojista.pdf`
**Depends on**: T2, T3, T4 e as tarefas da fase 2 que tiverem sido desbloqueadas
**Reuses**: render PDFKit já usado no projeto

**Done when**:

- [ ] Nenhuma página tem texto cortado ou botão em cima de cartão
- [ ] Capa, sumário e marca d'água continuam como estão
- [ ] O checklist de sucesso do spec.md está marcado

**Verify**:

Render de todas as páginas. Percorrer capa, sumário, um passo do Chen, as páginas de catálogo da Cris e as duas de mensagem.

---

## Parallel Execution Map

```
Phase 1:
  T1 → T2
  T3 → T4

Phase 2 (depois das respostas):
  T5
  T6
  T7
  T8

Phase 3:
  T9
```

---

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1: Apagar descrições repetidas | dados num arquivo | Granular |
| T2: Conferir a lista | uma verificação | Granular |
| T3: Aviso de fim do passo | um campo e um desenho | Granular |
| T4: Cópia do endereço | uma verificação | Granular |
| T5–T8 | uma decisão cada | Bloqueadas |
| T9: Revisão visual | uma passagem | Granular |

**Granularity check**: nenhuma tarefa mexe em mais de um comportamento.
