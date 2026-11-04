"""
Atelier Lettre IB — générateur de lettre de motivation investment banking (FR / EN).
Auteur du contenu : Alexis Hamdi (d'après son CV).

Lancement :
    python3 lettre_ib.py

Dépendances :
    - Tkinter (inclus avec Python ; sur Mac avec Homebrew : `brew install python-tk`)
    - Optionnel : python-docx pour un vrai .docx  ->  pip install python-docx
      (sans lui, l'export Word produit un .doc que Word ouvre normalement)
"""

import datetime
import json
import platform
import re
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
    import docx  # python-docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


# =====================================================================
# 1. PROFIL — tiré du CV. Modifie ici si ton CV évolue.
# =====================================================================
PROFILE = {
    "name": "Alexis Hamdi",
    "phone": "+33 7 81 62 64 12",
    "email": "alexishmd@outlook.fr",
    "linkedin": "linkedin.com/in/alexis-hd",
}

SAVE_FILE = Path(__file__).with_name("lettres_ib_versions.json")


# =====================================================================
# 2. BIBLIOTHÈQUE DE CONTENU (FR / EN)
#    why = attrait pour le métier, bring = ce que tu apportes,
#    env = environnement (utilisé dans la phrase sur la résistance à la pression).
#    Les formulations françaises sont neutres (aucun accord masculin/féminin).
# =====================================================================
SECTORS = {
    "ma": {
        "label": "Fusions & Acquisitions (M&A)",
        "team": {"fr": "M&A", "en": "M&A"},
        "why": {
            "fr": "Le conseil en fusions-acquisitions m'attire tout particulièrement, car il place l'analyse financière au cœur de décisions stratégiques qui transforment durablement les entreprises.",
            "en": "M&A advisory particularly appeals to me because it places financial analysis at the heart of strategic decisions that durably reshape companies.",
        },
        "bring": {
            "fr": "Ces expériences me donnent des bases solides pour contribuer à la valorisation de sociétés (DCF, multiples boursiers, transactions comparables), à la construction de modèles financiers, à la préparation de pitch books et d'information memorandums, ainsi qu'au suivi des processus de due diligence.",
            "en": "These experiences give me a solid foundation to contribute to company valuation (DCF, trading and transaction comparables), financial modelling, the preparation of pitch books and information memoranda, and the management of due diligence processes.",
        },
        "env": {"fr": "l'exécution de transactions", "en": "deal execution"},
    },
    "ecm": {
        "label": "Equity Capital Markets (ECM)",
        "team": {"fr": "Equity Capital Markets", "en": "Equity Capital Markets"},
        "why": {
            "fr": "Les marchés actions m'attirent par la combinaison qu'ils exigent entre analyse fondamentale, lecture fine des conditions de marché et dialogue avec les investisseurs, notamment lors d'introductions en bourse et d'augmentations de capital.",
            "en": "Equity capital markets appeal to me for the combination they require between fundamental analysis, a sharp reading of market conditions and dialogue with investors, particularly on IPOs and capital increases.",
        },
        "bring": {
            "fr": "Ces expériences me permettent de contribuer à la valorisation d'émetteurs, au suivi quotidien des marchés et des opérations comparables, à la préparation de supports investisseurs et à l'exécution d'IPO, d'augmentations de capital et de placements accélérés.",
            "en": "These experiences allow me to contribute to issuer valuation, daily market and precedent monitoring, the preparation of investor materials, and the execution of IPOs, rights issues and accelerated bookbuilds.",
        },
        "env": {"fr": "les opérations de marché", "en": "live market transactions"},
    },
    "dcm": {
        "label": "Debt Capital Markets (DCM)",
        "team": {"fr": "Debt Capital Markets", "en": "Debt Capital Markets"},
        "why": {
            "fr": "Les marchés de dette me passionnent, car ils se situent au croisement de l'analyse de crédit, de la structuration et de la connaissance des investisseurs, dans un environnement de taux qui reste déterminant pour les émetteurs.",
            "en": "Debt capital markets fascinate me because they sit at the crossroads of credit analysis, structuring and investor knowledge, in a rate environment that remains decisive for issuers.",
        },
        "bring": {
            "fr": "Ces expériences me permettent de contribuer à l'analyse de la qualité de crédit des émetteurs, au suivi du marché obligataire, à la préparation de présentations de financement et à l'exécution d'émissions obligataires.",
            "en": "These experiences allow me to contribute to issuer credit analysis, bond market monitoring, the preparation of financing presentations and the execution of bond issues.",
        },
        "env": {"fr": "les marchés de capitaux", "en": "capital markets"},
    },
    "levfin": {
        "label": "Leveraged & Acquisition Finance",
        "team": {"fr": "Leveraged Finance", "en": "Leveraged Finance"},
        "why": {
            "fr": "Le financement d'acquisitions à effet de levier m'attire par sa dimension très analytique : il impose de comprendre en profondeur la capacité d'un actif à générer du cash et à supporter une structure de dette.",
            "en": "Leveraged and acquisition finance appeals to me for its highly analytical nature: it requires an in-depth understanding of an asset's ability to generate cash and sustain a debt structure.",
        },
        "bring": {
            "fr": "Ces expériences me permettent de contribuer à la modélisation de LBO, à l'analyse de la capacité de remboursement (levier, couverture des intérêts, covenants), à la structuration des tranches de dette et à la rédaction de notes de crédit.",
            "en": "These experiences allow me to contribute to LBO modelling, debt capacity analysis (leverage, interest cover, covenants), the structuring of debt tranches and the drafting of credit papers.",
        },
        "env": {"fr": "la structuration de financements", "en": "financing execution"},
    },
    "rx": {
        "label": "Restructuring",
        "team": {"fr": "Restructuring", "en": "Restructuring"},
        "why": {
            "fr": "Le restructuring m'attire, car il exige de comprendre rapidement la situation financière d'une entreprise sous tension et de bâtir, avec l'ensemble des parties prenantes, des solutions qui préservent sa valeur.",
            "en": "Restructuring appeals to me because it requires quickly understanding the financial position of a distressed company and building, with all stakeholders, solutions that preserve its value.",
        },
        "bring": {
            "fr": "Ces expériences me permettent de contribuer à l'analyse de la liquidité et des prévisions de trésorerie à 13 semaines, à la revue des structures de dette, à la modélisation de scénarios de refinancement et à la préparation de supports pour créanciers et actionnaires.",
            "en": "These experiences allow me to contribute to liquidity analysis and 13-week cash flow forecasts, the review of capital structures, the modelling of refinancing scenarios and the preparation of materials for creditors and shareholders.",
        },
        "env": {"fr": "les situations complexes", "en": "complex, time-critical situations"},
    },
    "pe": {
        "label": "Private Equity",
        "team": {"fr": "investissement", "en": "investment"},
        "why": {
            "fr": "Le private equity m'attire par la responsabilité qu'il implique : identifier les meilleures opportunités, en évaluer finement les risques, puis accompagner les équipes dirigeantes dans la création de valeur.",
            "en": "Private equity appeals to me for the responsibility it entails: identifying the best opportunities, assessing their risks rigorously, then supporting management teams in creating value.",
        },
        "bring": {
            "fr": "Ces expériences me permettent de contribuer au sourcing et au screening d'opportunités, à la modélisation de LBO, au pilotage des due diligences, à la rédaction de mémos d'investissement et au suivi des participations.",
            "en": "These experiences allow me to contribute to deal sourcing and screening, LBO modelling, coordinating due diligence, drafting investment memoranda and monitoring portfolio companies.",
        },
        "env": {"fr": "l'investissement", "en": "investing"},
    },
    "ts": {
        "label": "Transaction Services",
        "team": {"fr": "Transaction Services", "en": "Transaction Services"},
        "why": {
            "fr": "Les Transaction Services m'attirent, car ils offrent une lecture précise de la réalité économique d'une entreprise au moment clé d'une opération : qualité des résultats, besoin en fonds de roulement et dette nette.",
            "en": "Transaction Services appeal to me because they provide a precise view of a company's economic reality at the key moment of a deal: quality of earnings, working capital and net debt.",
        },
        "bring": {
            "fr": "Ces expériences me permettent de contribuer à l'analyse de la qualité des résultats (EBITDA normatif, retraitements), du BFR et de la dette nette, ainsi qu'à la rédaction de rapports de due diligence financière.",
            "en": "These experiences allow me to contribute to quality of earnings analysis (normalised EBITDA, adjustments), working capital and net debt reviews, and the drafting of financial due diligence reports.",
        },
        "env": {"fr": "les missions transactionnelles", "en": "transaction work"},
    },
    "cf": {
        "label": "Corporate Finance mid-cap",
        "team": {"fr": "Corporate Finance", "en": "Corporate Finance"},
        "why": {
            "fr": "Le corporate finance mid-cap m'attire par la proximité qu'il offre avec les dirigeants et actionnaires de PME et d'ETI, et par la diversité des opérations accompagnées : cessions, levées de fonds, LBO et opérations de haut de bilan.",
            "en": "Mid-cap corporate finance appeals to me for the proximity it offers with founders and shareholders of SMEs and mid-sized companies, and for the variety of deals: sell-sides, fundraisings, LBOs and capital structure transactions.",
        },
        "bring": {
            "fr": "Ces expériences me permettent de contribuer à la valorisation, à la modélisation financière, à la rédaction de teasers et d'information memorandums, à l'identification d'acquéreurs et d'investisseurs, et au suivi des processus jusqu'au closing.",
            "en": "These experiences allow me to contribute to valuation, financial modelling, drafting teasers and information memoranda, identifying buyers and investors, and running processes through to closing.",
        },
        "env": {"fr": "l'exécution de mandats", "en": "mandate execution"},
    },
    "coverage": {
        "label": "Coverage / Corporate Banking",
        "team": {"fr": "Coverage", "en": "Coverage"},
        "why": {
            "fr": "Le coverage m'attire par sa dimension à la fois relationnelle et stratégique : comprendre les enjeux de grands clients corporates pour leur proposer, au bon moment, l'ensemble des expertises de la banque.",
            "en": "Coverage appeals to me for its relationship-driven and strategic nature: understanding the challenges of large corporate clients in order to bring them the bank's full range of expertise at the right time.",
        },
        "bring": {
            "fr": "Ces expériences me permettent de contribuer à l'analyse financière et sectorielle des clients, à la préparation de pitch books et de présentations stratégiques, aux analyses de crédit et à la coordination avec les équipes produits.",
            "en": "These experiences allow me to contribute to client financial and industry analysis, pitch book and strategic presentation preparation, credit analysis and coordination with product teams.",
        },
        "env": {"fr": "la relation client", "en": "client coverage"},
    },
    "am": {
        "label": "Asset Management",
        "team": {"fr": "gestion", "en": "investment"},
        "why": {
            "fr": "La gestion d'actifs m'attire par l'exigence d'analyse et de conviction qu'elle requiert pour allouer le capital de façon disciplinée sur le long terme.",
            "en": "Asset management appeals to me for the analytical rigour and conviction it requires to allocate capital in a disciplined way over the long term.",
        },
        "bring": {
            "fr": "Ces expériences me permettent de contribuer à l'analyse fondamentale de sociétés et de secteurs, à la valorisation, au suivi de la performance des portefeuilles et à la préparation de reportings pour les clients et les comités d'investissement.",
            "en": "These experiences allow me to contribute to fundamental company and sector analysis, valuation, portfolio performance monitoring and reporting for clients and investment committees.",
        },
        "env": {"fr": "la gestion de portefeuille", "en": "portfolio management"},
    },
}

