# 🎓 AI-EdTech: AI-Powered Learning Platform

A full-stack AI-powered EdTech web application that transforms any topic into an interactive learning experience with AI-generated summaries, flashcards, quizzes, and curated educational videos.

## ✨ Features

### 🧠 AI-Powered Content Processing
- **Wikipedia Integration**: Automatically fetches comprehensive content on any topic
- **NLP Summarization**: Uses Natural Language Processing to create concise, meaningful summaries
- **Keyword Extraction**: Identifies and highlights key concepts using NLTK
- **Smart Content Analysis**: Processes and structures information for optimal learning

### 📚 Interactive Learning Tools
- **Flashcards**: AI-generated flashcards with question-answer format and flip animation
- **MCQ Quizzes**: Multiple-choice questions with instant scoring and detailed explanations
- **Video Library**: Curated YouTube educational videos embedded directly in the app
- **Topic Summaries**: Easy-to-understand summaries of complex topics

### 🎨 Modern User Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Beautiful UI**: Modern gradient design with smooth animations
- **Intuitive Navigation**: Tab-based interface for easy content exploration
- **Interactive Elements**: Flip cards, hover effects, and smooth transitions

### 🔌 REST API
- **POST /api/learn**: Submit a topic and receive comprehensive learning materials
- **POST /api/check-answer**: Validate quiz answers with instant feedback
- **JSON Responses**: Clean, structured data for easy integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- (Optional) YouTube Data API key for video integration

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/drunkprada/AI-EdTech.git
cd AI-EdTech
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (optional but recommended for YouTube videos)
```bash
cp .env.example .env
# Edit .env and add your YouTube API key
```

To get a YouTube API key:
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or select an existing one
- Enable the YouTube Data API v3
- Create credentials (API Key)
- Copy the API key to your `.env` file

5. **Run the application**
```bash
python app.py
```

6. **Open your browser**
Navigate to `http://localhost:5000`

## 📖 Usage

1. **Enter a Topic**: Type any subject you want to learn about (e.g., "Quantum Physics", "Ancient Rome", "Machine Learning")

2. **Explore Content**:
   - **Summary Tab**: Read an AI-generated summary and view key concepts
   - **Flashcards Tab**: Study with interactive flip cards
   - **Quiz Tab**: Test your knowledge with multiple-choice questions
   - **Videos Tab**: Watch curated educational videos

3. **Interactive Learning**:
   - Flip flashcards by clicking on them
   - Navigate through cards using Previous/Next buttons
   - Answer quiz questions and get instant feedback
   - View your final score and retake quizzes
   - Click on video thumbnails to watch embedded content

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework for REST API
- **NLTK**: Natural Language Toolkit for text processing
- **Wikipedia API**: Content fetching from Wikipedia
- **YouTube Data API**: Video search and retrieval
- **Python Libraries**: transformers, scikit-learn, requests

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with animations and responsive design
- **JavaScript (Vanilla)**: Interactive functionality without frameworks
- **REST API Integration**: Async fetch calls for data retrieval

### NLP Processing
- **Tokenization**: Sentence and word tokenization using NLTK
- **Keyword Extraction**: Frequency-based keyword identification
- **Text Summarization**: Sentence scoring and extraction
- **Content Generation**: Automated flashcard and quiz creation

## 📁 Project Structure

```
AI-EdTech/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
└── static/               # Frontend files
    ├── index.html        # Main HTML structure
    ├── styles.css        # CSS styling
    └── script.js         # JavaScript functionality
```

## 🔧 API Documentation

### POST /api/learn
Fetches and processes learning content for a given topic.

**Request Body:**
```json
{
  "topic": "Artificial Intelligence"
}
```

**Response:**
```json
{
  "success": true,
  "topic": "Artificial Intelligence",
  "summary": "AI is...",
  "keywords": ["machine learning", "neural networks", ...],
  "flashcards": [
    {
      "question": "What is machine learning?",
      "answer": "Machine learning is...",
      "keyword": "machine learning"
    }
  ],
  "quiz": [
    {
      "id": 1,
      "question": "Fill in the blank: ______",
      "options": ["option1", "option2", ...],
      "correct_answer": "option1",
      "explanation": "Explanation text"
    }
  ],
  "videos": [
    {
      "id": "video_id",
      "title": "Video Title",
      "description": "Description",
      "thumbnail": "thumbnail_url"
    }
  ],
  "wiki_url": "https://en.wikipedia.org/wiki/..."
}
```

### POST /api/check-answer
Validates a quiz answer.

**Request Body:**
```json
{
  "answer": "user_answer",
  "correct_answer": "correct_answer"
}
```

**Response:**
```json
{
  "correct": true,
  "correct_answer": "correct_answer"
}
```

## 🎯 Features in Detail

### NLP Processing Pipeline
1. **Content Fetching**: Retrieves Wikipedia articles using the Wikipedia API
2. **Text Cleaning**: Removes unnecessary formatting and special characters
3. **Tokenization**: Breaks text into sentences and words
4. **Stopword Removal**: Filters out common words (the, is, at, etc.)
5. **Frequency Analysis**: Calculates word frequency distributions
6. **Keyword Extraction**: Identifies the most important terms
7. **Summarization**: Selects key sentences based on word frequency scores
8. **Content Generation**: Creates flashcards and quizzes from extracted keywords

### Responsive Design
- Mobile-first approach with breakpoints at 768px and 480px
- Touch-friendly buttons and interactive elements
- Optimized layouts for different screen sizes
- Accessible navigation on all devices

### User Experience
- Loading animations during content fetching
- Error handling with user-friendly messages
- Smooth transitions between sections
- Visual feedback for all interactions
- Progress tracking for quizzes and flashcards

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:
- Report bugs and suggest features
- Improve documentation
- Add new NLP processing techniques
- Enhance UI/UX design
- Add support for more content sources

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Wikipedia API for providing free educational content
- YouTube Data API for video integration
- NLTK team for natural language processing tools
- Flask framework for backend development

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Built with ❤️ for learners everywhere