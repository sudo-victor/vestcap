import "server-only"

import guia from "../dados/guia.json"
import { type DadosGuia } from "../app/guia"

export function lerGuia(): DadosGuia {
  return guia as unknown as DadosGuia
}
