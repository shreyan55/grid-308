# Personalized Product Recommendation System </br>
## The aim is to enhance user experience by implementing a personalized product ranking system.</br>
The task is to develop an algorithm or model that can generate accurate and relevant product rankings for individual users. The ranking system should consider factors such as user preferences, past interactions, product popularity, and user similarity. It should be able to predict the most suitable products for a user based on their unique characteristics and preferences. You are not provided with a specific dataset for this challenge. Instead, you are expected to design and implement a solution that simulates user interactions and generates personalized rankings. You can define user profiles, product categories, and interaction patterns within your solution. To evaluate the effectiveness of your solution, you should define an appropriate metrics for measuring the accuracy and relevance of the rankings. You should also provide a report explaining your approach, describing the algorithms or techniques used, and discussing the strengths and limitations of your solution.

## Solution

#### 1. User Profiling and Preferences:
Problem: Define user profiles and preferences based on attributes such as age, gender, interests, and historical interactions.
Solution: Create user profiles with weighted preferences for different product categories. Utilize historical interactions to
determine the extent of interest in specific categories.
#### 2. Product Representation:
Problem: Define product categories and attributes that will be used to match user preferences.
Solution: Create a product catalog with categories and attributes such as price, features, and popularity. Represent products as
vectors with attributes as dimensions.
#### 3. User Similarity Calculation:
Problem: Determine how similar users are to each other to identify potential recommendations.
Solution: Calculate user similarity using metrics like cosine similarity or Pearson correlation based on their preferences and
interactions. This establishes connections between users with similar tastes.
#### 4. Predicting User Preferences:
Problem: Predict how much a user would like a product based on their preferences and interactions.
Solution: Combine collaborative filtering and content-based methods. Use user similarity scores and product attributes to predict
preferences. Assign scores to products and sort them to generate initial recommendations.5. Popularity and Diversity:
Problem: Balance between popular products and diverse recommendations to avoid recommending only mainstream items.
Solution: Incorporate product popularity as a factor in the ranking process. Apply techniques like matrix factorization to diversify
recommendations and account for niche interests.
#### 6. Generating Personalized Rankings:
Problem: Create personalized rankings that consider user preferences, historical interactions, user similarity, and product popularity.
Solution: Combine predicted preference scores, historical interactions, and popularity scores. Sort products in descending order
to generate personalized rankings.
#### 7. Evaluation Metrics:
Problem: Define metrics to measure the accuracy and relevance of the generated rankings.
Solution: Define metrics such as Precision, Recall, Mean Average Precision (MAP), Coverage, Diversity. All these metrics will be
represented using graphs and will help evaluate the effectiveness of the ranking system.
#### 8. Simulating User Interactions:
Problem: Generate simulated user interactions for testing and evaluating the ranking system.
Solution: Simulate user interactions by randomly generating preferences and historical actions. Alternatively, use a synthetic dataset
generator to create more realistic interaction patterns.
#### 9. Cold Start Problem:
Problem: Address the issue of providing recommendations for new users or products with limited data.
Solution: Utilize content-based recommendations initially, based on the attributes of the new user or product. Gradually transition to
collaborative recommendations as more interaction data becomes available.
</br>
</br>

#### This is the data set used for the project: https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products

#### This is the block diagram of the approach of solution of this project:
![WhatsApp Image 2023-10-03 at 23 43 07](https://github.com/shreyan55/grid-308/assets/78748065/e2e13f36-7736-4e64-87de-1d03675c58a1)

#### The Demo of this project is demonstrated through this video:

https://github.com/shreyan55/grid-308/assets/78748065/1253c61a-8074-4235-af85-9eba48a5d849












