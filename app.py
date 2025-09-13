import streamlit as st
import requests
from PIL import Image
import io
import base64
from datetime import datetime
import os
from dotenv import load_dotenv
import json
import openai
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Photo Editor",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Dark theme styling */
    .stApp {
        background-color: #1a1a1a;
    }
    
    /* Upload area styling */
    .upload-box {
        border: 2px dashed #4a4a4a;
        border-radius: 10px;
        padding: 40px;
        text-align: center;
        background-color: #242424;
        margin: 20px 0;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #4a4a4a;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #3d3d3d;
        border-color: #6a6a6a;
    }
    
    /* Primary button style */
    .primary-button > button {
        background-color: #5865F2 !important;
        color: white !important;
        font-weight: bold;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #4a4a4a;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #4a4a4a;
        border-radius: 8px;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #4a4a4a;
    }
    
    /* Success alert */
    .success-box {
        padding: 10px;
        background-color: #1e3a1e;
        border: 1px solid #2e5a2e;
        border-radius: 5px;
        color: #4ade80;
        margin: 10px 0;
    }
    
    /* Error alert */
    .error-box {
        padding: 10px;
        background-color: #3a1e1e;
        border: 1px solid #5a2e2e;
        border-radius: 5px;
        color: #f87171;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_prompt' not in st.session_state:
    st.session_state.generated_prompt = ""
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'api_configured' not in st.session_state:
    st.session_state.api_configured = False
if 'openai_key' not in st.session_state:
    st.session_state.openai_key = ""
if 'gemini_key' not in st.session_state:
    st.session_state.gemini_key = ""

def get_api_key(provider):
    """Get API key from session state, user input, or Streamlit secrets"""
    if provider == "openai":
        # Priority: 1. Session state (user input), 2. Streamlit secrets, 3. Environment variable
        if st.session_state.openai_key:
            return st.session_state.openai_key
        elif hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            return st.secrets['OPENAI_API_KEY']
        else:
            return os.getenv('OPENAI_API_KEY', '')
    elif provider == "gemini":
        if st.session_state.gemini_key:
            return st.session_state.gemini_key
        elif hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
            return st.secrets['GEMINI_API_KEY']
        else:
            return os.getenv('GEMINI_API_KEY', '')
    return ""

def generate_with_openai(prompt, image=None):
    """Generate image using OpenAI API"""
    api_key = get_api_key("openai")
    
    if not api_key:
        st.error("OpenAI API key not configured. Please add it in the sidebar.")
        return None
    
    try:
        # Configure OpenAI
        openai.api_key = api_key
        
        # Generate image
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="hd",
            model="dall-e-3"
        )
        
        # Get image URL
        image_url = response['data'][0]['url']
        
        # Download image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            return Image.open(io.BytesIO(img_response.content))
        else:
            st.error("Failed to download generated image")
            return None
            
    except openai.error.AuthenticationError:
        st.error("Invalid OpenAI API key. Please check your key.")
        return None
    except openai.error.RateLimitError:
        st.error("Rate limit reached. Please wait and try again.")
        return None
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def generate_with_gemini(prompt, image=None):
    """Generate image using Gemini API"""
    api_key = get_api_key("gemini")
    
    if not api_key:
        st.error("Gemini API key not configured. Please add it in the sidebar.")
        return None
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Note: Gemini currently doesn't have image generation capability
        # This is a placeholder for when it becomes available
        st.info("Note: Gemini image generation is not yet available. This is a placeholder for future functionality.")
        
        # For now, we can use Gemini to enhance the prompt
        model = genai.GenerativeModel('gemini-pro')
        enhanced_prompt_response = model.generate_content(
            f"Enhance this image generation prompt to be more detailed and creative: {prompt}"
        )
        
        if enhanced_prompt_response.text:
            st.info(f"Enhanced prompt with Gemini: {enhanced_prompt_response.text[:200]}...")
            st.session_state.generated_prompt = enhanced_prompt_response.text
        
        return None
        
    except Exception as e:
        st.error(f"Error with Gemini API: {str(e)}")
        return None

