from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

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

def evaluate_responses(candidate_answers, post_description):
    """Évalue les réponses du candidat en les comparant avec la description du poste."""
    total_score = 0
    scores = []

    model = SentenceTransformer('all-MiniLM-L6-v2')
    post_embedding = model.encode(post_description)

    for i, candidate_answer in enumerate(candidate_answers):
        try:
            answer_embedding = model.encode(candidate_answer)
            similarity_score = util.cos_sim(answer_embedding, post_embedding).item()
            score = round(similarity_score * 100, 2)
            scores.append(score)
            total_score += score
        except Exception as e:
            print(f"Erreur lors de l'évaluation de la réponse {i + 1}: {e}")
            scores.append(0)

    final_score = round(total_score / len(candidate_answers), 2) if candidate_answers else 0
    return final_score, scores