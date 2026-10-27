# Roadmap

**Current Milestone:** Visual da página
**Status:** Built, waiting on Vercel env

---

## Guia em PDF

**Goal:** O arquivo que já existe continua saindo de `gerar_guia.py`.
**Target:** Já em uso. O refino visual do spec `guia-10` fica parado até a página fechada existir.

### Features

**PDF do lojista** - COMPLETE

- Sumário, Chen, Cris, tamanhos, mensagens copiáveis e checklist
- Links `https://wa.me/` e links de catálogo

**Refino para nota 10** - PLANNED

- Spec em `.specs/features/guia-10/`
- Não bloqueia a página

---

## Página fechada

**Goal:** Um cliente entra com o próprio código no celular, usa o guia e, se o código for apagado, deixa de entrar.
**Target:** O primeiro cliente que não seja a VestCap consegue pedir pelo celular sem abrir o PDF.

### Features

**Entrar com código** - COMPLETE

- A página pede o código antes de mostrar qualquer contato
- Código errado ou apagado não revela catálogo, número nem mensagem
- Cada cliente tem o seu código

**Guia no celular** - COMPLETE

- O mesmo roteiro do PDF: antes de comprar, Chen, Cris, tamanhos, passos, mensagens e checklist
- Abrir catálogo e WhatsApp funciona no navegador do celular
- Copiar a mensagem leva o texto inteiro, com as quebras de linha

**Cortar um acesso** - COMPLETE

- Apagar ou desligar um código trava só aquela pessoa
- Os outros códigos continuam válidos

---

## Visual da página

**Goal:** Quem abre o link no celular vê a marca antes de digitar o código, e o pedido continua fácil de ler.
**Target:** A entrada impressiona e o guia autenticado não perde cópia, catálogo nem WhatsApp.

### Features

**Porta de entrada** - COMPLETE

- Fundo Aurora no verde da marca e título VestCap com brilho lima
- Formulário por cima, na altura da janela
- Menos movimento deixa o fundo parado
- Spec em `.specs/features/visual-impacto/`

**Catálogo com luz** - COMPLETE

- Cada catálogo em SpotlightCard claro
- Tabela, passo e mensagem permanecem estáticos

---

## Operação

**Goal:** A VestCap atualiza contatos e acessos sem gerar um arquivo novo para cada cliente.
**Target:** Mudar um link ou desligar uma pessoa reflete na próxima vez que ela abre a página.

### Features

**Uma fonte só** - PLANNED

- Editar o dado do contato atualiza o PDF e a página
- A página não mantém uma cópia solta dos números e dos links

**Códigos sem mexer no código-fonte** - PLANNED

- Criar e apagar acessos por uma lista simples, fora do texto do guia

---

## Future Considerations

- Cobrança que libera o código sozinha
- Vídeos dentro do guia, se `MOSTRAR_VIDEOS` voltar
- Aviso quando um código é usado em muitos aparelhos ao mesmo tempo
