# 🌾 CROPIFY | Smart Crop Recommendation System

## 📝 Description

**Cropify** is a professional-grade smart agriculture platform that leverages Machine Learning to help farmers and agronomists make data-driven decisions. By analyzing soil nutrients (N-P-K), pH, rainfall, and real-time climate data, Cropify recommends the most suitable crops for a specific land area to maximize yield and sustainability.

The system features a premium web interface built with Streamlit, real-time weather integration via OpenWeather API, and support for 22 different crop types with detailed cultivation guides in multiple languages.

---

## ✨ Key Features

-   **🧠 Multi-Model Prediction**: Choose between four specialized ML models:
    -   **Random Forest** (High Accuracy)
    -   **MLP** (Neural Network)
    -   **Naive Bayes** (Probabilistic)
    -   **Decision Tree** (Interpretability)
-   **🔐 Secure Access**: Built-in authentication system with configurable user roles (Admin/Demo).
-   **🌦️ Live Weather Integration**: Automatic city detection and real-time fetching of Temperature and Humidity using the OpenWeatherMap API.
-   **🌍 Multi-lingual Support**: Full UI and database support for **English**, **Hindi**, and **Tamil**.
-   **📊 Dynamic Crop Database**: Powered by a customizable `crops.yaml` file, providing:
    -   High-quality crop imagery.
    -   Cultivation tips & yield improvement suggestions.
    -   Interesting botanical facts.
-   **📈 Data Analysis**: Interactive "Data Analysis" tab to upload CSV datasets and generate feature correlation heatmaps.
-   **🛠️ Robust Pipeline**: Implements `StandardScaler` for feature normalization and `LabelEncoder` for target decoding, ensuring high prediction reliability.

---

## 🚀 Installation & Setup

### Prerequisites
-   Python 3.10 or higher
-   OpenWeatherMap API Key (optional, default provided)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Cropify-final
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Model Assets
Ensure the following files are present in the root directory:
-   **Models**: `random_forest.pkl`, `MLP.pkl`, `naive_bayes.pkl`, `random_tree.pkl`
-   **Preprocessing**: `scaler.pkl`, `label_encoder.pkl`
-   **Database**: `crops.yaml`, `config.yaml`

---

## 💻 Usage

### Starting the Application
To run the web interface, use:
```bash
python -m streamlit run cropii.py
```

### Login Credentials
Check `config.yaml` for active users. Default demo credentials:
-   **Username**: `demo`
-   **Password**: `demo123`

### Using the Prediction Tool
1.  **Select Language**: Choose your language from the sidebar.
2.  **Configure Location**: The app will attempt to auto-detect your city. You can manually override this in the sidebar.
3.  **Input Soil Data**: Enter the Nitrogen (N), Phosphorus (P), Potassium (K), and pH levels.
4.  **Run Prediction**: Click the **Predict Crop** button to see the AI recommendation.

---

## 📂 Project Structure

-   `cropii.py`: Main application entry point.
-   `crops.yaml`: Central database for crop-specific facts and tips.
-   `config.yaml`: Configuration for authentication and cookies.
-   `model_training.py`: Script used to train and export the ML models.
-   `assets/`: Directory containing crop images and workflow diagrams.
-   `csv/`: Dataset storage (e.g., `Crop_recommendation.csv`).

---

## 🛠️ Tech Stack

-   **Frontend**: Streamlit
-   **ML Framework**: Scikit-Learn
-   **Data Processing**: Pandas, NumPy
-   **Visualization**: Seaborn, Matplotlib
-   **Authentication**: Streamlit-Authenticator
-   **Weather**: Requests (OpenWeather API)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
