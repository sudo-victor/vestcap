import { cookies } from "next/headers"

import { lerGuia } from "../lib/dados"
import { lerAcessos, abrir } from "../lib/sessao"
import { entrar } from "./acoes"
import { Entrada } from "./entrada"
import { Guia } from "./guia"

export const dynamic = "force-dynamic"

export default async function Pagina({
  searchParams,
}: {
  searchParams: Promise<{ erro?: string }>
}) {
  const jar = await cookies()
  const pessoa = abrir(
    jar.get("vestcap")?.value,
    lerAcessos(),
    process.env.VESTCAP_SEGREDO || "",
  )
  if (!pessoa) {
    const params = await searchParams
    return <Entrada erro={params.erro === "1"} action={entrar} />
  }
  return <Guia dados={lerGuia()} />
}
