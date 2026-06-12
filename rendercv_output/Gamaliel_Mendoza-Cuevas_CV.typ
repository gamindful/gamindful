// Import the rendercv function and all the refactored components
#import "@preview/rendercv:0.3.0": *

// Apply the rendercv template with custom configuration
#show: rendercv.with(
  name: "Gamaliel Mendoza-Cuevas",
  title: "Gamaliel Mendoza-Cuevas - CV",
  footer: context { [#emph[Gamaliel Mendoza-Cuevas -- #str(here().page())\/#str(counter(page).final().first())]] },
  top-note: [ #emph[Last updated in June 2026] ],
  locale-catalog-language: "en",
  text-direction: ltr,
  page-size: "us-letter",
  page-top-margin: 0.7in,
  page-bottom-margin: 0.7in,
  page-left-margin: 0.7in,
  page-right-margin: 0.7in,
  page-show-footer: true,
  page-show-top-note: true,
  colors-body: rgb(0, 0, 0),
  colors-name: rgb(0, 79, 144),
  colors-headline: rgb(0, 79, 144),
  colors-connections: rgb(0, 79, 144),
  colors-section-titles: rgb(0, 79, 144),
  colors-links: rgb(0, 79, 144),
  colors-footer: rgb(128, 128, 128),
  colors-top-note: rgb(128, 128, 128),
  typography-line-spacing: 0.6em,
  typography-alignment: "justified",
  typography-date-and-location-column-alignment: right,
  typography-font-family-body: "Source Sans 3",
  typography-font-family-name: "Source Sans 3",
  typography-font-family-headline: "Source Sans 3",
  typography-font-family-connections: "Source Sans 3",
  typography-font-family-section-titles: "Source Sans 3",
  typography-font-size-body: 10pt,
  typography-font-size-name: 30pt,
  typography-font-size-headline: 10pt,
  typography-font-size-connections: 10pt,
  typography-font-size-section-titles: 1.4em,
  typography-small-caps-name: false,
  typography-small-caps-headline: false,
  typography-small-caps-connections: false,
  typography-small-caps-section-titles: false,
  typography-bold-name: true,
  typography-bold-headline: false,
  typography-bold-connections: false,
  typography-bold-section-titles: true,
  links-underline: false,
  links-show-external-link-icon: false,
  header-alignment: center,
  header-photo-width: 3.5cm,
  header-space-below-name: 0.7cm,
  header-space-below-headline: 0.7cm,
  header-space-below-connections: 0.7cm,
  header-connections-hyperlink: true,
  header-connections-show-icons: true,
  header-connections-display-urls-instead-of-usernames: false,
  header-connections-separator: "",
  header-connections-space-between-connections: 0.5cm,
  section-titles-type: "with_partial_line",
  section-titles-line-thickness: 0.5pt,
  section-titles-space-above: 0.5cm,
  section-titles-space-below: 0.3cm,
  sections-allow-page-break: true,
  sections-space-between-text-based-entries: 0.3em,
  sections-space-between-regular-entries: 1.2em,
  entries-date-and-location-width: 4.15cm,
  entries-side-space: 0.2cm,
  entries-space-between-columns: 0.1cm,
  entries-allow-page-break: false,
  entries-short-second-row: true,
  entries-degree-width: 1cm,
  entries-summary-space-left: 0cm,
  entries-summary-space-above: 0cm,
  entries-highlights-bullet:  "•" ,
  entries-highlights-nested-bullet:  "•" ,
  entries-highlights-space-left: 0.15cm,
  entries-highlights-space-above: 0cm,
  entries-highlights-space-between-items: 0cm,
  entries-highlights-space-between-bullet-and-text: 0.5em,
  date: datetime(
    year: 2026,
    month: 6,
    day: 11,
  ),
)


#grid(
  columns: (auto, 1fr),
  column-gutter: 0cm,
  align: horizon + left,
  [#pad(left: 0.4cm, right: 0.4cm, image("me.jpg", width: 3.5cm))
],
  [
= Gamaliel Mendoza-Cuevas

  #headline([PhD. in Neuroscience, Data Science enthusiast and quantitative researcher.])

#connections(
  [#link("mailto:gimc@tutanota.de", icon: false, if-underline: false, if-color: false)[#connection-with-icon("envelope")[gimc\@tutanota.de]]],
  [#link("https://orcid.org/0000-0003-4054-1373", icon: false, if-underline: false, if-color: false)[#connection-with-icon("link")[orcid.org\/0000-0003-4054-1373]]],
  [#link("https://linkedin.com/in/gamaliel-mendoza-cuevas", icon: false, if-underline: false, if-color: false)[#connection-with-icon("linkedin")[gamaliel-mendoza-cuevas]]],
  [#link("https://github.com/gamindful", icon: false, if-underline: false, if-color: false)[#connection-with-icon("github")[gamindful]]],
)
  ]
)


== Profile

PhD in Neuroscience and Data Science implementer with experience in the development of machine learning models for healthcare applications, and basic research in animal models of neurological diseases. Background in signal processing, data analysis, and scientific research. Passionate about leveraging data-driven approaches to advance our understanding of neurological health and pathology.

(Engineering ↔ Analysis ↔ Science)

== Expertise and certifications

#strong[Data Engineering (Databricks), Databases and SQL for Data Science (IBM):] Infrastructure (Hadoop, Databricks, Oracle, MySQL).

#strong[Deep Learning (NMA), Machine Learning Practitioner (Databricks), Machine Learning with Python (IBM):] ML Frameworks (PyTorch, TensorFlow, Sci-Kit, Transformers).

#strong[Data Analyst Associate (Databricks), Python for Data Science (IBM):] Programming languages (Python, Spark, SQL, R, MATLAB).

#strong[Version control:] Git, GitHub, Bitbucket.

#strong[Research & development:] Signal processing in Neuroscience, Data Science and Neuroscience, Machine Learning for healthcare.

== Employment history

#regular-entry(
  [
    #strong[Cotiviti], Data & Insight Analyst.

    - Deployment of model serving endpoints for Neural Network predictors for healthcare data.

    - Development and monitoring of a recommendation system for healthcare.

    - Development of recommendation systems for healthcare based on K-means clustering.

    - Development of classifiers for healthcare data using convolutional neural networks.

    - Development of Byte-Pair Encoding tokenizers for the analysis of healthcare data.

    - Fine-tuning of Transformer-based language models for the analysis of healthcare data.

    - Development of ETL pipelines for local and cloud deployment (Databricks).

    - Implementation of data quality monitoring systems (mlflow).

    - Generation of Bronze, Silver, and Gold datasets for data analysis.

    - Development of Python-based applications using machine learning models for the analysis of healthcare data.

  ],
  [
    Remote, Mexico City, Mexico.

    Aug 2025 – present

  ],
)

#regular-entry(
  [
    #strong[BIOINVERT], Data Analyst.

    #summary[Standardization and publication of Neurophysiological measurements.]

    - Analysis of CT scans for the quantification of bone density.

    - Statistical analysis of Aging-related changes in bone density.

    - Co-authored paper accepted at Veterinary radiology and ultrasound.

  ],
  [
    Mexico City, Mexico

    Jan 2017 – June 2017

  ],
)

#regular-entry(
  [
    #strong[APREXBIO], Research Intern.

    #summary[Standardization and publication of Neurophysiological measurements.]

    - Analysis of visual evoked potentials in Rhesus monkeys.

    - Certification on the use of MRI equipment for the acquisition of anatomical images.

    - Book chapter of standardization of normal values for visual evoked potentials.

    - Co-authored paper accepted at Experimental Gerontology.

  ],
  [
    Mexico City, Mexico

    Jan 2016 – Jan 2017

  ],
)

== Education

#education-entry(
  [
    #strong[National Autonomous University of Mexico], Neuroscience.

    #summary[PhD in Neuroscience under the Biomedical Sciences program. Basic research on Neuropathology, behavior and Neurophysiology in animal models.]

    - Published article accepted at Journal of Neurophysiology.

    - Thesis: Enhancement of visual discrimination deficits in a model of Parkinson's Disease by low dosages of L-DOPA.

    - Advisor: PhD. Luis Alberto Carrillo Reid.

    - Scholarship for PhD studies, Mexican Secretariat of Science, Humanities, Technology, and Innovation.

  ],
  [
    Queretaro, Mexico

    Aug 2020 – Apr 2026

  ],
  degree-column: [
    #strong[PhD]
  ],
)

