// Alvorada Instagram carousel template
// Output: square 1080 x 1080 pt pages. Export PNGs at 1x or 2x for Instagram.

#let azul = rgb("#00035d")
#let papel = rgb("#f3ead7")
#let tinta = papel
#let serif = "EB Garamond 12"

#set page(
  width: 1080pt,
  height: 1080pt,
  margin: 0pt,
  fill: azul,
)
#set text(
  font: serif,
  fill: tinta,
  lang: "pt",
  hyphenate: false,
)
#set par(leading: 1.35em)

#let frame(body) = block(
  width: 100%,
  height: 100%,
  inset: (x: 104pt, y: 96pt),
  body,
)

#let backdrop(path) = place(top + left,
  image(path, width: 1080pt, height: 1080pt, fit: "cover"),
)

#let mark = align(right)[
  #text(size: 14pt, weight: "bold", tracking: 1.5pt)[ALVORADA]
]

#let footer(number: none) = {
  place(bottom + left, dx: 104pt, dy: -54pt)[
    #image("alvorada-logo.png", width: 28pt, height: 28pt, fit: "contain")
  ]
  if number != none {
    place(bottom + right, dx: -104pt, dy: -50pt)[
      #text(size: 14pt)[#number]
    ]
  }
}

// Use this for a strong opening or closing card.
#let title-page(title, subtitle: none, number: none, bg: none) = {
  if bg != none { backdrop(bg) }
  frame(
    align(center + horizon)[
      #mark
      #v(132pt)
      #text(size: 64pt, weight: "regular")[#title]
      #if subtitle != none [
        #v(28pt)
        #text(size: 22pt)[#subtitle]
      ]
    ]
  )
  footer(number: number)
}

// Use this for text-led carousel cards. Keep titles short for the book feel.
#let text-page(heading, body: none, kicker: none, number: none, bg: none) = {
  if bg != none { backdrop(bg) }
  frame({
    if kicker != none {
      text(size: 14pt, weight: "bold", tracking: 1.2pt, upper(kicker))
      v(76pt)
    }
    block(width: 760pt)[
      #text(size: 56pt, weight: "regular")[#heading]
    ]
    if body != none {
      v(44pt)
      block(width: 720pt)[
        #text(size: 22pt)[#body]
      ]
    }
  })
  footer(number: number)
}

// Use this for artwork. Images are contained, never cropped or stretched.
#let image-page(path, caption: none, number: none, bg: none) = {
  if bg != none { backdrop(bg) }
  frame({
    align(center)[
      #image(path, width: 908pt, height: 820pt, fit: "contain")
    ]
    if caption != none {
      v(24pt)
      align(center)[#text(size: 18pt)[#caption]]
    }
  })
  footer(number: number)
}

// Replace these example pages with your own sequence. Every page stays 1:1.
#title-page("Alvorada", subtitle: "por um novo alvorecer", number: 1)
#pagebreak()

#image-page("annunciation-fra-angelico.jpg", caption: "A Anunciação · Fra Angelico", number: 2)
#pagebreak()

#text-page(
  [Fizestes-nos #linebreak() para Vós],
  body: "A inquietação não é apenas ausência. É também procura, movimento e desejo de encontrar um lugar onde o coração possa repousar.",
  kicker: "Santo Agostinho · Confissões, I, 1, 1",
  number: 3,
  bg: "bg-noise.png",
)
#pagebreak()

#image-page("annunciation-caravaggio.jpg", caption: "A Anunciação · Caravaggio", number: 4)
#pagebreak()

#text-page(
  [Nada te #linebreak() perturbe],
  body: "Nada permanece exatamente como era. A fé oferece outra medida para o tempo: uma confiança paciente, capaz de atravessar a mudança sem perder o centro.",
  kicker: "Santa Teresa d'Ávila",
  number: 5,
)
#pagebreak()

#text-page(
  [Ditosa #linebreak() noite],
  body: "Há uma noite que não é fim, mas passagem. Nela, aquilo que parecia separado se aproxima, e a espera começa a revelar uma forma de encontro.",
  kicker: "São João da Cruz · Noite Escura",
  number: 6,
)
#pagebreak()

#image-page("Pasted image (3).png", caption: "A imagem como memória", number: 7)
#pagebreak()

#text-page(
  [A manhã não chega #linebreak() de uma vez],
  body: "Ela aparece primeiro como uma alteração quase imperceptível na cor das coisas. Depois, como uma forma de reconhecer o caminho. Alvorada é esse intervalo entre a noite que termina e a luz que ainda está por vir.",
  kicker: "Alvorada · caderno de imagens",
  number: 8,
  bg: "bg-blur-a.png",
)
#pagebreak()

#title-page("Alvorada", subtitle: "por um novo alvorecer", number: 9)
