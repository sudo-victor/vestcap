import assert from "node:assert/strict"
import test from "node:test"

import { liberar, type Acesso } from "./acesso"

const acessos: Acesso[] = [
  { id: "ana", codigo: "codigo-da-ana", ativo: true },
  { id: "bia", codigo: "codigo-da-bia", ativo: false },
]

test("código desconhecido não libera", () => {
  assert.equal(liberar("outro", acessos), null)
})

test("código ativo libera só aquela pessoa", () => {
  assert.equal(liberar("codigo-da-ana", acessos), "ana")
})

test("código desligado não libera", () => {
  assert.equal(liberar("codigo-da-bia", acessos), null)
})

test("código vazio não libera", () => {
  assert.equal(liberar("", acessos), null)
  assert.equal(liberar("   ", acessos), null)
})
