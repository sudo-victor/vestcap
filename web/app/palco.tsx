"use client"

import { useEffect, useState, type ReactNode } from "react"

import Aurora from "@/components/Aurora"
import ShinyText from "@/components/ShinyText"
import { cena } from "@/lib/cena"

export function useMovimentoReduzido() {
  const [reduzir, setReduzir] = useState(false)
  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)")
    const aplicar = () => setReduzir(media.matches)
    aplicar()
    media.addEventListener("change", aplicar)
    return () => media.removeEventListener("change", aplicar)
  }, [])
  return reduzir
}

export function Palco({
  children,
  reduzirMovimento,
}: {
  children: ReactNode
  reduzirMovimento?: boolean
}) {
  const sistema = useMovimentoReduzido()
  const visual = cena(reduzirMovimento ?? sistema)
  return (
    <div className="palco" style={{ background: visual.fundo }}>
      <Aurora
        className="palco-seda"
        colorStops={[visual.fundo, visual.seda.color, visual.seda.sheenColor]}
        paused={visual.seda.paused}
        amplitude={1.25}
        blend={0.55}
        speed={0.85}
      />
      <div className="palco-velo" />
      <div className="palco-grade" aria-hidden="true" />
      <div className="palco-conteudo">
        <header className="palco-topo">
          <span className="palco-marca">VESTCAP</span>
          <span className="palco-edicao">ARQUIVO 01 · USO INTERNO</span>
        </header>

        <div className="palco-miolo">
          <div className="palco-carimbo-linha">
            <p className="kicker">acesso restrito</p>
            <span className="carimbo">CONFIDENCIAL</span>
          </div>

          <h1 className="palco-titulo">
            <span className="palco-palavra">ACESSO</span>
            <span className="palco-destaque">RESTRITO</span>
            <span className="palco-submarca">
              <ShinyText text="VestCap" {...visual.titulo} />
            </span>
          </h1>

          <p className="palco-lead">
            Os contatos que a gente usa pra comprar. Não estão em site nem em post. Ficam só aqui.
          </p>

          <div className="palco-tags" aria-hidden="true">
            <span>CAMISA DE TIME</span>
            <i />
            <span>TÊNIS</span>
            <i />
            <span>ÓCULOS E BOLSAS</span>
          </div>

          <div className="palco-cofre">{children}</div>
        </div>

        <footer className="palco-rodape">
          <div>
            <span>ARQUIVO</span>
            <strong>Contatos e catálogos</strong>
          </div>
          <div>
            <span>ACESSO</span>
            <strong>Só quem recebeu</strong>
          </div>
          <div>
            <span>REGRA</span>
            <strong>Não encaminhar</strong>
          </div>
        </footer>
      </div>
    </div>
  )
}
