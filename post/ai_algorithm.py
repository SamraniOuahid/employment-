from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare_cv_with_post(cv_text, post_description):
    """
    Compare a CV with a job description using TF-IDF and cosine similarity.

    Parameters:
        cv_text (str): The text content of the CV.
        post_description (str): The text content of the job description.

    Returns:
        float: A similarity score between 0 and 1, where 1 indicates perfect similarity.

    Raises:
        ValueError: If either `cv_text` or `post_description` is empty or not a string.
    """
    if not isinstance(cv_text, str) or not isinstance(post_description, str):
        raise ValueError("Both cv_text and post_description must be strings.")

    if not cv_text.strip() or not post_description.strip():
        raise ValueError("Both cv_text and post_description must be non-empty.")

    # Create the TF-IDF vectorizer
    vectorizer = TfidfVectorizer().fit_transform([cv_text, post_description])
    vectors = vectorizer.toarray()

    # Calculate and return the cosine similarity score
    similarity_score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return similarity_score