import assert from "node:assert/strict"
import test from "node:test"
import React from "react"
import { renderToStaticMarkup } from "react-dom/server"

import { Entrada } from "../app/entrada"
import { Guia, type DadosGuia } from "../app/guia"

const dados: DadosGuia = {
  textos: {
    antes: [["PRAZO", "Vinte dias."]],
    imposto: { link: "https://apps.correios.com.br/portalimportador/", intro: "Vincule o CPF." },
  },
  contatos: [
    {
      nome: "Chen",
      linha: "Camisa",
      whatsapp: "+86 136 9032 3804",
      catalogos: [{ titulo: "Geral", link: "https://chen.example/catalogo" }],
      mensagens: [["PEDIDO", "Copie.", "Camisa torcedor\nTamanho L"]],
    },
  ],
}

test("a entrada não mostra contato nem link", () => {
  const html = renderToStaticMarkup(<Entrada erro={false} action={async () => {}} />)
  assert.equal(html.includes("wa.me"), false)
  assert.equal(html.includes("chen.example"), false)
  assert.equal(html.includes("13690323804"), false)
  assert.equal(html.includes("Código"), true)
  assert.equal(html.includes("VestCap"), true)
  assert.equal(html.includes("#10280A"), true)
  assert.equal(html.includes("aurora-container"), true)
  assert.equal(html.includes("Entrar"), true)
})

test("o guia autenticado tem whatsapp, catálogo e o texto para copiar", () => {
  const html = renderToStaticMarkup(<Guia dados={dados} />)
  assert.equal(html.includes("https://wa.me/8613690323804"), true)
  assert.equal(html.includes("https://chen.example/catalogo"), true)
  assert.equal(html.includes("Camisa torcedor\nTamanho L"), true)
  const cartao = html.indexOf("spotlight-card")
  const link = html.indexOf("chen.example")
  const borda = html.lastIndexOf("spotlight-card")
  const mensagem = html.indexOf("Camisa torcedor")
  assert.ok(cartao !== -1 && cartao < link && link < borda && mensagem > borda)
})
