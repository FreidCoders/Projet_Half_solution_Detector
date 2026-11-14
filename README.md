# SaaS Gap Analyzer

Un outil open source qui aide les fondateurs à analyser quelle part des tâches promises par leur SaaS
un modèle IA local peut potentiellement accomplir seul, puis à repérer les besoins moins bien couverts.

## Fonctionnalités du MVP

- Saisie du problème client, de l'audience et de la proposition de valeur.
- Décomposition en tâches concrètes par un LLM.
- Estimation de capacité tâche par tâche.
- Score pondéré de couverture IA et estimation du gap.
- Pistes initiales de différenciation et export JSON.

## Stack

- Python
- Streamlit
- Ollama
- Qwen 2.5 (modèle local par défaut)

## Installation

Prérequis : Python 3.10+ et Ollama installés.

```bash
git clone https://github.com/VOTRE-PSEUDO/saas-gap-analyzer.git
cd saas-gap-analyzer

python -m venv .venv
# Windows :
.venv\\Scripts\\activate
# macOS / Linux :
source .venv/bin/activate

pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
```

Dans un autre terminal :

```bash
streamlit run app.py
```

Ouvrez l'adresse locale affichée par Streamlit (généralement http://localhost:8501).

## Limites importantes

Le score actuel est une **estimation générée par le modèle**, et non une mesure scientifique.
Le MVP ne réalise pas encore de benchmark automatisé sur des jeux de tests représentatifs.
Avant toute décision commerciale, tester chaque tâche sur des exemples réels, mesurer la qualité,
le coût, le temps, les erreurs et faire valider le besoin par des clients.

## Feuille de route

- [ ] Tests empiriques par tâche et jeux de cas
- [ ] Comparaison de plusieurs modèles
- [ ] Score de confiance et traçabilité des évaluations
- [ ] Export PDF
- [ ] Historique des analyses
- [ ] Entretiens clients et validation de la volonté de payer

## Licence

MIT
