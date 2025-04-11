from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

def generate_questions(post_description, num_questions=5):
    """
    Generates distinct technical and HR-related questions based on the job description.

    Parameters:
        post_description (str): The text content of the job description.
        num_questions (int): The number of questions to generate (default is 5).

    Returns:
        list: A list of generated questions as strings.
    """
    generator = pipeline("text2text-generation", model="google/flan-t5-base")
    questions_list = []
    prompts = [
        f"Generate a question about the key skills required for excelling in the role described as: {post_description}.",
        f"Generate a question about a challenging scenario one might face in the role of: {post_description}.",
        f"Generate a question about the practical experiences most relevant to succeed in the position of: {post_description}.",
        f"Generate a question about what makes someone a good fit for the role of: {post_description}.",
        f"Generate a question about how to define success in the role of: {post_description}."
    ]

    for i in range(num_questions):
        prompt = prompts[i % len(prompts)]  # Cycle through prompts if num_questions > len(prompts)
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
    """Evaluates candidate answers by comparing them with the job description and questions."""
    total_score = 0
    scores = []

    model = SentenceTransformer('all-MiniLM-L6-v2')
    post_embedding = model.encode(post_description)
    question_embeddings = [model.encode(question) for question in questions]

    for i, candidate_answer in enumerate(candidate_answers):
        try:
            answer_embedding = model.encode(candidate_answer)
            
            # Calculate similarity to job description
            description_similarity = util.cos_sim(answer_embedding, post_embedding).item()
            
            # Calculate similarity to the specific question
            question_similarity = util.cos_sim(answer_embedding, question_embeddings[i]).item()
            
            # Combine the scores (you can adjust the weights)
            combined_similarity = (0.3 * description_similarity + 0.7 * question_similarity)  # 30% description, 70% question
            
            score = round(combined_similarity * 100, 2)
            scores.append(score)
            total_score += score
        except Exception as e:
            print(f"Error while evaluating answer {i + 1}: {e}")
            scores.append(0)

    final_score = round(total_score / len(candidate_answers), 2) if candidate_answers else 0
    return final_score, scores