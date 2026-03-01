# Bank Customer Churn Prediction

An ML-powered customer attrition prediction system built for the banking sector using Logistic Regression, Decision Tree, and Random Forest — with an interactive **ChurnSense** dashboard built in Streamlit.

Enter customer profile data and instantly get an AI-powered churn risk prediction with probability scores and a banker action plan.

---

## Features

- ML-based bank customer churn prediction
- 3 models trained and compared (LR · DT · RF)
- Instant risk classification with probability scores
- Risk meter, churn vs retention breakdown
- Banker action plan based on prediction outcome
- Professional bank-themed dark UI (Deep Black + Emerald Green)
- Animated background with floating grid
- Uses Churn_Modelling dataset (10,000 customers)
- Real-time prediction engine with saved model artifacts

---

## How It Works

### 1️⃣ Dataset

**Churn_Modelling.csv** — 10,000 bank customers across France, Germany, and Spain

| Feature | Description |
|---|---|
| CreditScore | Customer credit score (300–850) |
| Geography | Country (France / Germany / Spain) |
| Gender | Male / Female |
| Age | Customer age |
| Tenure | Years with the bank (0–10) |
| Balance | Account balance ($) |
| NumOfProducts | Banking products held (1–4) |
| HasCrCard | Has a credit card? (Yes/No) |
| IsActiveMember | Active account member? (Yes/No) |
| EstimatedSalary | Annual salary ($) |
| Exited | **Target** — Churned (1) / Stayed (0) |

---

### 2️⃣ Data Processing (Notebook)

- Dropped irrelevant columns → `RowNumber`, `CustomerId`, `Surname`
- Checked for missing values and duplicates
- Label encoding for categorical features → `Geography`, `Gender`
- Feature scaling → `StandardScaler`
- Train-test split → 80/20, stratified by target

---

### 3️⃣ EDA Performed

- Churn distribution (Stayed vs Churned)
- Churn rate by Geography (Germany highest)
- Age vs Churn boxplot
- Correlation heatmap across all numeric features

---

### 4️⃣ ML Models

- **3 Models Trained** → Logistic Regression, Decision Tree, Random Forest
- **Evaluation** → Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Best Model** → Random Forest (Accuracy: 86.6% | ROC-AUC: 84.7%)
- **Saved as** → `models/best_model.pkl` + `models/scaler.pkl` + encoders

---

## Model Results

| Model | Accuracy | Churn Recall | ROC-AUC |
|---|---|---|---|
| **Random Forest** | **86.6%** | **46%** | **84.7%** |
| Logistic Regression | 81.5% | 18% | — |
| Decision Tree | 78.4% | 52% | — |

> Random Forest selected as best model — highest accuracy with balanced precision/recall tradeoff.

---

## Key Findings

- **Germany** has significantly higher churn rate than France and Spain
- **Older customers** (40–60) churn more than younger ones
- Customers with **only 1 product** are at highest churn risk
- **Inactive members** are far more likely to exit
- **Account balance** is a stronger churn signal than salary

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Pandas & NumPy | Data manipulation |
| Matplotlib & Seaborn | EDA visualizations |
| Scikit-learn | ML models, preprocessing, evaluation |
| Pickle | Model serialization |
| Streamlit | Interactive web dashboard |

---

## Project Structure
```
bank-churn-prediction/
│
├── app.py                              ← Streamlit dashboard (ChurnSense UI)
├── Bank_Customer_Churn_Prediction.ipynb ← Full ML pipeline notebook
├── Churn_Modelling.csv                 ← Raw dataset
│
├── models/
│   ├── best_model.pkl                  ← Trained Random Forest model
│   ├── scaler.pkl                      ← StandardScaler
│   ├── le_geo.pkl                      ← Geography LabelEncoder
│   ├── le_gen.pkl                      ← Gender LabelEncoder
│   └── feature_names.pkl               ← Feature name list
│
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/your-username/bank-churn-prediction.git
cd bank-churn-prediction
```

### 2️⃣ Create virtual environment
```bash
python -m venv venv
```

### 3️⃣ Activate environment

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 4️⃣ Install requirements
```bash
pip install -r requirements.txt
```

### 5️⃣ Run the notebook first (to generate model files)
```bash
jupyter notebook Bank_Customer_Churn_Prediction.ipynb
```

### 6️⃣ Run the Streamlit app
```bash
streamlit run app.py
```

---

## requirements.txt
```
streamlit
pandas
numpy
scikit-learn
matplotlib
seaborn
```

---

## Dataset

Available on Kaggle: https://www.kaggle.com/datasets/radheshyamkollipara/bank-customer-churn
---

## Live Demo

https://bankrisk-ai.streamlit.app/

---

## Screenshots

![img alt](https://github.com/nikhil-kumarrr/images/blob/main/Screenshot%202026-03-01%20160355.png?raw=true)
![img alt](https://github.com/nikhil-kumarrr/images/blob/main/Screenshot%202026-03-01%20160411.png?raw=true)
