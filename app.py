import json
import streamlit as st
from core.llm_engine import OllamaClient
from core.task_extractor import extract_tasks
from core.capability_tester import evaluate_tasks
from core.scoring import calculate_score
from analysis.monetization import build_opportunities

st.set_page_config(page_title="SaaS Gap Analyzer", page_icon="🔎", layout="wide")
st.title("🔎 SaaS Gap Analyzer")
st.caption("Mesurez ce qu'un modèle IA local peut déjà faire — et identifiez ce qui reste monétisable.")

with st.sidebar:
    st.header("Configuration")
    model = st.text_input("Modèle Ollama", value="qwen2.5:3b")
    base_url = st.text_input("Adresse Ollama", value="http://localhost:11434")
    st.caption("Le modèle doit être téléchargé dans Ollama.")

st.subheader("1. Décrivez votre SaaS")
name = st.text_input("Nom du produit", placeholder="Ex. StyliApp")
audience = st.text_input("Client cible", placeholder="Ex. couturiers indépendants et ateliers")
problem = st.text_area("Problème client", placeholder="Quel problème concret votre client cherche-t-il à résoudre ?", height=100)
value_prop = st.text_area("Proposition de valeur", placeholder="Décrivez ce que votre SaaS permet de faire.", height=140)
features = st.text_area("Fonctionnalités (facultatif)", placeholder="Une fonctionnalité par ligne", height=100)

if st.button("Analyser le potentiel IA", type="primary", use_container_width=True):
    if not value_prop.strip() or not problem.strip():
        st.error("Renseignez au minimum le problème client et la proposition de valeur.")
        st.stop()

    client = OllamaClient(base_url=base_url, model=model)
    with st.spinner("Vérification de la connexion à Ollama…"):
        try:
            client.check_connection()
        except Exception as exc:
            st.error(f"Connexion Ollama impossible : {exc}")
            st.info("Lancez Ollama, puis téléchargez le modèle avec : ollama pull qwen2.5:3b")
            st.stop()

    context = {
        "name": name,
        "audience": audience,
        "problem": problem,
        "value_proposition": value_prop,
        "features": [x.strip() for x in features.splitlines() if x.strip()],
    }
    try:
        with st.spinner("Étape 1/2 — Décomposition du besoin…"):
            tasks = extract_tasks(client, context)
        with st.spinner("Étape 2/2 — Évaluation des capacités du modèle…"):
            evaluations = evaluate_tasks(client, context, tasks)

        score = calculate_score(evaluations)
        opportunities = build_opportunities(evaluations)

        st.divider()
        st.subheader("2. Résultat")
        c1, c2, c3 = st.columns(3)
        c1.metric("Couverture IA estimée", f"{score['ai_coverage']:.1f}%")
        c2.metric("Besoin non couvert", f"{score['gap']:.1f}%")
        c3.metric("Tâches analysées", len(evaluations))
        st.progress(min(max(score["ai_coverage"] / 100, 0), 1))

        st.warning(
            "Diagnostic exploratoire : ces pourcentages sont des estimations produites par le LLM, "
            "pas des résultats de benchmark. Validez-les avec des tests réels et des utilisateurs."
        )

        st.subheader("3. Analyse par tâche")
        st.dataframe(
            [{
                "Tâche": e["task"],
                "Importance": e["weight"],
                "Capacité IA (%)": e["capability"],
                "Autonomie": e["autonomy"],
                "Limite principale": e["limitation"],
            } for e in evaluations],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("4. Pistes de monétisation à explorer")
        for item in opportunities:
            st.markdown(f"- **{item['task']}** — {item['reason']}")

        report = {
            "product": context,
            "score": score,
            "evaluations": evaluations,
            "monetization_opportunities": opportunities,
            "methodology_note": "LLM-estimated; not empirically benchmarked.",
        }
        st.download_button(
            "Télécharger le rapport JSON",
            data=json.dumps(report, ensure_ascii=False, indent=2),
            file_name="saas_gap_analysis.json",
            mime="application/json",
        )
    except Exception as exc:
        st.error(f"L'analyse a échoué : {exc}")
