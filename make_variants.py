"""Generate role-targeted variants of gama_cv.html (DS / MLE / DE).

CSS, section structure and the language-switching script are copied verbatim
from the source; only the content inside sections is rewritten. All facts come
from the source CV - nothing is invented, only reordered and reframed.
"""

import os

SRC = "/Users/gamaliel/Documents/G/DS/Repos/gamindful/gama_cv.html"
OUT_DIR = os.path.dirname(SRC)


# ─── replacement helpers ──────────────────────────────────────────────────────

def repl_line(text, marker, new):
    i = text.find(marker)
    assert i != -1, f"marker not found: {marker[:70]}"
    start = text.rfind("\n", 0, i) + 1
    end = text.find("\n", i)
    return text[:start] + new + text[end:]


def repl_block(text, start_marker, end_marker, new):
    i = text.find(start_marker)
    assert i != -1, f"start not found: {start_marker[:70]}"
    j = text.find(end_marker, i)
    assert j != -1, f"end not found: {end_marker[:70]}"
    return text[:i] + new + text[j + len(end_marker):]


def tri(cls, en, de, es):
    return f'<div class="{cls}" data-en="{en}" data-de="{de}" data-es="{es}">{en}</div>'


def skill(labels, details):
    return ('<div class="skill-item">\n'
            + tri("skill-label", *labels) + "\n"
            + tri("skill-details", *details) + "\n"
            + "</div>")


def li(en, de, es):
    return f'<li data-en="{en}" data-de="{de}" data-es="{es}">{en}</li>'


# ─── shared achievement pool (Cotiviti) ───────────────────────────────────────
# Same facts as the source CV; variants reorder these and override the few
# where the honest framing genuinely differs by role.

B = {
"serving": (
 "Deployed and maintained model-serving endpoints for neural network classifiers, enabling real-time, scalable healthcare data intelligence.",
 "Ich habe Model-Serving-Endpoints für neuronale Netze gebaut und betrieben. Damit bekommen wir Vorhersagen in Echtzeit.",
 "Desplegué y mantuve endpoints de model serving para clasificadores de redes neuronales, habilitando inteligencia de datos de salud escalable y en tiempo real."),

"recsys": (
 "Architected and operationalized end-to-end recommendation systems, driving measurable improvements in healthcare service delivery outcomes.",
 "Ich habe komplette Empfehlungssysteme gebaut und betrieben. Das hat den Gesundheitsservice messbar besser gemacht.",
 "Diseñé y operé sistemas de recomendación de extremo a extremo, impulsando mejoras medibles en los resultados de prestación de servicios de salud."),

"kmeans": (
 "Engineered K-means clustering-based recommendation engines to optimize resource allocation and elevate stakeholder value.",
 "Ich habe Empfehlungssysteme mit K-means-Clustering gebaut. Das spart Ressourcen und hilft allen Partnern.",
 "Desarrollé motores de recomendación basados en agrupamiento K-means para optimizar la asignación de recursos y elevar el valor para las partes interesadas."),

"cnn": (
 "Delivered high-performance CNN-based classification solutions, enhancing predictive accuracy across mission-critical healthcare data assets.",
 "Ich habe starke CNN-Modelle für die Klassifikation gebaut. Die Vorhersagen sind jetzt genauer.",
 "Entregué soluciones de clasificación de alto rendimiento basadas en CNN, mejorando la precisión predictiva en activos de datos de salud críticos."),

"bpe": (
 "Designed and implemented custom Byte-Pair Encoding (BPE) tokenization pipelines, optimizing downstream NLP performance on enterprise healthcare datasets.",
 "Ich habe eigene BPE-Tokenizer-Pipelines gebaut. Das macht die NLP-Analyse von Gesundheitsdaten besser.",
 "Diseñé e implementé pipelines de tokenización personalizados con Byte-Pair Encoding (BPE), optimizando el desempeño de NLP en conjuntos de datos de salud a nivel empresarial."),

"transformers": (
 "Led the fine-tuning of Transformer-based large language models, unlocking actionable insights from complex, unstructured healthcare data.",
 "Ich mache Fine-Tuning von Transformer-Sprachmodellen (LLMs). So finden wir wichtige Informationen in unstrukturierten Daten.",
 "Lideré el fine-tuning de modelos de lenguaje de gran escala basados en Transformers, generando información accionable a partir de datos de salud complejos y no estructurados."),

"etl": (
 "Built and scaled robust ETL pipelines across local and cloud (Databricks) environments, ensuring enterprise-grade data integrity and availability.",
 "Ich habe starke ETL-Pipelines gebaut, lokal und in der Cloud (Databricks). Die Daten sind sicher und immer verfügbar.",
 "Construí y escalé pipelines ETL robustos en entornos locales y en la nube (Databricks), garantizando integridad y disponibilidad de datos a nivel empresarial."),

"mlflow": (
 "Implemented proactive data quality and model performance monitoring frameworks (MLflow), safeguarding reliability and regulatory compliance.",
 "Ich habe ein Monitoring für Datenqualität und Modell-Leistung gebaut (MLflow). Das schützt die Qualität und folgt den Regeln.",
 "Implementé marcos de monitoreo proactivo de calidad de datos y desempeño de modelos (MLflow), salvaguardando la confiabilidad y el cumplimiento normativo."),

"medallion": (
 "Delivered a tiered Bronze/Silver/Gold (medallion) data architecture, establishing a single source of truth to accelerate organization-wide analytics.",
 "Ich habe Daten in drei Stufen organisiert: Bronze, Silber und Gold (Medallion). So hat die Firma eine zentrale Datenquelle.",
 "Implementé una arquitectura de datos por niveles Bronce/Plata/Oro (medallion), estableciendo una fuente única de verdad para acelerar la analítica a nivel organizacional."),

"apps": (
 "Developed and deployed Python-based, ML-powered applications, translating advanced analytics into scalable, business-ready healthcare solutions.",
 "Ich habe Python-Anwendungen mit Machine Learning gebaut und deployed. Diese Lösungen helfen direkt im Gesundheitswesen.",
 "Desarrollé y desplegué aplicaciones basadas en Python e impulsadas por Machine Learning, traduciendo analítica avanzada en soluciones de salud escalables y listas para el negocio."),
}

