#!/usr/bin/env python3
"""
Generate trilingual HTML CV from YAML files (GIMC_CV.yaml, GAMA.yaml)
Supports English, German, and Spanish with language toggle
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List

# Comprehensive translations dictionary
TRANSLATIONS = {
    # Common terms
    "Profile": {"de": "Profil", "es": "Perfil"},
    "Summary": {"de": "Zusammenfassung", "es": "Resumen"},
    "Experience": {"de": "Erfahrung", "es": "Experiencia"},
    "Education": {"de": "Ausbildung", "es": "Educación"},
    "Publications": {"de": "Veröffentlichungen", "es": "Publicaciones"},
    "Awards": {"de": "Auszeichnungen", "es": "Premios"},
    "Skills": {"de": "Fähigkeiten", "es": "Habilidades"},
    "Certifications": {"de": "Zertifizierungen", "es": "Certificaciones"},
    "Languages": {"de": "Programmiersprachen", "es": "Lenguajes de Programación"},
    "Expertise and certifications": {"de": "Fachkompetenz und Zertifizierungen", "es": "Experiencia y Certificaciones"},
    "Employment history": {"de": "Berufsgeschichte", "es": "Historial Laboral"},
    "Docs and repositories": {"de": "Docs und Repositories", "es": "Documentos y Repositorios"},
    
    # Header
    "PhD. in Neuroscience, Data Science Practitioner.": {"de": "PhD. in Neurowissenschaften, Data-Science-Praktiker.", "es": "PhD. en Neurociencia, Profesional de Ciencia de Datos."},
    "PhD. in Neuroscience, Data Science enthusiast and quantitative researcher.": {"de": "PhD. in Neurowissenschaften, Data-Science-Enthusiast und quantitativer Forscher.", "es": "PhD. en Neurociencia, entusiasta de Ciencia de Datos e investigador cuantitativo."},
    
    # GAMA Profile
    "PhD in Neuroscience and Data Science practitioner with experience in the development of machine learning models for healthcare applications, and basic research in animal models of neurological diseases. Background in signal processing, data analysis, and scientific research. Passionate about leveraging data-driven approaches to advance our understanding of neurological health and pathology.": {
        "de": "PhD in Neurowissenschaften und Data-Science-Praktiker mit Erfahrung in der Entwicklung von Machine-Learning-Modellen für Healthcare-Anwendungen und Grundlagenforschung in Tiermodellen neurologischer Erkrankungen. Hintergrund in Signalverarbeitung, Datenanalyse und wissenschaftlicher Forschung. Leidenschaftlich daran interessiert, datengesteuerte Ansätze zu nutzen, um unser Verständnis der neurologischen Gesundheit und Pathologie zu verbessern.",
        "es": "PhD en Neurociencia e ingeniero de datos con experiencia en el desarrollo de modelos de aprendizaje automático para aplicaciones de salud, e investigación básica en modelos animales de enfermedades neurológicas. Experiencia en procesamiento de señales, análisis de datos e investigación científica. Apasionado por aprovechar enfoques basados en datos para avanzar en nuestra comprensión de la salud y patología neurológica."
    },
    "(Engineering ↔ Analysis ↔ Science)": {"de": "(Ingenieurwesen ↔ Analyse ↔ Wissenschaft)", "es": "(Ingeniería ↔ Análisis ↔ Ciencia)"},
    
    # Employment
    "Cotiviti": {"de": "Cotiviti", "es": "Cotiviti"},
    "Data & Insight Analyst.": {"de": "Daten- und Insight-Analyst.", "es": "Analista de Datos e Insights."},
    "Remote, Mexico City, Mexico.": {"de": "Remote, Mexiko-Stadt, Mexiko.", "es": "Remoto, Ciudad de México, México."},
    "Aug 2025 – Present": {"de": "Aug. 2025 – Heute", "es": "Ago. 2025 – Presente"},
    "Development and monitoring of a recommendation system for healthcare.": {"de": "Entwicklung und Überwachung eines Empfehlungssystems für das Gesundheitswesen.", "es": "Desarrollo y monitoreo de un sistema de recomendación para atención médica."},
    "Development of recommendation systems for healthcare based on K-means clustering.": {"de": "Entwicklung von Empfehlungssystemen im Gesundheitswesen basierend auf K-means-Clustering.", "es": "Desarrollo de sistemas de recomendación para atención médica basados en agrupamiento K-means."},
    "Development of classifiers for healthcare data using convolutional neural networks.": {"de": "Entwicklung von Klassifizierern für Gesundheitsdaten mit Faltungs-Neuronalen Netzen.", "es": "Desarrollo de clasificadores para datos de salud utilizando redes neuronales convolucionales."},
    "Development of Byte-Pair Encoding tokenizers for the analysis of healthcare data.": {"de": "Entwicklung von Byte-Pair-Encoding-Tokenisierern zur Analyse von Gesundheitsdaten.", "es": "Desarrollo de tokenizadores de codificación de pares de bytes para el análisis de datos de salud."},
    "Fine-tuning of Transformer-based language models for the analysis of healthcare data.": {"de": "Feinabstimmung von Transformer-basierten Sprachmodellen zur Analyse von Gesundheitsdaten.", "es": "Ajuste fino de modelos de lenguaje basados en transformadores para el análisis de datos de salud."},
    "Development of ETL pipelines for local and cloud deployment (Databricks).": {"de": "Entwicklung von ETL-Pipelines für lokale und Cloud-Bereitstellung (Databricks).", "es": "Desarrollo de tuberías ETL para implementación local y en la nube (Databricks)."},
    "Implementation of data quality monitoring systems (mlflow).": {"de": "Implementierung von Datenqualitätsüberwachungssystemen (mlflow).", "es": "Implementación de sistemas de monitoreo de calidad de datos (mlflow)."},
    "Generation of Bronze, Silver, and Gold datasets for data analysis.": {"de": "Generierung von Bronze-, Silver- und Gold-Datensätzen zur Datenanalyse.", "es": "Generación de conjuntos de datos Bronze, Silver y Gold para análisis de datos."},
    "Development of Python-based applications using machine learning models for the analysis of healthcare data.": {"de": "Entwicklung von Python-basierten Anwendungen mit Machine-Learning-Modellen zur Analyse von Gesundheitsdaten.", "es": "Desarrollo de aplicaciones basadas en Python utilizando modelos de aprendizaje automático para el análisis de datos de salud."},
    
    "BIOINVERT": {"de": "BIOINVERT", "es": "BIOINVERT"},
    "Data Analyst.": {"de": "Datenanalyst.", "es": "Analista de Datos."},
    "Jan 2017 – Jun 2017": {"de": "Jan. 2017 – Juni 2017", "es": "Ene. 2017 – Jun. 2017"},
    "Mexico City, Mexico": {"de": "Mexiko-Stadt, Mexiko", "es": "Ciudad de México, México"},
    "Standardization and publication of Neurophysiological measurements.": {"de": "Standardisierung und Veröffentlichung neurophysiologischer Messungen.", "es": "Estandarización y publicación de mediciones neurofisiológicas."},
    "Analysis of CT scans for the quantification of bone density.": {"de": "Analyse von CT-Scans zur Quantifizierung der Knochendichte.", "es": "Análisis de tomografías computarizadas para la cuantificación de la densidad ósea."},
    "Statistical analysis of Aging-related changes in bone density.": {"de": "Statistische Analyse alterungsbedingter Veränderungen der Knochendichte.", "es": "Análisis estadístico de cambios relacionados con el envejecimiento en la densidad ósea."},
    "Co-authored paper accepted at Veterinary radiology and ultrasound": {"de": "Co-Autor eines Papiers akzeptiert in Veterinary Radiology and Ultrasound", "es": "Artículo coautor aceptado en Radiología Veterinaria y Ultrasonido"},
    
    "APREXBIO": {"de": "APREXBIO", "es": "APREXBIO"},
    "Research Intern.": {"de": "Forschungspraktikant.", "es": "Practicante de Investigación."},
    "Jan 2016 – Jan 2017": {"de": "Jan. 2016 – Jan. 2017", "es": "Ene. 2016 – Ene. 2017"},
    "Analysis of visual evoked potentials in Rhesus monkeys.": {"de": "Analyse visuell evozierter Potenziale bei Rhesusaffen.", "es": "Análisis de potenciales evocados visuales en monos Rhesus."},
    "Certification on the use of MRI equipment for the acquisition of anatomical images.": {"de": "Zertifizierung zur Verwendung von MRI-Geräten zur Erfassung anatomischer Bilder.", "es": "Certificación sobre el uso de equipos de resonancia magnética para la adquisición de imágenes anatómicas."},
    "Book chapter of standardization of normal values for visual evoked potentials.": {"de": "Buchkapitel zur Standardisierung normaler Werte für visuell evozierte Potenziale.", "es": "Capítulo de libro sobre estandarización de valores normales para potenciales evocados visuales."},
    "Co-authored paper accepted at Experimental Gerontology": {"de": "Co-Autor eines Papiers akzeptiert in Experimental Gerontology", "es": "Artículo coautor aceptado en Gerontología Experimental"},
    
    # Education
    "National Autonomous University of Mexico": {"de": "Nationale Autonome Universität von Mexiko", "es": "Universidad Nacional Autónoma de México"},
    "Neuroscience.": {"de": "Neurowissenschaften.", "es": "Neurociencia."},
    "Neurobiology.": {"de": "Neurobiologie.", "es": "Neurobiología."},
    "PhD": {"de": "PhD", "es": "PhD"},
    "MsC": {"de": "MsC", "es": "MsC"},
    "Aug 2020 – Apr 2026": {"de": "Aug. 2020 – Apr. 2026", "es": "Ago. 2020 – Abr. 2026"},
    "Aug 2018 – May 2020": {"de": "Aug. 2018 – Mai 2020", "es": "Ago. 2018 – May. 2020"},
    "Queretaro, Mexico": {"de": "Querétaro, Mexiko", "es": "Querétaro, México"},
    "PhD in Neuroscience under the Biomedical Sciences program, basic research in animal models, Neuropathology, behavior and Neurophysiology.": {
        "de": "PhD in Neurowissenschaften im Rahmen des Biomedical Sciences Programms, Grundlagenforschung in Tiermodellen, Neuropathologie, Verhalten und Neurophysiologie.",
        "es": "PhD en Neurociencia bajo el programa de Ciencias Biomédicas, investigación básica en modelos animales, Neuropatología, comportamiento y Neurofisiología."
    },
    "Published article accepted at Journal of Neurophysiology.": {"de": "Veröffentlichter Artikel akzeptiert im Journal of Neurophysiology.", "es": "Artículo publicado aceptado en Journal of Neurophysiology."},
    "Thesis: Enhancement of visual discrimination deficits in a mouse model of Parkinson's Disease by low dosages of L-DOPA.": {
        "de": "These: Verbesserung von Beeinträchtigungen der visuellen Diskriminierung in einem Mausmodell der Parkinson-Krankheit durch niedrige Dosen L-DOPA.",
        "es": "Tesis: Mejora de los déficits de discriminación visual en un modelo de ratón de la enfermedad de Parkinson mediante dosis bajas de L-DOPA."
    },
    "Advisor: PhD. Luis Alberto Carrillo Reid.": {"de": "Berater: PhD. Luis Alberto Carrillo Reid.", "es": "Asesor: PhD. Luis Alberto Carrillo Reid."},
    "Scholarship for PhD studies, Mexican Secretariat of Science, Humanities, Technology, and Innovation.": {
        "de": "Stipendium für PhD-Studien, Mexikanisches Sekretariat für Wissenschaft, Geisteswissenschaften, Technologie und Innovation.",
        "es": "Beca para estudios de doctorado, Secretaría Mexicana de Ciencia, Humanidades, Tecnología e Innovación."
    },
    "Behavioral assessment of visual discrimination in a mouse model of Parkinson's Disease.": {
        "de": "Verhaltensbewertung der visuellen Diskriminierung in einem Mausmodell der Parkinson-Krankheit.",
        "es": "Evaluación conductual de la discriminación visual en un modelo de ratón de la enfermedad de Parkinson."
    },
    "GPA: 9.16/10.00, Honorific mention.": {"de": "Durchschnitt: 9,16/10,00, ehrenvolle Erwähnung.", "es": "Promedio: 9,16/10,00, Mención Honorífica."},
    "Scholarship for Master's studies, Mexican Secretariat of Science, Humanities, Technology, and Innovation.": {
        "de": "Stipendium für Masterstudien, Mexikanisches Sekretariat für Wissenschaft, Geisteswissenschaften, Technologie und Innovation.",
        "es": "Beca para estudios de maestría, Secretaría Mexicana de Ciencia, Humanidades, Tecnología e Innovación."
    },
    
    # Languages
    "English": {"de": "Englisch", "es": "Inglés"},
    "C1 (TOEFL iBT 100).": {"de": "C1 (TOEFL iBT 100).", "es": "C1 (TOEFL iBT 100)."},
    "German": {"de": "Deutsch", "es": "Alemán"},
    "A2 (Ongoing studies; A1, Goethe-Zertifikat).": {"de": "A2 (Laufende Studien; A1, Goethe-Zertifikat).", "es": "A2 (Estudios en curso; A1, Certificado Goethe)."},
    "Spanish": {"de": "Spanisch", "es": "Español"},
    "Native.": {"de": "Muttersprache.", "es": "Nativo."},
    
    # Publications & Awards
    "Impaired visually guided behavior in a mouse model of Parkinson's disease": {
        "de": "Beeinträchtigtes visuell gesteuertes Verhalten in einem Mausmodell der Parkinson-Krankheit",
        "es": "Comportamiento guiado visualmente deteriorado en un modelo de ratón de la enfermedad de Parkinson"
    },
    "Journal of Neurophysiology, 2025": {"de": "Journal of Neurophysiology, 2025", "es": "Journal of Neurophysiology, 2025"},
    "DOI: 10.1152/jn.00307.2025": {"de": "DOI: 10.1152/jn.00307.2025", "es": "DOI: 10.1152/jn.00307.2025"},
    "Visual evoked potentials in the Rhesus monkey": {
        "de": "Visuell evozierte Potenziale beim Rhesusaffen",
        "es": "Potenciales evocados visuales en el mono Rhesus"
    },
    "Computed tomography is a feasible method for quantifying bone density in Macaca mulatta": {
        "de": "Computertomographie ist eine praktikable Methode zur Quantifizierung der Knochendichte bei Macaca mulatta",
        "es": "La tomografía computarizada es un método viable para cuantificar la densidad ósea en Macaca mulatta"
    },
    "Veterinary Radiology and Ultrasound, 2018": {"de": "Veterinary Radiology and Ultrasound, 2018", "es": "Radiología Veterinaria y Ultrasonido, 2018"},
    "DOI: 10.1111/vru.12624": {"de": "DOI: 10.1111/vru.12624", "es": "DOI: 10.1111/vru.12624"},
    "Electrical activity of sensory pathways in female and male geriatric Rhesus monkeys (Macaca mulatta), and its relation to oxidative stress": {
        "de": "Elektrische Aktivität sensorischer Bahnen bei älteren weiblichen und männlichen Rhesusaffen (Macaca mulatta) und ihre Beziehung zu oxidativem Stress",
        "es": "Actividad eléctrica de las vías sensoriales en monos Rhesus geriátricos hembras y machos (Macaca mulatta), y su relación con el estrés oxidativo"
    },
    "Experimental Gerontology, 2018": {"de": "Experimental Gerontology, 2018", "es": "Gerontología Experimental, 2018"},
    "DOI: 10.1016/j.exger.2017.11.003": {"de": "DOI: 10.1016/j.exger.2017.11.003", "es": "DOI: 10.1016/j.exger.2017.11.003"},
    "The effect of oxidative stress on brain electrical activity and its repercussions on sensory organization in geriatric Rhesus monkeys in captivity": {
        "de": "Die Auswirkung von oxidativem Stress auf die elektrische Gehirnaktivität und ihre Auswirkungen auf die sensorische Organisation bei älteren Rhesusaffen in Gefangenschaft",
        "es": "El efecto del estrés oxidativo en la actividad eléctrica del cerebro y sus repercusiones en la organización sensorial en monos Rhesus geriátricos en cautiverio"
    },
    "Second place at the 9th state health research forum": {
        "de": "Zweiter Platz auf dem 9. staatlichen Gesundheitsforschungsforum",
        "es": "Segundo lugar en el 9º foro estatal de investigación en salud"
    },
    "Visual discrimination in a mouse model of Parkinson's Disease": {
        "de": "Visuelle Diskriminierung in einem Mausmodell der Parkinson-Krankheit",
        "es": "Discriminación visual en un modelo de ratón de la enfermedad de Parkinson"
    },
    "2024": {"de": "2024", "es": "2024"},
    "Third place at design contest for the Latin American Brain Initiative (LATBrain)": {
        "de": "Dritter Platz im Designwettbewerb der Latin American Brain Initiative (LATBrain)",
        "es": "Tercer lugar en el concurso de diseño de la Iniciativa Latinoamericana del Cerebro (LATBrain)"
    },
    "2021": {"de": "2021", "es": "2021"},
    
    # Footer
    "Last updated: March 15, 2026": {"de": "Zuletzt aktualisiert: 15. März 2026", "es": "Última actualización: 15 de marzo de 2026"},
}

def get_translation(text: str, lang: str = "en") -> str:
    """Get translation for text, return original if not found"""
    if lang == "en":
        return text
    if text in TRANSLATIONS and lang in TRANSLATIONS[text]:
        return TRANSLATIONS[text][lang]
    return text

def create_data_attributes(text: str) -> str:
    """Create data-en, data-de, and data-es attributes"""
    de_text = get_translation(text, "de")
    es_text = get_translation(text, "es")
    return f'data-en="{text}" data-de="{de_text}" data-es="{es_text}"'

def generate_html(yaml_path: str, output_path: str = "index.html") -> None:
    """Generate trilingual HTML CV from YAML file"""
    
    # Read YAML file
    with open(yaml_path, 'r', encoding='utf-8') as f:
        cv_data = yaml.safe_load(f)
    
    cv = cv_data['cv']
    
    # Extract data
    name = cv.get('name', '')
    headline = cv.get('headline', '')
    email = cv.get('email', '')
    website = cv.get('website', '')
    
    # Social networks
    socials = cv.get('social_networks', [])
    
    sections = cv.get('sections', {})
    profile = sections.get('Profile', [''])[0] if 'Profile' in sections else sections.get('summary', [''])[0]
    profile_extra = sections.get('Profile', ['', ''])[1] if 'Profile' in sections and len(sections.get('Profile', [])) > 1 else ''
    expertise = sections.get('Expertise and certifications', [])
    employment = sections.get('Employment history', [])
    education = sections.get('education', [])
    languages = sections.get('languages', [])
    docs = sections.get('Docs and repositories', [])
    publications = sections.get('publications', [])
    awards = sections.get('Other awards', [])
    
    # Start HTML generation
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gamaliel Mendoza-Cuevas - CV</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Source Sans 3', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: #000;
            line-height: 1.6;
            background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            padding: 20px;
        }

        .language-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 10px;
            z-index: 1000;
            background: white;
            padding: 10px 15px;
            border-radius: 50px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .lang-btn {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            opacity: 0.5;
            transition: opacity 0.3s ease;
            padding: 5px;
        }

        .lang-btn.active {
            opacity: 1;
        }

        .lang-btn:hover {
            opacity: 0.8;
        }

        .container {
            max-width: 8.5in;
            margin: 40px auto;
            background: white;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            border-radius: 8px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            position: relative;
            padding-top: 140px;
        }

        .photo {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #004f90;
            position: absolute;
            top: 0;
            left: 0;
        }

        .header-info {
            text-align: center;
        }

        .name {
            font-size: 30pt;
            font-weight: bold;
            color: #004f90;
            margin-bottom: 5px;
        }

        .headline {
            font-size: 10pt;
            color: #004f90;
            margin-bottom: 10px;
        }

        .connections {
            font-size: 9pt;
            color: #004f90;
        }

        .connections a {
            color: #004f90;
            text-decoration: none;
            margin-right: 15px;
        }

        .connections a:hover {
            text-decoration: underline;
        }

        .section {
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 14pt;
            font-weight: bold;
            color: #004f90;
            margin: 20px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 0.5pt solid #004f90;
        }

        .entry {
            margin-bottom: 15px;
        }

        .entry-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 3px;
        }

        .entry-title {
            font-weight: bold;
            font-size: 10pt;
            color: #000;
        }

        .entry-company {
            font-weight: bold;
            color: #000;
        }

        .entry-position {
            font-size: 10pt;
            color: #333;
        }

        .entry-meta {
            font-size: 9pt;
            color: #666;
            text-align: right;
        }

        .entry-institution {
            font-weight: bold;
            color: #000;
        }

        .entry-area {
            font-size: 10pt;
            color: #333;
            display: inline;
        }

        .entry-summary {
            font-size: 10pt;
            color: #333;
            margin: 5px 0;
            font-style: italic;
        }

        .entry-highlights {
            font-size: 10pt;
            color: #333;
            margin: 5px 0 5px 20px;
            list-style: none;
        }

        .entry-highlights li:before {
            content: "• ";
            margin-right: 8px;
            color: #000;
        }

        .entry-highlights li {
            margin: 3px 0;
        }

        .entry-highlights li ul {
            margin: 5px 0 5px 20px;
            list-style: none;
        }

        .entry-highlights li ul li:before {
            content: "◦ ";
            margin-right: 6px;
        }

        .authors {
            font-size: 9pt;
            color: #666;
            margin: 5px 0;
        }

        .journal-info {
            font-size: 9pt;
            color: #666;
            margin: 3px 0;
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .skill-item {
            font-size: 10pt;
        }

        .skill-label {
            font-weight: bold;
            color: #000;
        }

        .skill-details {
            color: #333;
            margin-top: 2px;
        }

        .profile-text {
            font-size: 10pt;
            color: #333;
            margin: 8px 0;
            line-height: 1.5;
        }

        .footer {
            text-align: center;
            font-size: 8pt;
            color: #808080;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }

        .hidden {
            display: none;
        }

        @media (max-width: 800px) {
            .container {
                padding: 20px;
                max-width: 100%;
            }

            .header {
                flex-direction: column;
                text-align: center;
            }

            .header-info {
                text-align: center;
            }

            .skills-grid {
                grid-template-columns: 1fr;
            }

            .language-toggle {
                position: static;
                margin-bottom: 20px;
                justify-content: center;
            }
        }

        @print {
            body {
                background: white;
                padding: 0;
            }

            .container {
                max-width: 100%;
                margin: 0;
                padding: 0;
                box-shadow: none;
                border-radius: 0;
            }

            .language-toggle {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="language-toggle">
        <button class="lang-btn active" data-lang="en" title="English">🇬🇧</button>
        <button class="lang-btn" data-lang="de" title="Deutsch">🇩🇪</button>
        <button class="lang-btn" data-lang="es" title="Español">🇲🇽</button>
    </div>

    <div class="container">
'''
    
    # Header
    html += f'''        <!-- Header -->
        <div class="header">
            <img src="Me.jpeg" alt="{name}" class="photo" onerror="this.style.display='none'">
            <div class="header-info">
                <div class="name" {create_data_attributes(name)}>{name}</div>
                <div class="headline" {create_data_attributes(headline)}>{headline}</div>
                <div class="connections">
                    <a href="mailto:{email}">{email}</a>
'''
    
    if website:
        html += f'                    <a href="{website}" target="_blank">ORCID</a>\n'
    
    for social in socials:
        username = social.get('username', '')
        network = social.get('network', '').lower()
        if network == 'linkedin':
            html += f'                    <a href="https://www.linkedin.com/in/{username}/" target="_blank">LinkedIn</a>\n'
        elif network == 'github':
            html += f'                    <a href="https://github.com/{username}" target="_blank">GitHub</a>\n'
    
    html += '''                </div>
            </div>
        </div>

'''
    
    # Profile Section (for GAMA)
    if profile:
        html += f'''        <!-- Profile Section -->
        <div class="section">
            <div class="section-title" {create_data_attributes("Profile")}>Profile</div>
            <div class="profile-text" {create_data_attributes(profile)}>{profile}</div>
'''
        if profile_extra:
            html += f'            <div class="profile-text" {create_data_attributes(profile_extra)}>{profile_extra}</div>\n'
        html += '''        </div>

'''
    
    # Expertise Section
    if expertise:
        html += '''        <!-- Expertise and Certifications Section -->
        <div class="section">
            <div class="section-title" data-en="Expertise and certifications" data-de="Fachkompetenz und Zertifizierungen" data-es="Experiencia y Certificaciones">Expertise and certifications</div>
'''
        for item in expertise:
            label = item.get('label', '')
            details = item.get('details', '')
            html += f'''            <div class="skill-item">
                <div class="skill-label" {create_data_attributes(label)}>{label}</div>
                <div class="skill-details" {create_data_attributes(details)}>{details}</div>
            </div>
'''
        html += '''        </div>

'''
    
    # Employment Section
    if employment:
        html += '''        <!-- Employment Section -->
        <div class="section">
            <div class="section-title" data-en="Employment history" data-de="Berufsgeschichte" data-es="Historial Laboral">Employment history</div>

'''
        for exp in employment:
            company = exp.get('company', '')
            position = exp.get('position', '')
            location = exp.get('location', '')
            start = exp.get('start_date', '')
            end = exp.get('end_date', '')
            summary_text = exp.get('summary', '')
            highlights = exp.get('highlights', [])
            
            date_range = f"{start} – {end}" if start and end else ""
            meta_text = f"{date_range} | {location}" if date_range and location else location
            
            html += f'''            <div class="entry">
                <div class="entry-header">
                    <div>
                        <div class="entry-company" {create_data_attributes(company)}>{company}</div>
                        <div class="entry-position" {create_data_attributes(position)}>{position}</div>
                    </div>
                    <div class="entry-meta" {create_data_attributes(meta_text)}>{meta_text}</div>
                </div>
'''
            
            if summary_text:
                html += f'                <div class="entry-summary" {create_data_attributes(summary_text)}>{summary_text}</div>\n'
            
            if highlights:
                html += '                <ul class="entry-highlights">\n'
                for highlight in highlights:
                    if isinstance(highlight, str):
                        html += f'                    <li {create_data_attributes(highlight)}>{highlight}</li>\n'
                    elif isinstance(highlight, dict):
                        # Handle nested highlights
                        main_text = highlight.get('', '')
                        if main_text:
                            html += f'                    <li {create_data_attributes(main_text)}>{main_text}\n'
                            nested = highlight.get('', [])
                            if nested:
                                html += '                        <ul>\n'
                                for nested_item in nested if isinstance(nested, list) else [nested]:
                                    html += f'                            <li {create_data_attributes(nested_item)}>{nested_item}</li>\n'
                                html += '                        </ul>\n'
                            html += '                    </li>\n'
                html += '                </ul>\n'
            
            html += '            </div>\n\n'
        
        html += '''</div>

'''
    
    # Education Section
    if education:
        html += '''        <!-- Education Section -->
        <div class="section">
            <div class="section-title" data-en="Education" data-de="Ausbildung" data-es="Educación">Education</div>

'''
        for edu in education:
            institution = edu.get('institution', '')
            area = edu.get('area', '')
            degree = edu.get('degree', '')
            location = edu.get('location', '')
            start = edu.get('start_date', '')
            end = edu.get('end_date', '')
            summary_text = edu.get('summary', '')
            highlights = edu.get('highlights', [])
            
            date_range = f"{start} – {end}" if start and end else ""
            degree_text = degree if degree else ""
            meta_text = f"{degree_text} | {date_range} | {location}" if degree_text and date_range and location else location
            
            html += f'''            <div class="entry">
                <div class="entry-header">
                    <div>
                        <div class="entry-institution" {create_data_attributes(institution)}>{institution}</div>
                        <div class="entry-area" {create_data_attributes(area)}>{area}</div>
                    </div>
                    <div class="entry-meta" {create_data_attributes(meta_text)}>{meta_text}</div>
                </div>
'''
            
            if summary_text:
                html += f'                <div class="entry-summary" {create_data_attributes(summary_text)}>{summary_text}</div>\n'
            
            if highlights:
                html += '                <ul class="entry-highlights">\n'
                for highlight in highlights:
                    html += f'                    <li {create_data_attributes(highlight)}>{highlight}</li>\n'
                html += '                </ul>\n'
            
            html += '            </div>\n\n'
        
        html += '''</div>

'''
    
    # Languages Section
    if languages:
        html += '''        <!-- Languages Section -->
        <div class="section">
            <div class="section-title" data-en="Languages" data-de="Sprachen" data-es="Idiomas">Languages</div>
'''
        for lang in languages:
            label = lang.get('label', '')
            details = lang.get('details', '')
            html += f'''            <div class="skill-item">
                <div class="skill-label" {create_data_attributes(label)}>{label}</div>
                <div class="skill-details" {create_data_attributes(details)}>{details}</div>
            </div>
'''
        html += '''        </div>

'''
    
    # Docs Section
    if docs:
        html += '''        <!-- Docs and Repositories Section -->
        <div class="section">
            <div class="section-title" data-en="Docs and repositories" data-de="Docs und Repositories" data-es="Documentos y Repositorios">Docs and repositories</div>
'''
        for doc in docs:
            label = doc.get('label', '')
            details = doc.get('details', '')
            html += f'''            <div class="skill-item">
                <div class="skill-label" {create_data_attributes(label)}>{label}</div>
                <div class="skill-details"><a href="{details}" target="_blank" {create_data_attributes(details)}>{details}</a></div>
            </div>
'''
        html += '''        </div>

'''
    
    # Publications Section
    if publications:
        html += '''        <!-- Publications Section -->
        <div class="section">
            <div class="section-title" data-en="Publications" data-de="Veröffentlichungen" data-es="Publicaciones">Publications</div>

'''
        for pub in publications:
            title = pub.get('title', '')
            authors = pub.get('authors', [])
            journal = pub.get('journal', '')
            doi = pub.get('doi', '')
            date = pub.get('date', '')
            
            authors_str = ', '.join(str(a) for a in authors) if authors else ''
            
            journal_info = ''
            if journal and date:
                journal_info = f"{journal}, {date}"
                if doi:
                    journal_info += f" | DOI: {doi.replace('https://doi.org/', '')}"
            elif journal:
                journal_info = journal
            elif date:
                journal_info = date
            
            html += f'''            <div class="entry">
                <div class="entry-title" {create_data_attributes(title)}>{title}</div>
'''
            
            if authors_str:
                html += f'                <div class="authors" {create_data_attributes(authors_str)}>{authors_str}</div>\n'
            
            if journal_info:
                html += f'                <div class="journal-info" {create_data_attributes(journal_info)}>{journal_info}</div>\n'
            
            html += '            </div>\n\n'
        
        html += '''</div>

'''
    
    # Awards Section
    if awards:
        html += '''        <!-- Awards Section -->
        <div class="section">
            <div class="section-title" data-en="Awards" data-de="Auszeichnungen" data-es="Premios">Awards</div>

'''
        for award in awards:
            title = award.get('title', '')
            authors = award.get('authors', [])
            journal = award.get('journal', '')
            date = award.get('date', '')
            
            summary_text = ''
            if authors:
                summary_text = ', '.join(str(a) for a in authors if a) if authors else ''
            if journal:
                if summary_text:
                    summary_text += f" • {journal}"
                else:
                    summary_text = journal
            if date:
                if summary_text:
                    summary_text += f" • {date}"
                else:
                    summary_text = date
            
            html += f'''            <div class="entry">
                <div class="entry-title" {create_data_attributes(title)}>{title}</div>
'''
            
            if summary_text:
                html += f'                <div class="entry-summary" {create_data_attributes(summary_text)}>{summary_text}</div>\n'
            
            html += '            </div>\n\n'
        
        html += '''</div>

'''
    
    # Footer
    html += '''        <!-- Footer -->
        <div class="footer">
            <p data-en="Last updated: March 15, 2026" data-de="Zuletzt aktualisiert: 15. März 2026" data-es="Última actualización: 15 de marzo de 2026">Last updated: March 15, 2026</p>
        </div>
    </div>

    <script>
        function switchLanguage(lang) {
            // Update active button
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelector(`[data-lang="${lang}"]`).classList.add('active');

            // Update page content
            document.querySelectorAll('[data-en]').forEach(element => {
                const attr = `data-${lang}`;
                if (element.hasAttribute(attr)) {
                    element.textContent = element.getAttribute(attr);
                }
            });

            // Update document language
            document.documentElement.lang = lang;
            
            // Store preference
            localStorage.setItem('preferredLanguage', lang);
        }

        // Event listeners
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                switchLanguage(this.getAttribute('data-lang'));
            });
        });

        // Load saved preference
        const saved = localStorage.getItem('preferredLanguage') || 'en';
        switchLanguage(saved);
    </script>
</body>
</html>'''
    
    # Write to file
    output_file = Path(output_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Trilingual HTML CV generated successfully: {output_file.absolute()}")

if __name__ == "__main__":
    import sys
    
    yaml_file = "GAMA.yaml"
    output_file = "index.html"
    
    if len(sys.argv) > 1:
        yaml_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    try:
        generate_html(yaml_file, output_file)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
