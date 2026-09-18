# Spam Mail Detector
# Machine Learning + NLP

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------------
# 1. Load Dataset
# -----------------------------------

data = pd.read_csv("spam.csv")

# Dataset should contain:
# label   -> spam / ham
# message -> email text

data = data[["label", "message"]]

# Remove missing values
data.dropna(inplace=True)

# -----------------------------------
# 2. Convert Labels
# -----------------------------------

data["label"] = data["label"].map({
    "spam": 1,
    "ham": 0
})

# -----------------------------------
# 3. Split Dataset
# -----------------------------------

X = data["message"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# -----------------------------------
# 4. Convert Text into Numbers
# -----------------------------------

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# -----------------------------------
# 5. Train Machine Learning Model
# -----------------------------------

model = MultinomialNB()

model.fit(X_train_tfidf, y_train)

# -----------------------------------
# 6. Test Model
# -----------------------------------

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------------
# 7. Detect New Email
# -----------------------------------

print("\n===== SPAM MAIL DETECTOR =====")

while True:

    email = input("\nEnter your email message (or type 'exit'): ")

    if email.lower() == "exit":
        print("Program closed.")
        break

    # Convert email into TF-IDF
    email_tfidf = vectorizer.transform([email])

    # Prediction
    prediction = model.predict(email_tfidf)

    if prediction[0] == 1:
        print("🚨 Result: SPAM EMAIL")
    else:
        print("✅ Result: NOT SPAM")
