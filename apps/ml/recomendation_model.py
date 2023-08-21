from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import os 
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import copy
from collections import defaultdict
import pickle
from apps.user.models import Customer
from apps.interaction.models import Interaction
cosine_sim=[]
data=[]
similar_users_dict={}


def make_data():
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory,"apps/ml/data/flipkart_com-ecommerce_sample.csv")
    # Load the dataset
    data = pd.read_csv(file_path)
    products=data['pid'].unique()

    # Clean product category tree text (replace NaN with empty string)
    data['product_category_tree'] = data['product_category_tree'].fillna('')
    data['description'] = data['description'].fillna('')
    data['product_specifications'] = data['product_specifications'].fillna('')

    # Keep only relevant columns
    data = data[['pid', 'product_name', 'brand', 'product_category_tree', 'description', 'overall_rating', 'retail_price','discounted_price', 'image']]

    # Combine relevant columns into a single text
    data['combined_text'] = data['product_name'] + ' ' + data['product_category_tree'] + ' ' + data['description']

    # Create a TF-IDF vectorizer with tuned parameters
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', min_df=2, ngram_range=(1, 2))

    # Fit and transform the combined text
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined_text'])

    # Calculate the cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    with open(os.path.join(current_directory,'apps/ml/data/data.pkl'), 'wb') as f:
        pickle.dump(data, f)
    
    with open(os.path.join(current_directory,'apps/ml/data/cosine_sim.pkl'), 'wb') as f:
        pickle.dump(cosine_sim, f)
        
    with open(os.path.join(current_directory,'apps/ml/data/products.pkl'), 'wb') as f:
        pickle.dump(products, f)





def get_item_score(itemlist, item_id):
    # itemlist=[
    # ('SRTEH2FF9KEDEFGF', 0.6),
    # ('SBEEH3QGU7MFYJFY', 0.6),
    # ('SHOEH4GRSUBJGZXE', 0.7)
    # ]
    # item_id="SRTEH2F6HUZMQ6SJ"
    with open(os.path.join(os.getcwd(),'apps/ml/data/data.pkl'), 'rb') as f:
        data = pickle.load(f)
    with open(os.path.join(os.getcwd(),'apps/ml/data/cosine_sim.pkl'), 'rb') as f:
        cosine_sim = pickle.load(f)
    index0 = data[data['pid'] == item_id].index[0]
    result=0
    no=0
    for item in itemlist:
        item_key=item
        index1 = data[data['pid'] == item_key].index[0]
        result+=cosine_sim[index0][index1]
        no=no+1
    result=result/no
    return result



def get_user_similarity_matrix(user_id, percentile=90):
    # print(os.getcwd)
    # Load the dataset
    users_dataset =  Customer.objects.all().values("id","age","gender","intrest")
    data = pd.DataFrame(users_dataset)
    age_bins = [0, 18, 30, 50, 100]  # Adjust the bins as needed
    age_labels = ['0-18', '19-30', '31-50', '51+']

    # Use pd.cut() to create age groups
    data['age_group'] = pd.cut(data['age'], bins=age_bins, labels=age_labels, right=False)

    # Select relevant columns for user characteristics
    user_data = data[['id', 'age_group', 'gender', 'intrest']]

    # Handle missing values
    user_data.loc[:, 'intrest'] = user_data['intrest'].fillna('')


    # Encode categorical features
    label_encoders = {}
    for column in ['age_group', 'gender']:
        le = LabelEncoder()
        user_data[column] = le.fit_transform(user_data[column])
        label_encoders[column] = le

    # Feature extraction for 'intrest' using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    intrest_tfidf = tfidf_vectorizer.fit_transform(user_data['intrest'])

    # Calculate cosine similarity between users based on their characteristics
    user_similarity_matrix = cosine_similarity(user_data[['age_group', 'gender']], dense_output=False)

    # print ('User similarity matrix',user_similarity_matrix)

    return user_similarity_matrix



def generate_user_product_matrix():
    user_product_interaction_matrix = defaultdict(lambda: defaultdict(int))
    user_product_event_matrix = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    user_product_single_value_matrix = defaultdict(lambda: defaultdict(int))
    
    data = Interaction.objects.all().values_list('customer__id','product__pid','interaction','rating')

    for row in data:
        user_id, product_id, event, rating = row[0], row[1], row[2], row[3]

        if event == "click":
            user_product_interaction_matrix[user_id][product_id] = 1

        user_product_event_matrix[user_id][product_id][event] += 1

        if event == "order":
            user_product_single_value_matrix[user_id][product_id] = 5
        elif event == "rating":
            user_product_single_value_matrix[user_id][product_id] = rating
        elif event == "cart":
            user_product_single_value_matrix[user_id][product_id] = 4
        elif event == "wishlist":
            user_product_single_value_matrix[user_id][product_id] = 3

    final_matrix = defaultdict(lambda: defaultdict(int))

    for user_id in user_product_interaction_matrix.keys():
        for product_id in user_product_interaction_matrix[user_id].keys():
            views = sum(user_product_event_matrix[user_id][product_id].values())
            if views > 0:
                score = user_product_single_value_matrix[user_id][product_id] * views
                final_matrix[user_id][product_id] = score

    # print(final_matrix)

    max_score = max(score for user_scores in final_matrix.values() for score in user_scores.values())
    
    if max_score != 0:
        normalized_matrix = {
            user_id: {
                product_id: score / max_score for product_id, score in user_scores.items()
            }
            for user_id, user_scores in final_matrix.items()
        }
    else:
        normalized_matrix = final_matrix  # To handle the case where max_score is 0

    return normalized_matrix


