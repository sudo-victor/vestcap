import assert from "node:assert/strict"
import test from "node:test"

import { type Acesso } from "./acesso"
import { abrir, assinar } from "./sessao"

const segredo = "segredo-de-teste"
const acessos: Acesso[] = [
  { id: "ana", codigo: "codigo-da-ana", ativo: true },
  { id: "bia", codigo: "codigo-da-bia", ativo: false },
]

test("cookie assinado reconhece quem entrou", () => {
  const token = assinar("ana", segredo, 1_000)
  assert.equal(abrir(token, acessos, segredo, 1_000), "ana")
})

test("código desligado derruba a sessão", () => {
  const token = assinar("bia", segredo, 1_000)
  assert.equal(abrir(token, acessos, segredo, 1_000), null)
})

test("sem segredo a sessão não vale", () => {
  const token = assinar("ana", segredo, 1_000)
  assert.equal(abrir(token, acessos, "", 1_000), null)
})
