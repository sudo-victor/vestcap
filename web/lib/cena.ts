export function cena(reduzirMovimento: boolean) {
  return {
    fundo: "#10280A",
    seda: { color: "#145C38", sheenColor: "#DCFF00", paused: reduzirMovimento },
    titulo: { color: "#DCFF00", shineColor: "#FBF6E4", disabled: reduzirMovimento },
  }
}
