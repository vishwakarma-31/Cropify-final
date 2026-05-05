# =============================================================================
# CDN Configuration for Asset Storage (Phase 2)
# =============================================================================
# Replace these URLs with your Cloudinary/S3 bucket URLs afterUpload

CDN_BASE_URL = ""

# Asset URLs - Add your CDN URLs here after uploading to Cloudinary/S3
ASSETS = {
    "rice": "",
    "wheat": "",
    "maize": "",
    "bajra": "",
    "cotton": "",
    "jute": "",
    "logo": "",
    "work_diagram": "",
    "chart_diagram": ""
}

def get_asset_url(asset_name, local_path=None):
    """
    Get asset URL (CDN preferred, local fallback)
    
    Args:
        asset_name: Name of the asset key in ASSETS dict
        local_path: Local file path as fallback if CDN not configured
    
    Returns:
        str: CDN URL if available, otherwise local path
    """
    if CDN_BASE_URL and ASSETS.get(asset_name):
        return f"{CDN_BASE_URL}/{ASSETS[asset_name]}"
    elif local_path:
        return local_path
    else:
        return None

# =============================================================================
# INSTRUCTIONS FOR PHASE 2 IMPLEMENTATION:
# =============================================================================
# 1. Create a Cloudinary or AWS S3 account
# 2. Upload all images from assets/ folder:
#    - Rice.jpg, Wheat.jpg, Maize.jpg, Bajra.jpg
#    - Cropify logo.png
#    - work_diagram.png, diagram_of_chart.png
# 3. Copy the CDN URLs and update ASSETS dict above
# 4. Set CDN_BASE_URL to your cloud storage base URL
# 5. Delete local assets/ folder from repository
# 6. The app will automatically use CDN URLs
# =============================================================================