# ai_question_generator.py

from transformers import pipeline

def generate_questions(post_description, num_questions=5):
    """Génère des questions basées sur la description du poste."""
    question_generator = pipeline("text2text-generation", model="valhalla/t5-base-qa-qg-hl")
    questions = question_generator([post_description] * num_questions)
    return [q['generated_text'] for q in questions]