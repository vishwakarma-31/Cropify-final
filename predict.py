import sys
import json
import joblib
import numpy as np

# =============================================================================
# predict.py - ML Model Prediction Service
# Isolated prediction script for secure ML inference
# =============================================================================

# Feature order: N, P, K, temperature, humidity, ph, rainfall
FEATURE_NAMES = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

def load_models():
    """Load the trained MLP model and scaler"""
    model = joblib.load('MLP.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    return model, scaler, label_encoder

def predict(n, p, k, temp, hum, ph, rainfall, model=None, scaler=None, label_encoder=None):
    """
    Make crop prediction based on soil and climate parameters
    
    Args:
        n: Nitrogen (0-140)
        p: Phosphorus (0-140)
        k: Potassium (0-200)
        temp: Temperature (10-45 °C)
        hum: Humidity (10-100 %)
        ph: Soil pH (3.5-9.0)
        rainfall: Rainfall (0-400 mm)
        model: Pre-loaded model (optional)
        scaler: Pre-loaded scaler (optional)
        label_encoder: Pre-loaded label encoder (optional)
    
    Returns:
        dict: Prediction result with crop name and confidence
    """
    # Load models if not provided
    if model is None:
        model, scaler, label_encoder = load_models()
    
    # Create input array
    input_data = np.array([[n, p, k, temp, hum, ph, rainfall]])
    
    # Scale the data using StandardScaler
    if scaler is not None:
        input_data = scaler.transform(input_data)
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    crop_name = label_encoder.inverse_transform([prediction])[0]
    
    # Get prediction probabilities if available
    try:
        probabilities = model.predict_proba(input_data)[0]
        confidence = float(max(probabilities))
    except (AttributeError, IndexError):
        confidence = None
    
    return {
        'crop': crop_name,
        'confidence': confidence,
        'input': {
            'N': n, 'P': p, 'K': k,
            'temperature': temp, 'humidity': hum,
            'ph': ph, 'rainfall': rainfall
        }
    }

if __name__ == "__main__":
    # Expected format: python predict.py N P K temp hum ph rainfall
    # Example: python predict.py 90 42 43 20 82 6.5 202
    
    if len(sys.argv) == 8:
        try:
            n = float(sys.argv[1])
            p = float(sys.argv[2])
            k = float(sys.argv[3])
            temp = float(sys.argv[4])
            hum = float(sys.argv[5])
            ph = float(sys.argv[6])
            rainfall = float(sys.argv[7])
            
            result = predict(n, p, k, temp, hum, ph, rainfall)
            
            # Output as JSON
            print(json.dumps(result))
            
        except Exception as e:
            print(json.dumps({'error': str(e)}))
            sys.exit(1)
    else:
        print(json.dumps({'error': 'Invalid arguments. Expected: N P K temp hum ph rainfall'}))
        sys.exit(1)