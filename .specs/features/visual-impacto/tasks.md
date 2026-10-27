# Visual de impacto Tasks

**Design**: `.specs/features/visual-impacto/design.md`
**Status**: Complete

---

## Execution Plan

### Phase 1

T1 → T2 → T3 → T4

### Phase 2

T4 → T5 → T6 → T7

---

## Task Breakdown

### T1: Registro do React Bits sem Tailwind

**What**: `components.json` em `web/` com o registro `@react-bits` e alias para `web/components`, sem migrar o CSS do app para Tailwind
**Where**: `web/components.json`
**Depends on**: None
**Reuses**: o CSS atual em `web/app/globals.css`
**Requirement**: VIS-01

**Done when**:

- [x] O registro aponta para `https://reactbits.dev/r/{name}.json`
- [x] O app continua compilando com o CSS de hoje

**Verify**: `npx next build` em `web/` passa depois do arquivo existir.

---

### T2: Instalar Silk e ShinyText

**What**: Trazer os arquivos TS-CSS dos dois componentes para `web/components`
**Where**: `web/components/Silk.tsx`, `web/components/ShinyText.tsx` e os CSS ao lado
**Depends on**: T1
**Reuses**: os registros conferidos, ambos com `dependencies: []`
**Requirement**: VIS-01, VIS-02

**Done when**:

- [x] Os arquivos existem e o import usa `"use client"` que já vem neles
- [x] `package.json` não ganhou `three`, `gsap`, `ogl` nem `motion`

**Verify**: `npx shadcn@latest add @react-bits/Silk-TS-CSS` e o mesmo para `ShinyText-TS-CSS`. Se o CLI pedir um pacote que o registro não listou, parar.

---

### T3: Palco na entrada

**What**: `Palco` com Silk e ShinyText, e a `Entrada` renderizando o formulário dentro dele
**Where**: `web/app/palco.tsx`, `web/app/movimento.tsx`, `web/app/entrada.tsx`, `web/app/globals.css`
**Depends on**: T2
**Reuses**: o formulário e a action atuais
**Requirement**: VIS-01, VIS-02, VIS-03, VIS-04

**Done when**:

- [x] A entrada ocupa a altura da janela no fundo `#10280A`
- [x] O título usa ShinyText nas cores da marca
- [x] Menos movimento deixa Silk `paused` e ShinyText `disabled`
- [x] O teste de HTML da entrada continua sem `wa.me`, sem catálogo e sem número

**Verify**: `npm test` em `web/` e uma olhada no navegador em `/` sem cookie.

---

### T4: Instalar SpotlightCard

**What**: Trazer o SpotlightCard TS-CSS
**Where**: `web/components/SpotlightCard.tsx` e o CSS ao lado
**Depends on**: T1
**Reuses**: o registro conferido, `dependencies: []`
**Requirement**: VIS-05

**Done when**:

- [x] O componente está em `web/components`
- [x] Nenhuma dependência nova de animação entrou no `package.json`

**Verify**: o arquivo existe e `npm test` segue passando.

---

### T5: Cartão só no catálogo

**What**: Envolver o `<article>` de cada catálogo com SpotlightCard claro e luz lima
**Where**: `web/app/guia.tsx`
**Depends on**: T4
**Reuses**: os dados que o guia já recebe por props
**Requirement**: VIS-05, VIS-06

**Done when**:

- [x] Catálogo usa `theme="light"` e `spotlightColor="#DCFF00"`
- [x] Tabela, passo, checklist e `<pre>` ficam fora do cartão
- [x] O teste do guia autenticado continua achando `https://wa.me/` e o texto da mensagem com quebra de linha

**Verify**: `npm test` em `web/`.

---

### T6: Fundo legível sem WebGL

**What**: A área do palco tem fundo `#10280A` no CSS, então a falta de WebGL2 não esconde o formulário
**Where**: `web/app/globals.css`, `web/app/palco.tsx`
**Depends on**: T3
**Reuses**: a cor já usada no PDF
**Requirement**: VIS-03

**Done when**:

- [x] O container do palco pinta `#10280A` mesmo antes do canvas
- [x] O campo e o botão ficam acima do canvas

**Verify**: inspeção do CSS e da ordem no DOM.

---

### T7: Build e celular

**What**: Conferir o build de produção e o fluxo no navegador, na largura de celular e na largura de mesa
**Where**: `web/`
**Depends on**: T3, T5, T6
**Reuses**: o teste de entrada e o teste do guia
**Requirement**: VIS-01, VIS-05, VIS-06

**Done when**:

- [x] `npx next build` passa
- [x] Sem cookie, a porta aparece e o código errado ainda mostra "Código não entra."
- [x] Com código ativo, o cartão do catálogo aparece e a mensagem continua selecionável
- [x] A largura estreita não corta o campo de código

**Verify**: build mais o fluxo no navegador.

---

## Parallel Execution Map

```
T1 ──→ T2 ──→ T3 ──→ T6 ──→ T7
T1 ──→ T4 ──→ T5 ──────────→ T7
```

T2 e T4 podem andar juntos depois de T1. T3 e T5 podem andar juntos depois que cada instalação existir.

---

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1: registro | 1 arquivo | Granular |
| T2: Silk e ShinyText | 1 instalação | Granular |
| T3: palco | 1 componente | Granular |
| T4: SpotlightCard | 1 instalação | Granular |
| T5: cartão no guia | 1 arquivo | Granular |
| T6: fallback | 1 ajuste de CSS | Granular |
| T7: verificação | 1 passagem | Granular |

---

## Diagrams

- Arquitetura no `design.md`. `mermaid-studio` não está instalado. O mermaid desse arquivo é o fonte.

---

## Checkpoint

Sete tarefas. Fase 1 entrega a porta. Fase 2 entrega o cartão e a verificação. Nenhuma tarefa pede pacote de animação além dos arquivos do React Bits já conferidos.
