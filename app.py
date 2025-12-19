from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import wikipedia
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import random
import re

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# YouTube API setup
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

def fetch_wikipedia_content(topic):
    """Fetch Wikipedia content for a given topic"""
    try:
        # Search for the topic
        search_results = wikipedia.search(topic, results=3)
        if not search_results:
            return None, "No Wikipedia articles found for this topic."
        
        # Get the first result's content
        page = wikipedia.page(search_results[0], auto_suggest=False)
        return {
            'title': page.title,
            'content': page.content,
            'url': page.url,
            'summary': page.summary
        }, None
    except wikipedia.exceptions.DisambiguationError as e:
        # If there's a disambiguation, try the first option
        try:
            page = wikipedia.page(e.options[0], auto_suggest=False)
            return {
                'title': page.title,
                'content': page.content,
                'url': page.url,
                'summary': page.summary
            }, None
        except:
            return None, f"Multiple articles found. Please be more specific."
    except Exception as e:
        return None, f"Error fetching Wikipedia content: {str(e)}"

def fetch_youtube_videos(topic, max_results=5):
    """Fetch YouTube videos for a given topic"""
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == 'your_youtube_api_key_here':
        # Return sample data if no API key
        return [{
            'id': 'sample_video',
            'title': f'Sample Educational Video about {topic}',
            'description': 'Please add your YouTube API key to .env file to see real videos.',
            'thumbnail': 'https://via.placeholder.com/320x180?text=Add+API+Key'
        }]
    
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # Search for educational videos
        search_response = youtube.search().list(
            q=f"{topic} tutorial educational",
            type='video',
            part='id,snippet',
            maxResults=max_results,
            relevanceLanguage='en',
            safeSearch='strict'
        ).execute()
        
        videos = []
        for item in search_response.get('items', []):
            videos.append({
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url']
            })
        
        return videos
    except Exception as e:
        print(f"Error fetching YouTube videos: {str(e)}")
        return []

def extract_keywords(text, num_keywords=10):
    """Extract important keywords from text using NLTK"""
    try:
        # Tokenize and convert to lowercase
        words = word_tokenize(text.lower())
        
        # Remove stopwords and non-alphabetic tokens
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.isalpha() and word not in stop_words and len(word) > 3]
        
        # Calculate frequency distribution
        fdist = FreqDist(words)
        
        # Get most common keywords
        keywords = [word for word, freq in fdist.most_common(num_keywords)]
        
        return keywords
    except Exception as e:
        print(f"Error extracting keywords: {str(e)}")
        return []

def summarize_text(text, num_sentences=5):
    """Summarize text by extracting key sentences"""
    try:
        # Split into sentences
        sentences = sent_tokenize(text)
        
        # If text is already short, return as is
        if len(sentences) <= num_sentences:
            return ' '.join(sentences)
        
        # Calculate word frequency
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.isalpha() and word not in stop_words]
        
        word_freq = FreqDist(words)
        
        # Score sentences based on word frequency
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_freq[word]
                    else:
                        sentence_scores[sentence] += word_freq[word]
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        
        # Sort by original order
        summary_sentences = []
        for sentence in sentences:
            if any(sentence == sent[0] for sent in top_sentences):
                summary_sentences.append(sentence)
                if len(summary_sentences) == num_sentences:
                    break
        
        return ' '.join(summary_sentences)
    except Exception as e:
        print(f"Error summarizing text: {str(e)}")
        return text[:500] + "..."

def generate_flashcards(text, keywords, num_cards=10):
    """Generate flashcards from text and keywords"""
    try:
        sentences = sent_tokenize(text)
        flashcards = []
        
        # Create flashcards from keywords
        for keyword in keywords[:num_cards]:
            # Find sentences containing the keyword
            relevant_sentences = [s for s in sentences if keyword.lower() in s.lower()]
            
            if relevant_sentences:
                # Use the first relevant sentence as the answer
                answer = relevant_sentences[0].strip()
                
                # Create a question
                question = f"What is {keyword}?"
                
                flashcards.append({
                    'question': question,
                    'answer': answer,
                    'keyword': keyword
                })
        
        return flashcards
    except Exception as e:
        print(f"Error generating flashcards: {str(e)}")
        return []

def generate_quiz(text, keywords, num_questions=5):
    """Generate multiple-choice quiz questions"""
    try:
        sentences = sent_tokenize(text)
        quiz = []
        
        # Generate questions from keywords
        for i, keyword in enumerate(keywords[:num_questions]):
            # Find sentences with this keyword
            relevant_sentences = [s for s in sentences if keyword.lower() in s.lower()]
            
            if relevant_sentences:
                sentence = relevant_sentences[0]
                
                # Create a fill-in-the-blank question
                question_text = sentence.replace(keyword, "______")
                
                # Create options (correct answer + distractors)
                options = [keyword]
                
                # Add random keywords as distractors
                other_keywords = [k for k in keywords if k != keyword]
                random.shuffle(other_keywords)
                options.extend(other_keywords[:3])
                
                # Shuffle options
                random.shuffle(options)
                
                quiz.append({
                    'id': i + 1,
                    'question': f"Fill in the blank: {question_text}",
                    'options': options,
                    'correct_answer': keyword,
                    'explanation': sentence
                })
        
        return quiz
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        return []

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/api/learn', methods=['POST'])
def learn():
    """Main endpoint to process a learning topic"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Fetch Wikipedia content
        wiki_data, wiki_error = fetch_wikipedia_content(topic)
        if wiki_error:
            return jsonify({'error': wiki_error}), 404
        
        # Extract content
        content = wiki_data['content']
        
        # Process with NLP
        keywords = extract_keywords(content, num_keywords=15)
        summary = summarize_text(content, num_sentences=5)
        flashcards = generate_flashcards(content, keywords, num_cards=10)
        quiz = generate_quiz(content, keywords, num_questions=5)
        
        # Fetch YouTube videos
        videos = fetch_youtube_videos(topic, max_results=5)
        
        # Prepare response
        response = {
            'success': True,
            'topic': wiki_data['title'],
            'summary': summary,
            'keywords': keywords,
            'flashcards': flashcards,
            'quiz': quiz,
            'videos': videos,
            'wiki_url': wiki_data['url']
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error in /api/learn: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/check-answer', methods=['POST'])
def check_answer():
    """Check quiz answer"""
    try:
        data = request.get_json()
        user_answer = data.get('answer', '')
        correct_answer = data.get('correct_answer', '')
        
        is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
        
        return jsonify({
            'correct': is_correct,
            'correct_answer': correct_answer
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
