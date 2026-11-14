def evaluate_tasks(client, context, tasks):
    results = []
    for item in tasks:
        prompt = f"""
Évalue honnêtement si le modèle IA local actuel pourrait accomplir cette tâche pour le client,
sans accès au SaaS proposé, sans outils externes, sans base de données privée et sans intervention humaine.

Retourne uniquement ce JSON :
{{
  "capability": 0,
  "autonomy": "faible|moyenne|élevée",
  "limitation": "limite concrète",
  "evidence_type": "raisonnement du modèle, pas test empirique",
  "confidence": "faible|moyenne|élevée"
}}

capability = estimation de 0 à 100 de la part de la tâche que le modèle pourrait accomplir seul.
Ne donne pas 100 simplement parce que le modèle peut expliquer comment faire.
Si la tâche nécessite stockage persistant, synchronisation, transactions, données privées,
identité, intégration matérielle ou garantie opérationnelle, tiens-en compte.

Produit : {context}
Tâche : {item['task']}
Importance : {item['weight']}/5
"""
        data = client.generate_json(prompt)
        results.append({
            "task": item["task"],
            "weight": item["weight"],
            "capability": max(0, min(100, float(data.get("capability", 0)))),
            "autonomy": str(data.get("autonomy", "faible")),
            "limitation": str(data.get("limitation", "Non précisée")),
            "confidence": str(data.get("confidence", "faible")),
        })
    return results
