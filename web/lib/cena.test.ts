import assert from "node:assert/strict"
import test from "node:test"

import { cena } from "./cena"

test("a porta usa o verde da marca e para quando o movimento é reduzido", () => {
  const parada = cena(true)
  assert.equal(parada.fundo, "#10280A")
  assert.deepEqual(parada.seda, { color: "#145C38", sheenColor: "#DCFF00", paused: true })
  assert.deepEqual(parada.titulo, { color: "#DCFF00", shineColor: "#FBF6E4", disabled: true })
})

test("com movimento, a seda e o título seguem vivos", () => {
  const viva = cena(false)
  assert.equal(viva.seda.paused, false)
  assert.equal(viva.titulo.disabled, false)
})
