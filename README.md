# 📄 Resume Parser with Ragie

An intelligent resume parsing application that extracts structured information from resumes in various formats (PDF, DOCX, TXT) using the Ragie AI platform.

## 🚀 Features

- **Multi-format Support**: Process resumes in PDF, DOCX, and TXT formats
- **Structured Data Extraction**: Automatically extracts:
  - Personal Information (name, email, phone, location)
  - Professional Summary
  - Skills and Certifications
  - Work Experience (company, position, duration)
  - Education History
- **Batch Processing**: Upload and process multiple resumes at once
- **Web Interface**: User-friendly Streamlit web interface
- **API Integration**: Built on Ragie's powerful AI platform

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/icode247/ragie-resume-parser.git
   cd ragie-resume-parser
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your Ragie API token:
   ```
   RAGIE_AUTH_TOKEN=your_ragie_auth_token_here
   ```

## 🚀 Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. In the sidebar, click "Create Extraction Schema" to set up the parsing schema

4. Upload one or more resume files using the file uploader

5. Click "Parse Resumes" to start the extraction process

6. View the extracted information in the right panel

## 📊 Output

The parser extracts and displays:
- Personal details
- Contact information
- Professional summary
- Skills and certifications
- Work experience (company, position, duration)
- Education history

## 🔧 Requirements

- Python 3.7+
- Ragie API token
- Required Python packages (see `requirements.txt`)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For any questions or feedback, please open an issue on GitHub.
