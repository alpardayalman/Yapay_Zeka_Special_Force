import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv("your_dataset.csv")
test_df = df[df['Durum'] != 'Tarafsız']
X = test_df['Gorus']
y = test_df['Durum']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

nb_classifier = MultinomialNB()
nb_classifier.fit(X_train_vec, y_train)

joblib.dump(nb_classifier, "sentiment_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model and vectorizer saved successfully.")
