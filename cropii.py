import streamlit as st
import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import os
import requests
import base64

# =============================================================================
# WEATHER SETUP AND FUNCTIONS
# =============================================================================
# API_KEY should be set as an environment variable for security
API_KEY = os.getenv("OPENWEATHER_API_KEY", "78e9075ace378bb96203be576111af4e")

def get_location():
    """Get user's location using multiple fallback services"""
    # Try multiple location services for better reliability
    location_services = [
        "https://ipinfo.io/json",
        "https://ipapi.co/json/",
        "http://ip-api.com/json/"
    ]
    
    for service_url in location_services:
        try:
            response = requests.get(service_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Try different possible keys for city name
                city = (data.get("city") or 
                       data.get("town") or 
                       data.get("region") or 
                       data.get("district"))
                if city:
                    return city
        except Exception as e:
            print(f"Location fetch error from {service_url}: {e}")
            continue
    return None

def get_weather(city):
    """Get weather data for a given city"""
    if not city:
        return None, None, None
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            weather = data["weather"][0]["main"]
            return temp, humidity, weather
        else:
            print(f"Weather API error: Status {response.status_code}")
            return None, None, None
    except Exception as e:
        print(f"Weather fetch error: {e}")
        return None, None, None

# 🌍 Get user's city with improved reliability
location_attempts = 0
max_attempts = 3

city = None
while location_attempts < max_attempts and not city:
    city = get_location()
    location_attempts += 1
    if not city:
        print(f"Attempt {location_attempts} failed to get location. Retrying...")

# If still no city after retries, set to None to trigger manual input prompt
if not city:
    city = None
    print("⚠️ Location detection failed after multiple attempts. Please enter your city manually.")

# 🌦 Get weather data with retry logic
weather_attempts = 0
max_weather_attempts = 2
temp, hum, condition = None, None, None

while weather_attempts < max_weather_attempts and (temp is None or hum is None):
    if city:  # Only try to get weather if we have a city
        temp, hum, condition = get_weather(city)
    weather_attempts += 1
    if temp is None or hum is None:
        print(f"Attempt {weather_attempts} failed to get weather. Retrying...")

# ⚡ If failed, fallback values
if temp is None or hum is None:
    temp = 24.0
    hum = 60.0
    condition = "Clear"
    if not city:  # Only set default city if no city was detected
        city = None  # Set to None to clearly indicate no location detected
    print("⚠️ Could not fetch live weather. Using default values.")


# # ---------------------- Translations -----------------------
translations = {
    "English": {
        "title": "Enter Soil and Climate Parameters",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "soil_ph": "Soil pH",
        "predict_crop": "Predict Crop",
        "current_location": "Current Location",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "weather": "Weather",
        "more_about": "More about",
        "tips": "Tips to Grow",
        "facts": "Interesting Facts",
        "suggestions_to_improve_yield": "Suggestions to Improve Yield",
        "description": "Description"
    },
    "Hindi": {
        "title": "मृदा और जलवायु पैरामीटर दर्ज करें",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फॉस्फोरस (P)",
        "potassium": "पोटेशियम (K)",
        "soil_ph": "मिट्टी का पीएच",
        "predict_crop": "फसल का पूर्वानुमान करें",
        "current_location": "वर्तमान स्थान",
        "temperature": "तापमान",
        "humidity": "आर्द्रता",
        "weather": "मौसम",
        "more_about": "के बारे में अधिक",
        "tips": "उगाने के टिप्स",
        "facts": "दिलचस्प तथ्य",
        "suggestions_to_improve_yield": "उपज बढ़ाने के सुझाव",
        "description": "विवरण"
    },
    "Tamil": {
        "title": "மண் மற்றும் காலநிலை அளவுருக்களை உள்ளிடவும்",
        "nitrogen": "நைட்ரஜன் (N)",
        "phosphorus": "பாஸ்பரஸ் (P)",
        "potassium": "பொட்டாசியம் (K)",
        "soil_ph": "மண்ணின் பிஎச்",
        "predict_crop": "பயிர் கணிப்பு",
        "current_location": "தற்போதைய இடம்",
        "temperature": "வெப்பநிலை",
        "humidity": "ஈரப்பதம்",
        "weather": "வானிலை",
        "more_about": "பற்றி மேலும்",
        "tips": "வளர்க்கும் குறிப்புகள்",
        "facts": "சுவாரஸ்யமான தகவல்கள்",
        "suggestions_to_improve_yield": "உற்பத்தியை மேம்படுத்தும் யோசனைகள்",
        "description": "விளக்கம்"
    }
}

# --- CORRECTION: Use relative paths from the 'assets' folder ---
# Note: For crops without specific images (cotton, jute), we're using Rice.jpg as a placeholder
# TODO: Add specific images for cotton and jute when available
crop_info = {
    "rice": {
        "image": r"assets/Rice.jpg",
        "facts": {
            "English": "Rice feeds more than half of the world's population.",
            "Hindi": "चावल दुनिया की आधी से अधिक आबादी का भोजन है।",
            "Tamil": "அரிசி உலக மக்கள் தொகையின் பாதிக்குமேல் உணவாகும்."
        },
        "tips": {
            "English": "Maintain standing water in the fields.",
            "Hindi": "खेतों में पानी भरा रहना चाहिए।",
            "Tamil": "வயல்களில் நிலைநிறைந்த நீரை பராமரிக்கவும்."
        },
        "suggestions": {
            "English": "Use high-yielding hybrid seeds.",
            "Hindi": "उच्च उपज देने वाले संकर बीजों का उपयोग करें।",
            "Tamil": "உயர் மகசூல் தரும் கலப்பு விதைகளை பயன்படுத்தவும்."
        }
    },
    "wheat": {
        "image": r"assets/Wheat.jpg",
        "facts": {
            "English": "Wheat is one of the oldest cultivated crops.",
            "Hindi": "गेहूं सबसे पुरानी खेती की जाने वाली फसलों में से एक है।",
            "Tamil": "கோதுமை பழமையான விளைவிக்கப்பட்ட பயிர்களில் ஒன்று."
        },
        "tips": {
            "English": "Sow during cooler temperatures.",
            "Hindi": "ठंडे मौसम में बुवाई करें।",
            "Tamil": "குளிர்ந்த காலநிலையில் விதைப்பை செய்யவும்."
        },
        "suggestions": {
            "English": "Apply nitrogen fertilizer in split doses.",
            "Hindi": "नाइट्रोजन उर्वरक को विभाजित खुराकों में दें।",
            "Tamil": "நைட்ரஜன் உரத்தை பிரிக்கப்பட்ட அளவுகளில் வழங்கவும்."
        }
    },
    "maize": {
        "image": r"assets/Maize.jpg",
        "facts": {
            "English": "Maize originated in southern Mexico 10,000 years ago.",
            "Hindi": "मक्का की उत्पत्ति 10,000 साल पहले दक्षिणी मेक्सिको में हुई थी।",
            "Tamil": "சோளம் 10,000 ஆண்டுகளுக்கு முன்பு தெற்கு மெக்ஸிகோவில் தோன்றியது."
        },
        "tips": {
            "English": "Ensure proper weed management.",
            "Hindi": "सही खरपतवार प्रबंधन सुनिश्चित करें।",
            "Tamil": "சரியான கொடிகள் மேலாண்மையை உறுதி செய்யவும்."
        },
        "suggestions": {
            "English": "Irrigate at critical growth stages.",
            "Hindi": "महत्वपूर्ण वृद्धि चरणों में सिंचाई करें।",
            "Tamil": "முக்கிய வளர்ச்சி நிலைகளில் நீர்ப்பாசனம் செய்யவும்."
        }
    },
    "bajra": {
        "image": r"assets/Bajra.jpg",
        "facts": {
            "English": "Bajra is a drought-resistant crop.",
            "Hindi": "बाजरा एक सूखा प्रतिरोधी फसल है।",
            "Tamil": "கம்பு ஒரு வறண்ட நிலத்திற்கேற்ற பயிர் ஆகும்."
        },
        "tips": {
            "English": "Use minimal water for irrigation.",
            "Hindi": "सिंचाई के लिए न्यूनतम पानी का उपयोग करें।",
            "Tamil": "நீர்ப்பாசனத்திற்கு குறைந்த நீரை பயன்படுத்தவும்."
        },
        "suggestions": {
            "English": "Opt for early sowing before monsoon.",
            "Hindi": "मानसून से पहले जल्दी बुवाई करें।",
            "Tamil": "மழைக்காலத்திற்கு முன்பு நேரத்துடன் விதைநிறுவுதல் செய்யவும்."
        }
    },
    "cotton": {
        "image": r"assets/Rice.jpg",
        "facts": {
            "English": "Cotton is one of the most widely used natural fibers in the world.",
            "Hindi": "कपास दुनिया में सबसे अधिक इस्तेमाल किए जाने वाले प्राकृतिक फाइबर में से एक है।",
            "Tamil": "பருத்தி உலகில் மிகவும் அதிகமாக பயன்படுத்தப்படும் இயற்கை இழைகளில் ஒன்றாகும்."
        },
        "tips": {
            "English": "Ensure proper spacing between plants for good air circulation.",
            "Hindi": "अच्छे हवा के संचलन के लिए पौधों के बीच उचित दूरी सुनिश्चित करें।",
            "Tamil": "நல்ல காற்றோட்டம் இருக்க தாவரங்களுக்கு இடையில் ஏற்ற இடைவெளியை உறுதி செய்க."
        },
        "suggestions": {
            "English": "Use disease-resistant varieties for better yield.",
            "Hindi": "बेहतर उपज के लिए रोग प्रतिरोधी किस्मों का उपयोग करें।",
            "Tamil": "சிறந்த விளைச்சலுக்கு நோய் எதிர்ப்பு தகுதியுள்ள இனங்களை பயன்படுத்தவும்."
        }
    },
    "jute": {
        "image": r"assets/Rice.jpg",
        "facts": {
            "English": "Jute is known as the 'Golden Fiber' and is primarily grown in Bangladesh and India.",
            "Hindi": "जूट को 'गोल्डन फाइबर' के नाम से जाना जाता है और इसे मुख्य रूप से बांग्लादेश और भारत में उगाया जाता है।",
            "Tamil": "சணல் 'தங்க இழை' என அழைக்கப்படுகிறது மற்றும் முக்கியமாக வங்காளதேசம் மற்றும் இந்தியாவில் வளர்க்கப்படுகிறது."
        },
        "tips": {
            "English": "Jute grows best in well-drained, fertile soils with high rainfall.",
            "Hindi": "जूट अच्छी तरह से निकासी वाली, उपजाऊ मिट्टी में और अधिक वर्षा के साथ सबसे अच्छा उगता है।",
            "Tamil": "சணல் நன்கு வடிந்து செல்லும், செழிமன்றற்ற மண்ணில் அதிக மழை பெய்யும் இடங்களில் சிறப்பாக வளரும்."
        },
        "suggestions": {
            "English": "Harvest jute when the plants are in full bloom for best fiber quality.",
            "Hindi": "सबसे अच्छी फाइबर गुणवत्ता के लिए जूट को पूरी तरह से खिले हुए पौधों से काटें।",
            "Tamil": "சிறந்த இழை தரத்திற்கு சணலை முழு மலர்ச்சியில் உள்ள தாவரங்களை அறுவை செய்யவும்."
        }
    }
}

# ---------------------- Streamlit Config and Styling --------------
st.set_page_config(page_title="🌾 CROPIFY | Smart Crop Recommendation", layout="wide", page_icon="🌿")

st.markdown("""
    <style>
        html, body, [data-testid="stApp"] {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 40%, #2c5364 80%, #00bf8f 100%);
            color: white;
        }
        .main-header {
            background: linear-gradient(135deg, #00c9ff 0%, #92fe9d 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            text-align: center;
            padding: 20px;
            border-bottom: 2px solid #00bf8f;
            margin-bottom: 40px;
        }
        .section-card {
            background-color: rgba(255, 255, 255, 0.08);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        }
        .metric-box {
            font-size: 18px;
            padding: 15px;
            border-radius: 12px;
            background: rgba(0, 255, 200, 0.15);
            margin-bottom: 10px;
            box-shadow: 0 4px 12px rgba(0,255,200,0.3);
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, #16222A 0%, #3A6073 100%);
            color: white;
            box-shadow: 2px 0px 15px rgba(0,255,200,0.2);
        }
        h4 {
            margin-top: 0;
            color: #00ffcc;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Header with Circular Logo ----------------------
# --- CORRECTION: Use a relative path to your logo in the 'assets' folder ---
# --- Make sure your logo file is named 'logo.png' or change the name here ---
logo_path = r"assets/Cropify logo.png" 

if os.path.exists(logo_path):
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <img src="data:image/png;base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}" 
             style="width:120px;height:120px;border-radius:50%;box-shadow:0 4px 15px rgba(0,0,0,0.2), 0 0 30px #00ffcc;
                    border: 4px solid #00ffcc; animation: pulse-border 1.5s infinite ease-in-out; margin-bottom:10px;">
        <h1 style="background: linear-gradient(135deg, #00c9ff 0%, #92fe9d 100%);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-weight: bold;">🌾CROPIFY </h1>
        <h4 style="color: #00ffcc;">TURNING FIELDS INTO FORTUNES</h4>
    </div>

    <style>
        @keyframes pulse-border {{
            0% {{
                transform: scale(1);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), 0 0 30px #00ffcc;
            }}
            50% {{
                transform: scale(1.05);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), 0 0 40px #00ffcc;
            }}
            100% {{
                transform: scale(1);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), 0 0 30px #00ffcc;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.error(f"Logo not found at path: {logo_path}")


# -------------------- Sidebar ----------------------
st.sidebar.title("CONFIGURATIONS")
selected_language = st.sidebar.selectbox("Select Language", ["English","Hindi", "Tamil"])
language = translations[selected_language]

# Location Settings
st.sidebar.subheader("Location Settings")

# Auto-detection status
if city:
    st.sidebar.success(f"✅ Auto-detected: {city}")
else:
    st.sidebar.warning("⚠️ Could not auto-detect location")

st.sidebar.info("📍 Accurate location helps provide better crop recommendations based on your local climate conditions.")

# Manual location override
manual_city = st.sidebar.text_input("Enter City Name", value=city or "", key="manual_city", placeholder="e.g., New York, London, Tokyo", help="Enter your city name for accurate weather data")
update_weather = st.sidebar.button("Update Weather Data")

if update_weather and manual_city:
    if manual_city != city:
        city = manual_city
        # Show loading message
        weather_loading = st.sidebar.empty()
        weather_loading.info("🔄 Fetching weather data...")
        
        # Refresh weather data with manual city
        new_temp, new_hum, new_condition = get_weather(city)
        
        # Clear loading message
        weather_loading.empty()
        
        if new_temp is not None and new_hum is not None:
            temp, hum, condition = new_temp, new_hum, new_condition
            st.sidebar.success(f"✅ Weather data updated for {city}")
        else:
            # If weather data fetch fails, keep current values or use defaults
            if temp is None or hum is None:
                temp = 24.0
                hum = 60.0
                condition = "Clear"
            st.sidebar.error("⚠️ Could not fetch live weather for the entered city. Using previous/default values.")
elif update_weather and not manual_city:
    # If manual city is empty, fallback to default values
    temp = 24.0
    hum = 60.0
    condition = "Clear"
    if not city:  # Only set default city if no city was detected
        city = None  # Set to None to clearly indicate no location detected
    st.sidebar.warning("⚠️ Please enter a city name to get weather data")

# -------------------- Weather Metrics -------------------
location_display = city if city else "Not specified"
st.markdown(f"""
<div class="section-card">
    <h4>📍 {language['current_location']}: {location_display}</h4>
    <div class="metric-box">🌡️ {language['temperature']}: <b>{temp} °C</b></div>
    <div class="metric-box">💧 {language['humidity']}: <b>{hum}%</b></div>
    <div class="metric-box">🌤️ {language['weather']}: <b>{condition}</b></div>
</div>
""", unsafe_allow_html=True)

# -------------------- Load ML Models --------------------
# --- CORRECTION: Use raw strings and correct .pkl extension ---
model_paths = {
    "Random Forest": r"random_forest.pkl",
    "MLP": r"MLP.pkl",
    "Naive Bayes": r"naive_bayes.pkl",
    "Decision Tree": r"random_tree.pkl"
}
models = {}

# Show loading message
loading_placeholder = st.sidebar.empty()
loading_placeholder.info("🔄 Loading machine learning models...")

for name, path in model_paths.items():
    if os.path.exists(path):
        models[name] = joblib.load(path)
    else:
        st.sidebar.error(f"Model not found: {path}")

# Clear loading message
loading_placeholder.empty()

if not models:
    st.error("No ML models were found. Please make sure the .pkl files are in the main project directory.")
    st.stop()

selected_model = st.sidebar.selectbox("ML Model", list(models.keys()))
model = models[selected_model]

# ------------------- Tabs Section ----------------------
tab1, tab2, tab3 = st.tabs([language["title"], " DATA ANALYSIS", "WORK FLOW MODELS"])

# ------------------ Crop Prediction Tab -----------------
with tab1:
    with st.form("crop_form"):
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader(f"🧪 {language['title']}")
        col1, col2 = st.columns(2)
        with col1:
            nitrogen = st.slider(f"🧪 {language['nitrogen']}", 0, 140, 60)
            phosphorus = st.slider(f"🧪 {language['phosphorus']}", 0, 140, 30)
            potassium = st.slider(f"🧪 {language['potassium']}", 0, 200, 70)
            ph = st.slider(f"🌱 {language['soil_ph']}", 3.5, 9.0, 6.8)
        with col2:
            # Ensure temp and hum are valid numbers for sliders
            default_temp = float(temp) if temp is not None else 24.0
            default_hum = float(hum) if hum is not None else 60.0
            temperature = st.slider(f"🌡️ {language['temperature']} (°C)", 10.0, 45.0, default_temp)
            humidity = st.slider(f"💧 {language['humidity']} (%)", 10.0, 100.0, default_hum)
            rainfall = st.slider("🌧️ Rainfall (mm)", 0.0, 400.0, 150.0)

        submitted = st.form_submit_button(f"🌾 {language['predict_crop']}")
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        # Create a DataFrame with proper column names to avoid feature name warnings
        feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        input_data = pd.DataFrame([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]], 
                                  columns=feature_names)
        prediction = model.predict(input_data)[0]
        crop_lower = prediction.lower()

        st.success(f"✅ {language['predict_crop']} using {selected_model}: **{prediction.capitalize()}**")

        if crop_lower in crop_info:
            crop_img_path = crop_info[crop_lower]["image"]
            if os.path.exists(crop_img_path):
                st.image(crop_img_path, width=300, caption=f"{prediction.capitalize()}")
            else:
                st.warning(f"Image for {prediction.capitalize()} not found.")

            fact = crop_info[crop_lower]["facts"][selected_language]
            tip = crop_info[crop_lower]["tips"][selected_language]
            suggestion = crop_info[crop_lower]["suggestions"][selected_language]

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader(f"🌟 {language['facts']}")
            st.info(fact)

            st.subheader(f"🌱 {language['tips']}")
            st.success(tip)

            st.subheader(f"🚀 {language['suggestions_to_improve_yield']}")
            st.warning(suggestion)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("🔍 Info about this crop is not available yet!")

# ---------------- Data Analysis Tab ------------------
with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📤 Upload Dataset for Correlation Analysis")

    uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully!")
            st.write("🔍 Data Preview:", df.head())

            numeric_df = df.select_dtypes(include=[np.number])
            if numeric_df.empty:
                st.warning("⚠️ No numeric columns found for correlation analysis.")
            else:
                corr = numeric_df.corr()

                st.subheader("🧩 Feature Correlation Heatmap")
                fig, ax = plt.subplots(figsize=(10, 7))
                sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
                st.pyplot(fig)
        except pd.errors.EmptyDataError:
            st.error("⚠️ The uploaded file is empty. Please upload a valid CSV.")
        except Exception as e:
            st.error(f"⚠️ Error reading file: {e}")
    else:
        st.info("👆 Please upload a dataset CSV to see correlation analysis.")

    st.markdown('</div>', unsafe_allow_html=True)
# ------------------ Workflow Models Tab -----------------
with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🛠️ Work Flow of Models")

    st.markdown("""
    - 📥 Input Parameters: Soil NPK values, pH, Rainfall, Temperature, Humidity.
    - ⚙️ Preprocessing: Data Cleaning and Scaling.
    - 🧠 ML Models: Random Forest, MLP, Naive Bayes, Decision Tree.
    - 🔮 Prediction: Best suitable crop suggestion.
    - 📊 Output: Crop info with tips, facts, and suggestions for better yield.
    """)

    col1, col2 = st.columns(2)

    # --- CORRECTION: Use relative paths for workflow images ---
    work_diagram_path = r"assets/work_diagram.png"
    chart_diagram_path = r"assets/diagram_of_chart.png"

    with col1:
        if os.path.exists(work_diagram_path):
            st.image(work_diagram_path, caption="Model Workflow", width=400)
        else:
            st.info("Workflow diagram not available.")

    with col2:
        if os.path.exists(chart_diagram_path):
            st.image(chart_diagram_path, caption="Systematic Workflow", width=400)
        else:
            st.info("Systematic workflow diagram not available.")

    st.markdown('</div>', unsafe_allow_html=True)
    