def enhance_prompt(base_params, style_description="", style_reference=None):
    """Create an enhanced prompt based on parameters"""
    prompt_parts = []
    
    # Add base description
    if style_description:
        prompt_parts.append(style_description)
    
    # Add lighting style
    lighting = base_params.get('lighting', '')
    if lighting:
        lighting_prompts = {
            "Natural Sunlight": "natural sunlight, soft shadows, outdoor lighting",
            "Studio Softbox": "professional studio lighting, softbox diffusion, even illumination",
            "Golden Hour": "golden hour lighting, warm orange glow, long shadows",
            "Dramatic Shadows": "dramatic chiaroscuro lighting, deep shadows, high contrast",
            "Neon/Cyberpunk": "neon lighting, vibrant colors, cyberpunk aesthetic",
            "Candlelight": "warm candlelight, soft flickering glow, intimate atmosphere",
            "High Key": "high key lighting, bright and airy, minimal shadows",
            "Low Key": "low key lighting, dark and moody, selective illumination"
        }
        prompt_parts.append(lighting_prompts.get(lighting, lighting))
    
    # Add aspect ratio
    aspect = base_params.get('aspect_ratio', '')
    if aspect:
        aspect_prompts = {
            "1:1 Square": "square format composition, centered subject",
            "16:9 Landscape": "cinematic widescreen composition, horizontal emphasis",
            "9:16 Portrait": "vertical smartphone format, tall composition",
            "4:3 Standard": "classic photography ratio, balanced composition",
            "3:2 Classic": "traditional 35mm film ratio, natural proportions"
        }
        prompt_parts.append(aspect_prompts.get(aspect, aspect))
    
    # Add camera perspective
    perspective = base_params.get('perspective', '')
    if perspective:
        perspective_prompts = {
            "Eye Level": "eye level perspective, natural viewing angle",
            "Bird's Eye View": "bird's eye view, top-down aerial perspective",
            "Low Angle": "low angle hero shot, looking up perspective",
            "Dutch Angle": "dutch angle, tilted camera, dynamic composition",
            "Close-up/Macro": "extreme close-up macro photography, detailed texture",
            "Wide Angle": "wide angle lens, expanded field of view",
            "Isometric": "isometric perspective, 3/4 view angle"
        }
        prompt_parts.append(perspective_prompts.get(perspective, perspective))
    
    # Add quality modifiers
    prompt_parts.extend([
        "ultra-detailed",
        "professional photography",
        "high quality",
        "8K resolution"
    ])
    
    # Add style reference note if provided
    if style_reference:
        prompt_parts.append("matching the style and aesthetic of the reference image")
    
    return ", ".join(filter(None, prompt_parts))

# Sidebar for API Configuration
with st.sidebar:
    st.markdown("## 🔑 API Configuration")
    st.markdown("Enter your API keys or use Streamlit secrets")
    
    # OpenAI API Key
    openai_input = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.openai_key,
        placeholder="sk-...",
        help="Get your key from platform.openai.com"
    )
    if openai_input:
        st.session_state.openai_key = openai_input
    
    # Gemini API Key
    gemini_input = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.gemini_key,
        placeholder="AIza...",
        help="Get your key from makersuite.google.com"
    )
    if gemini_input:
        st.session_state.gemini_key = gemini_input
    
    # Check API status
    st.markdown("---")
    st.markdown("### 📊 API Status")
    
    openai_configured = bool(get_api_key("openai"))
    gemini_configured = bool(get_api_key("gemini"))
    
    if openai_configured:
        st.success("✅ OpenAI API configured")
    else:
        st.warning("⚠️ OpenAI API not configured")
    
    if gemini_configured:
        st.success("✅ Gemini API configured")
    else:
        st.warning("⚠️ Gemini API not configured")
    
    # Instructions
    st.markdown("---")
    st.markdown("### 📖 Instructions")
    st.markdown("""
    1. **Add API Keys**: Enter your keys above or add them to Streamlit secrets
    2. **Upload Image**: Select your product photo
    3. **Set Parameters**: Choose lighting, aspect ratio, and perspective
    4. **Create Scene**: Describe your desired scene
    5. **Generate**: Create your AI-enhanced image
    
    **For Streamlit Cloud:**
    Add keys in Settings → Secrets:
    ```toml
    OPENAI_API_KEY = "your-key"
    GEMINI_API_KEY = "your-key"
    ```
    """)

