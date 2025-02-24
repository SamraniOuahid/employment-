# interview_system.py

from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch

# Fonction pour générer des questions à partir d'une description de poste
def generate_questions(post_description, num_questions=5):
    """Génère des questions techniques basées sur la description du poste."""
    generator = pipeline("text2text-generation", model="google/flan-t5-base")
    inputs = [f"Generate technical interview questions about: {post_description}"] * num_questions
    questions = generator(
        inputs,
        num_beams=4,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        repetition_penalty=2.0,
        max_length=100
    )
    return [q['generated_text'] for q in questions]

# Fonction pour évaluer les réponses du candidat par rapport à la description du poste
def evaluate_responses(candidate_answers, post_description):
    """Évalue les réponses du candidat en les comparant avec la description du poste."""
    total_score = 0
    scores = []

    # Charger le modèle Sentence Transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encoder la description du poste une seule fois
    post_embedding = model.encode(post_description)

    for i, candidate_answer in enumerate(candidate_answers):
        try:
            # Encoder la réponse du candidat
            answer_embedding = model.encode(candidate_answer)
            
            # Calculer la similarité cosinus entre la réponse et la description du poste
            similarity_score = util.cos_sim(answer_embedding, post_embedding).item()
            score = round(similarity_score * 100, 2)
            scores.append(score)
            total_score += score
        except Exception as e:
            print(f"Erreur lors de l'évaluation de la réponse {i + 1}: {e}")
            scores.append(0)

    # Calculer la note finale (moyenne des scores)
    final_score = round(total_score / len(candidate_answers), 2) if candidate_answers else 0
    return final_score, scores

# Exemple d'utilisation
if __name__ == "__main__":
    # Description du poste
    post_description = (
        "Compétences requises : Connaissance approfondie de Django, y compris les vues, les modèles, les formulaires et les templates. "
        "Expérience avec la création d'API REST en utilisant Django REST Framework. "
        "Compréhension des bases de données relationnelles et des requêtes SQL."
    )

    # Générer des questions
    questions = generate_questions(post_description, num_questions=3)
    print("Questions générées :")
    for i, question in enumerate(questions):
        print(f"{i + 1}. {question}")

    # Simuler les réponses du candidat
    candidate_answers = [
        "Un modèle en Django représente une table de base de données.",
        "Pour créer une API REST, utilisez Django REST Framework avec des sérializers et des vues génériques.",
        "Les requêtes SQL peuvent être optimisées en utilisant des index et des jointures efficaces."
    ]

    # Évaluer les réponses par rapport à la description du poste
    final_score, scores = evaluate_responses(candidate_answers, post_description)
    print("\nRésultats de l'évaluation :")
    print(f"Note finale : {final_score}%")
    for i, score in enumerate(scores):
        print(f"Réponse {i + 1} : {score}%")