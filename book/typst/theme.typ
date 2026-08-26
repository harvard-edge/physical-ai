// ===========================================================================
// Physical AI Systems, Custom Typst Theme & Architecture
// ===========================================================================

// Harvard Crimson & ETH Zurich Academic Semantic Palette
#let harvardcrimson = rgb("#A51C30")
#let ethdarkblue = rgb("#1F407A")
#let ethblue = rgb("#215CAF")
#let ethpetrol = rgb("#007A87")
#let ethbronze = rgb("#B87333")
#let ethpurple = rgb("#5B4B8A")
#let ethgreen = rgb("#1B6B48")
#let ink = rgb("#0F172A")
#let softink = rgb("#334155")
#let muted = rgb("#64748B")
#let cardbg = rgb("#F8FAFC")
#let border = rgb("#CBD5E1")

// Typography & Paragraph Flow
#set text(
  font: ("STIX Two Text", "STIXTwoText", "Times New Roman"),
  size: 9.5pt,
  fill: ink,
  lang: "en",
  region: "US"
)

#set par(
  leading: 0.65em,
  justify: true,
  first-line-indent: 0pt
)

// Part Page Layout (Clean Harvard/ETH Style, No Blue Blobs or Overlaps)
#let part(title) = {
  pagebreak(to: "odd")
  part-counter.step()
  v(28%)
  align(center)[
    #text(font: "Avenir Next", size: 13pt, weight: "bold", fill: ethpetrol, tracking: 0.2em)[#smallcaps[PART #part-counter.display("I")]]
    #v(0.8em)
    #text(font: "STIX Two Text", size: 24pt, weight: "bold", fill: harvardcrimson)[#title]
    #v(1.2em)
    #line(length: 35%, stroke: 1.5pt + harvardcrimson)
  ]
  v(2em)
}

// Heading Hierarchy
#show heading.where(level: 1): it => block(width: 100%, below: 1.5em)[
  #v(1em)
  #text(font: "Avenir Next", size: 9pt, weight: "bold", fill: ethpetrol, tracking: 0.1em)[#smallcaps[CHAPTER #counter(heading).display()]]
  #v(0.4em)
  #text(font: "STIX Two Text", size: 19pt, weight: "bold", fill: ethdarkblue)[#it.body]
  #v(0.6em)
  #line(length: 100%, stroke: 1pt + ethdarkblue)
  #v(0.8em)
]

#show heading.where(level: 2): it => block(width: 100%, below: 1em)[
  #v(0.8em)
  #text(font: "Avenir Next", size: 12.5pt, weight: "bold", fill: ethdarkblue)[#it.body]
  #v(0.2em)
]

#show heading.where(level: 3): it => block(width: 100%, below: 0.8em)[
  #v(0.6em)
  #text(font: "Avenir Next", size: 10.5pt, weight: "bold", fill: ink)[#it.body]
  #v(0.2em)
]

// Callout Boxes Styling
#show figure.where(kind: "quarto-float-fig"): it => block(width: 100%, inset: (y: 0.8em))[
  #set align(center)
  #it.body
  #v(0.5em)
  #block(width: 95%)[
    #set align(left)
    #set text(size: 8.5pt, fill: softink)
    #it.caption
  ]
]