# {c} est remplacé par le nom de l'entreprise.
FIRM_TYPES = {
    "bb": {
        "label": "Banque internationale (bulge bracket)",
        "fr": "Rejoindre {c} représenterait l'opportunité de travailler sur des transactions d'envergure internationale, au sein d'une plateforme reconnue pour l'excellence de son exécution et la qualité de la formation de ses analystes.",
        "en": "Joining {c} would give me the opportunity to work on large cross-border transactions within a platform renowned for the excellence of its execution and the quality of its analyst training.",
    },
    "eb": {
        "label": "Boutique d'élite",
        "fr": "{c} se distingue par un conseil indépendant et libre de conflits d'intérêts, une forte exposition des juniors aux dossiers et une culture d'exigence qui correspondent pleinement à ce que je recherche.",
        "en": "{c} stands out for its independent, conflict-free advice, the strong exposure it gives junior bankers to live deals and a culture of excellence that fully matches what I am looking for.",
    },
    "mid": {
        "label": "Boutique mid-cap",
        "fr": "La taille humaine des équipes de {c} et sa proximité avec les dirigeants de PME et d'ETI offrent une exposition directe à l'ensemble du processus transactionnel, de l'origination au closing, ce qui répond à mon envie de prendre rapidement des responsabilités.",
        "en": "The lean teams at {c} and its proximity to founders and management of mid-sized companies offer direct exposure to the entire deal process, from origination to closing, which matches my wish to take on responsibility early.",
    },
    "cib": {
        "label": "Banque française (CIB)",
        "fr": "Rejoindre {c} me permettrait de bénéficier de la force d'une grande banque de financement et d'investissement, de la diversité de ses expertises et de la profondeur de ses relations avec les grands groupes européens.",
        "en": "Joining {c} would allow me to benefit from the strength of a leading corporate and investment bank, the breadth of its expertise and the depth of its relationships with major European corporates.",
    },
    "big4": {
        "label": "Big Four / cabinet de conseil",
        "fr": "La plateforme pluridisciplinaire de {c}, la diversité de ses clients et la rigueur méthodologique de ses équipes constituent un cadre idéal pour développer une expertise transactionnelle solide.",
        "en": "The multidisciplinary platform of {c}, the diversity of its clients and the methodological rigour of its teams provide an ideal environment to build strong transaction expertise.",
    },
    "fund": {
        "label": "Fonds d'investissement",
        "fr": "La stratégie d'investissement de {c}, son approche de la création de valeur aux côtés des équipes dirigeantes et la taille resserrée de ses équipes offrent un cadre unique pour apprendre et contribuer rapidement.",
        "en": "The investment strategy of {c}, its approach to value creation alongside management teams and its lean investment team provide a unique setting to learn and contribute quickly.",
    },
    "amco": {
        "label": "Société de gestion",
        "fr": "La philosophie d'investissement de {c}, fondée sur une analyse fondamentale exigeante et une vision de long terme, correspond pleinement à ma manière d'aborder les marchés.",
        "en": "The investment philosophy of {c}, built on demanding fundamental analysis and a long-term view, fully matches the way I approach markets.",
    },
}

