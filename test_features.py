"""
Test script to demonstrate the AI EdTech application functionality
"""

import json
from app import (
    extract_keywords,
    summarize_text,
    generate_flashcards,
    generate_quiz
)

# Sample text for testing
SAMPLE_TEXT = """
Machine learning is a subset of artificial intelligence that focuses on enabling computers 
to learn from data without being explicitly programmed. Deep learning is a subset of machine 
learning that uses neural networks with multiple layers. Neural networks are computational 
models inspired by the human brain's structure. Supervised learning uses labeled data to 
train models, while unsupervised learning finds patterns in unlabeled data. Reinforcement 
learning involves agents learning through trial and error by receiving rewards or penalties.
The training process involves feeding data to the model and adjusting its parameters to 
minimize error. Overfitting occurs when a model performs well on training data but poorly 
on new data. Feature engineering is the process of selecting and transforming variables 
for machine learning models.
"""

def test_nlp_features():
    """Test NLP processing features"""
    print("=" * 70)
    print("AI EDTECH - NLP FEATURES TEST")
    print("=" * 70)
    
    # Test keyword extraction
    print("\n1. KEYWORD EXTRACTION")
    print("-" * 70)
    keywords = extract_keywords(SAMPLE_TEXT, num_keywords=10)
    print(f"Extracted Keywords: {', '.join(keywords)}")
    
    # Test summarization
    print("\n2. TEXT SUMMARIZATION")
    print("-" * 70)
    summary = summarize_text(SAMPLE_TEXT, num_sentences=3)
    print(f"Summary:\n{summary}")
    
    # Test flashcard generation
    print("\n3. FLASHCARD GENERATION")
    print("-" * 70)
    flashcards = generate_flashcards(SAMPLE_TEXT, keywords, num_cards=5)
    for i, card in enumerate(flashcards, 1):
        print(f"\nFlashcard {i}:")
        print(f"  Question: {card['question']}")
        print(f"  Answer: {card['answer'][:100]}...")
    
    # Test quiz generation
    print("\n4. QUIZ GENERATION")
    print("-" * 70)
    quiz = generate_quiz(SAMPLE_TEXT, keywords, num_questions=3)
    for q in quiz:
        print(f"\nQuestion {q['id']}: {q['question']}")
        for i, option in enumerate(q['options'], 1):
            marker = "✓" if option == q['correct_answer'] else " "
            print(f"  {marker} {i}. {option}")
        print(f"  Correct Answer: {q['correct_answer']}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == '__main__':
    test_nlp_features()