# skill categories reused across variants
SOFT = (("Professional / Soft Skills", "Berufliche &amp; Soziale Kompetenzen", "Habilidades Profesionales / Blandas"),
        ("Remote Work · Cross-functional Collaboration · Executive Reporting · Data Visualization · Stakeholder Communication · Bilingual (EN/ES) · German (A2)",
         "Remote-Arbeit · Bereichsübergreifende Zusammenarbeit · Berichtswesen für Führungskräfte · Datenvisualisierung · Kommunikation mit Stakeholdern · Zweisprachig (EN/ES) · Deutsch (A2)",
         "Trabajo Remoto · Colaboración Multifuncional · Reportes Ejecutivos · Visualización de Datos · Comunicación con Stakeholders · Bilingüe (EN/ES) · Alemán (A2)"))

DOMAIN = (("Domain", "Fachgebiet", "Dominio"),
          ("Healthcare Analytics · Healthcare Data · Neuroscience · Translational Research · Signal Processing",
           "Gesundheitsanalytik · Gesundheitsdaten · Neurowissenschaften · Translationale Forschung · Signalverarbeitung",
           "Analítica de Salud · Datos de Salud · Neurociencia · Investigación Traslacional · Procesamiento de Señales"))


# ─── variant definitions ──────────────────────────────────────────────────────

VARIANTS = {}

