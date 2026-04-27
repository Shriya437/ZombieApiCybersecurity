# 🧟‍♂️ Zombie API Detection System (AETHER Sentinel)

A Python-based system for detecting **Zombie API behavior** using **data analysis, feature engineering, visualization, and machine learning**, with an added layer of **face authentication security**.

---

## 🚀 Project Overview

Zombie APIs are hidden or compromised endpoints that show abnormal traffic patterns and can be exploited for attacks like DDoS, scanning, and bot activity.

This project focuses on:

* 📊 Understanding network data
* ⚙️ Engineering meaningful features
* 📈 Visualizing behavior patterns
* 🤖 Applying ML for detection
* 🔐 Securing access using face authentication

---

## 🧠 Key Highlights

* Strong focus on **Feature Engineering**
* Extensive **Data Visualization & Insights**
* Hybrid ML approach (Anomaly + Classification)
* **Explainable Outputs (Risk Score + Behavior Tags)**
* Secure dashboard using **Face Authentication**

---

## 📁 Project Structure

```bash
Python_Zombie_Api/
│
├── auth/                          # Face authentication (FaceNet, OpenCV)
├── ZombieApi/
│   ├── artifacts/                 # Saved models, scaler, encoders
│   ├── dashboard/                 # FastAPI backend + frontend UI
│   ├── data/                      # Processed datasets (train/test)
│   ├── data_prep/                 # Data cleaning scripts
│   ├── feature_engineering/       # Feature engineering pipeline
│   │   └── feature_engineering_ml.py
│   ├── models/                    # ML training & prediction
│
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Core Components

### 🔹 1. Data Handling

* Cleaned large dataset (~2M+ rows)
* Removed NaN and infinite values
* Selected numerical features
* Used sampling for performance optimization

---

### 🔹 2. Feature Engineering (Core Strength ⭐)

Converted raw traffic into behavior-based features:

#### 📡 Traffic Features

* `packets_per_second` → traffic speed
* `bytes_per_packet` → packet size

#### ⚖️ Behavioral Features

* `packet_ratio` → imbalance detection
* `forward_dominance` → one-sided traffic

#### 🚨 Attack Indicators

* `flag_ratio` → SYN flood detection
* `reset_rate` → abnormal resets

#### ⏱️ Timing Features

* `time_between_requests`
* `iat_variability`

#### 🔁 Pattern Features

* `burstiness` → sudden spikes
* `traffic_imbalance`
* `repeat_call_ratio` → bot behavior

#### 🌐 Network Behavior

* `endpoint_diversity` → port scanning

---

### 🔹 3. Data Preprocessing

* Log transformation for skewed features
* StandardScaler for normalization
* Correlation-based feature removal
* Random Forest-based feature importance

---

### 🔹 4. Data Visualization 📊

Used multiple plots to extract insights:

* Scatter → behavior separation
* Boxplots → distribution comparison
* KDE → timing patterns
* Histograms → feature spread
* Heatmaps → correlation

👉 Helps understand **attack vs normal behavior clearly**

---

### 🔹 5. Machine Learning 🤖

#### Isolation Forest

* Detects anomalies (unknown attacks)

#### Random Forest

* Classifies attack type
* Provides confidence score

#### Insight Layer

* `risk_score`
* `risk_level` (High / Medium / Low)
* `behavior_tag`

---

### 🔹 6. Face Authentication 🔐

Secures system access using:

* OpenCV → image capture
* MTCNN → face detection
* FaceNet → embeddings
* Cosine similarity → verification

👉 Only authorized users can access the dashboard

---

### 🔹 7. Backend (FastAPI)

Endpoints:

* `/face-login` → authentication
* `/upload-data` → run ML pipeline
* `/results` → return insights

---

### 🔹 8. Frontend

* Dashboard with visual insights
* Secure login system
* Dynamic results display

---

## 🔁 System Workflow

```text
Face Login → Upload Data → Feature Engineering → Visualization → ML → Insights
```

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/ZombieApi.git
cd Python_Zombie_Api

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Run the Project

### Train Models

```bash
python ZombieApi/models/train.py
```

### Start Server

```bash
cd ZombieApi/dashboard
uvicorn main:app --reload
```

### Open in Browser

```
http://127.0.0.1:8000
```

---

## 📊 Output

* Anomaly detection
* Attack classification
* Risk score & level
* Behavioral insights

---

## 🔮 Future Scope

* Real-time monitoring
* Graph-based detection
* Cloud deployment
* Integration with security tools

---


## 📌 Conclusion

This project focuses on **understanding network behavior through data**, rather than just prediction.

It transforms raw traffic into **actionable and explainable insights**, making intrusion detection more effective and interpretable.

---

⭐ *Star the repo if you found it useful!*
