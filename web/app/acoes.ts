"use server"

import { cookies } from "next/headers"
import { redirect } from "next/navigation"

import { liberar } from "../lib/acesso"
import { assinar, lerAcessos } from "../lib/sessao"

export async function entrar(formData: FormData) {
  const segredo = process.env.VESTCAP_SEGREDO || ""
  const id = segredo ? liberar(String(formData.get("codigo") || ""), lerAcessos()) : null
  if (!id) redirect("/?erro=1")
  const jar = await cookies()
  jar.set("vestcap", assinar(id, segredo), {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
  })
  redirect("/")
}
