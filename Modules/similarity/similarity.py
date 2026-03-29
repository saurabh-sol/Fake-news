from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 🔹 Step 1: Compute similarity scores
def compute_similarity_scores(tweet, news_titles):
    texts = [tweet] + news_titles

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)

    tweet_vec = vectors[0]
    news_vecs = vectors[1:]

    scores = cosine_similarity(tweet_vec, news_vecs)[0]

    return scores


# 🔹 Step 2: Rank news based on similarity
def get_ranked_news(tweet, news_list):
    titles = [news["title"] for news in news_list]

    scores = compute_similarity_scores(tweet, titles)

    ranked_news = []

    for i, news in enumerate(news_list):
        ranked_news.append({
            "title": news["title"],
            "link": news.get("link", ""),
            "raw_score": float(scores[i])
        })

    # Sort by similarity descending
    ranked_news.sort(key=lambda x: x["raw_score"], reverse=True)

    return ranked_news


# 🔹 Step 3: Normalize scores (0–1 scaling)
def normalize_scores(news_list):
    scores = [n["raw_score"] for n in news_list]

    if len(scores) == 0:
        return news_list

    min_s = min(scores)
    max_s = max(scores)

    if max_s == min_s:
        for n in news_list:
            n["score"] = 1.0
        return news_list

    for n in news_list:
        n["score"] = (n["raw_score"] - min_s) / (max_s - min_s)

    return news_list


# 🔹 Step 4: Get top K news
def get_top_k_news(tweet, news_list, top_k=5):
    ranked = get_ranked_news(tweet, news_list)
    top_news = ranked[:top_k]
    top_news = normalize_scores(top_news)

    return top_news


# 🔹 Step 5: Compute final similarity score (Top 3 Avg)
def compute_final_similarity_score(top_news, top_n=3, threshold=0.3):

    # Filter relevant news
    filtered = [n for n in top_news if n["score"] >= threshold]

    if len(filtered) == 0:
        return 0.0

    # Take top N
    selected = filtered[:top_n]

    # Compute average
    avg_score = sum(n["score"] for n in selected) / len(selected)

    return round(avg_score, 3)


# 🔹 Final Pipeline Function (USE THIS)
def similarity_pipeline(tweet, news_list):

    # Step 1: Get top 5 similar news
    top_news = get_top_k_news(tweet, news_list, top_k=5)

    # Step 2: Compute final similarity score
    final_score = compute_final_similarity_score(top_news)

    return {
        "top_news": top_news,
        "similarity_score": final_score
    }