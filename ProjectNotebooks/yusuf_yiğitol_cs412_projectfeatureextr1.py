# -*- coding: utf-8 -*-
"""Yusuf-Yiğitol-Cs412-ProjectFeatureExtR1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JXOc1Bb87E9kjlRMcD8oGDD1wSVmo8Dk
"""

import numpy as np
import pandas as pd
import gzip
import json
import nltk
from nltk.corpus import stopwords
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import re
import os

# Download Turkish Stopwords
nltk.download('stopwords')
turkish_stopwords = stopwords.words('turkish')

try:
    from google.colab import drive
    drive.mount('/content/drive')
    base_path = "/content/drive/MyDrive/CS 412/Project/"
except ImportError:
    base_path = "./"

train_classification_path = os.path.join(base_path, "train-classification.csv")
train_data_path = os.path.join(base_path, "training-dataset.jsonl.gz")
test_classification_path = os.path.join(base_path, "test-classification-round1.dat")
test_regression_path = os.path.join(base_path, "test-regression-round1.jsonl")

train_classification_df = pd.read_csv(train_classification_path)
train_classification_df = train_classification_df.rename(columns={'Unnamed: 0': 'user_id', 'label': 'category'})
train_classification_df["category"] = train_classification_df["category"].apply(str.lower)
username2_category = train_classification_df.set_index("user_id").to_dict()["category"]

# Stats about labels
print(train_classification_df.groupby("category").count())

username2posts_train = dict()
username2profile_train = dict()
username2posts_test = dict()
username2profile_test = dict()

with gzip.open(train_data_path, "rt") as fh:
    for line in fh:
        sample = json.loads(line)
        profile = sample["profile"]
        username = profile["username"]
        if username in username2_category:
            username2posts_train[username] = sample["posts"]
            username2profile_train[username] = profile
        else:
            username2posts_test[username] = sample["posts"]
            username2profile_test[username] = profile

train_profile_df = pd.DataFrame(username2profile_train).T.reset_index(drop=True)
test_profile_df = pd.DataFrame(username2profile_test).T.reset_index(drop=True)
print("Training profiles shape:", train_profile_df.shape)
print("Test profiles shape:", test_profile_df.shape)

def preprocess_text(text: str):
    text = text.casefold()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zçğıöşü0-9\s#@]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Prepare Corpus for TF-IDF
corpus = []
train_usernames = []
for username, posts in username2posts_train.items():
    train_usernames.append(username)
    cleaned_captions = []
    for post in posts:
        post_caption = post.get("caption", "")
        if post_caption:
            cleaned_captions.append(preprocess_text(post_caption))
    corpus.append("\n".join(cleaned_captions))

vectorizer = TfidfVectorizer(stop_words=turkish_stopwords, max_features=5000)
vectorizer.fit(corpus)

# Transform Data
x_post_train = vectorizer.transform(corpus)
y_train = [username2_category[uname] for uname in train_usernames]

# Prepare Test Data
test_usernames = []
test_corpus = []
for username, posts in username2posts_test.items():
    test_usernames.append(username)
    cleaned_captions = []
    for post in posts:
        post_caption = post.get("caption", "")
        if post_caption:
            cleaned_captions.append(preprocess_text(post_caption))
    test_corpus.append("\n".join(cleaned_captions))

x_post_test = vectorizer.transform(test_corpus)

# Ensure no "NA" in y_train
assert y_train.count("NA") == 0

# Train-Test Split
x_train, x_val, y_train, y_val = train_test_split(x_post_train, y_train, test_size=0.2, stratify=y_train)

# Train Naive Bayes Classifier
model = MultinomialNB()
model.fit(x_train, y_train)

# Evaluate on Train and Validation Data
print("Train Accuracy:", accuracy_score(y_train, model.predict(x_train)))
print("Validation Accuracy:", accuracy_score(y_val, model.predict(x_val)))
print("Validation Report:\n", classification_report(y_val, model.predict(x_val), zero_division=0))

# Predict Test Data
x_test_usernames = []
x_test_vectors = []

with open(test_classification_path, "r") as fh:
    for line in fh:
        username = line.strip()
        if username in test_usernames:
            x_test_vectors.append(x_post_test[test_usernames.index(username)].toarray()[0])
            x_test_usernames.append(username)

df_test = pd.DataFrame(np.array(x_test_vectors), columns=vectorizer.get_feature_names_out())

# Predict and Save Classification Results
predictions = model.predict(df_test)
output_classification = {uname: predictions[i] for i, uname in enumerate(x_test_usernames)}
output_classification_path = os.path.join(base_path, "prediction-classification-round1.json")

with open(output_classification_path, "w") as outfile:
    json.dump(output_classification, outfile)

print("Classification predictions saved.")

def predict_like_count(username, current_post=None):
    def avg_like_count(posts):
        total = sum(post.get("like_count", 0) or 0 for post in posts if post.get("id") != current_post)
        return total / len(posts) if posts else 0

    if username in username2posts_train:
        return avg_like_count(username2posts_train[username])
    elif username in username2posts_test:
        return avg_like_count(username2posts_test[username])
    return 0

# Process Test Regression Data
output_regression = []
output_regression_path = os.path.join(base_path, "prediction-regression-round1.json")

# Open and process the JSONL file
with open(test_regression_path, "r") as fh:
    for line in fh:
        try:
            sample = json.loads(line.strip())  # Each line should be a dictionary

            if isinstance(sample, dict) and "username" in sample:
                predicted_like = predict_like_count(sample["username"])
                sample["like_count"] = int(predicted_like)
                output_regression.append(sample)
            else:
                print(f"Skipped sample due to missing 'username': {sample}")
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}, line: {line.strip()}")
        except Exception as e:
            print(f"Unexpected error: {e}, line: {line.strip()}")

# Simplify Regression Output
simplified_regression_output = {
    sample["id"]: sample["like_count"] for sample in output_regression
}

# Save Simplified Regression Predictions
with open(output_regression_path, "w") as outfile:
    json.dump(simplified_regression_output, outfile)

print("Regression predictions saved in the expected format.")
