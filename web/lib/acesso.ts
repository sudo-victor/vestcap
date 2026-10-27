export type Acesso = {
  id: string
  codigo: string
  ativo: boolean
}

export function liberar(codigo: string | null | undefined, acessos: Acesso[]): string | null {
  const informado = (codigo ?? "").trim()
  if (!informado) return null
  for (const acesso of acessos) {
    if (!acesso.ativo) continue
    if (informado === acesso.codigo) return acesso.id
  }
  return null
}
