# Health-insigh-Agent

AI Agent to analyze blood reports and provide detailed health insights.

## 🌟 Features

- Intelligent agent-based architecture with multi-model cascade system
- In-context learning from previous analyses and knowledge base building
- Medical report analysis with personalized health insights
- PDF upload, validation and text extraction (up to 20MB)
- Secure user authentication and session management
- Session history with report analysis tracking
- Modern, responsive UI with real-time feedback

## 🛠️ Tech Stack

- **Frontend Framework**: Streamlit
- **AI Integration**: Multi-model architecture via Groq
  - Primary: meta-llama/llama-4-maverick-17b-128e-instruct
  - Secondary: llama-3.3-70b-versatile
  - Tertiary: llama-3.1-8b-instant
  - Fallback: llama3-70b-8192
- **Database**: Supabase
- **PDF Processing**: PDFPlumber
- **Authentication**: Supabase Auth