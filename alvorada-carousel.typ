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
#set par(leading: 0.35em)

#let frame(body) = block(
  width: 100%,
  height: 100%,
  inset: (x: 104pt, y: 96pt),
  body,
)

#let backdrop(path) = place(top + left,
  image(path, width: 1080pt, height: 1080pt, fit: "cover"),
)

#let header = place(top + center, dy: 72pt)[
  #text(size: 21pt, weight: "bold", tracking: 1.5pt)[movimento alvorada]
]

#let footer(number: none) = {
  if number != none {
    place(bottom + right, dx: -104pt, dy: -50pt)[
      #text(size: 21pt)[#number]
    ]
  }
}

// Use this for a strong opening or closing card.
#let title-page(title, subtitle: none, number: none, bg: none) = {
  if bg != none { backdrop(bg) }
  header
  frame(
    align(center + horizon)[
      #v(132pt)
      #text(size: 96pt, weight: "regular")[#title]
      #if subtitle != none [
        #v(28pt)
        #text(size: 33pt)[#subtitle]
      ]
    ]
  )
  footer(number: number)
}

// Use this for text-led carousel cards. Keep titles short for the book feel.
#let text-page(heading, body: none, kicker: none, number: none, bg: none) = {
  if bg != none { backdrop(bg) }
  header
  frame({
    if kicker != none {
      text(size: 21pt, weight: "bold", tracking: 1.2pt, upper(kicker))
      v(76pt)
    }
    block(width: 760pt)[
      #set par(leading: 0.05em)
      #text(size: 84pt, weight: "regular")[#heading]
    ]
    if body != none {
      v(44pt)
      block(width: 720pt)[
        #text(size: 33pt)[#body]
      ]
    }
  })
  footer(number: number)
}

// Use this for artwork. Images are contained, never cropped or stretched.
#let image-page(path, caption: none, number: none, bg: none) = {
  if bg != none { backdrop(bg) }
  header
  frame({
    align(center)[
      #image(path, width: 908pt, height: 820pt, fit: "contain")
    ]
    if caption != none {
      v(24pt)
      align(center)[#text(size: 27pt)[#caption]]
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
  body: "A inquietação também é procura. O coração busca um lugar onde possa repousar.",
  kicker: "Santo Agostinho · Confissões, I, 1, 1",
  number: 3,
  bg: "bg-noise.png",
)
#pagebreak()

#image-page("annunciation-caravaggio.jpg", caption: "A Anunciação · Caravaggio", number: 4)
#pagebreak()

#text-page(
  [Nada te #linebreak() perturbe],
  body: "Tudo passa. A fé permanece. É uma confiança paciente para atravessar a mudança sem perder o centro.",
  kicker: "Santa Teresa d'Ávila",
  number: 5,
)
#pagebreak()

#text-page(
  [Ditosa #linebreak() noite],
  body: "A noite também pode ser passagem. O que parecia separado começa a se aproximar.",
  kicker: "São João da Cruz · Noite Escura",
  number: 6,
)
#pagebreak()

#image-page("Pasted image (3).png", caption: "A imagem como memória", number: 7)
#pagebreak()

#text-page(
  [A manhã não chega #linebreak() de uma vez],
  body: "A manhã aparece primeiro como uma mudança na cor das coisas. Alvorada é o intervalo entre a noite e a luz.",
  kicker: "Alvorada · caderno de imagens",
  number: 8,
  bg: "bg-blur-a.png",
)
#pagebreak()

#title-page("Alvorada", subtitle: "por um novo alvorecer", number: 9)
