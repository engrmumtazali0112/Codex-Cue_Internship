import os
import PyPDF2
import docx
import nltk
import numpy as np
import openai
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Configure OpenAI API
openai.api_key = "use-your-own-api"
# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    """Preprocess text for plagiarism detection."""
    # Initialize NLTK components
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens 
             if token not in stop_words]
    
    return ' '.join(tokens)

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts using TF-IDF and cosine similarity."""
    # Create TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    
    # Preprocess texts
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)
    
    try:
        # Calculate TF-IDF
        tfidf_matrix = vectorizer.fit_transform([processed_text1, processed_text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return float(similarity)
    except Exception as e:
        print(f"Error calculating similarity: {str(e)}")
        return 0.0

def check_ai_generated(text):
    """Check if text is likely AI-generated using OpenAI's API."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze if the following text is likely AI-generated:\n\n{text[:1000]}\n\nIs this AI-generated?",
            max_tokens=100,
            temperature=0.3
        )
        
        analysis = response.choices[0].text.strip().lower()
        # Simple threshold based on the API response
        is_ai_generated = "yes" in analysis or "likely" in analysis
        confidence = 0.8 if is_ai_generated else 0.2
        
        return {
            'is_ai_generated': is_ai_generated,
            'confidence': confidence,
            'analysis': analysis
        }
    except Exception as e:
        print(f"Error checking AI generation: {str(e)}")
        return {
            'is_ai_generated': False,
            'confidence': 0,
            'analysis': "Error analyzing text"
        }

def extract_text_from_pdf(file_path):
    """Extract text from PDF files."""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {str(e)}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from DOCX files."""
    try:
        doc = docx.Document(file_path)
        text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX {file_path}: {str(e)}")
        return ""

def find_exact_matches(text1, text2):
    """Find exact matching phrases between two texts."""
    sentences1 = sent_tokenize(text1)
    sentences2 = sent_tokenize(text2)
    matches = []
    
    for i, sent1 in enumerate(sentences1):
        for j, sent2 in enumerate(sentences2):
            # Find common substrings
            words1 = sent1.split()
            words2 = sent2.split()
            
            for length in range(4, len(words1) + 1):  # Min 4 words for a match
                for start in range(len(words1) - length + 1):
                    phrase = ' '.join(words1[start:start + length])
                    if phrase in sent2 and len(phrase.split()) >= 4:
                        matches.append({
                            'text': phrase,
                            'position1': (i, start),
                            'position2': (j, sent2.index(phrase))
                        })
    
    return matches

def detect_plagiarism(file_paths):
    """Enhanced main function to check plagiarism across multiple documents."""
    results = []
    file_contents = {}

    # Extract text from all documents
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            continue
            
        if text:
            file_contents[file_path] = text
            # Check for AI-generated content
            ai_check = check_ai_generated(text)
            file_contents[file_path + '_ai_check'] = ai_check

    # Compare documents
    for i, (file1, text1) in enumerate(file_contents.items()):
        if '_ai_check' in file1:
            continue
            
        for j, (file2, text2) in enumerate(file_contents.items()):
            if '_ai_check' in file2 or i >= j:
                continue

            # Calculate overall similarity
            similarity_score = calculate_similarity(text1, text2)
            
            # Find exact matching phrases
            exact_matches = find_exact_matches(text1, text2)
            
            # Get AI detection results
            ai_check1 = file_contents.get(file1 + '_ai_check', {})
            ai_check2 = file_contents.get(file2 + '_ai_check', {})
            
            results.append({
                'file1': os.path.basename(file1),
                'file2': os.path.basename(file2),
                'overall_similarity': similarity_score,
                'exact_matches': exact_matches,
                'ai_detection': {
                    'file1': ai_check1,
                    'file2': ai_check2
                }
            })

    return results