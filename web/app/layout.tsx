import type { Metadata } from "next"
import "../components/Aurora.css"
import "../components/GlareHover.css"
import "../components/ShinyText.css"
import "../components/SpotlightCard.css"
import "./globals.css"

export const metadata: Metadata = {
  title: "VestCap",
  description: "Guia interno",
}

export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  )
}
