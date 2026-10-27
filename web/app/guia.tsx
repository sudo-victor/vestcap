import { GuiaInterativo } from "./guia-interativo"

export type Passo = {
  titulo?: string
  texto?: string
  lista?: string[]
  exemplo?: [string, string, string]
  notas?: [string, string][]
}

export type Catalogo = {
  titulo: string
  link: string
  descricao?: string
  botao?: string
  itens?: [string, string][]
}

export type Contato = {
  key?: string
  nome: string
  linha: string
  resumo?: string
  whatsapp: string
  pagamento?: string
  medidas_intro?: string
  medidas?: [string, string, string[], string[][]][][]
  catalogos: Catalogo[]
  adicionais?: [string, string][]
  frete?: [string, string][]
  passos?: (Passo | [string, string, string?])[]
  mensagens?: [string, string, string][]
  checklist?: string[]
}

export type DadosGuia = {
  contatos: Contato[]
  textos: {
    antes: [string, string][]
    imposto: {
      link: string
      intro: string
      passos?: [string, string][]
      regra?: string
      exemplo?: string
      riscos?: [string, string][]
      dica?: string
    }
    tamanhos?: [string, string][]
    tamanhos_texto?: string
  }
}

export function Guia({ dados }: { dados: DadosGuia }) {
  return <GuiaInterativo dados={dados} />
}
