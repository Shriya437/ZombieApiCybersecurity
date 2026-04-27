# Zombie API: Intelligent Network Intrusion & API Abuse Detection System

## 🔹 1. PROBLEM STATEMENT
Modern web infrastructure is increasingly vulnerable to "Zombie APIs"—abandoned, undocumented, or poorly secured endpoints that serve as backdoors for malicious actors. Traditional rule-based security systems are failing because they rely on static signatures and cannot adapt to zero-day attacks, sophisticated DDoS campaigns, or stealthy bot activity. 

**The Real-World Problem:** Organizations lack real-time, explainable intelligence to detect when an API is being abused or experiencing anomalous traffic patterns. We need a system that not only flags bad traffic but explains *why* it's bad, bridging the gap between raw network packets and actionable cybersecurity insights.

**Industry Relevance:** In the era of microservices, API abuse constitutes a massive percentage of cyberattacks. Our solution directly targets API security, bot detection, and automated intrusion detection—critical areas for modern cloud environments.

---

## 🔹 2. DATASET UNDERSTANDING
To train a robust, real-world ready model, we utilized the **CICIDS2017** dataset.

*   **Why CICIDS2017?** It contains a comprehensive, highly realistic mix of modern benign traffic and up-to-date attack scenarios (DDoS, Brute Force, Web Attacks, Port Scans, Infiltration). It includes deep packet-level features rather than just high-level logs.
*   **Key Columns & Networking Relevance:**
    *   **Flow Duration:** The time elapsed from the first to the last packet in a flow. Abnormal durations can indicate slow-rate attacks (like Slowloris).
    *   **Flow Bytes/s & Packets/s:** Measures traffic volume. Massive spikes indicate volumetric DDoS or flooding.
    *   **IAT (Inter Arrival Time):** The time between packets. Consistent, robotic IATs strongly suggest automated bot scanning or scraping.
    *   **Flag Counts (SYN, ACK, RST):** TCP flags controlling connection states. An imbalance here (e.g., too many SYN requests without ACK) is the fingerprint of a SYN Flood attack.

---

## 🔹 3. DATA CLEANING + FEATURE ENGINEERING
Data quality dictates model performance. We executed a rigorous, multi-stage preprocessing pipeline:

*   **Cleaning:** Handled missing values (`NaN`) and replaced infinite values (`np.inf`) with 0 to prevent model corruption.
*   **Skewness & Transformation:** Analyzed feature skewness. For features with high skewness (>1), we applied **Log1p Transformation** (`np.log1p`) to normalize the distributions, making the data more digestible for distance-based anomaly detection.
*   **Scaling & Reduction:** Applied `StandardScaler` to ensure all features contribute equally. Conducted correlation analysis to identify highly correlated pairs (>0.95), strategically dropping redundant columns to prevent multicollinearity while preserving the most important signals.

**Engineered Behavioral Features:**
Instead of relying on raw packet counts, we engineered high-level behavioral signals:
*   `packet_ratio` & `forward_dominance`: Ratio of forward to backward packets. High forward dominance without responses signals scanning or blind flooding.
*   `burstiness`: Multiplying Packets/s by IAT Std Dev to detect sudden, erratic spikes in traffic typical of application-layer DDoS.
*   `flag_ratio`: SYN / ACK ratio. Critical for detecting TCP handshake anomalies.
*   `endpoint_diversity`: Measures how many different ports an IP is hitting. High diversity indicates horizontal Port Scanning.
*   `iat_variability`: Timing irregularities that differentiate human web browsing from scripted bot attacks.

---

## 🔹 4. DATA VISUALIZATION + INSIGHTS
To understand the latent space of our network traffic, we built comprehensive visualizations:

*   **Scatter Plots (Flow Duration vs Bytes/s):** Shows traffic volume over time. *Insight:* Isolates high-volume, short-duration bursts (classic DDoS) from low-volume, long-duration flows (stealthy data exfiltration).
*   **Boxplots (Feature Distributions):** Maps the spread of variables like `packet_ratio`. *Insight:* Highlights extreme outliers, helping us set the optimal clipping thresholds (99th percentile) during preprocessing.
*   **KDE Plots (Timing Behavior):** Visualizes the density of Inter-Arrival Times (IAT). *Insight:* Shows distinct multi-modal distributions separating human traffic (variable timing) from bot traffic (highly rigid timing).
*   **Histograms:** Tracks the distribution of attack classes across different days. *Insight:* Ensures our training data maintains a realistic class balance without extreme biases.
*   **Correlation Heatmap:** Visualizes feature dependencies. *Insight:* Validates our feature reduction strategy by confirming that remaining features provide orthogonal, non-overlapping information.

---

## 🔹 5. MACHINE LEARNING PIPELINE
We engineered a **Hybrid Intelligence Architecture** combining both unsupervised and supervised learning.

1.  **Isolation Forest (Unsupervised Anomaly Detection):**
    *   *Why?* It doesn't rely on known attack labels. It isolates data points by randomly selecting features.
    *   *Output:* Generates an `anomaly_score` (distance from "normal" traffic) and an `is_anomaly` boolean flag. It catches zero-day attacks that the supervised model has never seen.
2.  **Random Forest (Supervised Classification):**
    *   *Why?* Highly robust, non-linear classifier for known attack types.
    *   *Output:* Performs multi-class classification (DDoS, PortScan, WebAttack, etc.) and generates a `confidence` probability score.