INDUSTRIES = {
    "none": {"label": "Généraliste", "fr": "", "en": ""},
    "infra": {
        "label": "Infrastructures / data centers",
        "fr": "Mon expérience chez Ultra Edge, au cœur du secteur des data centers, nourrit par ailleurs un intérêt marqué pour les infrastructures numériques, l'une des classes d'actifs les plus actives en matière de transactions.",
        "en": "My experience at Ultra Edge, at the heart of the data center industry, has also given me a strong interest in digital infrastructure, one of the most active asset classes in terms of deal flow.",
    },
    "re": {
        "label": "Immobilier",
        "fr": "Mes expériences chez Foncia et au Comptoir du Financement ont par ailleurs développé mon intérêt pour l'immobilier et son financement, un secteur où la compréhension des actifs sous-jacents est déterminante.",
        "en": "My experiences at Foncia and Le Comptoir du Financement have also developed my interest in real estate and its financing, a sector where understanding the underlying assets is decisive.",
    },
    "tmt": {
        "label": "TMT",
        "fr": "Je porte un intérêt particulier au secteur TMT, dont la transformation numérique, étudiée lors de mon Bachelor in Digital & International Business, génère une activité transactionnelle soutenue.",
        "en": "I have a particular interest in TMT, whose digital transformation, which I studied during my Bachelor in Digital & International Business, drives sustained deal activity.",
    },
    "energy": {
        "label": "Énergie / transition",
        "fr": "Je porte un intérêt particulier au secteur de l'énergie, dont les besoins de financement liés à la transition énergétique donnent lieu à des opérations structurantes.",
        "en": "I have a particular interest in energy, where the financing needs of the energy transition are generating landmark transactions.",
    },
    "health": {
        "label": "Santé",
        "fr": "Je porte un intérêt particulier au secteur de la santé, un secteur résilient dont la consolidation alimente une activité transactionnelle soutenue.",
        "en": "I have a particular interest in healthcare, a resilient sector whose ongoing consolidation drives sustained deal activity.",
    },
    "fig": {
        "label": "FIG (institutions financières)",
        "fr": "Je porte un intérêt particulier aux institutions financières, dont la transformation par la fintech, étudiée lors de mon Bachelor, redessine le paysage concurrentiel.",
        "en": "I have a particular interest in financial institutions, whose transformation by fintech, which I studied during my Bachelor, is reshaping the competitive landscape.",
    },
    "consumer": {
        "label": "Consumer / luxe",
        "fr": "Je porte un intérêt particulier aux secteurs de la consommation et du luxe, que mon engagement bénévole au sein d'Emotion Auto Prestige, association dédiée aux véhicules de prestige, m'a permis d'aborder sous l'angle de la marque et de l'expérience client.",
        "en": "I have a particular interest in consumer and luxury, which my volunteering at Emotion Auto Prestige, a luxury vehicle association, allowed me to approach from a brand and client experience angle.",
    },
    "industrials": {
        "label": "Industrie",
        "fr": "Je porte un intérêt particulier au secteur industriel, dont la consolidation et les enjeux de réindustrialisation créent de nombreuses opérations.",
        "en": "I have a particular interest in industrials, where consolidation and reshoring dynamics are creating numerous transactions.",
    },
}