VARIANTS["DS"] = dict(
 title="Gamaliel Mendoza-Cuevas - Data Scientist CV",
 headline=(
  "PhD in Neuroscience and Data Scientist delivering predictive modeling, statistical inference, and machine learning for healthcare analytics.",
  "PhD in Neurowissenschaften und Data Scientist. Ich mache Vorhersage-Modelle, Statistik und Machine Learning für die Gesundheitsanalyse.",
  "Doctor en Neurociencia y Científico de Datos, especializado en modelado predictivo, inferencia estadística y machine learning para analítica de salud."),
 overview=(
  """A Data Scientist with a PhD in Neuroscience and a proven track record of translating complex biological and healthcare data into predictive models and actionable, data-driven insights. I pair rigorous statistical inference and experimental design with modern machine learning to answer business questions end to end.
I own the full analytical lifecycle — exploratory data analysis, feature engineering, model development, validation, and executive-level reporting — delivering measurable, stakeholder-ready outcomes through robust visualizations. My peer-reviewed publication record demonstrates hypothesis-driven analysis and the ability to communicate technical findings clearly to stakeholders at every organizational level, including senior leadership.""",
  """Ich bin Data Scientist und habe einen Doktortitel (PhD) in Neurowissenschaften. Ich mache aus komplexen Gesundheitsdaten klare Vorhersage-Modelle. Ich verbinde Statistik und Experiment-Design mit modernem Machine Learning.
Ich mache den ganzen Analyse-Prozess: Datenanalyse, Feature Engineering, Modell-Entwicklung, Validierung und Berichte für das Management. Meine Grafiken sind klar und die Ergebnisse sind messbar. Ich veröffentliche auch wissenschaftliche Artikel. Das zeigt: Ich erkläre technische Ergebnisse gut, auch für die Geschäftsführung.""",
  """Científico de Datos con Doctorado en Neurociencia y una trayectoria comprobada en la traducción de datos biológicos y de salud complejos en modelos predictivos e información accionable. Combino inferencia estadística rigurosa y diseño experimental con machine learning moderno para responder preguntas de negocio de extremo a extremo.
Gestiono el ciclo analítico completo — análisis exploratorio, ingeniería de características, desarrollo de modelos, validación y reportes de nivel ejecutivo — entregando resultados medibles mediante visualizaciones robustas. Mi trayectoria de publicaciones arbitradas demuestra análisis basado en hipótesis y la capacidad de comunicar hallazgos técnicos con claridad en todos los niveles de la organización, incluyendo la alta dirección."""),
 skills=[
  (("Data Science &amp; Machine Learning", "Datenwissenschaft &amp; Machine Learning", "Ciencia de Datos y Machine Learning"),
   ("Data Science · Machine Learning · Predictive Modeling · Statistical Modeling · Deep Learning · Neural Networks · Computer Vision (CNNs) · NLP · Transformers · LLM Fine-Tuning · Recommender Systems · Clustering (K-Means) · Feature Engineering · Model Evaluation · Explainable AI",
    "Data Science · Maschinelles Lernen · Prädiktive Modellierung · Statistische Modellierung · Deep Learning · Neuronale Netze · Computer Vision (CNNs) · NLP · Transformers · LLM Fine-Tuning · Empfehlungssysteme · Clustering (K-Means) · Feature Engineering · Modellbewertung · Erklärbare KI",
    "Ciencia de Datos · Aprendizaje Automático · Modelado Predictivo · Modelado Estadístico · Deep Learning · Redes Neuronales · Visión por Computadora (CNNs) · NLP · Transformers · Fine-Tuning de LLM · Sistemas de Recomendación · Clustering (K-Means) · Ingeniería de Características · Evaluación de Modelos · IA Explicable")),
  (("Analytics &amp; Research", "Analytik &amp; Forschung", "Analítica e Investigación"),
   ("Data Analytics · Statistical Inference · Hypothesis Testing · Experimental Design · Exploratory Data Analysis · Behavioral Analytics · Signal Processing · Research Design · Data Visualization · Scientific Writing",
    "Datenanalytik · Statistische Inferenz · Hypothesentests · Experimentelles Design · Explorative Datenanalyse · Verhaltensanalytik · Signalverarbeitung · Forschungsdesign · Datenvisualisierung · Wissenschaftliches Schreiben",
    "Analítica de Datos · Inferencia Estadística · Pruebas de Hipótesis · Diseño Experimental · Análisis Exploratorio de Datos · Analítica Conductual · Procesamiento de Señales · Diseño de Investigación · Visualización de Datos · Redacción Científica")),
  (("Languages &amp; Tools", "Sprachen &amp; Tools", "Lenguajes y Herramientas"),
   ("Python · SQL · R · MATLAB · Spark · Databricks · PyTorch · TensorFlow · Scikit-learn · Transformers · MLflow · Hadoop · Oracle · MySQL · Git · GitHub · Bitbucket",
    "Python · SQL · R · MATLAB · Spark · Databricks · PyTorch · TensorFlow · Scikit-learn · Transformers · MLflow · Hadoop · Oracle · MySQL · Git · GitHub · Bitbucket",
    "Python · SQL · R · MATLAB · Spark · Databricks · PyTorch · TensorFlow · Scikit-learn · Transformers · MLflow · Hadoop · Oracle · MySQL · Git · GitHub · Bitbucket")),
  (("Data Engineering", "Data Engineering", "Ingeniería de Datos"),
   ("ETL Pipelines · Data Warehousing · Data Architecture · Data Quality · Feature Pipelines · Model Deployment",
    "ETL-Pipelines · Data Warehousing · Datenarchitektur · Datenqualität · Feature-Pipelines · Modell-Deployment",
    "Pipelines ETL · Almacenamiento de Datos · Arquitectura de Datos · Calidad de Datos · Pipelines de Características · Despliegue de Modelos")),
  SOFT,
  DOMAIN,
 ],
 position=(
  "Associate Data Scientist — Healthcare Analytics &amp; Applied Machine Learning.",
  "Junior-Datenwissenschaftler — Gesundheitsanalytik und angewandtes Machine Learning.",
  "Científico de Datos Junior — Analítica de Salud y Machine Learning Aplicado."),
 order=["recsys", "kmeans", "cnn", "transformers", "bpe", "mlflow", "serving", "etl", "medallion", "apps"],
 overrides={},
 phd_summary=(
  "Doctoral research portfolio spanning experimental design, statistical modeling, behavioral analytics, neurophysiology, and translational neuroscience, delivered within a top-tier Biomedical Sciences program.",
  "Meine Doktorarbeit umfasst Experiment-Design, statistische Modelle, Verhaltensanalyse, Neurophysiologie und translationale Neurowissenschaft. Das Programm heißt Biomedizinische Wissenschaften und ist sehr gut.",
  "Portafolio de investigación doctoral que abarca diseño experimental, modelado estadístico, analítica conductual, neurofisiología y neurociencia traslacional, desarrollado dentro de un programa de Ciencias Biomédicas de primer nivel."),
 msc_summary=(
  "Designed and executed behavioral experiments with statistical analysis of visual discrimination performance within a translational Parkinson's Disease model.",
  "Ich habe Verhaltens-Experimente geplant und gemacht. Ich habe die Daten statistisch ausgewertet, in einem Parkinson-Modell.",
  "Diseñé y ejecuté experimentos conductuales con análisis estadístico del desempeño de discriminación visual dentro de un modelo traslacional de la enfermedad de Parkinson."),
 bio_summary=(
  "Drove data standardization and statistical modeling of neuro- and physiological metrics, published in the peer-reviewed literature.",
  "Ich habe Daten standardisiert und statistisch modelliert: neuro- und physiologische Werte. Die Ergebnisse wurden veröffentlicht.",
  "Impulsé la estandarización de datos y el modelado estadístico de métricas neuro- y fisiológicas, con publicación arbitrada."),
 aprex_summary=(
  "Led standardization protocols and statistical analysis of neurophysiological benchmark data.",
  "Ich habe Standard-Protokolle geleitet und neurophysiologische Daten statistisch ausgewertet.",
  "Lideré protocolos de estandarización y el análisis estadístico de datos neurofisiológicos de referencia."),
)

