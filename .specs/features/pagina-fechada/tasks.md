# Página fechada Tasks

**Design**: `.specs/features/pagina-fechada/design.md`
**Status**: Complete

---

## Execution Plan

### Phase 1

T1 → T2 → T3 → T4

### Phase 2

T5

---

## Task Breakdown

### T1: Regra de acesso em TypeScript

**What**: `liberar` em `web/lib/acesso.ts`, com o mesmo comportamento do teste Python
**Where**: `web/lib/acesso.ts`, `web/lib/acesso.test.ts`
**Depends on**: None
**Reuses**: `acesso.py`
**Requirement**: ACESSO-01, ACESSO-03, ACESSO-04

**Done when**:

- [x] Código vazio, desconhecido e desligado não liberam
- [x] Código ativo devolve o id daquela pessoa
- [x] `node --experimental-strip-types --test web/lib/acesso.test.ts` passa

**Verify**: o comando acima termina com pass.

---

### T2: Exportar o dado do PDF

**What**: `exportar_dados.py` grava `web/dados/guia.json` a partir de `gerar_guia.py`
**Where**: `exportar_dados.py`, `web/dados/guia.json`
**Depends on**: None
**Reuses**: `CONTATOS`, `TEXTOS`
**Requirement**: GUIA-01

**Done when**:

- [x] O JSON contém os contatos e os textos
- [x] Não é importado por componente de cliente

**Verify**: `python3 exportar_dados.py` e o arquivo existe com a chave `contatos`.

---

### T3: Tela de entrada sem contatos

**What**: `app/page.tsx` sem sessão mostra só o formulário
**Where**: `web/app/page.tsx`, `web/lib/sessao.ts`
**Depends on**: T1, T2
**Reuses**: cores do guia
**Requirement**: ACESSO-01, ACESSO-02

**Done when**:

- [x] HTML sem cookie não contém `wa.me` nem os links dos catálogos
- [x] Código ativo grava cookie e a próxima leitura reconhece a pessoa
- [x] Código desligado não grava sessão

**Verify**: teste de `liberar` mais uma checagem do HTML de entrada.

---

### T4: Guia autenticado

**What**: Com sessão válida, a página lista contatos, links, WhatsApp e botão Copiar
**Where**: `web/app/guia.tsx`, `web/app/copiar.tsx`
**Depends on**: T3
**Reuses**: `dados/guia.json`
**Requirement**: GUIA-01, GUIA-02

**Done when**:

- [x] Há link `https://wa.me/` e link de catálogo só nessa renderização
- [x] O botão Copiar recebe o texto da mensagem com quebras de linha
- [x] `npx next build` em `web/` passa

**Verify**: `npx next build` e inspeção do componente do guia.

---

### T5: Aposentar o servidor Python

**What**: Remover `acesso.py` e `test_acesso.py` para não parecer que o app é o `http.server`
**Where**: raiz do repositório
**Depends on**: T1
**Reuses**: nada
**Requirement**: ACESSO-01

**Done when**:

- [x] Não existe módulo Python de servidor ou de sessão
- [x] O teste que resta é o TypeScript

**Verify**: `ls acesso.py` falha e o teste em `web/lib` passa.

---

## Parallel Execution Map

```
T1 ──→ T3 ──→ T4
T2 ──→ T3
T1 ──→ T5
```

---

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1: liberar | 1 função | Granular |
| T2: exportar JSON | 1 script | Granular |
| T3: entrada | 1 página | Granular |
| T4: guia | 1 render | Granular |
| T5: remover Python | 1 limpeza | Granular |
