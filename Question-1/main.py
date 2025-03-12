import streamlit as st
from PIL import Image
import joblib
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

question="Question-1/"

def split_at_last_comma(text):
    last_comma_index = text.rfind(',')
    
    if last_comma_index != -1:
        before_comma = text[:last_comma_index]
        after_comma = text[last_comma_index + 1:]
        return before_comma, after_comma
    else:
        return text, '' 

def get_data(path):
    data = []
    with open(path, 'r', encoding='utf-16') as file:
        i = 0
        for line in file:
            if i == 0:
                column_names = line.strip().split(',')
                i=1
            else:
                X = split_at_last_comma(line.strip())
                data.append([X[0],X[1]])
        df = pd.DataFrame(data)
        df.columns=column_names
    return df

def train_and_save_model():
    df = get_data(f"{question}data/data.csv")
    test_df = df[df['Durum'] != 'Tarafsız']
    X = test_df['Gorus']
    y = test_df['Durum']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train_vec, y_train)
    
    joblib.dump(nb_classifier, f"{question}sentiment_model.pkl")
    joblib.dump(vectorizer, f"{question}vectorizer.pkl")
    st.success("Model başarıyla eğitildi ve kaydedildi!")

def load_model():
    model_path = f"{question}sentiment_model.pkl"
    vectorizer_path = f"{question}vectorizer.pkl"
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        nb_classifier = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        return nb_classifier, vectorizer
    else:
        st.warning("Model dosyaları bulunamadı. Modeli eğitmek ve kaydetmek için yukarıdaki düğmeye tıklayın.")
        return None, None

def predict_sentiment(text, model, vectorizer):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    return prediction

def main():
    st.title("Ka|Ve 2025 - Duygu Analiz Motoru")
    
    if not os.path.exists(f"{question}sentiment_model.pkl") or not os.path.exists(f"{question}vectorizer.pkl"):
        if st.button("Modeli Eğitin ve Kaydedin"):
            train_and_save_model()
    
    nb_classifier, vectorizer = load_model()
    if not nb_classifier or not vectorizer:
        return
    
    user_input = st.text_input("Metninizi girin:")
    submit_button = st.button("Duyguları Analiz Edin")
    
    if submit_button and user_input:
        sentiment = predict_sentiment(user_input, nb_classifier, vectorizer)
        st.success(f"Duygu: {sentiment}")
        
        if sentiment == "Olumlu":
            image = Image.open(f"{question}positive.png")
        else:
            image = Image.open(f"{question}negative.png")
        
        st.image(image, width=48)

if __name__ == "__main__":
    main()