#education-entry(
  [
    #strong[National Autonomous University of Mexico], Neurobiology.

    #summary[Behavioral assessment of visual discrimination in a mouse model of Parkinson's Disease.]

    - GPA: 9.16\/10.00, Honorific mention.

    - Scholarship for Master's studies, Mexican Secretariat of Science, Humanities, Technology, and Innovation.

  ],
  [
    Queretaro, Mexico

    Aug 2018 – May 2020

  ],
  degree-column: [
    #strong[MsC]
  ],
)

== Languages

#strong[English:] C1 (TOEFL iBT 110\/120).

#strong[German:] A2 (Ongoing studies; A1, Goethe-Zertifikat).

#strong[Spanish:] Native.

== Docs and repositories

#strong[Personal cloud:] https:\/\/c.mail.com\/\@1436672005888810536\/5BhDibj6-RjvzxFlB2KcfQ

== Publications

#regular-entry(
  [
    #strong[Impaired visually guided behavior in a mouse model of Parkinson's disease]

    #emph[Mendoza-Cuevas, G.], Perez-Becerra, J., Velazquez-Contreras, R., Calderon, V, Carrillo-Reid, L.

    #link("https://doi.org/https://doi.org/10.1152/jn.00307.2025")[https:\/\/doi.org\/10.1152\/jn.00307.2025] (Journal of Neurophysiology)

  ],
  [
    2025

  ],
)

