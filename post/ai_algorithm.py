# ai_algorithm.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare_cv_with_post(cv_text, post_description):
    """Compare un CV avec une description de poste en utilisant TF-IDF et similarité cosinus."""
    vectorizer = TfidfVectorizer().fit_transform([cv_text, post_description])
    vectors = vectorizer.toarray()
    similarity_score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return similarity_score