import math

def normalize_engagement(likes, retweets, comments):
    return (
        math.log1p(likes) +
        2 * math.log1p(retweets) +
        1.5 * math.log1p(comments)
    )

def verified_score(is_verified):
    return 1.0 if is_verified else 0.5

def compute_user_credibility(likes, retweets, comments, verified):

    engagement = normalize_engagement(likes, retweets, comments)

    engagement_norm = min(1.0, engagement / 10)

    verified_val = verified_score(verified)

    credibility = (
        0.6 * verified_val +
        0.4 * engagement_norm
    )

    return round(credibility, 3)