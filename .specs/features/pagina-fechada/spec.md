# Página fechada Specification

## Problem Statement

O guia precisa abrir no celular, com link e cópia funcionando, e não pode ficar público. O PDF continua existindo. A página tem que subir na Vercel.

## Goals

- [ ] Visitante sem código válido não recebe catálogo, WhatsApp nem mensagem no HTML
- [ ] Cliente com código ativo abre o guia, o catálogo, o WhatsApp e copia a mensagem
- [ ] Desligar o código de uma pessoa trava só essa pessoa na próxima abertura
- [ ] O projeto sobe na Vercel com Next.js

## Out of Scope

| Feature | Reason |
| --- | --- |
| Servidor Python contínuo | A Vercel não hospeda o `http.server` que ficou para trás |
| Impedir print | Fora do projeto |
| Painel visual de códigos | A lista vive na variável de ambiente, neste marco |
| Cobrança automática | Fora do projeto |
| Página de vídeos | `MOSTRAR_VIDEOS` segue falso |

---

## User Stories

### P1: Entrar com código ⭐ MVP

**User Story**: Como lojista, quero entrar com o meu código, para ver o guia sem que outra pessoa abra o mesmo endereço.

**Why P1**: Sem isso a página não pode ir ao ar.

**Acceptance Criteria**:

1. WHEN o código não existe ou está vazio THEN a resposta SHALL ser só a tela de entrada, sem número de WhatsApp e sem URL de catálogo
2. WHEN o código está ativo THEN a resposta SHALL gravar a sessão daquela pessoa e mostrar o guia
3. WHEN o código foi desligado THEN a sessão antiga SHALL deixar de ver o guia
4. WHEN o código de outra pessoa é usado THEN a sessão SHALL identificar só essa outra pessoa

**Independent Test**: Teste de `liberar` e um GET da página sem cookie. O HTML não contém os telefones nem os links dos catálogos.

---

### P1: Guia no celular ⭐ MVP

**User Story**: Como lojista, quero o roteiro do PDF na página, para pedir pelo navegador.

**Why P1**: É o que substitui o uso do PDF no celular.

**Acceptance Criteria**:

1. WHEN a pessoa está autenticada THEN a página SHALL mostrar os contatos, os catálogos, o frete, os passos, as mensagens e o checklist que estão em `gerar_guia.py`
2. WHEN a pessoa toca em copiar THEN o texto da mensagem SHALL ir inteiro para a área de transferência, com as quebras de linha
3. WHEN a pessoa toca no catálogo ou no WhatsApp THEN o link SHALL ser `https` (`wa.me` no WhatsApp)

**Independent Test**: Entrar com um código de teste e ver Chen e Cris, um botão Copiar e um `wa.me`.

---

## Edge Cases

- WHEN `VESTCAP_ACESSOS` está vazio ou inválido THEN ninguém SHALL entrar e a tela de entrada SHALL continuar sem contatos
- WHEN `VESTCAP_SEGREDO` falta THEN a sessão SHALL não ser aceita
- WHEN dois códigos ativos existem THEN desligar um SHALL manter o outro

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| ACESSO-01 | P1: Entrar com código | Tasks | Pending |
| ACESSO-02 | P1: Entrar com código | Tasks | Pending |
| ACESSO-03 | P1: Entrar com código | Tasks | Pending |
| GUIA-01 | P1: Guia no celular | Tasks | Pending |
| GUIA-02 | P1: Guia no celular | Tasks | Pending |

**Coverage:** 5 total, 5 mapped to tasks

---

## Success Criteria

- [ ] `npx next build` dentro de `web/` termina sem erro
- [ ] A pasta `web/` é um projeto Next.js que a Vercel aceita como raiz
- [ ] Teste automatizado cobre código errado, código ativo e código desligado