CONTRACTS = {
    "pfe": {"label": "Stage de fin d'études", "fr": "un stage de fin d'études", "en": "an end-of-studies internship", "pos_fr": "Stagiaire Analyste", "pos_en": "Analyst Intern"},
    "stage": {"label": "Stage", "fr": "un stage", "en": "an internship", "pos_fr": "Stagiaire Analyste", "pos_en": "Analyst Intern"},
    "offcycle": {"label": "Stage off-cycle", "fr": "un stage off-cycle", "en": "an off-cycle internship", "pos_fr": "Stagiaire Analyste (off-cycle)", "pos_en": "Off-Cycle Analyst Intern"},
    "summer": {"label": "Summer internship", "fr": "un summer internship", "en": "a summer internship", "pos_fr": "Summer Analyst", "pos_en": "Summer Analyst"},
    "alt": {"label": "Alternance", "fr": "une alternance", "en": "a work-study apprenticeship", "pos_fr": "Analyste en alternance", "pos_en": "Apprentice Analyst"},
    "analyst": {"label": "CDI Analyst", "fr": "un poste d'Analyste", "en": "a full-time Analyst position", "pos_fr": "Analyste", "pos_en": "Analyst"},
}

BLOCKS = {
    "ultra": ("Ultra Edge (DCF, data centers)", True),
    "comptoir": ("Comptoir du Financement", True),
    "foncia": ("Foncia", False),
    "skema": ("SKEMA Finance Paris", True),
    "cfa": ("CFA Level I + outils", False),
    "perso": ("Basse jazz & sport", True),
}

MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
             "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]

DEFAULTS = {
    "lang": "fr", "company": "Exemple Partners", "firm_type": "eb", "team": "",
    "civility": "", "recipient": "", "recipient_role": "", "office_city": "Paris",
    "address": "", "sector": "ma", "industry": "infra", "contract": "pfe",
    "duration": "6 mois", "start": "janvier 2027", "position": "", "hook": "",
    "why": "", "contact": "", "extra": "", "send_city": "Paris", "letter_date": "",
    "blocks": {k: v[1] for k, v in BLOCKS.items()},
}


# =====================================================================
# 3. ASSEMBLAGE DE LA LETTRE
#    Renvoie une liste de (texte, style). Styles : "name", "left", "right",
#    "right_bold", "subject", "body", "sign", "gap".
# =====================================================================
def end_dot(s):
    s = (s or "").strip()
    return s + "." if s and s[-1] not in ".!?…" else s


def de(name):
    """« de » ou « d' » selon la première lettre (élision française)."""
    return ("d'" if name[:1].lower() in "aeiouyhéèêàâîôû" else "de ") + name


def today(lang):
    d = datetime.date.today()
    months = MONTHS_FR if lang == "fr" else MONTHS_EN
    return f"{d.day} {months[d.month - 1]} {d.year}"


