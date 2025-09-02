from flask import Flask, request, send_file, send_from_directory
import os
from werkzeug.utils import secure_filename
from pdf2docx import Converter
from docx2pdf import convert as docx2pdf_convert

app = Flask(__name__)

# Folder to store uploaded and converted files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# === ROUTES ===

# Serve index.html from the project root (not from templates/)
@app.route('/')
def index():
    # Change to 'PDFTODOCX.html' if that’s your file name
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    uploaded_file = request.files.get('file')
    convert_type = request.form.get('convert_type')

    if not uploaded_file:
        return "No file uploaded", 400

    filename = secure_filename(uploaded_file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(input_path)

    try:
        if convert_type == 'pdf_to_docx' and filename.endswith('.pdf'):
            output_path = input_path.replace('.pdf', '.docx')
            cv = Converter(input_path)
            cv.convert(output_path)
            cv.close()
            return send_file(output_path, as_attachment=True)

        elif convert_type == 'docx_to_pdf' and filename.endswith('.docx'):
            output_path = input_path.replace('.docx', '.pdf')
            docx2pdf_convert(input_path, output_path)
            return send_file(output_path, as_attachment=True)

        else:
            return "Invalid file type or conversion type", 400

    except Exception as e:
        return f"Error during conversion: {str(e)}", 500

# === MAIN ENTRY ===
if __name__ == '__main__':
    app.run(debug=True)

