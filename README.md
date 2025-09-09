# Cropify ML

## Description

Cropify ML is a smart crop recommendation system that leverages machine learning algorithms to suggest the most suitable crops based on soil and climate parameters. The system integrates real-time weather data and provides comprehensive crop information including growing tips, interesting facts, and yield improvement suggestions. Built with a user-friendly web interface, it supports multiple languages and offers data analysis capabilities.

## Features

- **Web Interface**: Interactive Streamlit-based application with modern UI design
- **Weather Integration**: Automatic location detection and real-time weather data fetching using OpenWeatherMap API
- **Multi-lingual Support**: Available in English, Hindi, and Tamil languages
- **Machine Learning Models**: Multiple ML algorithms including Random Forest, MLP (Multi-Layer Perceptron), Naive Bayes, and Decision Tree
- **Crop Information**: Detailed information for major crops (Rice, Wheat, Maize, Bajra) with images, facts, and cultivation tips
- **Data Analysis**: Correlation analysis with interactive heatmaps for uploaded datasets
- **Workflow Visualization**: Visual representation of the ML model workflow and system architecture
- **Real-time Prediction**: Instant crop recommendations based on soil parameters (N, P, K, pH) and environmental factors

## Installation

### Prerequisites
- Python 3.7 or higher
- Internet connection for weather data fetching

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cropify-ml
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```

4. Ensure all model files (.pkl) and assets are in the correct directories:
   - ML models: `random_forest.pkl`, `MLP.pkl`, `naive_bayes.pkl`, `random_tree.pkl`
   - Assets: `assets/` folder with crop images and diagrams

## Usage

### Running the Application
1. Start the Streamlit app:
   ```bash
   streamlit run cropii.py
   ```

2. Open your browser and navigate to the provided local URL (typically http://localhost:8501)

### Application Interface

#### Language Selection
- Use the sidebar to select your preferred language (English, Hindi, Tamil)

#### Weather Information
- The app automatically detects your location and fetches current weather data
- Displays temperature, humidity, and weather conditions
- Falls back to default values if weather data cannot be fetched

#### Crop Prediction Tab
1. Input soil parameters:
   - Nitrogen (N): 0-140
   - Phosphorus (P): 0-140
   - Potassium (K): 0-200
   - Soil pH: 3.5-9.0

2. Environmental parameters:
   - Temperature (°C): 10.0-45.0 (auto-filled from weather data)
   - Humidity (%): 10.0-100.0 (auto-filled from weather data)
   - Rainfall (mm): 0.0-400.0

3. Select ML model from the sidebar:
   - Random Forest
   - MLP
   - Naive Bayes
   - Decision Tree

4. Click "Predict Crop" to get recommendations

5. View results including:
   - Recommended crop with image
   - Interesting facts about the crop
   - Cultivation tips
   - Suggestions to improve yield

#### Data Analysis Tab
- Upload CSV datasets for correlation analysis
- View data preview
- Generate interactive correlation heatmaps for numeric features

#### Workflow Models Tab
- Visualize the ML model workflow
- Understand the system architecture
- View systematic workflow diagrams

## Contributing

We welcome contributions to improve Cropify ML! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines for Python code
- Add docstrings to new functions
- Test your changes with different scenarios
- Update documentation for any new features
- Ensure compatibility with existing dependencies

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: Make sure to obtain your own OpenWeatherMap API key and replace it in the code if you plan to deploy or modify the weather integration functionality.
