import { createHmac, timingSafeEqual } from "node:crypto"

import { type Acesso } from "./acesso"

const TRINTA_DIAS = 1000 * 60 * 60 * 24 * 30

export function lerAcessos(): Acesso[] {
  const bruto = process.env.VESTCAP_ACESSOS
  if (!bruto) return []
  try {
    const lista = JSON.parse(bruto) as Acesso[]
    return Array.isArray(lista) ? lista : []
  } catch {
    return []
  }
}

export function assinar(id: string, segredo: string, agora = Date.now()): string {
  const exp = String(agora + TRINTA_DIAS)
  const corpo = `${id}.${exp}`
  const sig = createHmac("sha256", segredo).update(corpo).digest("hex")
  return `${corpo}.${sig}`
}

export function abrir(token: string | undefined, acessos: Acesso[], segredo: string, agora = Date.now()): string | null {
  if (!token || !segredo) return null
  const partes = token.split(".")
  if (partes.length !== 3) return null
  const [id, exp, sig] = partes
  const esperado = createHmac("sha256", segredo).update(`${id}.${exp}`).digest("hex")
  const recebido = Buffer.from(sig)
  const oficial = Buffer.from(esperado)
  if (recebido.length !== oficial.length || !timingSafeEqual(recebido, oficial)) return null
  if (Number(exp) < agora) return null
  const acesso = acessos.find((item) => item.id === id && item.ativo)
  return acesso ? acesso.id : null
}