def process_result_matrix(result_matrix):
    
    user_list=Customer.objects.all().values('id')
    users=[item['id'] for item in user_list]
    with open(os.path.join(os.getcwd(),'apps/ml/data/products.pkl'), 'rb') as f:
        products = pickle.load(f)
    
    new_result_matrix=copy.deepcopy(result_matrix)

    # List to store tuples with missing or zero entries
    missing_entries = []

    # Iterate through users and products
    for user in users:
        for product in products:

            if user not in result_matrix or product not in result_matrix[user] or result_matrix[user][product] == 0.00:
                missing_entries.append((user, product))

    # for user, product, score in result_matrix:
    for entry in missing_entries:
        user_or, item_or = entry

        items_matrix = []
        user_items=[]

        items = result_matrix[user_or].keys()
        for item in items:
            user_items.append((user_or, item))
        

        user_items.sort(key=lambda x: x[1], reverse=True) # Sort items by score in descending order
        top_items = user_items[:10]  # Get top 10 items for the user
        for item in top_items:
            items_matrix.append(str(item[1]))     
        value = get_item_score(items_matrix, item_or)

        new_result_matrix[user_or][item_or] = value

    return new_result_matrix


def covert_to_format(a):
    user_item_score_matrix = {}

    for user_id, item_scores in a.items():
        item_score_list = []
        for item, score in item_scores.items():
            item_score_list.append((item, score))
        user_item_score_matrix[user_id] = item_score_list

    return(user_item_score_matrix)



def collaborative_filtering(user_item_score_matrix):
    # Convert user_item_score_matrix to a numeric matrix
    users = list(user_item_score_matrix.keys())
    items = list(set(item for items in user_item_score_matrix.values() for item, _ in items))
    num_users = len(users)
    num_items = len(items)
    
    user_indices = {user: i for i, user in enumerate(users)}
    item_indices = {item: j for j, item in enumerate(items)}
    
    score_matrix = np.zeros((num_users, num_items))
    
    for user, item_scores in user_item_score_matrix.items():
        user_index = user_indices[user]
        for item, score in item_scores:
            item_index = item_indices[item]
            score_matrix[user_index, item_index] = score
    
    # Perform SVD on the score matrix
    U, sigma, Vt = np.linalg.svd(score_matrix)
    
    # Calculate the probability of a user being recommended an item
    user_similarity_matrix = cosine_similarity(U)
    recommendation_matrix = np.dot(user_similarity_matrix, score_matrix)
    
    # Normalize values in the recommendation matrix from 0 to 1 using Min-Max normalization
    min_val = np.min(recommendation_matrix)
    max_val = np.max(recommendation_matrix)
    recommendation_matrix = (recommendation_matrix - min_val) / (max_val - min_val)
    
    # Create the output in the specified format
    normalized_recommendations = {}
    for i, user in enumerate(users):
        item_scores = [(items[j], recommendation_matrix[i, j]) for j in range(num_items)]
        item_scores = sorted(item_scores, key=lambda x: x[1], reverse=True)
        normalized_recommendations[user] = item_scores
    
    return normalized_recommendations









def recommend_items(user_id):
    
    user_similarity_matrix = get_user_similarity_matrix(user_id)
    print("got user_similarity_matrix")
    user_product_matrix = generate_user_product_matrix()
    print("got user_product_matrix")
    print(user_product_matrix)
    result_matrix = process_result_matrix(user_product_matrix)
    print("got result_matrix")
    formatted_matrix=covert_to_format(result_matrix)
    print("got formatted_matrix")
    user_item_score_matrix = collaborative_filtering(formatted_matrix)
    print("got user_item_score_matrix")
    user_similarity_matrix = [
    (1, 0.8),
    (2, 0.6)
    ]

    # user_item_score_matrix = {
    #     'user1': [('uiklukikjm', 0.9), ('rterhr', 0.7)],
    #     'user2': [('rterhr', 0.8), ('fdgdsfd', 0.6)],
    #     'user3': [('uiklukikjm', 0.5), ('fdgdsfd', 0.7)]
    # }
    
    # Step 1: Extract users with user IDs in user_similarity_matrix
    similar_users = [user_id for user_id, _ in user_similarity_matrix]

    # Step 2: Calculate item_probability for each item
    item_probability = {}
    for user_id, similarity_score in user_similarity_matrix:
        if user_id not in similar_users:
            continue
        for item_id, item_score in user_item_score_matrix[user_id]:
            if item_id not in item_probability:
                item_probability[item_id] = 0
            item_probability[item_id] += similarity_score * item_score

    # Step 2b: Calculate the weighted average of item_score for each item
    for item_id in item_probability:
        item_probability[item_id] /= len(similar_users)

    # Return the dictionary with item IDs as keys and item probabilities as values
    return item_probability





