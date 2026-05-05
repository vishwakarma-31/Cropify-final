import streamlit as st

# =============================================================================
# Loading Animation Component (Phase 3 - GSAP-style)
# =============================================================================

def render_loading_animation(message="Loading...", duration=2):
    """
    Render a GSAP-style loading animation
    
    Args:
        message: Loading message to display
        duration: Animation duration in seconds
    """
    st.markdown(f"""
    <div class="loading-container">
        <div class="loading-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
        </div>
        <p class="loading-message">{message}</p>
    </div>
    
    <style>
    .loading-container {{
        text-align: center;
        padding: 40px;
    }}
    .loading-spinner {{
        position: relative;
        width: 80px;
        height: 80px;
        margin: 0 auto;
    }}
    .spinner-ring {{
        position: absolute;
        width: 100%;
        height: 100%;
        border: 4px solid transparent;
        border-top-color: #00ffcc;
        border-radius: 50%;
        animation: spin {duration}s linear infinite;
    }}
    .spinner-ring:nth-child(2) {{
        width: 70%;
        height: 70%;
        top: 15%;
        left: 15%;
        border-top-color: #00c9ff;
        animation-duration: {duration * 0.8}s;
        animation-direction: reverse;
    }}
    .spinner-ring:nth-child(3) {{
        width: 40%;
        height: 40%;
        top: 30%;
        left: 30%;
        border-top-color: #92fe9d;
        animation-duration: {duration * 0.6}s;
    }}
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    .loading-message {{
        color: #00ffcc;
        font-size: 18px;
        margin-top: 20px;
        animation: pulse 1.5s ease-in-out infinite;
    }}
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_loading_with_progress(message="Processing...", progress=0):
    """
    Render loading animation with progress bar
    
    Args:
        message: Loading message
        progress: Progress percentage (0-100)
    """
    st.markdown(f"""
    <div class="loading-with-progress">
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%"></div>
        </div>
        <p class="progress-message">{message}</p>
    </div>
    
    <style>
    .loading-with-progress {{
        padding: 20px;
    }}
    .progress-container {{
        width: 100%;
        height: 8px;
        background: rgba(255,255,255,0.2);
        border-radius: 4px;
        overflow: hidden;
    }}
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, #00ffcc, #00c9ff);
        border-radius: 4px;
        transition: width 0.3s ease;
    }}
    .progress-message {{
        color: #00ffcc;
        font-size: 14px;
        margin-top: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

def render_crop_reveal(crop_name, animation_type="fade"):
    """
    Render crop result with reveal animation
    
    Args:
        crop_name: Name of predicted crop
        animation_type: Type of animation ('fade', 'scale', 'slide')
    """
    animation_css = {
        "fade": """
            @keyframes reveal {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            animation: reveal 0.8s ease-out forwards;
        """,
        "scale": """
            @keyframes reveal {
                from { transform: scale(0.5); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
            animation: reveal 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        """,
        "slide": """
            @keyframes reveal {
                from { transform: translateY(30px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            animation: reveal 0.8s ease-out forwards;
        """
    }
    
    st.markdown(f"""
    <div class="crop-reveal">
        <h2 class="crop-result">{crop_name}</h2>
    </div>
    
    <style>
    .crop-reveal {{
        text-align: center;
        padding: 30px;
    }}
    .crop-result {{
        color: #00ffcc;
        font-size: 48px;
        font-weight: bold;
        text-transform: capitalize;
        {animation_css.get(animation_type, animation_css['fade'])}
    }}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# EXAMPLES FOR PHASE 3:
# =============================================================================
# 
# 1. Before making prediction (show loading):
#    render_loading_animation("Analyzing soil data...")
#
# 2. With progress indicator:
#    render_loading_with_progress("Loading ML model...", 30)
#    render_loading_with_progress("Processing input...", 70)
#    render_loading_with_progress("Generating prediction...", 100)
#
# 3. After prediction (reveal animation):
#    render_crop_reveal("Rice", animation_type="scale")
# =============================================================================