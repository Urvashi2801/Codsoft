import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Sample Data (Items & Users)

# Items: Movies, Books, and Products
items = pd.DataFrame({
    'item_id': range(1, 13),
    'title': [
        'Avengers: Endgame', 'Iron Man', 'Harry Potter', 'Sherlock Holmes',
        'Apple iPhone 14', 'Samsung Galaxy S22', 'Amazon Kindle',
        'The Hobbit', 'Sony Headphones', 'Captain America', 
        'Digital Watch', 'Bluetooth Speaker'
    ],
    'category': [
        'Movie', 'Movie', 'Book', 'Movie',
        'Product', 'Product', 'Product',
        'Book', 'Product', 'Movie',
        'Product', 'Product'
    ],
    'description': [
        'Superheroes team up to defeat a powerful alien villain.',
        'A genius billionaire builds a powerful suit to fight crime.',
        'A young wizard faces challenges at a magical school.',
        'A detective solves mysteries in 19th century London.',
        'Smartphone with A16 chip, retina display and dual cameras.',
        'High-end Android phone with AMOLED display and 108MP camera.',
        'E-reader for digital books with high-resolution display.',
        'Fantasy adventure involving dragons, battles, and a quest.',
        'Wireless headphones with noise cancellation and deep bass.',
        'A patriotic superhero fights in World War II.',
        'Fitness tracking digital watch with heart-rate monitor.',
        'Portable Bluetooth speaker with deep bass and long battery life.'
    ]
})

# User ratings (user_id, item_id, rating)
ratings = pd.DataFrame({
    'user_id': [1,1,1,2,2,3,3,4,4,5,5,6,6,7,8,9,10,10,11,12],
    'item_id': [1,2,3,1,4,2,5,3,6,7,8,1,9,10,11,3,3,12,5,6],
    'rating':  [5,4,5,4,5,4,5,5,4,5,4,5,3,4,4,5,4,5,3,4]
})


# Content-Based Filtering Class


class ContentBasedRecommender:
    def __init__(self, items_df):
        self.items = items_df
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.item_indices = None
        self._prepare()

    def _prepare(self):
        vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = vectorizer.fit_transform(self.items['description'])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        self.item_indices = pd.Series(self.items.index, index=self.items['title'])

    def recommend(self, item_title, top_n=5):
        if item_title not in self.item_indices:
            return []
        
        idx = self.item_indices[item_title]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        item_indices = [i[0] for i in sim_scores]
        return self.items.iloc[item_indices][['title', 'category', 'description']]


# Collaborative Filtering Class


class CollaborativeRecommender:
    def __init__(self, ratings_df, items_df):
        self.ratings = ratings_df
        self.items = items_df
        self.user_similarity = None
        self.user_item_matrix = None
        self._prepare()

    def _prepare(self):
        self.user_item_matrix = self.ratings.pivot(index='user_id', columns='item_id', values='rating').fillna(0)
        self.user_similarity = cosine_similarity(self.user_item_matrix)

    def recommend(self, user_id, top_n=5):
        if user_id not in self.user_item_matrix.index:
            return []
        
        sim_scores = list(enumerate(self.user_similarity[user_id - 1]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]

        scores = {}
        for sim_user, sim in sim_scores:
            sim_user_id = sim_user + 1
            sim_user_ratings = self.ratings[self.ratings['user_id'] == sim_user_id]

            for _, row in sim_user_ratings.iterrows():
                if row['item_id'] not in self.ratings[self.ratings['user_id'] == user_id]['item_id'].values:
                    if row['item_id'] not in scores:
                        scores[row['item_id']] = sim * row['rating']
                    else:
                        scores[row['item_id']] += sim * row['rating']

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
        item_ids = [item_id for item_id, _ in sorted_scores]
        return self.items[self.items['item_id'].isin(item_ids)][['title', 'category', 'description']]


# Hybrid Recommendation Function

def hybrid_recommendation(user_id, liked_item_title, content_model, collab_model, top_n=3):
    print(f"\n📚 Content-Based Recommendations for '{liked_item_title}':")
    content_recs = content_model.recommend(liked_item_title, top_n)
    print(content_recs.to_string(index=False))

    print(f"\n👤 Collaborative Recommendations for User {user_id}:")
    collab_recs = collab_model.recommend(user_id, top_n)
    print(collab_recs.to_string(index=False))


# Run the Full System


# Initialize recommenders
content_recommender = ContentBasedRecommender(items)
collaborative_recommender = CollaborativeRecommender(ratings, items)

# Test: Recommend for user 6 who likes "Harry Potter"
hybrid_recommendation(user_id=6, liked_item_title='Harry Potter', 
                      content_model=content_recommender, 
                      collab_model=collaborative_recommender, 
                      top_n=4)
