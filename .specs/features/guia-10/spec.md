# Guia 10 Specification

## Problem Statement

O guia já ensina o pedido, mas não chega a 10 em UX, intuição e design. Páginas de passo terminam no vazio, a lista da Cris repete o título em cada linha, e o PDF afirma telefone, frete e pagamento que ainda podem ser fictícios. Quem segue o guia ao pé da letra liga para o número errado ou paga um frete que ninguém combinou.

## Goals

- [ ] Design: nenhuma página de passo termina com um único bloco e o resto da tela vazia
- [ ] Intuição: a lista da Cris se lê pelo título; a segunda linha só existe quando acrescenta uma regra
- [ ] UX: o PDF não publica WhatsApp, frete ou pagamento que não tenham sido confirmados
- [ ] Os dois blocos de endereço continuam copiando para o WhatsApp com uma linha por campo

## Out of Scope

| Feature | Reason |
| --- | --- |
| Voltar os prints dos passos | Foram tirados de propósito até existirem os arquivos certos |
| Botão "Próximo" | A navegação é o stepper e o sumário |
| Página de vídeos | `MOSTRAR_VIDEOS` continua falso |
| Inventar preço, frete ou telefone | Número inventado é o que tira o 10 de UX |
| Novo contato | O guia continua Chen e Cris |

---

## User Stories

### P1: Lista da Cris sem legenda repetida ⭐ MVP

**User Story**: Como lojista, quero achar o catálogo pelo nome, para não ler "catálogo de tênis Nike" embaixo de "Tênis Nike".

**Why P1**: É a página nova e a que mais pesa o design e a intuição.

**Acceptance Criteria**:

1. WHEN a descrição só repete o título THEN o PDF SHALL mostrar a linha sem essa descrição
2. WHEN a lista passar da altura útil THEN o PDF SHALL continuar na página seguinte, com "VER O RESTO DOS CATÁLOGOS" só se existir próxima página
3. WHEN o catálogo for "Tudo" THEN o PDF SHALL manter uma linha curta dizendo quando usá-lo, com o texto decidido no context.md

**Independent Test**: Gerar o PDF e ler as páginas de catálogo da Cris. Nenhuma linha de marca repete o próprio nome na descrição.

---

### P1: Passo com fim claro ⭐ MVP

**User Story**: Como lojista, quero saber quando o passo acabou, para ir à etapa seguinte sem achar que falta um print.

**Why P1**: As páginas de passo são as que parecem inacabadas.

**Acceptance Criteria**:

1. WHEN um passo é desenhado THEN o PDF SHALL fechar o conteúdo com um aviso "Acabou quando" de uma frase
2. WHEN o aviso for desenhado THEN o PDF SHALL usar o cartão escuro que já existe nas notas, sem componente novo
3. WHEN os prints estiverem desligados THEN o PDF SHALL continuar sem imagem de print

**Independent Test**: Abrir os oito passos. Cada um tem o aviso e nenhum mostra quadro de print.

---

### P1: Nada fictício no lugar de regra ⭐ MVP

**User Story**: Como lojista, quero que telefone, frete e pagamento sejam os combinados, para não pagar ou chamar o contato errado.

**Why P1**: É o que impede o 10 de UX. Sem isso, design e intuição altos ainda produzem pedido errado.

**Acceptance Criteria**:

1. WHEN o WhatsApp ainda for o placeholder `90000-0001` ou `90000-0002` THEN o PDF SHALL omitir o botão e o número
2. WHEN o usuário confirmar o número real THEN o PDF SHALL mostrar o botão "CHAMAR NO WHATSAPP" com esse número
3. WHEN frete, adicional ou pagamento da Cris não estiverem confirmados THEN o PDF SHALL omitir esses valores
4. WHEN os valores da Cris forem confirmados THEN o PDF SHALL mostrar só os confirmados
5. WHEN os preços e o frete do Chen já escritos no arquivo forem confirmados THEN o PDF SHALL mantê-los
6. WHEN óculos e bolsas forem outro atendimento THEN o PDF SHALL não mandar esses catálogos para o WhatsApp dos tênis

**Independent Test**: Com os placeholders atuais, buscar `90000-000` no texto do PDF e não achar. Com um número real no arquivo, o botão volta.

---

### P2: Cópia do endereço intacta

**User Story**: Como lojista, quero colar o endereço no WhatsApp do jeito que o fornecedor pediu.

**Why P2**: Já funciona. O plano não pode quebrar isso ao mexer nas páginas.

**Acceptance Criteria**:

1. WHEN o bloco branco do Chen é selecionado THEN o texto copiado SHALL ser `to this address pls`, `name=`, `Street=`, `Country=`, `city=`, `state=`, `zip code=`, `phone=`, `CPF=`, um por linha
2. WHEN o bloco branco da Cris é selecionado THEN o texto copiado SHALL ser `Nome:`, `Endereço:`, `Cidade:`, `Estado:`, `País:`, `CEP:`, `Telefone:`, `CPF:`, `E-mail:`, um por linha
3. WHEN a marca d'água cruza o bloco THEN a seleção SHALL não incluir "TIME INTERNO VESTCAP"

**Independent Test**: Selecionar só o retângulo do bloco branco nas páginas de mensagem e comparar com as strings acima.

---

## Edge Cases

- WHEN a Cris tiver descrição útil numa linha e repetida nas outras THEN o PDF SHALL mostrar a útil e omitir as repetidas
- WHEN todos os catálogos couberem numa página THEN o PDF SHALL não mostrar "VER O RESTO DOS CATÁLOGOS"
- WHEN o passo já termina perto do rodapé THEN o aviso "Acabou quando" SHALL caber acima de "Voltar ao sumário", sem sobrepor o botão de WhatsApp se ele existir
- WHEN só o frete da Cris for confirmado e o pagamento não THEN o PDF SHALL mostrar o frete e omitir o pagamento

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| LISTA-01 | P1: Lista sem legenda repetida | Tasks | Pending |
| LISTA-02 | P1: Lista sem legenda repetida | Tasks | Pending |
| LISTA-03 | P1: Lista sem legenda repetida | Discuss | Pending |
| PASSO-01 | P1: Passo com fim claro | Tasks | Pending |
| PASSO-02 | P1: Passo com fim claro | Tasks | Pending |
| DADO-01 | P1: Nada fictício | Discuss | Pending |
| DADO-02 | P1: Nada fictício | Discuss | Pending |
| DADO-03 | P1: Nada fictício | Discuss | Pending |
| DADO-04 | P1: Nada fictício | Discuss | Pending |
| COPY-01 | P2: Cópia do endereço | Tasks | Pending |

**Coverage:** 10 total, 6 mapped to tasks, 4 unmapped até o context.md ⚠️

---

## Success Criteria

- [ ] Notas-alvo: design 10, intuição 10, UX 10 no mesmo critério do review
- [ ] Lojista percorre Chen e Cris sem encontrar número `90000-000` nem valor de frete não confirmado
- [ ] Os oito passos dizem quando acabaram
- [ ] A seleção do bloco de endereço cola no WhatsApp com as quebras de linha de hoje
