from transformers import pipeline

def generate_questions(post_description, num_questions=5):
    """Génère des questions basées sur la description du poste."""
    generator = pipeline("text2text-generation", model="google/flan-t5-base")
    
    # Formuler l'entrée pour guider le modèle vers des questions techniques
    inputs = [f"Generate technical interview questions about: {post_description}"] * num_questions
    
    # Générer des questions avec diversité et pertinence
    questions = generator(
        inputs,
        num_beams=4,  # Augmente la qualité des générations
        do_sample=True,  # Active le sampling pour diversifier les résultats
        top_k=50,  # Nombre de tokens candidats à considérer
        top_p=0.95,  # Probabilité cumulée pour le sampling
        repetition_penalty=2.0,  # Pénalise fortement les répétitions
        max_length=100  # Limite la longueur des questions pour éviter des phrases trop longues
    )
    
    # Extraire les questions générées
    return [q['generated_text'] for q in questions]

# Exemple d'utilisation
post_description = (
    "Compétences requises : Connaissance approfondie de Django, y compris les vues, les modèles, les formulaires et les templates. "
    "Expérience avec la création d'API REST en utilisant Django REST Framework. "
    "Compréhension des bases de données relationnelles et des requêtes SQL."
)

questions = generate_questions(post_description, num_questions=5)
print(questions)