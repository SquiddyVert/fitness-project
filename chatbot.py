from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
import numpy as np
import re 

nltk.download('stopwords')
nltk.download('wordnet')
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    lemmatizer = WordNetLemmatizer()
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    text = ' '.join(tokens)
    return text

questions = [entry['question'] for entry in qna_list]
answers = [entry['answer'] for entry in qna_list]

processed_questions = [preprocess_text(question) for question in questions]  
vectorizer = TfidfVectorizer() 
question_vectors = vectorizer.fit_transform(processed_questions) 

def find_most_similar_question(user_query):
    processed_query = preprocess_text(user_query)
    query_vector = vectorizer.transform([processed_query])
    similarities = cosine_similarity(query_vector, question_vectors)
    best_match_index = np.argmax(similarities)
    return best_match_index, similarities[0][best_match_index] 

def chatbot():
    print("What is your name? ", end="")
    username = input() 
    print(f"\nQ&A support: Hi, {username}, welcome to Q&A support. How can I help you?\n")

    while True:
        user_input = input(f"{username}: ")
        if user_input.lower() == 'bye':
            print("Q&A support: Goodbye!")
            break

        best_match_index, similarity_score = find_most_similar_question(user_input)
        response = answers[best_match_index]
         
        print(f"Q&A support: {response}\n")

if __name__ == "__main__":
    chatbot()