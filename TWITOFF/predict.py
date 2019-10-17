import pickle
from sklearn.linear_model import LogisticRegression
import numpy as np
from .models import User
from .twitter import BASILICA

def predict_user(user1_name, user2_name, tweet_text, cache=None):
    """Determine and return which user would be more likely to say the thing"""
    user_set = pickle.dumps((user1_name, user2_name))
    if cache and cache.exists(user_set):
        log_reg = pickle.loads(cache.get(user_set))
    else:
        user1 = User.query.filter(User.name == user1_name).one()
        user2 = User.query.filter(User.name == user2_name).one()
        user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
        user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
        embeddings = np.vstack([user1_embeddings, user2_embeddings])
        labels = np.concatenate([np.ones(len(user1.tweets)),
                                 np.zeros(len(user2.tweets))])
        log_reg = LogisticRegression().fit(embeddings, labels)
        cache and cache.set(user_set, pickle.dumps(log_reg))
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