def build_letter(st):
    L = st["lang"]
    fr = L == "fr"
    S = SECTORS.get(st["sector"], SECTORS["ma"])
    F = FIRM_TYPES.get(st["firm_type"], FIRM_TYPES["bb"])
    I = INDUSTRIES.get(st["industry"], INDUSTRIES["none"])
    C = CONTRACTS.get(st["contract"], CONTRACTS["pfe"])
    B = st["blocks"]

    company_raw = st["company"].strip()
    company = company_raw or ("votre établissement" if fr else "your firm")
    company_name = company_raw or ("Votre établissement" if fr else "Your firm")
    team = st["team"].strip() or S["team"][L]
    position = st["position"].strip() or f"{C['pos_fr'] if fr else C['pos_en']} – {team}"
    start = st["start"].strip()
    duration = st["duration"].strip()
    civ = st["civility"]
    recipient = st["recipient"].strip()
    last = recipient.split()[-1] if recipient else ""

    # Salutations
    if fr:
        dear = "Madame" if civ == "mme" else "Monsieur" if civ == "m" else "Madame, Monsieur"
        hello = dear + ","
    else:
        dear = ""
        hello = f"Dear {'Ms' if civ == 'mme' else 'Mr'} {last}," if civ and last else "Dear Hiring Team,"

    out = []
    # En-tête : expéditeur
    out.append((PROFILE["name"], "name"))
    for k in ("phone", "email", "linkedin"):
        out.append((PROFILE[k], "left"))
    out.append(("", "gap"))

    # Destinataire
    if recipient:
        prefix = {"mme": "Madame " if fr else "Ms ", "m": "Monsieur " if fr else "Mr "}.get(civ, "")
        out.append((prefix + recipient, "right"))
    if st["recipient_role"].strip():
        out.append((st["recipient_role"].strip(), "right"))
    out.append((f"Équipe {team}" if fr else f"{team} team", "right"))
    out.append((company_name, "right_bold"))
    for k in ("address", "office_city"):
        if st[k].strip():
            out.append((st[k].strip(), "right"))
    out.append(("", "gap"))

    city = st["send_city"].strip() or "Paris"
    date_txt = st["letter_date"].strip() or today(L)
    out.append((f"{city}, le {date_txt}" if fr else f"{city}, {date_txt}", "right"))
    out.append(("", "gap"))

    out.append((
        f"Objet : Candidature – {position}" + (f" – à partir de {start}" if start else "")
        if fr else
        f"Re: Application – {position}" + (f" – starting {start}" if start else ""),
        "subject",
    ))
    out.append(("", "gap"))
    out.append((hello, "body"))

    # P1 — accroche
    if fr:
        contract_txt = C["fr"] + (f" de {duration}" if duration else "")
        p1 = (f"Actuellement en MSc Corporate Financial Management à SKEMA Business School (promotion 2028), "
              f"je vous adresse ma candidature pour {contract_txt} au sein de l'équipe {team} {de(company)}"
              f"{', à compter de ' + start if start else ''}. {S['why']['fr']}")
    else:
        contract_txt = C["en"] + (f" ({duration})" if duration else "")
        p1 = (f"I am currently completing an MSc in Corporate Financial Management at SKEMA Business School (class of 2028) "
              f"and am writing to apply for {contract_txt} with the {team} team at {company}"
              f"{', starting ' + start if start else ''}. {S['why']['en']}")

    # P2 — pourquoi cette entreprise
    p2 = " ".join(x for x in [F[L].format(c=company), end_dot(st["hook"]), end_dot(st["why"]),
                               end_dot(st["contact"]), I[L]] if x)
    p2 = p2[:1].upper() + p2[1:]

    # P3 — expériences
    exp = []
    if B.get("ultra"):
        exp.append(
            "Lors de mon stage de Financial Controller chez Ultra Edge (avril–août 2026), j'ai suivi un portefeuille de projets de plus de 25 M€ réparti sur plus de 140 data centers et analysé un modèle DCF multi-scénarios (CAPEX, OPEX, EBITDA, P&L) fondé sur un taux d'occupation de 85 %, dont j'ai présenté l'analyse de sensibilité à la direction. J'y ai également conçu un processus de gouvernance d'approbation des investissements à deux niveaux."
            if fr else
            "During my Financial Controller internship at Ultra Edge (April–August 2026), I tracked a €25M+ project portfolio across more than 140 data centers and analysed a multi-scenario DCF model (CAPEX, OPEX, EBITDA, P&L) based on an 85% occupancy rate, presenting the sensitivity analysis to senior management. I also designed a two-tier investment approval governance process."
        )
    if B.get("comptoir"):
        if fr:
            exp.append(
                f"{'Auparavant, mon' if B.get('ultra') else 'Mon'} alternance d'un an en tant que Financial Analyst au Comptoir du Financement m'a permis d'analyser en détail les états financiers, ratios et niveaux d'endettement de nombreuses entreprises, d'évaluer des structures de financement et de contribuer à la signature de contrats de 0,5 à 1,3 M€. Plus de 2 000 appels de prospection par mois m'ont appris la rigueur commerciale et la résilience."
            )
        else:
            exp.append(
                f"{'Previously, my' if B.get('ultra') else 'My'} one-year apprenticeship as a Financial Analyst at Le Comptoir du Financement involved detailed analysis of financial statements, ratios and debt levels across a large portfolio of companies, the assessment of financing structures and helping secure contracts worth €0.5M–€1.3M. Making over 2,000 prospecting calls a month taught me commercial discipline and resilience."
            )
    if B.get("foncia"):
        exp.append(
            "Mon stage chez Foncia, où j'ai suivi un portefeuille immobilier de plus de 7 M€ (30+ projets) avec un reporting hebdomadaire à la direction, m'a enfin permis de développer mon sens du suivi d'actifs et de la relation client."
            if fr else
            "Finally, my internship at Foncia, where I managed a €7M+ real estate portfolio of 30+ projects with weekly reporting to management, sharpened my asset monitoring and client relationship skills."
        )
    p3 = " ".join(exp + [S["bring"][L]]) if exp else ""

    # P4 — profil
    prof = []
    if B.get("skema"):
        prof.append(
            "En parallèle de mes études, en tant que Head of Partnerships de SKEMA Finance Paris, j'encadre une équipe de plus de 20 membres et négocie les contrats de partenariat de l'association."
            if fr else
            "Alongside my studies, as Head of Partnerships at SKEMA Finance Paris, I lead a team of more than 20 members and negotiate the association's partnership contracts."
        )
    if B.get("cfa"):
        prof.append(
            "Ma préparation au CFA Level I et ma maîtrise d'Excel, de VBA et de Power BI renforcent ma capacité à produire des analyses fiables et rapides."
            if fr else
            "My preparation for the CFA Level I exam and my proficiency in Excel, VBA and Power BI strengthen my ability to deliver accurate analysis quickly."
        )
    if B.get("perso"):
        prof.append(
            f"Enfin, douze années de basse électrique jazz en conservatoire et la course à pied (marathon, deux Spartan Races) ont forgé mon endurance, ma discipline et ma capacité à garder un haut niveau d'exigence sous pression, des qualités essentielles dans {S['env']['fr']}."
            if fr else
            f"Finally, twelve years of jazz electric bass at the conservatory and running (a marathon, two Spartan Races) have built my stamina, discipline and ability to perform under pressure, all of which are essential in {S['env']['en']}."
        )
    p4 = " ".join(prof)
    p5 = end_dot(st["extra"])

    if fr:
        close = (f"Avec la conviction que ma rigueur analytique et ma capacité de travail seraient un atout pour l'équipe {team} {de(company)}, "
                 f"je vous remercie de l'attention portée à ma candidature et reste à votre disposition pour un entretien. "
                 f"Je vous prie d'agréer, {dear}, l'expression de mes salutations distinguées.")
    else:
        close = (f"I would welcome the opportunity to discuss how I could contribute to the {team} team at {company}. "
                 f"Thank you for your time and consideration.")

    for p in (p1, p2, p3, p4, p5, close):
        if p:
            out.append(("", "gap"))
            out.append((p, "body"))

    out.append(("", "gap"))
    if not fr:
        out.append(("Yours sincerely," if civ and last else "Yours faithfully,", "body"))
        out.append(("", "gap"))
    out.append((PROFILE["name"], "sign"))
    return out


