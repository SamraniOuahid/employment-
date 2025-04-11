# ai_question_generator.py

from transformers import pipeline

def generate_questions(post_description, num_questions=5):
    """
    Generate questions based on a job description using a text-to-text generation model.

    Parameters:
        post_description (str): The text content of the job description.
        num_questions (int): The number of questions to generate (default is 5).

    Returns:
        list: A list of generated questions as strings.

    Raises:
        ValueError: If `post_description` is empty or `num_questions` is not a positive integer.
    """
    if not isinstance(post_description, str) or not post_description.strip():
        raise ValueError("The post_description must be a non-empty string.")

    if not isinstance(num_questions, int) or num_questions <= 0:
        raise ValueError("The num_questions must be a positive integer.")

    # Initialize the question generation pipeline
    question_generator = pipeline("text2text-generation", model="valhalla/t5-base-qa-qg-hl")

    # Generate questions
    questions = question_generator([post_description] * num_questions)

    return [q['generated_text'] for q in questions]