VARIANTS["MLE"] = dict(
 title="Gamaliel Mendoza-Cuevas - Machine Learning Engineer CV",
 headline=(
  "Machine Learning Engineer building, deploying, and monitoring production-grade deep learning models and scalable ML pipelines.",
  "Machine Learning Engineer. Ich baue, deploye und überwache Deep-Learning-Modelle und skalierbare ML-Pipelines in der Produktion.",
  "Ingeniero de Machine Learning que construye, despliega y monitorea modelos de deep learning en producción y pipelines de ML escalables."),
 overview=(
  """A Machine Learning Engineer with a PhD in Neuroscience, focused on taking models from prototype to production. I build end-to-end ML systems — training pipelines, model-serving endpoints, experiment tracking, and performance monitoring — across Databricks, Spark, and Python.
My work spans deep learning architectures (CNNs, Transformers, LLM fine-tuning) and classical machine learning, engineered for reliability, scalability, and measurable business impact in enterprise healthcare environments. I instrument models with MLflow for reproducibility and monitoring, and collaborate through Git, GitHub, and Bitbucket within cross-functional engineering teams.""",
  """Ich bin Machine Learning Engineer mit einem Doktortitel (PhD) in Neurowissenschaften. Ich bringe Modelle von der Idee bis in die Produktion. Ich baue komplette ML-Systeme: Training-Pipelines, Model-Serving-Endpoints, Experiment-Tracking und Monitoring. Ich arbeite mit Databricks, Spark und Python.
Ich nutze Deep Learning (CNNs, Transformer, LLM Fine-Tuning) und klassisches Machine Learning. Meine Systeme sind stabil, skalierbar und bringen einen messbaren Nutzen. Mit MLflow sorge ich für Reproduzierbarkeit und Monitoring. Ich arbeite mit Git, GitHub und Bitbucket im Team zusammen.""",
  """Ingeniero de Machine Learning con Doctorado en Neurociencia, enfocado en llevar modelos del prototipo a producción. Construyo sistemas de ML de extremo a extremo — pipelines de entrenamiento, endpoints de model serving, seguimiento de experimentos y monitoreo de desempeño — sobre Databricks, Spark y Python.
Mi trabajo abarca arquitecturas de deep learning (CNN, Transformers, fine-tuning de LLM) y machine learning clásico, diseñados para confiabilidad, escalabilidad e impacto de negocio medible en entornos de salud a nivel empresarial. Instrumento los modelos con MLflow para reproducibilidad y monitoreo, y colaboro mediante Git, GitHub y Bitbucket en equipos de ingeniería multifuncionales."""),
 skills=[
  (("Machine Learning Engineering", "Machine Learning Engineering", "Ingeniería de Machine Learning"),
   ("Model Deployment · Model Serving · Real-Time Inference · ML Pipelines · MLOps · MLflow · Experiment Tracking · Model Monitoring · Model Lifecycle · Reproducibility · Scalable Systems",
    "Modell-Deployment · Model Serving · Echtzeit-Inferenz · ML-Pipelines · MLOps · MLflow · Experiment-Tracking · Modell-Monitoring · Modell-Lebenszyklus · Reproduzierbarkeit · Skalierbare Systeme",
    "Despliegue de Modelos · Model Serving · Inferencia en Tiempo Real · Pipelines de ML · MLOps · MLflow · Seguimiento de Experimentos · Monitoreo de Modelos · Ciclo de Vida de Modelos · Reproducibilidad · Sistemas Escalables")),
  (("Deep Learning &amp; ML", "Deep Learning &amp; ML", "Deep Learning y ML"),
   ("Deep Learning · Neural Networks · Computer Vision (CNNs) · NLP · Transformers · LLM Fine-Tuning · Tokenization (BPE) · Recommender Systems · Clustering (K-Means) · Predictive Modeling · Explainable AI",
    "Deep Learning · Neuronale Netze · Computer Vision (CNNs) · NLP · Transformers · LLM Fine-Tuning · Tokenisierung (BPE) · Empfehlungssysteme · Clustering (K-Means) · Prädiktive Modellierung · Erklärbare KI",
    "Deep Learning · Redes Neuronales · Visión por Computadora (CNNs) · NLP · Transformers · Fine-Tuning de LLM · Tokenización (BPE) · Sistemas de Recomendación · Clustering (K-Means) · Modelado Predictivo · IA Explicable")),
  (("Languages &amp; Tools", "Sprachen &amp; Tools", "Lenguajes y Herramientas"),
   ("Python · PyTorch · TensorFlow · Scikit-learn · Transformers · MLflow · Spark · Databricks · SQL · R · MATLAB · Hadoop · Oracle · MySQL · Git · GitHub · Bitbucket",
    "Python · PyTorch · TensorFlow · Scikit-learn · Transformers · MLflow · Spark · Databricks · SQL · R · MATLAB · Hadoop · Oracle · MySQL · Git · GitHub · Bitbucket",
    "Python · PyTorch · TensorFlow · Scikit-learn · Transformers · MLflow · Spark · Databricks · SQL · R · MATLAB · Hadoop · Oracle · MySQL · Git · GitHub · Bitbucket")),
  (("Data Engineering", "Data Engineering", "Ingeniería de Datos"),
   ("ETL Pipelines · Feature Pipelines · Data Architecture · Data Warehousing · Data Quality · Batch Processing · Cloud &amp; On-Premise Environments",
    "ETL-Pipelines · Feature-Pipelines · Datenarchitektur · Data Warehousing · Datenqualität · Stapelverarbeitung · Cloud- und On-Premise-Umgebungen",
    "Pipelines ETL · Pipelines de Características · Arquitectura de Datos · Almacenamiento de Datos · Calidad de Datos · Procesamiento por Lotes · Entornos Cloud y On-Premise")),
  SOFT,
  DOMAIN,
 ],
 position=(
  "Associate Data Scientist — Applied Machine Learning &amp; Model Deployment.",
  "Junior-Datenwissenschaftler — Angewandtes Machine Learning und Modell-Deployment.",
  "Científico de Datos Junior — Machine Learning Aplicado y Despliegue de Modelos."),
 order=["serving", "cnn", "transformers", "bpe", "mlflow", "recsys", "kmeans", "apps", "etl", "medallion"],
 overrides={
  "mlflow": (
   "Instrumented experiment tracking, model performance monitoring, and reproducibility with MLflow, safeguarding model quality in production.",
   "Ich nutze MLflow für Experiment-Tracking, Modell-Monitoring und Reproduzierbarkeit. So bleibt die Qualität in der Produktion gut.",
   "Instrumenté el seguimiento de experimentos, el monitoreo de desempeño de modelos y la reproducibilidad con MLflow, salvaguardando la calidad en producción."),
 },
 phd_summary=(
  "Doctoral research portfolio spanning computational modeling, signal processing, behavioral analytics, and neurophysiology, delivered within a top-tier Biomedical Sciences program.",
  "Meine Doktorarbeit umfasst computergestützte Modelle, Signalverarbeitung, Verhaltensanalyse und Neurophysiologie. Das Programm heißt Biomedizinische Wissenschaften und ist sehr gut.",
  "Portafolio de investigación doctoral que abarca modelado computacional, procesamiento de señales, analítica conductual y neurofisiología, desarrollado dentro de un programa de Ciencias Biomédicas de primer nivel."),
 msc_summary=(
  "Built and validated quantitative models of visual discrimination performance within a translational Parkinson's Disease model.",
  "Ich habe quantitative Modelle für visuelle Diskriminierung gebaut und validiert, in einem Parkinson-Modell.",
  "Construí y validé modelos cuantitativos del desempeño de discriminación visual dentro de un modelo traslacional de la enfermedad de Parkinson."),
 bio_summary=(
  "Automated quantitative analysis of medical imaging data and delivered statistical models published in the peer-reviewed literature.",
  "Ich habe die Analyse von medizinischen Bildern automatisiert. Ich habe statistische Modelle gebaut und veröffentlicht.",
  "Automaticé el análisis cuantitativo de datos de imagenología médica y entregué modelos estadísticos con publicación arbitrada."),
 aprex_summary=(
  "Built signal-processing workflows for neurophysiological data and standardized benchmark values for downstream analysis.",
  "Ich habe Workflows für die Signalverarbeitung gebaut. Ich habe Standard-Werte für die weitere Analyse definiert.",
  "Construí flujos de procesamiento de señales para datos neurofisiológicos y estandaricé valores de referencia para análisis posteriores."),
)