def body_word_count(lines):
    text = " ".join(t for t, s in lines if s == "body")
    return len(text.split())


# =====================================================================
# 4. EXPORTS
# =====================================================================
def export_docx(lines, path):
    d = docx.Document()
    sec = d.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21)
    sec.top_margin = sec.bottom_margin = Cm(2)
    sec.left_margin = sec.right_margin = Cm(2.2)
    normal = d.styles["Normal"]
    normal.font.name = "Garamond"
    normal.font.size = Pt(11.5)
    for text, style in lines:
        p = d.add_paragraph()
        pf = p.paragraph_format
        pf.space_after = Pt(0)
        pf.space_before = Pt(0)
        if style == "gap":
            pf.line_spacing = Pt(7)
            continue
        run = p.add_run(text)
        if style == "name":
            run.bold = True
            run.font.size = Pt(15)
        if style in ("right_bold", "subject", "sign"):
            run.bold = True
        if style.startswith("right"):
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif style == "body":
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    d.save(path)


def export_doc_html(lines, path):
    """Repli sans python-docx : HTML que Word ouvre comme un document."""
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    css = {
        "name": "font-size:15pt;font-weight:bold;margin:0",
        "left": "margin:0", "right": "text-align:right;margin:0",
        "right_bold": "text-align:right;font-weight:bold;margin:0",
        "subject": "font-weight:bold;margin:0", "body": "text-align:justify;margin:0",
        "sign": "font-weight:bold;margin:0", "gap": "margin:0;font-size:6pt",
    }
    html = "".join(f'<p style="{css[s]}">{esc(t) or "&nbsp;"}</p>' for t, s in lines)
    doc = ('<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word">'
           '<head><meta charset="utf-8"><style>@page{size:21cm 29.7cm;margin:2cm 2.2cm}'
           "body{font-family:Garamond,'Times New Roman',serif;font-size:11.5pt;line-height:1.35}</style></head>"
           f"<body>{html}</body></html>")
    Path(path).write_text(doc, encoding="utf-8")


