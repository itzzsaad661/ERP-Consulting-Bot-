# AI ERP Consultant Chatbot

A professional AI-powered chatbot that provides expert guidance on Enterprise Resource Planning (ERP) systems. Built with Flask and Azure AI services, featuring a modern web interface with a professional bot avatar.

## 🚀 Features

- **AI-Powered ERP Consulting**: Get expert advice on ERP modules, implementation strategies, and best practices
- **Modern Web Interface**: Clean, responsive chat interface with professional styling
- **Professional Bot Avatar**: Custom 3D character avatar for enhanced user experience
- **Real-time Chat**: Instant responses with typing indicators and error handling
- **Azure AI Integration**: Powered by Llama-4-Scout-17B-16E-Instruct model

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **AI Service**: Azure AI Inference with GitHub Models
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Model**: meta/Llama-4-Scout-17B-16E-Instruct
- **Styling**: Modern dark theme with responsive design

## 📋 Prerequisites

- Python 3.8+
- GitHub account with access token
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ai-chat-bot
```

### 2. Create Virtual Environment
```bash
python -m venv chatbot
```

### 3. Activate Virtual Environment
**Windows:**
```bash
chatbot\Scripts\activate
```

**Linux/Mac:**
```bash
source chatbot/bin/activate
```

### 4. Install Dependencies
```bash
pip install flask azure-ai-inference azure-core
```

### 5. Set Environment Variables
**Windows PowerShell:**
```powershell
$env:GITHUB_TOKEN = "your_github_token_here"
```

**Windows Command Prompt:**
```cmd
set GITHUB_TOKEN=your_github_token_here
```

**Linux/Mac:**
```bash
export GITHUB_TOKEN="your_github_token_here"
```

### 6. Run the Application
```bash
python app.py
```

## 🌐 Usage

1. **Start the server**: Run `python app.py`
2. **Open your browser**: Navigate to `http://localhost:5000`
3. **Start chatting**: Ask questions about ERP systems!

### Example Questions to Ask:
- "What are the key modules in an ERP system?"
- "How do I implement ERP in a manufacturing company?"
- "What's the difference between SAP and Oracle ERP?"
- "How can ERP integrate with CRM systems?"
- "What are the benefits of cloud-based ERP?"

## 📁 Project Structure

```
ai-chat-bot/
├── app.py                 # Main Flask application
├── main.py               # Command-line version
├── static/
│   └── bot.png           # Bot avatar image
├── chatbot/              # Virtual environment
│   ├── Scripts/
│   └── Lib/
├── Image.png             # Original bot image
└── README.md             # This file
```

## 🎨 Customization

### Changing the Bot Avatar
1. Replace `static/bot.png` with your desired image
2. Ensure the image is optimized for web (recommended: 64x64px or 128x128px)
3. Supported formats: PNG, JPG, WebP

### Modifying the System Prompt
Edit the `SYSTEM_PROMPT` variable in `app.py` to change the bot's personality and expertise area.

### Styling Customization
The CSS is embedded in the HTML template within `app.py`. You can modify:
- Color scheme (CSS variables in `:root`)
- Font families
- Layout and spacing
- Responsive breakpoints

## 🔧 Configuration

### Environment Variables
- `GITHUB_TOKEN`: Required for Azure AI API access
- `PORT`: Optional, defaults to 5000

### Model Configuration
- **Model**: `meta/Llama-4-Scout-17B-16E-Instruct`
- **Temperature**: 0.7 (creativity level)
- **Top-p**: 0.9 (response diversity)
- **Max Tokens**: 1024 (response length)

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production, consider using:
- **Gunicorn** (Linux/Mac)
- **Waitress** (Windows)
- **Docker** containerization
- **Cloud platforms** (Azure, AWS, Heroku)

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐛 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'flask'"**
   - Solution: Activate your virtual environment first

2. **"GITHUB_TOKEN not found"**
   - Solution: Set the environment variable with your GitHub token

3. **"Network error" or API failures**
   - Check your internet connection
   - Verify your GitHub token is valid
   - Ensure the Azure AI endpoint is accessible

4. **Image not loading**
   - Check that `static/bot.png` exists
   - Verify file permissions
   - Clear browser cache

### Debug Mode
The app runs in debug mode by default. To disable:
```python
app.run(host="0.0.0.0", port=port, debug=False)
```

## 📝 API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Chat API endpoint
  - **Request**: `{"message": "your question"}`
  - **Response**: `{"reply": "bot response"}`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure all dependencies are installed
4. Verify environment variables are set correctly

## 🔮 Future Enhancements

- [ ] Conversation history persistence
- [ ] Multiple bot personalities
- [ ] File upload capabilities
- [ ] Voice input/output
- [ ] Mobile app version
- [ ] Admin dashboard
- [ ] Analytics and usage tracking

---

**Built with ❤️ for ERP professionals and businesses seeking digital transformation guidance.**
