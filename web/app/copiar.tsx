"use client"

import { useState } from "react"

export function Copiar({ texto }: { texto: string }) {
  const [copiado, setCopiado] = useState(false)

  async function acionar() {
    try {
      await navigator.clipboard.writeText(texto)
      setCopiado(true)
      window.setTimeout(() => setCopiado(false), 1800)
    } catch {
      setCopiado(false)
    }
  }

  return (
    <button
      type="button"
      className={`copiar${copiado ? " copiar-ok" : ""}`}
      onClick={acionar}
    >
      {copiado ? "✓ Copiado para colar no WhatsApp" : "Copiar mensagem pronta"}
    </button>
  )
}
