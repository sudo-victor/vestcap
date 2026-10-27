# State

**Last Updated:** 2026-10-26
**Current Work:** Visual da página implementado em `web/`. A publicação na Vercel continua pendente.

---

## Recent Decisions (Last 60 days)

### AD-001: A página é o uso no celular; o PDF fica como arquivo (2026-10-26)

**Decision:** O cliente usa uma página. O PDF continua sendo gerado para quem quiser guardar.
**Reason:** Link e cópia falham no leitor de PDF do WhatsApp.
**Trade-off:** Dois destinos para o mesmo conteúdo. Os dois têm que nascer do mesmo dado.
**Impact:** O primeiro marco entrega a página. Não substitui `gerar_guia.py`.

### AD-002: Acesso é um código por cliente (2026-10-26)

**Decision:** Cada pessoa entra com um código só dela. Dá para apagar um sem afetar os outros.
**Reason:** Senha única e link secreto vazam no primeiro encaminhamento e não têm como desligar uma pessoa só.
**Trade-off:** Alguém precisa criar e apagar códigos. Não é automático.
**Impact:** A página não envia contatos antes da checagem. Print depois de entrar fica fora de escopo.

### AD-003: A página sobe na Vercel com Next.js (2026-10-26)

**Decision:** O app é Next.js 16 na pasta `web/`. A Vercel usa essa pasta como raiz. A checagem do código é no servidor.
**Reason:** A Vercel publica esse tipo de app sem um processo permanente. O `http.server` em Python não sobe lá.
**Trade-off:** Desligar um código pede atualizar `VESTCAP_ACESSOS` e publicar de novo. Não há banco neste marco.
**Impact:** B-001 fechado. O PDF segue em Python, local.

### AD-004: O impacto visual fica na porta; o guia continua em papel (2026-10-26)

**Decision:** A entrada é tela cheia no verde `#10280A`, com Silk e ShinyText do React Bits gratuito, variante TypeScript + CSS. O miolo do guia fica no creme `#FBF6E4`. Só o catálogo ganha SpotlightCard. Tabela, passo e mensagem ficam parados.
**Reason:** A primeira vista precisa impressionar. O pedido precisa ser lido e copiado.
**Trade-off:** O guia autenticado não vira uma página inteira de efeito. React Bits Pro, Tailwind e fundos 3D ficam de fora.
**Impact:** Spec, design e tarefas em `.specs/features/visual-impacto/`. Os componentes foram conferidos no registro com `dependencies: []`.

### AD-005: A porta usa Aurora porque o shader do Silk não compilou (2026-10-26)

**Decision:** O fundo da entrada é o Aurora do React Bits, com as cores `#10280A`, `#145C38` e `#DCFF00`. O título continua no ShinyText. O arquivo do Silk ficou instalado e fora da tela.
**Reason:** Neste navegador o shader do Silk não liga. A tela ficava sem tecido e o texto sumia.
**Trade-off:** A entrada não é a seda prevista. O Aurora é a reserva que o design já tinha.
**Impact:** `web/app/palco.tsx` monta o Aurora. Um véu escuro mantém o formulário legível.

---

## Active Blockers

Nenhum. B-001 fechou com a escolha do Next.js na Vercel.

---

## Lessons Learned

### L-001: Link de PDF no WhatsApp não é destino confiável

**Context:** O guia é enviado e aberto na conversa.
**Problem:** O visor do WhatsApp muitas vezes não segue link nenhum. O sumário quebra mais do que o link de fora.
**Solution:** A página no navegador é o lugar do pedido. O PDF fica como arquivo.
**Prevents:** Tratar o PDF como o único canal do celular.

---

## Quick Tasks Completed

| # | Description | Date | Commit | Status |
| --- | --- | --- | --- | --- |
| — | Nenhum registro ainda | — | — | — |

---

## Deferred Ideas

- [ ] Cobrança que libera o código sozinha — Captured during: plano da página
- [ ] Aviso de um código usado em muitos aparelhos — Captured during: plano da página
- [ ] Refino visual do PDF (`.specs/features/guia-10/`) — Captured during: review do PDF

---

## Todos

- [ ] Publicar `web/` na Vercel com `VESTCAP_SEGREDO` e `VESTCAP_ACESSOS`
- [ ] Rodar `python3 exportar_dados.py` sempre que o conteúdo do PDF mudar