VARIANTS["DE"] = dict(
 title="Gamaliel Mendoza-Cuevas - Data Engineer CV",
 headline=(
  "Data Engineer building scalable ETL pipelines, medallion data architectures, and analytics-ready data platforms on Databricks and Spark.",
  "Data Engineer. Ich baue skalierbare ETL-Pipelines, Medallion-Architekturen und Datenplattformen mit Databricks und Spark.",
  "Ingeniero de Datos que construye pipelines ETL escalables, arquitecturas de datos medallion y plataformas listas para analítica sobre Databricks y Spark."),
 overview=(
  """A Data Engineer with a PhD in Neuroscience and hands-on ownership of enterprise data platforms. I design and operate ETL pipelines, tiered medallion (Bronze/Silver/Gold) architectures, and data quality frameworks that make large healthcare datasets reliable, governed, and analytics-ready.
I work across Databricks, Spark, SQL, and Python to deliver a single source of truth that accelerates analytics and machine learning organization-wide. I partner with analysts, data scientists, and senior leadership to turn raw, unstructured data into well-modeled datasets, communicating clearly at every organizational level.""",
  """Ich bin Data Engineer und habe einen Doktortitel (PhD) in Neurowissenschaften. Ich baue und betreibe ETL-Pipelines, Medallion-Architekturen (Bronze, Silber, Gold) und Systeme für Datenqualität. So werden große Gesundheitsdaten zuverlässig und bereit für die Analyse.
Ich arbeite mit Databricks, Spark, SQL und Python. Die Firma bekommt eine zentrale Datenquelle für Analyse und Machine Learning. Ich arbeite mit Analysten, Data Scientists und der Geschäftsführung zusammen. Aus rohen Daten mache ich saubere und gut modellierte Datensätze.""",
  """Ingeniero de Datos con Doctorado en Neurociencia y responsabilidad directa sobre plataformas de datos empresariales. Diseño y opero pipelines ETL, arquitecturas medallion por niveles (Bronce/Plata/Oro) y marcos de calidad de datos que hacen que grandes conjuntos de datos de salud sean confiables, gobernados y estén listos para analítica.
Trabajo con Databricks, Spark, SQL y Python para entregar una fuente única de verdad que acelera la analítica y el machine learning a nivel organizacional. Colaboro con analistas, científicos de datos y la alta dirección para convertir datos crudos y no estructurados en conjuntos de datos bien modelados, comunicando con claridad en todos los niveles de la organización."""),
 skills=[
  (("Data Engineering", "Data Engineering", "Ingeniería de Datos"),
   ("Data Engineering · ETL Pipelines · Data Warehousing · Data Architecture · Medallion Architecture (Bronze/Silver/Gold) · Data Modeling · Data Quality · Data Integrity · Data Governance · Batch Processing · Single Source of Truth",
    "Data Engineering · ETL-Pipelines · Data Warehousing · Datenarchitektur · Medallion-Architektur (Bronze/Silber/Gold) · Datenmodellierung · Datenqualität · Datenintegrität · Data Governance · Stapelverarbeitung · Zentrale Datenquelle",
    "Ingeniería de Datos · Pipelines ETL · Almacenamiento de Datos · Arquitectura de Datos · Arquitectura Medallion (Bronce/Plata/Oro) · Modelado de Datos · Calidad de Datos · Integridad de Datos · Gobierno de Datos · Procesamiento por Lotes · Fuente Única de Verdad")),
  (("Platforms &amp; Databases", "Plattformen &amp; Datenbanken", "Plataformas y Bases de Datos"),
   ("Databricks · Spark · Hadoop · Oracle · MySQL · SQL · MLflow · Cloud &amp; On-Premise Environments",
    "Databricks · Spark · Hadoop · Oracle · MySQL · SQL · MLflow · Cloud- und On-Premise-Umgebungen",
    "Databricks · Spark · Hadoop · Oracle · MySQL · SQL · MLflow · Entornos Cloud y On-Premise")),
  (("Languages &amp; Tools", "Sprachen &amp; Tools", "Lenguajes y Herramientas"),
   ("SQL · Python · Spark · R · MATLAB · PyTorch · TensorFlow · Scikit-learn · Git · GitHub · Bitbucket",
    "SQL · Python · Spark · R · MATLAB · PyTorch · TensorFlow · Scikit-learn · Git · GitHub · Bitbucket",
    "SQL · Python · Spark · R · MATLAB · PyTorch · TensorFlow · Scikit-learn · Git · GitHub · Bitbucket")),
  (("Analytics &amp; ML", "Analytik &amp; ML", "Analítica y ML"),
   ("Data Analytics · Statistical Modeling · Machine Learning · Deep Learning · Model Deployment · Model Serving · Feature Pipelines · Data Visualization",
    "Datenanalytik · Statistische Modellierung · Maschinelles Lernen · Deep Learning · Modell-Deployment · Model Serving · Feature-Pipelines · Datenvisualisierung",
    "Analítica de Datos · Modelado Estadístico · Aprendizaje Automático · Deep Learning · Despliegue de Modelos · Model Serving · Pipelines de Características · Visualización de Datos")),
  SOFT,
  DOMAIN,
 ],
 position=(
  "Associate Data Scientist — Data Engineering &amp; Platform Architecture.",
  "Junior-Datenwissenschaftler — Data Engineering und Daten-Architektur.",
  "Científico de Datos Junior — Ingeniería de Datos y Arquitectura de Plataforma."),
 order=["etl", "medallion", "mlflow", "apps", "serving", "recsys", "kmeans", "cnn", "bpe", "transformers"],
 overrides={
  "mlflow": (
   "Implemented proactive data quality monitoring frameworks (MLflow), safeguarding data integrity, pipeline reliability, and regulatory compliance.",
   "Ich habe ein System für Datenqualität gebaut (MLflow). Das schützt die Daten, die Pipelines und folgt den Regeln.",
   "Implementé marcos de monitoreo proactivo de calidad de datos (MLflow), salvaguardando la integridad de los datos, la confiabilidad de los pipelines y el cumplimiento normativo."),
 },
 phd_summary=(
  "Doctoral research portfolio spanning large-scale experimental data acquisition and processing, behavioral analytics, neurophysiology, and translational neuroscience, delivered within a top-tier Biomedical Sciences program.",
  "Meine Doktorarbeit umfasst die Erfassung und Verarbeitung von großen Datenmengen, Verhaltensanalyse, Neurophysiologie und translationale Neurowissenschaft. Das Programm heißt Biomedizinische Wissenschaften und ist sehr gut.",
  "Portafolio de investigación doctoral que abarca la adquisición y el procesamiento de datos experimentales a gran escala, analítica conductual, neurofisiología y neurociencia traslacional, desarrollado dentro de un programa de Ciencias Biomédicas de primer nivel."),
 msc_summary=(
  "Structured, processed, and analyzed behavioral datasets measuring visual discrimination performance within a translational Parkinson's Disease model.",
  "Ich habe Verhaltens-Daten strukturiert, verarbeitet und analysiert, in einem Parkinson-Modell.",
  "Estructuré, procesé y analicé conjuntos de datos conductuales para medir el desempeño de discriminación visual dentro de un modelo traslacional de la enfermedad de Parkinson."),
 bio_summary=(
  "Standardized and structured imaging datasets, building reproducible processing workflows for neuro- and physiological metrics.",
  "Ich habe Bild-Datensätze standardisiert und strukturiert. Ich habe reproduzierbare Workflows für die Verarbeitung gebaut.",
  "Estandaricé y estructuré conjuntos de datos de imagenología, construyendo flujos de procesamiento reproducibles para métricas neuro- y fisiológicas."),
 aprex_summary=(
  "Led data standardization protocols and structured acquisition of neurophysiological benchmark datasets.",
  "Ich habe Standard-Protokolle für Daten geleitet und neurophysiologische Datensätze strukturiert erfasst.",
  "Lideré protocolos de estandarización de datos y la adquisición estructurada de conjuntos de datos neurofisiológicos de referencia."),
)