3.  **The Combined Hybrid Engine:**
    *   We don't just output raw predictions. We synthesize them into a weighted **Risk Score**.
    *   `risk_score = (is_anomaly * 0.5) + ((1 - confidence) * 0.3) + (normalized_pps * 0.2)`
    *   *Power:* This formula intelligently penalizes traffic that the Random Forest is unsure about (low confidence), while heavily weighting true statistical anomalies and traffic spikes.

---

## 🔹 6. INSIGHT ENGINE (Explainable AI)
Security dashboards are useless if analysts don't understand the alerts. Our Insight Engine translates math into English:

*   **Risk Level:** The `risk_score` is scaled (0-1) and bucketed into actionable tiers: **High (>0.8)**, **Medium (>0.5)**, and **Low**.
*   **Behavioral Tagging:** 
    *   `packets_per_second` > 90th percentile → **"High Traffic Burst"**
    *   `flag_ratio` (SYN/ACK) > 0.5 → **"SYN Flood Pattern"**
    *   `packet_ratio` > 2.0 → **"Scanning Behavior"**
*   **Explanation Generation:** The engine dynamically concatenates these tags to generate plain-text explanations (e.g., *"SYN imbalance indicates possible DDoS attack + Traffic pattern deviates significantly from baseline"*), moving from a "Black Box" model to transparent, Explainable AI.

---

## 🔹 7. TEMPORAL INTELLIGENCE
Attacks happen over time, not in isolation.
*   **Time Buckets:** We bin the `Flow Duration` into 10 discrete intervals using Pandas.
*   **Trend Analysis:** By grouping `is_anomaly` sums across these buckets, we generate a temporal curve that allows the frontend to graph precisely *when* an attack burst occurred during the packet capture window.

---

## 🔹 8. FACE AUTHENTICATION SYSTEM
A secure dashboard requires secure access. We implemented a Zero-Trust biometric entry point.

*   **Architecture:** Uses OpenCV for video capture, **MTCNN** for robust face detection (cropping the face from the background), and **FaceNet (InceptionResnetV1)** for generating a 512-dimensional facial embedding.
*   **Verification Logic:** 
    1.  `build_face_database()`: Pre-computes average embeddings for authorized admins using reference images.
    2.  `admin_login()`: Captures real-time webcam frames, computes the embedding, and calculates **Cosine Similarity** against the database.
    3.  If similarity > `0.65` (Threshold), access is granted.
*   **Impact:** Prevents unauthorized personnel from accessing sensitive threat intelligence data, eliminating password-based vulnerabilities.

---

## 🔹 9. BACKEND ARCHITECTURE (FastAPI)
Our backend is built for speed and asynchronous processing using FastAPI.

*   **`/face-login`:** Receives an image, runs the FaceNet pipeline. On success, generates a secure `UUID` token and adds it to an active session set.
*   **`/upload-data`:** Protected route (requires token). Accepts the raw PCAP/CSV data, temporarily stores it, pipes it through our ML predict engine (`run_prediction`), and automatically cleans up the filesystem.
*   **`/results`:** Serves the latest structured JSON state to the dashboard.
*   **Integration:** Seamlessly bridges the PyTorch facial recognition models with the Scikit-Learn threat detection pipelines within a unified, CORS-enabled asynchronous server.

---

## 🔹 10. FRONTEND WORKING
The User Interface is the bridge between complex data and the security analyst.
*   **Login Interface:** Integrates with the webcam to process the biometric check.
*   **Interactive Dashboard:** Driven by Vanilla JS and modern CSS. Fetches the JSON from `/upload-data`.
*   **Data Rendering:** Dynamically populates summary cards (Total Flows, High Risk counts), renders the temporal anomaly charts using graphing libraries, and displays the fully explained, row-by-row threat table with color-coded risk levels.

---

## 🔹 11. END-TO-END FLOW
1.  **Face Login:** Admin approaches the webcam; MTCNN + FaceNet authenticate identity.
2.  **Token Generation:** FastAPI issues a secure UUID session token.
3.  **Upload CSV:** Admin uploads the target network traffic log via the dashboard.
4.  **ML Pipeline:** Data is scaled → Scored by Isolation Forest → Classified by Random Forest.
5.  **Insights:** `risk_score` is calculated, behavioral tags are assigned, and human-readable explanations are generated.
6.  **Dashboard:** The frontend updates in real-time, displaying actionable threat intelligence.

---

## 🔹 12. UNIQUE SELLING POINTS
*   **Hybrid AI Architecture:** We don't just classify known attacks; unsupervised learning ensures we catch zero-day anomalies.
*   **Explainable AI (XAI):** We solve the "Black Box" problem. Analysts don't just see "Anomaly=True"; they see exactly *why* (e.g., SYN Flood Pattern).
*   **Biometric Zero-Trust:** Secure-by-default access using state-of-the-art PyTorch facial recognition.
*   **Behavioral Abstraction:** Moving beyond raw packet bytes to understand the *intent* of the traffic (Scanning vs. Flooding).

---

## 🔹 13. FUTURE SCOPE
*   **Real-Time Streaming:** Upgrading from CSV uploads to live PCAP parsing (via Kafka or sockets) for sub-second detection.
*   **Graph Neural Networks (GNNs):** Mapping IP-to-IP relationships as a graph to detect distributed, coordinated botnets.
*   **LLM Integration:** Feeding the JSON output into an LLM to generate automated, executive-level incident response reports.
*   **SIEM Integration:** Formatting alerts directly into Splunk or ELK stack formats for enterprise deployments.
