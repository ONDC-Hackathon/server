from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def overall_similarity_score_between_dict(dict1, dict2):
    """
    Calculate an overall similarity score across all matching keys in two dictionaries.

    Parameters:
    - dict1: dict, first dictionary containing texts for comparison.
    - dict2: dict, second dictionary containing texts for comparison.

    Returns:
    - overall_similarity: float, the average similarity score across all keys.
    """
    vectorizer = TfidfVectorizer()
    total_similarity = 0
    count = 0

    for key in dict1:
        if key in dict2:
            texts = [dict1[key], dict2[key]]
            tfidf_matrix = vectorizer.fit_transform(texts)
            similarity_matrix = cosine_similarity(
                tfidf_matrix[0:1], tfidf_matrix[1:2])
            total_similarity += similarity_matrix[0][0]
            count += 1

    # To avoid division by zero if there are no matching keys
    if count == 0:
        return 0
    overall_similarity = total_similarity / count
    return overall_similarity


def overall_similarity_score_between_text(text1, text2):
    """
    Calculate an overall similarity score across all matching keys in two dictionaries.

    Parameters:
    - text1: string, first text for comparison.
    - text2: string, second text for comparison.

    Returns:
    - overall_similarity: float, the average similarity score across all keys.
    """
    vectorizer = TfidfVectorizer()
    total_similarity = 0
    count = 0

    texts = [text1, text2]
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    total_similarity += similarity_matrix[0][0]
    count += 1

    # To avoid division by zero if there are no matching keys
    if count == 0:
        return 0

    overall_similarity = total_similarity / count
    return overall_similarity
