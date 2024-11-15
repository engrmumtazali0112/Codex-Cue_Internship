# 📝 Document Plagiarism Detector

A robust Flask-based web application that detects plagiarism and AI-generated content across PDF and DOCX documents using advanced NLP techniques and OpenAI's API.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![NLTK](https://img.shields.io/badge/NLTK-3.6+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

### 📺 Demo

Here’s a quick demo of the Plagiarism Detection Tool in action:

[![Plagiarism Detection Tool Video Demo](https://github.com/engrmumtazali0112/Codex-Cue_Internship/blob/main/plagiarism-detection-python/IMG_6924-ezgif.com-video-to-gif-converter.gif)](https://github.com/engrmumtazali0112/Codex-Cue_Internship/blob/main/plagiarism-detection-python/bandicam%202024-11-15%2008-36-19-818.mp4)


## 🚀 Features

- **Multi-Document Comparison**: Compare multiple documents simultaneously
- **Support for Multiple Formats**: Process PDF and DOCX files
- **Advanced Text Analysis**:
  - TF-IDF vectorization
  - Cosine similarity measurement
  - Exact phrase matching
- **AI Content Detection**: Integration with OpenAI API to identify AI-generated content
- **Detailed Results**:
  - Overall similarity scores
  - Exact matching phrases
  - AI content detection confidence scores
- **Clean Web Interface**: User-friendly upload and results visualization

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Text Processing**: NLTK, scikit-learn
- **Document Parsing**: PyPDF2, python-docx
- **AI Integration**: OpenAI API
- **Frontend**: HTML, CSS (static/css/style.css)

## 📁 Project Structure

```
plagiarism_detector/
├── app.py                     # Flask application main file
├── plagiarism_detector.py     # Core detection logic
├── static/
│   └── css/
│       └── style.css         # Styling files
├── templates/
│   ├── index.html            # Upload interface
│   └── results.html          # Results display
└── uploads/                  # Temporary file storage
```

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/engrmumtazali0112/Codex-Cue_Internship/tree/main/plagiarism-detection-python
cd plagiarism-detector
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'  # On Windows: set OPENAI_API_KEY=your-api-key-here
```

## 🚀 Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload at least two documents (PDF or DOCX format)

4. Click "Check Plagiarism" to analyze the documents

## 📊 How It Works

1. **Document Processing**:
   - Extracts text from PDF and DOCX files
   - Preprocesses text (tokenization, lemmatization, stopword removal)

2. **Similarity Detection**:
   - Converts text to TF-IDF vectors
   - Calculates cosine similarity between documents
   - Identifies exact matching phrases

3. **AI Content Detection**:
   - Analyzes text using OpenAI's API
   - Provides confidence scores for AI-generated content

## ⚠️ Important Notes

- Maximum file size: 16MB
- Supported formats: PDF, DOCX
- Temporary files are automatically deleted after processing
- Requires valid OpenAI API key for AI detection features

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NLTK for natural language processing capabilities
- OpenAI for AI content detection
- Flask framework for web implementation
- PyPDF2 and python-docx for document parsing

## 📧 Contact

Project maintained by [Mumtaz Ali](mailto:engrmumtazali01@gmail.com)

CodexCue Software Solutions - [codexcuepak@gmail.com](mailto:codexcuepak@gmail.com)