#regular-entry(
  [
    #strong[Visual evoked potentials in the Rhesus monkey]

    #emph[Mendoza-Cuevas, G.], Hernández-Godínez, B., Ibáñez-Contreras, A., #link("https://novapublishers.com/shop/evoked-potentials-and-electrical-stimulation-clinical-roles-challenges-and-emerging-research/")[ISBN: 9781536110753]

  ],
  [
    2017

  ],
)

#regular-entry(
  [
    #strong[Computed tomography is a feasible method for quantifying bone density in Macaca mulatta]

    Solís-Chávez, S., Castillo-Rivera, M., Arteaga-Silva, M., Ibáñez-Contreras, A., Hernández-Godínez, B., Morón-Mendoza, A., #emph[Mendoza-Cuevas, G.], Morales-Guadarrama, A., Sacristan-Rock, E.

    #link("https://doi.org/https://doi.org/10.1111/vru.12624")[https:\/\/doi.org\/10.1111\/vru.12624] (Veterinary Radiology and Ultrasound)

  ],
  [
    2018

  ],
)

#regular-entry(
  [
    #strong[Electrical activity of sensory pathways in female and male geriatric Rhesus monkeys (Macaca mulatta), and its relation to oxidative stress]

    Ibáñez-Contreras, A., Hernández-Arciga, U., Poblano, A., Arteaga-Silva, M., Hernández-Godínez, B., #emph[Mendoza-Cuevas, G.], Toledo-Pérez, R., Alarcón-Aguilar, A., González-Puertos, V., Konigsberg, M.

    #link("https://doi.org/https://doi.org/10.1016/j.exger.2017.11.003")[https:\/\/doi.org\/10.1016\/j.exger.2017.11.003] (Experimental Gerontology)

  ],
  [
    2018

  ],
)

#regular-entry(
  [
    #strong[The effect of oxidative stress on brain electrical activity and its repercussions on sensory organization in geriatric Rhesus monkeys in captivity]

    Ibáñez-Contreras, A., Hernández-Godínez, B., #emph[Mendoza-Cuevas, G.], Hernández-Arciga, U., Königsberg, M., #link("https://novapublishers.com/shop/evoked-potentials-and-electrical-stimulation-clinical-roles-challenges-and-emerging-research/")[ISBN: 9781536110753]

  ],
  [
    2017

  ],
)

== Other awards

#regular-entry(
  [
    #strong[Second place at the 9th state health research forum]

    Visual discrimination in a mouse model of Parkinson's Disease

    (Queretaro, Mexico)

  ],
  [
    2024

  ],
)

#regular-entry(
  [
    #strong[Third place at design contest for the Latin American Brain Initiative (LATBrain)]

  ],
  [
    2021

  ],
)
