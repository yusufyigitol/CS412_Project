# Machine Learning Course Project: Instagram Influencers

### Created by: Yusuf Yiğitol

---

## Overview

This project was part of the CS412 Machine Learning course and aimed to classify Instagram accounts into categories and predict post interactions. Over three rounds, I improved the pipeline by refining feature extraction, testing different machine learning models, and enhancing regression predictions.

---

## Implementation

In **Round 1**, I started with a Naive Bayes classifier for account category prediction and used a simple baseline approach for regression by averaging likes from training data. Captions were processed with TF-IDF, and the classifier achieved decent initial accuracy.

For **Round 2**, I continued with Naive Bayes but focused on improving feature representation and data balance. Regression predictions were also refined by incorporating patterns from training posts.

In **Round 3**, I shifted to Logistic Regression for classification, using grid search to optimize hyperparameters. For regression, I used a Gradient Boosting Regressor with additional features like average likes and caption lengths. This round produced the best results in both tasks.

---

## How to Run

The scripts for each round are organized to follow a step-by-step process. You can run them after preparing the data and updating the file paths. Outputs are generated as JSON files for both classification and regression tasks.

---

## Conclusion

This project demonstrates how iterative improvements in models and features can enhance performance. Starting with simple approaches and gradually adopting advanced techniques allowed for significant progress in solving the classification and regression tasks effectively.