# ─── build ────────────────────────────────────────────────────────────────────

def build(src, v):
    t = src

    t = repl_line(t, "<title>", f"<title>{v['title']}</title>")
    t = repl_line(t, '<div class="headline"', tri("headline", *v["headline"]))

    t = repl_block(t, '<div class="letter-content" data-en="A PhD in Neuroscience',
                   "executive-level reporting.</div>",
                   tri("letter-content", *v["overview"]))

    skills_html = "\n".join(skill(labels, details) for labels, details in v["skills"])
    t = repl_block(t, '<div class="skill-item">', "<!-- Employment Section -->",
                   skills_html + "\n</div>\n\n<!-- Employment Section -->")

    t = repl_line(t, '<div class="entry-position" data-en="Associate Data Scientist',
                  tri("entry-position", *v["position"]))

    bullets = [li(*v["overrides"].get(k, B[k])) for k in v["order"]]
    t = repl_block(t, '<ul class="entry-highlights">', "</ul>",
                   '<ul class="entry-highlights">\n' + "\n".join(bullets) + "\n</ul>")

    t = repl_line(t, '<div class="entry-summary" data-en="Drove standardization',
                  tri("entry-summary", *v["bio_summary"]))
    t = repl_line(t, '<div class="entry-summary" data-en="Led standardization protocols',
                  tri("entry-summary", *v["aprex_summary"]))
    t = repl_line(t, '<div class="entry-summary" data-en="Doctoral research portfolio',
                  tri("entry-summary", *v["phd_summary"]))
    t = repl_line(t, '<div class="entry-summary" data-en="Led behavioral assessment',
                  tri("entry-summary", *v["msc_summary"]))

    return t


if __name__ == "__main__":
    src = open(SRC, encoding="utf-8").read()
    for suffix, v in VARIANTS.items():
        assert len(v["order"]) == len(B), "every achievement must be kept"
        out = os.path.join(OUT_DIR, f"gama_cv_{suffix}.html")
        html = build(src, v)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"OK  {os.path.basename(out)}  ({len(html):,} chars)")
