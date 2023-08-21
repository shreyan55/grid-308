import os
import pickle
from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class Command(BaseCommand):
    help = 'Generate data for ML model'

    def handle(self, *args, **options):
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, "apps/ml/data/output.csv")
        
        data = pd.read_csv(file_path)
        products = data['pid'].unique()

        data['product_category_tree'] = data['product_category_tree'].fillna('')
        data['description'] = data['description'].fillna('')
        data['product_specifications'] = data['product_specifications'].fillna('')

        data = data[['pid', 'product_name', 'brand', 'product_category_tree', 'description', 'overall_rating', 'retail_price', 'discounted_price', 'image']]

        data['combined_text'] = data['product_name'] + ' ' + data['product_category_tree'] + ' ' + data['description']

        tfidf_vectorizer = TfidfVectorizer(stop_words='english', min_df=2, ngram_range=(1, 2))
        tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined_text'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        with open(os.path.join(current_directory, 'apps/ml/data/data.pkl'), 'wb') as f:
            pickle.dump(data, f)

        with open(os.path.join(current_directory, 'apps/ml/data/cosine_sim.pkl'), 'wb') as f:
            pickle.dump(cosine_sim, f)

        with open(os.path.join(current_directory, 'apps/ml/data/products.pkl'), 'wb') as f:
            pickle.dump(products, f)

        self.stdout.write(self.style.SUCCESS('Data generated successfully'))
