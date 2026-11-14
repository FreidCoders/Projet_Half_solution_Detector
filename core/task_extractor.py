def extract_tasks(client, context):
    prompt = f"""
Tu es analyste produit. Décompose la proposition de valeur en tâches concrètes que le client
cherche à accomplir. N'invente pas de fonctionnalités sans rapport.
Retourne uniquement un objet JSON de forme :
{{"tasks":[{{"task":"verbe + résultat concret","weight":1,"why_it_matters":"raison"}}]}}
Règles :
- 4 à 10 tâches distinctes.
- weight est un entier de 1 à 5 selon l'importance pour le client.
- Les tâches doivent être évaluables séparément par un modèle IA.
- Ne confonds pas une tâche métier complète avec la simple génération de texte.

Contexte produit :
{context}
"""
    data = client.generate_json(prompt)
    tasks = data.get("tasks", [])
    if not tasks:
        raise ValueError("Le modèle n'a extrait aucune tâche exploitable.")
    cleaned = []
    for item in tasks:
        task = str(item.get("task", "")).strip()
        if task:
            cleaned.append({
                "task": task,
                "weight": max(1, min(5, int(item.get("weight", 3)))),
                "why_it_matters": str(item.get("why_it_matters", "")),
            })
    return cleaned
