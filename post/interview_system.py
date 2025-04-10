from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

def generate_questions(post_description, num_questions=5):
    """Génère des questions techniques basées sur la description du poste."""
    generator = pipeline("text2text-generation", model="google/flan-t5-base")
    questions_list = []
    for i in range(num_questions):
        prompt = f"Generate a professional HR-style technical interview question about: {post_description}. Focus on practical skills and experience. Question number {i+1}."
        question = generator(
            prompt,
            num_beams=4,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            repetition_penalty=2.0,
            max_length=150,
            temperature=0.7
        )[0]['generated_text']
        questions_list.append(question)
    return questions_list

def evaluate_responses(candidate_answers, post_description, questions):
    """Évalue les réponses du candidat en les comparant avec la description du poste et les questions."""
    total_score = 0
    scores = []

    model = SentenceTransformer('all-MiniLM-L6-v2')
    post_embedding = model.encode(post_description)
    question_embeddings = [model.encode(question) for question in questions]

    for i, candidate_answer in enumerate(candidate_answers):
        try:
            answer_embedding = model.encode(candidate_answer)
            
            # Calculate similarity to post description
            description_similarity = util.cos_sim(answer_embedding, post_embedding).item()
            
            # Calculate similarity to the specific question
            question_similarity = util.cos_sim(answer_embedding, question_embeddings[i]).item()
            
            # Combine the scores (you can adjust the weights)
            combined_similarity = (0.3 * description_similarity + 0.7 * question_similarity)  # 40% description, 60% question
            
            score = round(combined_similarity * 100, 2)
            scores.append(score)
            total_score += score
        except Exception as e:
            print(f"Erreur lors de l'évaluation de la réponse {i + 1}: {e}")
            scores.append(0)

    final_score = round(total_score / len(candidate_answers), 2) if candidate_answers else 0
    return final_score, scores