# Main UI
st.title("🎨 AI Photo Editor")
st.markdown("Transform your product photos with AI-powered scene generation")

col1, col2 = st.columns([1, 1.2], gap="large")

# Left column - Product upload and parameters
with col1:
    st.markdown("### Your Product")
    
    # Product image upload
    product_image = st.file_uploader(
        "Upload Product Photo",
        type=['png', 'jpg', 'jpeg', 'webp'],
        key="product_upload"
    )
    
    if product_image:
        image = Image.open(product_image)
        st.image(image, caption="Uploaded Product", use_column_width=True)

# Right column - Scene creation
with col2:
    st.markdown("### Scene Parameters")
    
    # Lighting selection
    lighting_style = st.selectbox(
        "Lighting",
        ["Natural Sunlight", "Studio Softbox", "Golden Hour", 
         "Dramatic Shadows", "Neon/Cyberpunk", "Candlelight",
         "High Key", "Low Key"]
    )
    
    # Aspect ratio selection
    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        ["1:1 Square", "16:9 Landscape", "9:16 Portrait", 
         "4:3 Standard", "3:2 Classic"]
    )
    
    # Camera perspective selection
    camera_perspective = st.selectbox(
        "Camera Perspective",
        ["Eye Level", "Bird's Eye View", "Low Angle", 
         "Dutch Angle", "Close-up/Macro", "Wide Angle", "Isometric"]
    )
    
    st.markdown("### Create Your Own Scene")
    
    # Scene description
    scene_description = st.text_area(
        "Describe your scene",
        placeholder="e.g., A sunny beach with palm trees",
        height=100
    )
    
    # Style reference
    st.markdown("### Style Reference (Optional)")
    style_reference = st.file_uploader(
        "Upload style reference image",
        type=['png', 'jpg', 'jpeg', 'webp'],
        key="style_upload"
    )
    
    if style_reference:
        style_image = Image.open(style_reference)
        st.image(style_image, caption="Style Reference", use_column_width=True)
    
    st.markdown("---")
    
    # API Selection
    st.markdown("### Generation Settings")
    api_choice = st.selectbox(
        "Select AI Model",
        ["OpenAI", "Gemini (Enhanced Prompts Only)"]
    )
    
    # Generate buttons
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🎨 Generate Prompt", use_container_width=True):
            if scene_description or product_image:
                params = {
                    'lighting': lighting_style,
                    'aspect_ratio': aspect_ratio,
                    'perspective': camera_perspective
                }
                st.session_state.generated_prompt = enhance_prompt(
                    params, 
                    scene_description, 
                    style_reference
                )
    
    with col_btn2:
        generate_clicked = st.button(
            "✨ Generate Image", 
            use_container_width=True,
            type="primary"
        )
    
    # Display generated prompt
    if st.session_state.generated_prompt:
        st.text_area(
            "Generated Prompt:",
            st.session_state.generated_prompt,
            height=100,
            disabled=True
        )
    
    # Generate image
    if generate_clicked:
        if not st.session_state.generated_prompt:
            st.error("Please generate a prompt first!")
        else:
            with st.spinner("🎨 Creating your image..."):
                if api_choice == "OpenAI":
                    generated_image = generate_with_openai(st.session_state.generated_prompt)
                else:
                    generated_image = generate_with_gemini(st.session_state.generated_prompt)
                
                if generated_image:
                    st.session_state.generated_image = generated_image
    
    # Display generated image
    if st.session_state.generated_image:
        st.markdown("### Generated Image")
        st.image(st.session_state.generated_image, use_column_width=True)
        
        # Download button
        buf = io.BytesIO()
        st.session_state.generated_image.save(buf, format='PNG')
        st.download_button(
            label="⬇️ Download Image",
            data=buf.getvalue(),
            file_name=f"ai_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png"
        )
