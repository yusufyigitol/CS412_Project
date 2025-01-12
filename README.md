# Machine Learning Course Project: Instagram Influencers

### Created by: Yusuf Yiğitol

---

## Overview

This project was part of the CS412 Machine Learning course and aimed to classify Instagram accounts into categories and predict post interactions. Over three rounds, I improved the pipeline by refining feature extraction, testing different machine learning models, and enhancing classification and regression predictions.

---

## Implementation

In **Round 1**, I started with a Naive Bayes classifier for account category prediction and used a simple baseline approach for regression by averaging likes from training data. Captions were processed with TF-IDF, and the classifier achieved decent initial accuracy.

For **Round 2**, I continued with Naive Bayes but focused on improving feature representation and data balance. Regression predictions were also refined by combining patterns from training posts.

In **Round 3**, I shifted to Logistic Regression for classification, using grid search to optimize hyperparameters. For regression, I used a Gradient Boosting Regressor with additional features like average likes and caption lengths. This round produced the best results in both tasks.

---

## How to Run

The scripts for each round are organized to follow a step-by-step process. Before running the scripts, ensure that the data files required for training the models are placed in the correct directories on your local machine and that related paths in the notebooks are adjusted accordingly. Finally, outputs for both classification and regression tasks are provided in the sucourse submission.

---

## Conclusion

This project demonstrates how step-by-step improvements in models and features can enhance performance. Starting with simple approaches and slowly adopting advanced techniques have allowed the classification and regression tasks to be solved effectively.

