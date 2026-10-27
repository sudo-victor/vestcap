import { Palco } from "./palco"

export function Entrada({
  erro,
  action,
}: {
  erro: boolean
  action: (formData: FormData) => Promise<void>
}) {
  return (
    <Palco>
      <p className="cofre-chamada">O guia abre com o código individual que você recebeu.</p>
      <form action={action} className="cofre-form">
        <label htmlFor="codigo">Código de acesso</label>
        <input
          id="codigo"
          name="codigo"
          type="password"
          placeholder="Digite seu código"
          autoComplete="current-password"
          required
        />
        <button type="submit">Entrar no guia →</button>
      </form>
      {erro ? <p className="erro">Código não entra. Confira com quem te enviou.</p> : null}
    </Palco>
  )
}
