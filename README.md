# 🎨 AI Photo Editor - Scene Generation App

A powerful Streamlit application for AI-powered product photo editing and scene generation using OpenAI and Google Gemini APIs.

## 🌟 Features

- **Product Photo Upload**: Easy drag-and-drop interface for product images
- **Scene Parameters**: 
  - Multiple lighting styles (Natural, Studio, Golden Hour, etc.)
  - Various aspect ratios (Square, Landscape, Portrait, etc.)
  - Different camera perspectives (Eye Level, Bird's Eye, Macro, etc.)
- **AI-Powered Generation**: 
  - OpenAI image generation
  - Gemini prompt enhancement
- **Flexible API Key Management**:
  - Input keys directly in the app dashboard
  - Use Streamlit Cloud secrets
  - Environment variables support
- **Style Reference**: Upload reference images for style inspiration
- **Dark Mode UI**: Professional dark-themed interface
- **Download Functionality**: Save generated images locally

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Optional: Google Gemini API key

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-photo-editor.git
cd ai-photo-editor
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🔑 API Key Configuration

You have THREE options to configure API keys:

### Option 1: Direct Input in App
1. Open the app
2. Look at the sidebar on the left
3. Enter your API keys in the input fields
4. Keys are stored for your session

### Option 2: Streamlit Cloud Secrets
1. Deploy to Streamlit Cloud
2. Go to your app's Settings
3. Navigate to Secrets section
4. Add your secrets:
```toml
OPENAI_API_KEY = "sk-your-openai-key-here"
GEMINI_API_KEY = "AIza-your-gemini-key-here"
```

### Option 3: Environment Variables (Local)
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=AIza-your-gemini-key-here
```

## 🔗 Getting API Keys

### OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key starting with `sk-`

### Google Gemini API Key
1. Go to [makersuite.google.com](https://makersuite.google.com) or [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Get your API key from the dashboard
4. Copy the key starting with `AIza`

## 📦 Deployment to Streamlit Cloud

### Step 1: Prepare GitHub Repository

1. Create a new GitHub repository
2. Push your code with these files:
   - `app.py` (main application)
   - `requirements.txt` (dependencies)
   - `README.md` (this file)
   - `.gitignore`

**Important**: Do NOT commit your `.env` file or API keys to GitHub!

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Fill in:
   - Repository: Select your GitHub repo
   - Branch: main (or master)
   - Main file path: app.py
5. Click "Deploy"

### Step 3: Configure Secrets in Streamlit Cloud

1. Once deployed, go to your app's dashboard
2. Click on "Settings" (⚙️ icon)
3. Navigate to "Secrets"
4. Add your API keys:
```toml
OPENAI_API_KEY = "sk-your-key-here"
GEMINI_API_KEY = "AIza-your-key-here"
```
5. Click "Save"
6. Your app will restart with the keys configured

## 💰 API Costs

### OpenAI Pricing
- Image generation: ~$0.040-$0.080 per image
- Check [OpenAI Pricing](https://openai.com/pricing) for current rates

### Google Gemini Pricing
- Free tier: 60 requests per minute
- Check [Google AI Pricing](https://ai.google.dev/pricing) for details

## 🎨 Usage Guide

### Basic Workflow

1. **Configure API Keys**
   - Enter keys in the sidebar OR
   - Use Streamlit secrets

2. **Upload Product Photo** (optional)
   - Click or drag-drop your product image
   - Supports PNG, JPG, JPEG, WebP

3. **Set Scene Parameters**
   - Choose lighting style
   - Select aspect ratio
   - Pick camera perspective

4. **Describe Your Scene**
   - Enter a detailed description
   - Upload a style reference (optional)

5. **Generate Prompt**
   - Click "Generate Prompt"
   - Review the enhanced prompt

6. **Create Image**
   - Select AI model (OpenAI or Gemini)
   - Click "Generate Image"
   - Wait for generation (10-20 seconds)

7. **Download Result**
   - Review generated image
   - Click "Download Image" to save

## 🔧 Configuration Files

### `.env.example`
```env
# Copy this to .env and add your keys
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### `.gitignore`
```
# API Keys and Secrets
.env
.env.local
secrets.toml

# Python
__pycache__/
*.py[cod]
venv/
.venv/

# Streamlit
.streamlit/secrets.toml

# OS
.DS_Store
Thumbs.db
```

### `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#5865F2"
backgroundColor = "#1a1a1a"
secondaryBackgroundColor = "#242424"
textColor = "#FFFFFF"

[server]
maxUploadSize = 200
```

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "API key not configured" | Add key in sidebar or Streamlit secrets |
| "Invalid API key" | Check key format and validity |
| "Rate limit exceeded" | Wait a few minutes or upgrade API plan |
| "Image generation failed" | Check internet connection and API status |
| "Module not found" | Run `pip install -r requirements.txt` |

### API Key Issues

**OpenAI Key Not Working:**
- Ensure key starts with `sk-`
- Check if you have credits/billing set up
- Verify key hasn't expired

**Gemini Key Not Working:**
- Ensure key starts with `AIza`
- Check if API is enabled in Google Cloud Console
- Verify you're within rate limits

### Streamlit Cloud Issues

**Secrets Not Working:**
1. Ensure secrets are saved in Settings
2. Restart the app after adding secrets
3. Check secret names match exactly (case-sensitive)

**Deployment Fails:**
1. Check `requirements.txt` is valid
2. Ensure no syntax errors in `app.py`
3. Check logs in Streamlit Cloud dashboard

## 📊 Performance Tips

- **Image Generation**: Takes 10-20 seconds typically
- **Rate Limits**: Space out requests to avoid limits
- **File Size**: Keep uploads under 10MB for best performance
- **Caching**: App caches generated images during session

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google AI Studio](https://aistudio.google.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud Guide](https://docs.streamlit.io/streamlit-cloud)

## 📞 Support

- Create an issue on GitHub for bugs
- Check existing issues for solutions
- Review the troubleshooting section above

---

Built with ❤️ using Streamlit and AI
