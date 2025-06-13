import streamlit as st
import pandas as pd
from resume_parser import ResumeParser
import json
import tempfile
import os

def main():
    st.set_page_config(
        page_title="Resume Parser with Ragie",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Resume Parser with Ragie")
    st.markdown("Upload resume files and extract structured information automatically!")
    
    # Initialize the resume parser
    if 'parser' not in st.session_state:
        st.session_state.parser = ResumeParser()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        if st.button("Create Extraction Schema"):
            with st.spinner("Creating extraction instruction..."):
                result = st.session_state.parser.create_extraction_instruction()
                if result:
                    st.success(f"Schema created! ID: {result.id}")
                else:
                    st.error("Failed to create schema")
        
        if st.button("List Available Instructions"):
            with st.spinner("Loading instructions..."):
                instructions = st.session_state.parser.list_available_instructions()
                if instructions:
                    st.write("Available Instructions:")
                    for instruction in instructions:
                        st.write(f"- {instruction.name}")
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Upload Resumes")
        
        uploaded_files = st.file_uploader(
            "Choose resume files",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Upload PDF, DOCX, or TXT resume files"
        )
        
        if uploaded_files and st.button("Parse Resumes", type="primary"):
            with st.spinner("Processing resumes..."):
                results = []
                progress_bar = st.progress(0)
                
                for i, uploaded_file in enumerate(uploaded_files):
                    st.write(f"Processing: {uploaded_file.name}")
                    
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # Parse the resume
                    extracted_data = st.session_state.parser.upload_and_parse_resume(tmp_file_path)
                    
                    if extracted_data:
                        results.append({
                            "file_name": uploaded_file.name,
                            "extracted_data": extracted_data
                        })
                    else:
                        st.warning(f"Could not extract data from {uploaded_file.name}")
                    
                    # Clean up temporary file
                    os.unlink(tmp_file_path)
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                st.session_state.parsing_results = results
                st.success(f"Successfully processed {len(results)} resume(s)")
    
    with col2:
        st.header("Parsing Results")
        
        if 'parsing_results' in st.session_state and st.session_state.parsing_results:
            for i, result in enumerate(st.session_state.parsing_results):
                with st.expander(f"📄 {result['file_name']}", expanded=i==0):
                    data = result['extracted_data']
                    
                    # Personal Information
                    st.subheader("Personal Information")
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        first_name = data.get('firstName', 'N/A')
                        last_name = data.get('lastName', 'N/A')
                        full_name = f"{first_name} {last_name}".strip()
                        st.write(f"**Name:** {full_name}")
                        st.write(f"**Email:** {data.get('email', 'N/A')}")
                    
                    with col_b:
                        st.write(f"**Phone:** {data.get('phone', 'N/A')}")
                        st.write(f"**Location:** {data.get('location', 'N/A')}")
                    
                    # Summary
                    if data.get('summary'):
                        st.subheader("Summary")
                        st.write(data['summary'])
                    
                    # Skills
                    if data.get('skills') and len(data['skills']) > 0:
                        st.subheader("Skills")
                        skills_text = ", ".join(data['skills'])
                        st.write(skills_text)
                    
                    # Experience
                    if data.get('experience') and len(data['experience']) > 0:
                        st.subheader("Experience")
                        for exp in data['experience']:
                            st.write(f"**{exp.get('position', 'N/A')}** at {exp.get('company', 'N/A')}")
                            if exp.get('duration'):
                                st.write(f"Duration: {exp['duration']}")
                            if exp.get('description'):
                                st.write(f"Description: {exp['description']}")
                            st.write("---")
                    
                    # Education
                    if data.get('education') and len(data['education']) > 0:
                        st.subheader("Education")
                        for edu in data['education']:
                            degree = edu.get('degree', 'N/A')
                            institution = edu.get('institution', 'N/A')
                            st.write(f"**{degree}** from {institution}")
                            if edu.get('graduationYear'):
                                st.write(f"Graduated: {edu['graduationYear']}")
                            st.write("---")
                    
                    # Certifications
                    if data.get('certifications') and len(data['certifications']) > 0:
                        st.subheader("Certifications")
                        for cert in data['certifications']:
                            st.write(f"• {cert}")
                    
                    # Raw JSON data
                    if st.checkbox("Show Raw JSON Data", key=f"json_{result['file_name']}"):
                        st.json(data)
            
            # Export functionality
            st.subheader("Export Results")
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                if st.button("Export as JSON"):
                    json_data = json.dumps(st.session_state.parsing_results, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name="resume_parsing_results.json",
                        mime="application/json"
                    )
            
            with col_export2:
                if st.button("Export as CSV"):
                    # Flatten data for CSV export
                    flattened_data = []
                    for result in st.session_state.parsing_results:
                        data = result['extracted_data']
                        row = {
                            'file_name': result['file_name'],
                            'first_name': data.get('firstName', ''),
                            'last_name': data.get('lastName', ''),
                            'email': data.get('email', ''),
                            'phone': data.get('phone', ''),
                            'location': data.get('location', ''),
                            'summary': data.get('summary', ''),
                            'skills': ', '.join(data.get('skills', [])),
                            'certifications': ', '.join(data.get('certifications', []))
                        }
                        flattened_data.append(row)
                    
                    df = pd.DataFrame(flattened_data)
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name="resume_parsing_results.csv",
                        mime="text/csv"
                    )
        
        else:
            st.info("Upload and parse resumes to see results here.")
            st.markdown("""
            **How to get started:**
            1. Click 'Create Extraction Schema' in the sidebar
            2. Upload one or more resume files
            3. Click 'Parse Resumes' to extract structured data
            4. View and export the results
            """)

if __name__ == "__main__":
    main()
