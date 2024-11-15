from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from plagiarism_detector import detect_plagiarism, extract_text_from_pdf, extract_text_from_docx  # Ensure these are imported

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism():
    if 'files[]' not in request.files:
        flash('No files selected')
        return redirect(url_for('index'))
        
    files = request.files.getlist('files[]')
        
    if not files or files[0].filename == '':
        flash('No files selected')
        return redirect(url_for('index'))
        
    file_paths = []
    file_contents = {}
        
    try:
        # Save uploaded files
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)
                
        if len(file_paths) < 2:
            flash('Please upload at least two files to compare')
            return redirect(url_for('index'))
                
        # Read file contents before detection
        for file_path in file_paths:
            if file_path.endswith('.pdf'):
                content = extract_text_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                content = extract_text_from_docx(file_path)
            else:
                content = ""
            
            if content:
                file_contents[os.path.basename(file_path)] = content
                
        # Perform plagiarism check
        results = detect_plagiarism(file_paths)
                
        # Clean up uploaded files
        for file_path in file_paths:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing file {file_path}: {str(e)}")
                
        return render_template('results.html', 
                             results=results, 
                             file_contents=file_contents)
        
    except Exception as e:
        # Clean up any uploaded files in case of error
        for file_path in file_paths:
            try:
                os.remove(file_path)
            except:
                pass
        flash(f'Error processing files: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
