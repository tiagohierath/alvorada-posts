// Contact-sheet set showing occasional Alvorada treatments and endings.
#import "alvorada-carousel.typ": text-page, image-page, closing-page, closing-seal-page, closing-chrome-page, closing-hymn-page

#set page(width: 1080pt, height: 1080pt, margin: 0pt, fill: rgb("#00035d"))
#set text(font: "EB Garamond", fill: rgb("#f3ead7"), lang: "pt")

#text-page(
  [Fizestes-nos #linebreak() para Vós],
  body: "A inquietação também é procura. O coração busca um lugar onde possa repousar.",
  kicker: "Santo Agostinho · Confissões, I, 1, 1",
  number: 1,
  bg: "bg-noise.png",
)
#pagebreak()

#text-page(
  [A manhã não chega #linebreak() de uma vez],
  body: "A manhã aparece primeiro como uma mudança na cor das coisas.",
  kicker: "Alvorada · caderno de imagens",
  number: 2,
  bg: "bg-blur-a.png",
  seal: "brasaoalv-watermark.png",
)
#pagebreak()

#image-page("annunciation-fra-angelico.jpg", caption: "A Anunciação · Fra Angelico", number: 3)
#pagebreak()

#image-page("annunciation-caravaggio.jpg", caption: "A Anunciação · Caravaggio", number: 4)
#pagebreak()

#image-page("Pasted image (3).png", caption: "A imagem como memória", number: 5)
#pagebreak()

#closing-page(number: 6)
#pagebreak()

#closing-seal-page(number: 7)
#pagebreak()

#closing-chrome-page(number: 8)
#pagebreak()

#closing-hymn-page()
