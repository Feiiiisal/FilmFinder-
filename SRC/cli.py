import pickle
import pandas as pd

# Load the data objects from the file
with open('recommendation_data.pkl', 'rb') as file:
    cosine_sim_df, movie_matrix = pickle.load(file)


def get_weighted_recommendations(user, cosine_sim_df=cosine_sim_df, movie_matrix=movie_matrix):
    # Check if the user is in the matrix
    if user not in movie_matrix.index:
        print("User not found. Returning popular movies as fallback.")
        return movie_matrix.mean().sort_values(ascending=False).index[:5]
    
    # User's ratings
    user_ratings = movie_matrix.loc[user].dropna()

    # Initialize an empty DataFrame for weighted ratings
    weighted_ratings = pd.DataFrame(index=cosine_sim_df.index, columns=['score']).fillna(0)

    # Iterate through movies rated by the user
    for movie, rating in user_ratings.items():
        if movie in cosine_sim_df.columns:
            # Compute weighted ratings
            weighted_ratings['score'] += cosine_sim_df[movie] * rating

    # Normalize by the sum of the user's ratings
    recommendation_scores = weighted_ratings['score'] / user_ratings.sum()

    # Sort and return top recommendations
    top_recommendations = recommendation_scores.sort_values(ascending=False)
    return top_recommendations.index[top_recommendations.index != user][:5]

# Example usage
user = 'Alice' 
print(get_weighted_recommendations(user))



def main():
    while True:
        user_input = input("Enter your username (or 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            break
        try:
            recommendations = get_weighted_recommendations(user_input, cosine_sim_df, movie_matrix)
            print(f"Recommended movies for {user_input}: {recommendations}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()