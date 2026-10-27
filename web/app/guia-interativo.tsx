"use client"

import { useEffect, useState } from "react"

import SpotlightCard from "@/components/SpotlightCard"
import { Copiar } from "./copiar"
import { type DadosGuia, type Passo } from "./guia"

function wa(numero: string) {
  return "https://wa.me/" + numero.replace(/\D/g, "")
}

function passoDe(passo: Passo | [string, string, string?]): Passo {
  if (Array.isArray(passo)) return { titulo: passo[0], texto: passo[1] }
  return passo
}

function classificarCatalogo(titulo: string): "tenis" | "acessorios" | "geral" {
  const t = titulo.toLowerCase()
  if (t.includes("tênis") || t.includes("tenis")) return "tenis"
  if (t.includes("óculos") || t.includes("oculos") || t.includes("bolsa")) return "acessorios"
  return "geral"
}

type ItemSumario = {
  id: string
  rotulo: string
  nivel: 1 | 2
}

export function GuiaInterativo({ dados }: { dados: DadosGuia }) {
  const [secaoAtiva, setSecaoAtiva] = useState<string>("antes")
  const [abaMedida, setAbaMedida] = useState<number>(0)
  const [filtroCris, setFiltroCris] = useState<"todos" | "tenis" | "acessorios">("todos")
  const [marcados, setMarcados] = useState<Record<string, boolean>>({})
  const [menuAberto, setMenuAberto] = useState<boolean>(false)

  const sumario: ItemSumario[] = [
    { id: "antes", rotulo: "1. Antes de comprar", nivel: 1 },
    { id: "conversao", rotulo: "Conversão de tamanhos", nivel: 2 },
    { id: "imposto", rotulo: "2. Como pagar menos imposto", nivel: 1 },
    { id: "regra-cpf", rotulo: "Atenção: Regra do CPF", nivel: 2 },
    ...dados.contatos.flatMap((c, idx): ItemSumario[] => {
      const id = c.key || String(idx)
      const numero = idx + 3
      const itens: ItemSumario[] = [
        { id: `contato-${id}`, rotulo: `${numero}. ${c.nome} — ${c.linha}`, nivel: 1 },
        { id: `cat-${id}`, rotulo: `Catálogos (${c.catalogos.length})`, nivel: 2 },
      ]
      if (c.medidas?.length) {
        itens.push({ id: `med-${id}`, rotulo: "Tabela de medidas (cm)", nivel: 2 })
      }
      if (c.frete?.length || c.adicionais?.length || c.pagamento) {
        itens.push({ id: `frete-${id}`, rotulo: "Frete e pagamento", nivel: 2 })
      }
      if (c.passos?.length) {
        itens.push({ id: `passos-${id}`, rotulo: "Passo a passo", nivel: 2 })
      }
      if (c.mensagens?.length) {
        itens.push({ id: `msg-${id}`, rotulo: "Mensagens prontas", nivel: 2 })
      }
      if (c.checklist?.length) {
        itens.push({ id: `check-${id}`, rotulo: "Checklist do pedido", nivel: 2 })
      }
      return itens
    }),
  ]

  useEffect(() => {
    const ids = sumario.map((item) => item.id)
    const observar = () => {
      let atual = ids[0]
      for (const id of ids) {
        const el = document.getElementById(id)
        if (!el) continue
        const rect = el.getBoundingClientRect()
        if (rect.top <= 150) {
          atual = id
        }
      }
      setSecaoAtiva(atual)
    }
    window.addEventListener("scroll", observar, { passive: true })
    observar()
    return () => window.removeEventListener("scroll", observar)
  }, [])

  function alternarCheck(chave: string) {
    setMarcados((atual) => ({ ...atual, [chave]: !atual[chave] }))
  }

  function irPara(id: string) {
    setSecaoAtiva(id)
    setMenuAberto(false)
    const el = document.getElementById(id)
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }

  const todasMedidas =
    dados.contatos
      .find((c) => c.medidas?.length)
      ?.medidas?.flatMap((pagina) => pagina) ?? []

  return (
    <div className="docs-layout">
      {/* Barra superior compacta */}
      <header className="docs-topbar">
        <div className="docs-topbar-esq">
          <button
            type="button"
            className="docs-menu-toggle"
            onClick={() => setMenuAberto((v) => !v)}
            aria-label="Abrir estrutura do documento"
          >
            ☰ Sumário
          </button>
          <span className="guia-dot" />
          <span className="guia-brand">VESTCAP</span>
          <span className="guia-sep">/</span>
          <span className="docs-doc-title">Guia Oficial do Lojista</span>
        </div>

        <div className="docs-topbar-dir">
          {dados.contatos.map((c) => (
            <a
              key={c.nome}
              href={wa(c.whatsapp)}
              target="_blank"
              rel="noreferrer"
              className="docs-whats-chip"
            >
              <span>WhatsApp {c.nome}</span>
              <i>↗</i>
            </a>
          ))}
          <span className="carimbo carimbo-top">USO INTERNO</span>
        </div>
      </header>

      {/* Barra rápida no celular para pular direto sem abrir gaveta */}
      <nav className="mobile-quickbar" aria-label="Pular para seção">
        <a
          href="#antes"
          onClick={(e) => {
            e.preventDefault()
            irPara("antes")
          }}
          className={
            secaoAtiva === "antes" || secaoAtiva === "conversao" ? "quick-ativo" : ""
          }
        >
          1. Regras
        </a>
        <a
          href="#imposto"
          onClick={(e) => {
            e.preventDefault()
            irPara("imposto")
          }}
          className={
            secaoAtiva === "imposto" || secaoAtiva === "regra-cpf" ? "quick-ativo" : ""
          }
        >
          2. Imposto
        </a>
        {dados.contatos.map((c, idx) => {
          const id = c.key || String(idx)
          const ativo = secaoAtiva.endsWith(`-${id}`)
          return (
            <a
              key={c.nome}
              href={`#contato-${id}`}
              onClick={(e) => {
                e.preventDefault()
                irPara(`contato-${id}`)
              }}
              className={ativo ? "quick-ativo" : ""}
            >
              {idx + 3}. {c.nome}
            </a>
          )
        })}
      </nav>

      {menuAberto ? (
        <div
          className="docs-backdrop"
          onClick={() => setMenuAberto(false)}
          aria-hidden="true"
        />
      ) : null}

      <div className="docs-corpo">
        {/* Sidebar estilo Google Docs */}
        <aside
          className={`docs-sidebar${menuAberto ? " docs-sidebar-aberta" : ""}`}
          aria-label="Estrutura do documento"
        >
          <div className="docs-sidebar-inner">
            <div>
              <div className="docs-sidebar-head">
                <span>ESTRUTURA DO GUIA</span>
                <button
                  type="button"
                  className="docs-fechar-mobile"
                  onClick={() => setMenuAberto(false)}
                  aria-label="Fechar sumário"
                >
                  ✕ Fechar
                </button>
              </div>

              <nav className="docs-outline">
                {sumario.map((item) => {
                  const ativo = secaoAtiva === item.id
                  return (
                    <a
                      key={item.id}
                      href={`#${item.id}`}
                      onClick={(e) => {
                        e.preventDefault()
                        irPara(item.id)
                      }}
                      className={`docs-link docs-nivel-${item.nivel}${ativo ? " docs-link-ativo" : ""}`}
                    >
                      <span className="docs-link-barra" />
                      <span className="docs-link-texto">{item.rotulo}</span>
                    </a>
                  )
                })}
              </nav>
            </div>

            <div className="docs-sidebar-foot">
              <span>ATALHO DIRETO</span>
              {dados.contatos.map((c) => (
                <a
                  key={c.nome}
                  href={wa(c.whatsapp)}
                  target="_blank"
                  rel="noreferrer"
                  className="docs-sidebar-wa"
                >
                  <div>
                    <strong>{c.nome}</strong>
                    <small>{c.linha}</small>
                  </div>
                  <span>WhatsApp ↗</span>
                </a>
              ))}
            </div>
          </div>
        </aside>

        {/* Folha do documento */}
        <main className="docs-folha-wrap">
          <div className="folha">
            <div className="doc-capa-cabecalho">
              <p className="kicker">fornecedores oficiais & roteiro de pedido</p>
              <h1 className="doc-titulo-principal">VestCap — Guia do Lojista</h1>
              <p className="doc-subtitulo">
                Leia o <strong>Antes de comprar</strong> uma vez e siga as etapas numeradas de cada
                fornecedor na hora de fechar o pedido.
              </p>
            </div>

            {/* ================= 1. ANTES DE COMPRAR ================= */}
            <section id="antes" className="bloco-secao">
              <div className="secao-cabecalho">
                <span className="secao-tag">SEÇÃO 01 · LEIA PRIMEIRO</span>
                <h2>Antes de comprar</h2>
                <p className="secao-desc">
                  Quatro regras rápidas sobre prazo, dólar, alfândega e garantia com os
                  fornecedores.
                </p>
              </div>

              <ol className="grade-antes">
                {dados.textos.antes.map(([titulo, texto], i) => (
                  <li key={titulo} className="card-antes">
                    <span className="card-antes-num">0{i + 1}</span>
                    <div>
                      <strong>{titulo}</strong>
                      <p>{texto}</p>
                    </div>
                  </li>
                ))}
              </ol>

              {dados.textos.tamanhos?.length ? (
                <div id="conversao" className="quadro-tamanhos">
                  <div className="quadro-tamanhos-topo">
                    <div>
                      <span className="secao-tag secao-tag-lima">CONVERSÃO RÁPIDA DE ETIQUETA</span>
                      <h3>Tamanho no Brasil → Como escrever na mensagem</h3>
                    </div>
                  </div>
                  <div className="tamanhos-chips">
                    {dados.textos.tamanhos.map(([br, intl]) => (
                      <div key={br} className="tamanho-chip">
                        <div className="chip-col">
                          <small>BRASIL</small>
                          <span>{br}</span>
                        </div>
                        <i>→</i>
                        <div className="chip-col chip-col-destaque">
                          <small>ESCREVA</small>
                          <strong>{intl}</strong>
                        </div>
                      </div>
                    ))}
                  </div>
                  {dados.textos.tamanhos_texto ? (
                    <p className="tamanhos-obs">{dados.textos.tamanhos_texto}</p>
                  ) : null}
                </div>
              ) : null}
            </section>

            {/* ================= 2. IMPOSTO ================= */}
            <section id="imposto" className="bloco-secao">
              <div className="secao-cabecalho">
                <span className="secao-tag">SEÇÃO 02 · ALFÂNDEGA E CORREIOS</span>
                <h2>Como pagar menos imposto</h2>
                <p className="secao-desc">{dados.textos.imposto.intro}</p>
              </div>

              <div className="card-imposto">
                {dados.textos.imposto.passos?.length ? (
                  <div className="imposto-bloco-passos">
                    <span className="secao-tag">PASSO A PASSO NO SITE DOS CORREIOS</span>
                    <ol className="imposto-passos">
                      {dados.textos.imposto.passos.map(([acao, desc], i) => (
                        <li key={acao}>
                          <span className="imposto-num">{i + 1}</span>
                          <p>
                            <strong>{acao}</strong> {desc}
                          </p>
                        </li>
                      ))}
                    </ol>
                  </div>
                ) : null}

                {dados.textos.imposto.regra ? (
                  <div id="regra-cpf" className="alerta-cpf">
                    <div className="alerta-topo">
                      <span className="alerta-icone">!</span>
                      <div>
                        <span className="alerta-kicker">REGRA DE OURO · NÃO ERRE O CPF</span>
                        <strong>{dados.textos.imposto.regra}</strong>
                      </div>
                    </div>
                    {dados.textos.imposto.exemplo ? (
                      <p className="alerta-exemplo">
                        <strong>Exemplo prático:</strong> {dados.textos.imposto.exemplo}
                      </p>
                    ) : null}
                    {dados.textos.imposto.riscos?.length ? (
                      <div className="alerta-riscos">
                        {dados.textos.imposto.riscos.map(([rotulo, txt]) => (
                          <div key={rotulo} className="risco-item">
                            <span>✕ {rotulo}</span>
                            <p>{txt}</p>
                          </div>
                        ))}
                      </div>
                    ) : null}
                    {dados.textos.imposto.dica ? (
                      <p className="alerta-dica">💡 {dados.textos.imposto.dica}</p>
                    ) : null}
                  </div>
                ) : null}

                <div className="acao-portal-bar">
                  <div>
                    <strong>Já tem o código de rastreio em mãos?</strong>
                    <p>Vincule o CPF assim que o objeto aparecer postado no app dos Correios.</p>
                  </div>
                  <a
                    href={dados.textos.imposto.link}
                    target="_blank"
                    rel="noreferrer"
                    className="btn-lima"
                  >
                    Abrir o Portal do Importador ↗
                  </a>
                </div>
              </div>
            </section>

            {/* ================= FORNECEDORES ================= */}
            {dados.contatos.map((contato, idx) => {
              const id = contato.key || String(idx)
              const temPrecosFixos = contato.catalogos.some((c) => c.itens?.length)
              const catalogosFiltrados =
                temPrecosFixos || filtroCris === "todos"
                  ? contato.catalogos
                  : contato.catalogos.filter((cat) => {
                      const tipo = classificarCatalogo(cat.titulo)
                      if (filtroCris === "tenis") return tipo === "tenis" || tipo === "geral"
                      return tipo === "acessorios"
                    })

              const totalChecks = contato.checklist?.length || 0
              const concluidos =
                contato.checklist?.filter((item) => marcados[`${contato.nome}-${item}`]).length ||
                0

              let etapaNum = 0
              const proximaEtapa = () => {
                etapaNum += 1
                return `ETAPA 0${etapaNum}`
              }

              return (
                <section
                  key={contato.nome}
                  id={`contato-${id}`}
                  className="bloco-fornecedor"
                >
                  <div className="banner-fornecedor">
                    <div className="banner-fornecedor-esq">
                      <div className="banner-fornecedor-topo">
                        <span className="fornecedor-num">FORNECEDOR 0{idx + 1}</span>
                        {contato.pagamento ? (
                          <span className="fornecedor-pag">PAGAMENTO: {contato.pagamento}</span>
                        ) : null}
                      </div>
                      <h2>
                        {contato.nome} — {contato.linha}
                      </h2>
                      {contato.resumo ? (
                        <p className="fornecedor-resumo">{contato.resumo}</p>
                      ) : null}
                    </div>

                    <div className="banner-fornecedor-dir">
                      <div className="whats-meta">
                        <span className="whats-label">WHATSAPP DIRETO</span>
                        <strong className="whats-num">{contato.whatsapp}</strong>
                      </div>
                      <a
                        href={wa(contato.whatsapp)}
                        target="_blank"
                        rel="noreferrer"
                        className="btn-whatsapp"
                      >
                        <span>Chamar no WhatsApp</span>
                        <i>↗</i>
                      </a>
                    </div>
                  </div>

                  {/* CATÁLOGOS */}
                  <div id={`cat-${id}`} className="subbloco">
                    <div className="subbloco-header-row">
                      <div className="subbloco-topo">
                        <span className="etapa-pill">{proximaEtapa()} · ESCOLHA O PRODUTO</span>
                        <h3>
                          {temPrecosFixos
                            ? `Catálogos e Tabela de Preços (${contato.catalogos.length})`
                            : `Catálogos por categoria (${contato.catalogos.length} links)`}
                        </h3>
                        <p className="subbloco-desc">
                          {temPrecosFixos
                            ? "Abra o catálogo abaixo, escolha a peça e tire um print da foto inteira."
                            : "Importante: cada catálogo abaixo é um pedido separado. Não misture itens de catálogos diferentes na mesma mensagem."}
                        </p>
                      </div>

                      {!temPrecosFixos && (
                        <div className="filtros-catalogo" role="group" aria-label="Filtrar catálogos">
                          <button
                            type="button"
                            className={`filtro-btn${filtroCris === "todos" ? " filtro-btn-ativo" : ""}`}
                            onClick={() => setFiltroCris("todos")}
                          >
                            Todos ({contato.catalogos.length})
                          </button>
                          <button
                            type="button"
                            className={`filtro-btn${filtroCris === "tenis" ? " filtro-btn-ativo" : ""}`}
                            onClick={() => setFiltroCris("tenis")}
                          >
                            Só Tênis (11)
                          </button>
                          <button
                            type="button"
                            className={`filtro-btn${filtroCris === "acessorios" ? " filtro-btn-ativo" : ""}`}
                            onClick={() => setFiltroCris("acessorios")}
                          >
                            Óculos & Bolsas (2)
                          </button>
                        </div>
                      )}
                    </div>

                    <div
                      className={
                        temPrecosFixos ? "grade-catalogos-preco" : "grade-catalogos-links"
                      }
                    >
                      {catalogosFiltrados.map((cat, cIdx) => (
                        <SpotlightCard
                          key={cat.link}
                          theme="light"
                          spotlightColor="#DCFF00"
                          className="cartao-catalogo"
                        >
                          <article className="catalogo-miolo">
                            <div className="catalogo-cabecalho">
                              <span className="catalogo-indice">
                                {String(cIdx + 1).padStart(2, "0")}
                              </span>
                              <div>
                                <h3>{cat.titulo}</h3>
                                {cat.descricao ? <p>{cat.descricao}</p> : null}
                              </div>
                            </div>

                            {cat.itens ? (
                              <ul className="lista-precos">
                                {cat.itens.map(([nome, preco]) => (
                                  <li key={nome}>
                                    <span>{nome}</span>
                                    <strong>{preco}</strong>
                                  </li>
                                ))}
                              </ul>
                            ) : null}

                            <p className="catalogo-acao">
                              <a
                                href={cat.link}
                                target="_blank"
                                rel="noreferrer"
                                className="btn-catalogo"
                              >
                                <span>Abrir catálogo</span>
                                <i>↗</i>
                              </a>
                            </p>
                          </article>
                        </SpotlightCard>
                      ))}
                    </div>
                  </div>

                  {/* MEDIDAS */}
                  {contato.medidas?.length ? (
                    <div id={`med-${id}`} className="subbloco">
                      <div className="subbloco-topo">
                        <span className="etapa-pill">{proximaEtapa()} · ACERTE O TAMANHO</span>
                        <h3>Tabela de medidas da camisa</h3>
                      </div>

                      {contato.medidas_intro ? (
                        <div className="subbloco-intro">
                          <strong>Como ler a tabela:</strong> {contato.medidas_intro}
                        </div>
                      ) : null}

                      <div className="seletor-medidas" role="tablist" aria-label="Tipo de camisa">
                        {todasMedidas.map(([titulo, texto], mIdx) => (
                          <button
                            key={titulo}
                            type="button"
                            role="tab"
                            aria-selected={abaMedida === mIdx}
                            className={`medida-tab${abaMedida === mIdx ? " medida-tab-ativa" : ""}`}
                            onClick={() => setAbaMedida(mIdx)}
                          >
                            <strong>{titulo}</strong>
                            <small>{texto}</small>
                          </button>
                        ))}
                      </div>

                      <div className="grade-tabelas">
                        {todasMedidas.map(([titulo, texto, cols, rows], mIdx) => {
                          const ativa = abaMedida === mIdx
                          return (
                            <div
                              key={titulo}
                              className={`card-tabela${ativa ? " card-tabela-ativa" : " card-tabela-oculta"}`}
                            >
                              <div className="card-tabela-head">
                                <div>
                                  <h3>{titulo}</h3>
                                  <p>{texto}</p>
                                </div>
                                <span className="tabela-dica-badge">
                                  1ª coluna = código da mensagem
                                </span>
                              </div>
                              <div className="tabela-scroll">
                                <table>
                                  <thead>
                                    <tr>
                                      {cols.map((col, i) => (
                                        <th key={col} className={i === 0 ? "col-destaque" : ""}>
                                          {col}
                                        </th>
                                      ))}
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {rows.map((row) => (
                                      <tr key={row.join("-")}>
                                        {row.map((cel, i) => (
                                          <td
                                            key={`${cel}-${i}`}
                                            className={i === 0 ? "cel-codigo" : ""}
                                          >
                                            {cel}
                                          </td>
                                        ))}
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  ) : null}

                  {/* FRETE E ADICIONAIS */}
                  {contato.frete?.length || contato.adicionais?.length || contato.pagamento ? (
                    <div id={`frete-${id}`} className="subbloco">
                      <div className="subbloco-topo">
                        <span className="etapa-pill">{proximaEtapa()} · CALCULE O TOTAL</span>
                        <h3>Frete, adicionais e forma de pagamento</h3>
                      </div>

                      <div className="grade-condicoes">
                        {contato.frete?.length ? (
                          <div className="card-condicao">
                            <span className="secao-tag">TABELA DE FRETE</span>
                            <h3>Frete</h3>
                            <ul className="lista-precos">
                              {contato.frete.map(([nome, valor]) => (
                                <li key={nome}>
                                  <span>{nome}</span>
                                  <strong>{valor}</strong>
                                </li>
                              ))}
                            </ul>
                          </div>
                        ) : null}

                        {contato.adicionais?.length ? (
                          <div className="card-condicao">
                            <span className="secao-tag">PERSONALIZAÇÃO E EXTRAS</span>
                            <h3>Adicionais</h3>
                            <ul className="lista-precos">
                              {contato.adicionais.map(([nome, valor]) => (
                                <li key={nome}>
                                  <span>{nome}</span>
                                  <strong>{valor}</strong>
                                </li>
                              ))}
                            </ul>
                          </div>
                        ) : null}

                        {contato.pagamento ? (
                          <div className="card-condicao card-condicao-escura">
                            <span className="secao-tag secao-tag-lima">MÉTODO ACEITO</span>
                            <p className="pagamento-linha">Pagamento: {contato.pagamento}</p>
                            <p className="pagamento-aviso">
                              Nunca pague antes de o fornecedor confirmar que tem a peça em estoque
                              na conversa.
                            </p>
                            <p className="pagamento-whats">
                              <a
                                href={wa(contato.whatsapp)}
                                target="_blank"
                                rel="noreferrer"
                                className="btn-lima"
                              >
                                Chamar {contato.nome} no WhatsApp →
                              </a>
                            </p>
                          </div>
                        ) : null}
                      </div>
                    </div>
                  ) : null}

                  {/* PASSO A PASSO */}
                  {contato.passos?.length ? (
                    <div id={`passos-${id}`} className="subbloco">
                      <div className="subbloco-topo">
                        <span className="etapa-pill">{proximaEtapa()} · ORDEM DO PEDIDO</span>
                        <h3>Passo a passo na conversa</h3>
                      </div>
                      <ol className="lista-passos">
                        {contato.passos.map((bruto, pIdx) => {
                          const passo = passoDe(bruto)
                          return (
                            <li key={passo.titulo} className="card-passo">
                              <div className="passo-topo">
                                <span className="passo-badge">PASSO 0{pIdx + 1}</span>
                                <strong>{passo.titulo}</strong>
                              </div>
                              <p className="passo-texto">{passo.texto}</p>
                              {passo.lista ? (
                                <ul className="passo-sublista">
                                  {passo.lista.map((item) => (
                                    <li key={item}>{item}</li>
                                  ))}
                                </ul>
                              ) : null}
                              {passo.exemplo ? (
                                <div className="passo-exemplo">
                                  <span>EXEMPLO NA CONVERSA</span>
                                  <pre>{passo.exemplo[2]}</pre>
                                </div>
                              ) : null}
                              {passo.notas?.map(([rotulo, texto]) => (
                                <p key={rotulo} className="passo-nota">
                                  <strong>{rotulo}.</strong> {texto}
                                </p>
                              ))}
                            </li>
                          )
                        })}
                      </ol>
                    </div>
                  ) : null}

                  {/* MENSAGENS PRONTAS */}
                  {contato.mensagens?.length ? (
                    <div id={`msg-${id}`} className="subbloco">
                      <div className="subbloco-header-row">
                        <div className="subbloco-topo">
                          <span className="etapa-pill">{proximaEtapa()} · COPIE E COLE</span>
                          <h3>Mensagens prontas para o WhatsApp</h3>
                          <p className="subbloco-desc">
                            Toque em <strong>Copiar mensagem pronta</strong>, abra o WhatsApp de{" "}
                            {contato.nome} e cole. As quebras de linha já vão prontas.
                          </p>
                        </div>
                        <a
                          href={wa(contato.whatsapp)}
                          target="_blank"
                          rel="noreferrer"
                          className="btn-lima"
                        >
                          Abrir WhatsApp de {contato.nome} ↗
                        </a>
                      </div>

                      <div className="grade-mensagens">
                        {contato.mensagens.map(([titulo, dica, texto], mIdx) => (
                          <article key={titulo} className="cartao-mensagem">
                            <div className="cartao-mensagem-miolo">
                              <div className="cartao-mensagem-topo">
                                <span className="mensagem-tag">MODELO 0{mIdx + 1}</span>
                                <h3>{titulo}</h3>
                              </div>
                              <p className="mensagem-dica">{dica}</p>
                              <pre>{texto}</pre>
                            </div>
                            <Copiar texto={texto} />
                          </article>
                        ))}
                      </div>
                    </div>
                  ) : null}

                  {/* CHECKLIST */}
                  {contato.checklist?.length ? (
                    <div id={`check-${id}`} className="subbloco card-checklist">
                      <div className="checklist-header">
                        <div className="subbloco-topo">
                          <span className="secao-tag secao-tag-lima">
                            {proximaEtapa()} · CONFERÊNCIA FINAL
                          </span>
                          <h3>Checklist do pedido ({contato.nome})</h3>
                          <p className="checklist-sub">
                            Toque em cada item abaixo para marcar à medida que fizer o pedido.
                          </p>
                        </div>
                        <div className="checklist-placar">
                          <strong>
                            {concluidos}/{totalChecks}
                          </strong>
                          <span>conferidos</span>
                        </div>
                      </div>

                      <ul className="lista-checklist">
                        {contato.checklist.map((item, cIdx) => {
                          const chave = `${contato.nome}-${item}`
                          const feito = !!marcados[chave]
                          return (
                            <li key={item}>
                              <button
                                type="button"
                                className={`check-item-btn${feito ? " check-item-feito" : ""}`}
                                onClick={() => alternarCheck(chave)}
                              >
                                <span className="check-box">{feito ? "✓" : `0${cIdx + 1}`}</span>
                                <span className="check-texto">{item}</span>
                              </button>
                            </li>
                          )
                        })}
                      </ul>
                    </div>
                  ) : null}
                </section>
              )
            })}
          </div>
        </main>
      </div>
    </div>
  )
}