# =====================================================================
# 5. INTERFACE (Tkinter)
# =====================================================================
class App(tk.Tk):
    TEXT_FIELDS = ("hook", "why", "contact", "extra")

    def __init__(self):
        super().__init__()
        self.title("Atelier Lettre IB — Alexis Hamdi")
        self.geometry("1350x880")
        self.minsize(950, 600)
        self.state_data = json.loads(json.dumps(DEFAULTS))
        self.manual = False
        self._loading = False
        self.vars = {}
        self.texts = {}
        self.block_vars = {}
        self._build_ui()
        self._write_form()
        self.render(force=True)
        self._refresh_saved()

    # ---------- construction ----------
    def _build_ui(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Accent.TButton", foreground="white", background="#1f5a43")
        style.map("Accent.TButton", background=[("active", "#17483a")])

        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True)

        # Colonne gauche défilante
        left = ttk.Frame(paned)
        paned.add(left, weight=0)
        canvas = tk.Canvas(left, width=430, highlightthickness=0)
        sb = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        form = ttk.Frame(canvas, padding=12)
        form.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win = canvas.create_window((0, 0), window=form, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(win, width=e.width))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def on_wheel(e):
            delta = -e.delta if platform.system() == "Darwin" else -e.delta // 120
            canvas.yview_scroll(int(delta), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Langue
        lang_box = ttk.Frame(form)
        lang_box.pack(fill="x", pady=(0, 8))
        ttk.Label(lang_box, text="Langue :").pack(side="left")
        self.lang_var = tk.StringVar(value="fr")
        for val, txt in (("fr", "Français"), ("en", "English")):
            ttk.Radiobutton(lang_box, text=txt, value=val, variable=self.lang_var,
                            command=self._on_lang).pack(side="left", padx=6)

        g = self._group(form, "Entreprise")
        self._entry(g, "company", "Nom de l'entreprise")
        self._combo(g, "firm_type", "Type d'établissement", FIRM_TYPES)
        self._entry(g, "team", "Équipe / division (vide = auto)")
        self._combo(g, "civility", "Civilité du destinataire",
                    {"": {"label": "Non précisé"}, "mme": {"label": "Madame"}, "m": {"label": "Monsieur"}})
        self._entry(g, "recipient", "Nom du destinataire")
        self._entry(g, "recipient_role", "Fonction du destinataire")
        self._entry(g, "office_city", "Ville du bureau")
        self._entry(g, "address", "Adresse (facultatif)")

        g = self._group(form, "Poste")
        self._combo(g, "sector", "Métier", SECTORS)
        self._combo(g, "industry", "Secteur / industrie", INDUSTRIES)
        self._combo(g, "contract", "Type de contrat", CONTRACTS)
        self._entry(g, "duration", "Durée")
        self._entry(g, "start", "Date de début")
        self._entry(g, "position", "Intitulé exact du poste (vide = auto)")

        g = self._group(form, "Personnalisation (une phrase complète ; vide = retirée)")
        self._textbox(g, "hook", "Deal ou actualité récente de l'entreprise")
        self._textbox(g, "why", "Ce qui t'attire chez eux")
        self._textbox(g, "contact", "Contact / networking")
        self._textbox(g, "extra", "Paragraphe libre")

        g = self._group(form, "Contenu à mettre en avant")
        for k, (label, _) in BLOCKS.items():
            v = tk.BooleanVar()
            v.trace_add("write", lambda *a: self._on_change())
            self.block_vars[k] = v
            ttk.Checkbutton(g, text=label, variable=v).pack(anchor="w")
        self._entry(g, "send_city", "Ville d'envoi")
        self._entry(g, "letter_date", "Date de la lettre (vide = aujourd'hui)")

        g = self._group(form, "Mes versions enregistrées")
        row = ttk.Frame(g)
        row.pack(fill="x")
        ttk.Button(row, text="Enregistrer", style="Accent.TButton", command=self.save_version).pack(side="left")
        ttk.Button(row, text="Ouvrir", command=self.load_version).pack(side="left", padx=4)
        ttk.Button(row, text="Supprimer", command=self.delete_version).pack(side="left")
        ttk.Button(row, text="Nouvelle lettre", command=self.new_letter).pack(side="left", padx=4)
        self.saved_list = tk.Listbox(g, height=6)
        self.saved_list.pack(fill="x", pady=(6, 0))
        self.saved_list.bind("<Double-Button-1>", lambda e: self.load_version())

        # Colonne droite : barre d'outils + feuille
        right = ttk.Frame(paned, padding=(8, 12, 12, 12))
        paned.add(right, weight=1)
        bar = ttk.Frame(right)
        bar.pack(fill="x")
        self.meter = ttk.Label(bar, text="")
        self.meter.pack(side="left")
        ttk.Button(bar, text="Exporter TXT", command=self.export_txt).pack(side="right")
        ttk.Button(bar, text="Exporter Word", command=self.export_word).pack(side="right", padx=4)
        ttk.Button(bar, text="Copier le texte", style="Accent.TButton", command=self.copy).pack(side="right")
        self.regen_btn = ttk.Button(bar, text="Annuler mes retouches", command=lambda: self.render(force=True))
        self.status = ttk.Label(right, text="", foreground="#1f5a43")
        self.status.pack(fill="x", pady=(4, 4))

        desk = tk.Frame(right, background="#d9dfdb", padx=18, pady=18)
        desk.pack(fill="both", expand=True)
        serif = ("Garamond", 14) if platform.system() == "Darwin" else ("Georgia", 11)
        self.paper = tk.Text(desk, wrap="word", font=serif, background="white", foreground="#111",
                             insertbackground="#111", relief="flat", padx=48, pady=40, undo=True,
                             spacing1=0, spacing3=2)
        psb = ttk.Scrollbar(desk, orient="vertical", command=self.paper.yview)
        self.paper.configure(yscrollcommand=psb.set)
        self.paper.pack(side="left", fill="both", expand=True)
        psb.pack(side="right", fill="y")
        bold = (serif[0], serif[1], "bold")
        self.paper.tag_configure("name", font=(serif[0], serif[1] + 4, "bold"))
        self.paper.tag_configure("left")
        self.paper.tag_configure("right", justify="right")
        self.paper.tag_configure("right_bold", justify="right", font=bold)
        self.paper.tag_configure("subject", font=bold)
        self.paper.tag_configure("sign", font=bold)
        self.paper.tag_configure("body")
        self.paper.tag_configure("gap", font=(serif[0], 5))
        self.paper.bind("<Key>", self._on_paper_key)

    def _group(self, parent, title):
        f = ttk.LabelFrame(parent, text=title, padding=10)
        f.pack(fill="x", pady=6)
        return f

    def _entry(self, parent, key, label):
        ttk.Label(parent, text=label).pack(anchor="w")
        v = tk.StringVar()
        v.trace_add("write", lambda *a: self._on_change())
        self.vars[key] = v
        ttk.Entry(parent, textvariable=v, width=10).pack(fill="x", pady=(0, 6))

    def _combo(self, parent, key, label, options):
        ttk.Label(parent, text=label).pack(anchor="w")
        keys = list(options.keys())
        labels = [options[k]["label"] for k in keys]
        cb = ttk.Combobox(parent, values=labels, state="readonly", width=10)
        cb.pack(fill="x", pady=(0, 6))
        v = tk.StringVar()
        self.vars[key] = v

        def from_cb(e=None):
            v.set(keys[cb.current()])
        cb.bind("<<ComboboxSelected>>", from_cb)

        def to_cb(*a):
            if v.get() in keys:
                cb.current(keys.index(v.get()))
            self._on_change()
        v.trace_add("write", to_cb)

    def _textbox(self, parent, key, label):
        ttk.Label(parent, text=label).pack(anchor="w")
        t = tk.Text(parent, height=3, width=10, wrap="word", font=("TkDefaultFont", 11))
        t.pack(fill="x", pady=(0, 6))
        t.bind("<KeyRelease>", lambda e: self._on_change())
        self.texts[key] = t

    # ---------- état ----------
    def _read_form(self):
        st = self.state_data
        for k, v in self.vars.items():
            st[k] = v.get()
        for k, t in self.texts.items():
            st[k] = t.get("1.0", "end").strip()
        st["blocks"] = {k: v.get() for k, v in self.block_vars.items()}
        st["lang"] = self.lang_var.get()

    def _write_form(self):
        self._loading = True
        st = self.state_data
        for k, v in self.vars.items():
            v.set(st.get(k, ""))
        for k, t in self.texts.items():
            t.delete("1.0", "end")
            t.insert("1.0", st.get(k, ""))
        for k, v in self.block_vars.items():
            v.set(bool(st.get("blocks", {}).get(k)))
        self.lang_var.set(st.get("lang", "fr"))
        self._loading = False

    def _on_change(self):
        if self._loading:
            return
        self._read_form()
        if self.manual:
            self.say("Tu as retouché la lettre : clique « Annuler mes retouches » pour appliquer les nouveaux réglages.")
            return
        self.render()

    def _on_lang(self):
        st = self.state_data
        self._read_form()
        swaps = {"en": {"6 mois": "6 months", "janvier 2027": "January 2027"},
                 "fr": {"6 months": "6 mois", "January 2027": "janvier 2027"}}[st["lang"]]
        for k in ("duration", "start"):
            st[k] = swaps.get(st[k], st[k])
        self._write_form()
        self.render(force=True)

    def _on_paper_key(self, e):
        nav = {"Left", "Right", "Up", "Down", "Home", "End", "Prior", "Next",
               "Shift_L", "Shift_R", "Control_L", "Control_R", "Meta_L", "Meta_R", "Alt_L", "Alt_R"}
        if e.keysym in nav or (e.state & 0x0004 and e.keysym.lower() in ("c", "a")):
            return
        if not self.manual:
            self.manual = True
            self.regen_btn.pack(side="right", padx=4)
        self.after(10, self._update_meter_from_paper)

    # ---------- rendu ----------
    def render(self, force=False):
        if self.manual and not force:
            return
        self.lines = build_letter(self.state_data)
        self.paper.delete("1.0", "end")
        for text, style in self.lines:
            self.paper.insert("end", text + "\n", style)
        self.manual = False
        self.regen_btn.pack_forget()
        n = body_word_count(self.lines)
        self._set_meter(n)

    def _set_meter(self, n):
        warn = " — trop long, décoche un bloc" if n > 430 else ""
        self.meter.configure(text=f"{n} mots dans le corps · cible ≤ 430 pour une page{warn}",
                             foreground="#9a5b00" if warn else "#5b6862")

    def _paper_lines(self):
        """Relit la feuille (avec retouches) en conservant les styles de chaque ligne."""
        content = self.paper.get("1.0", "end-1c").split("\n")
        out = []
        for i, line in enumerate(content, start=1):
            tags = [t for t in self.paper.tag_names(f"{i}.0") if t != "sel"]
            style = tags[0] if tags else ("body" if line.strip() else "gap")
            out.append((line, "gap" if not line.strip() else style))
        while out and out[-1][1] == "gap":
            out.pop()
        return out

    def _update_meter_from_paper(self):
        self._set_meter(body_word_count(self._paper_lines()))

    def say(self, msg):
        self.status.configure(text=msg)
        self.after(4000, lambda: self.status.configure(text="") if self.status.cget("text") == msg else None)

    # ---------- actions ----------
    def _slug(self):
        s = re.sub(r"[^\w-]+", "_", self.state_data["company"].strip() or "entreprise")
        return f"LM_Alexis_Hamdi_{s}_{self.state_data['lang'].upper()}"

    def copy(self):
        text = re.sub(r"\n{3,}", "\n\n", self.paper.get("1.0", "end").strip())
        self.clipboard_clear()
        self.clipboard_append(text)
        self.say("Texte copié. Colle-le dans Word ou dans le formulaire de candidature.")

    def export_word(self):
        ext = ".docx" if HAS_DOCX else ".doc"
        path = filedialog.asksaveasfilename(defaultextension=ext, initialfile=self._slug() + ext,
                                            filetypes=[("Word", "*" + ext)])
        if not path:
            return
        lines = self._paper_lines()
        try:
            if HAS_DOCX:
                export_docx(lines, path)
            else:
                export_doc_html(lines, path)
            self.say(f"Exporté : {Path(path).name}" + ("" if HAS_DOCX else "  (pip install python-docx pour un vrai .docx)"))
        except Exception as err:
            messagebox.showerror("Export impossible", f"Le fichier n'a pas pu être écrit :\n{err}")

    def export_txt(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=self._slug() + ".txt",
                                            filetypes=[("Texte", "*.txt")])
        if path:
            Path(path).write_text(self.paper.get("1.0", "end").strip() + "\n", encoding="utf-8")
            self.say(f"Exporté : {Path(path).name}")

    # ---------- versions ----------
    def _load_saved(self):
        try:
            return json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _store_saved(self, data):
        SAVE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _refresh_saved(self):
        self.saved_list.delete(0, "end")
        for v in self._load_saved():
            self.saved_list.insert("end", f"{v['title']}  [{v['state']['lang'].upper()}]")

    def save_version(self):
        self._read_form()
        st = self.state_data
        title = f"{st['company'].strip() or 'Sans nom'} · {SECTORS[st['sector']]['label'].split(' (')[0]}"
        data = [v for v in self._load_saved() if not (v["title"] == title and v["state"]["lang"] == st["lang"])]
        data.insert(0, {
            "title": title,
            "state": json.loads(json.dumps(st)),
            "edited": self._paper_lines() if self.manual else None,
            "at": datetime.datetime.now().isoformat(timespec="seconds"),
        })
        self._store_saved(data)
        self._refresh_saved()
        self.say(f"Enregistré : {title}  ({SAVE_FILE.name})")

    def load_version(self):
        sel = self.saved_list.curselection()
        if not sel:
            self.say("Sélectionne d'abord une version dans la liste.")
            return
        v = self._load_saved()[sel[0]]
        st = json.loads(json.dumps(DEFAULTS))
        st.update(v["state"])
        self.state_data = st
        self._write_form()
        self.render(force=True)
        if v.get("edited"):
            self.paper.delete("1.0", "end")
            for text, style in v["edited"]:
                self.paper.insert("end", text + "\n", style)
            self.manual = True
            self.regen_btn.pack(side="right", padx=4)
            self._update_meter_from_paper()
        self.say(f"Version « {v['title']} » ouverte.")

    def delete_version(self):
        sel = self.saved_list.curselection()
        if not sel:
            self.say("Sélectionne d'abord une version à supprimer.")
            return
        data = self._load_saved()
        title = data[sel[0]]["title"]
        if messagebox.askyesno("Supprimer", f"Supprimer la version « {title} » ?"):
            data.pop(sel[0])
            self._store_saved(data)
            self._refresh_saved()
            self.say("Version supprimée.")

    def new_letter(self):
        self._read_form()
        keep = {k: self.state_data[k] for k in ("lang", "blocks", "send_city", "sector", "firm_type",
                                                "contract", "duration", "start")}
        st = json.loads(json.dumps(DEFAULTS))
        st.update(keep)
        st.update({k: "" for k in ("company", "team", "recipient", "recipient_role", "address",
                                   "position", "hook", "why", "contact", "extra")})
        self.state_data = st
        self._write_form()
        self.render(force=True)
        self.say("Nouvelle lettre : renseigne l'entreprise.")


if __name__ == "__main__":
    App().mainloop()