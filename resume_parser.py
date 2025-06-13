import os
from dotenv import load_dotenv
from ragie import Ragie
import json
import time

# Load environment variables
load_dotenv()

class ResumeParser:
    def __init__(self):
        self.client = Ragie(auth=os.getenv("RAGIE_AUTH_TOKEN"))
        self.instruction_id = None
    
    def create_extraction_instruction(self):
        """Create the entity extraction instruction for resume parsing"""
        
        # Define the entity schema using JSON Schema format
        entity_schema = {
            "type": "object",
            "properties": {
                "firstName": {
                    "type": "string",
                    "description": "First name of the candidate"
                },
                "lastName": {
                    "type": "string", 
                    "description": "Last name of the candidate"
                },
                "email": {
                    "type": "string",
                    "description": "Email address"
                },
                "phone": {
                    "type": "string",
                    "description": "Phone number"
                },
                "location": {
                    "type": "string",
                    "description": "City, State or full address"
                },
                "summary": {
                    "type": "string",
                    "description": "Professional summary or objective statement"
                },
                "skills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Array of technical and professional skills"
                },
                "experience": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "company": {"type": "string", "description": "Company name"},
                            "position": {"type": "string", "description": "Job title/position"},
                            "duration": {"type": "string", "description": "Employment duration"},
                            "description": {"type": "string", "description": "Brief job description"}
                        }
                    },
                    "description": "Array of work experience entries"
                },
                "education": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "institution": {"type": "string", "description": "School/University name"},
                            "degree": {"type": "string", "description": "Degree type and field"},
                            "graduationYear": {"type": "string", "description": "Year of graduation"}
                        }
                    },
                    "description": "Array of education entries"
                },
                "certifications": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Array of professional certifications"
                }
            }
        }
        
        try:
            response = self.client.entities.create_instruction(request={
                "name": f"Resume Parser {int(time.time())}",
                "prompt": "Extract structured information from resume documents including personal details, skills, experience, education, and certifications. If any field is not found, set it to null or empty array as appropriate.",
                "entity_schema": entity_schema
            })
            self.instruction_id = response.id
            print(f"Instruction created successfully with ID: {self.instruction_id}")
            return response
        except Exception as e:
            print(f"Error creating instruction: {str(e)}")
            return None
    
    def upload_and_parse_resume(self, file_path):
        """Upload a resume document and extract entities"""
        try:
            # Ensure we have an instruction
            if not self.instruction_id:
                print("No instruction found. Creating extraction instruction...")
                self.create_extraction_instruction()
            
            # Upload the document using the documents API
            with open(file_path, 'rb') as file:
                upload_response = self.client.documents.create(request={
                    "file": {
                        "file_name": os.path.basename(file_path),
                        "content": file,
                    }
                })
            
            document_id = upload_response.id
            print(f"Document uploaded successfully with ID: {document_id}")
            
            # Wait for document processing
            time.sleep(8)
            
            # Get extracted entities using the entities API
            extraction_response = self.client.entities.list_by_document(request={
                "document_id": "15895021-4a85-439e-a65b-97e884f785c6"
            })

            print("extraction_response", extraction_response)
            
            # Parse the response based on the actual API structure
            if hasattr(extraction_response, 'result') and hasattr(extraction_response.result, 'entities'):
                entities = extraction_response.result.entities
                if entities and len(entities) > 0:
                    # Merge data from all entities to create complete profile
                    merged_data = {}
                    for entity in entities:
                        if hasattr(entity, 'data') and entity.data:
                            for key, value in entity.data.items():
                                if value:  # Only use non-empty values
                                    if key in merged_data:
                                        if isinstance(value, list) and isinstance(merged_data[key], list):
                                            merged_data[key].extend(value)
                                        elif merged_data[key] is None:
                                            merged_data[key] = value
                                    else:
                                        merged_data[key] = value
                    
                    # Remove duplicates from arrays
                    for key in ["skills", "certifications"]:
                        if key in merged_data and isinstance(merged_data[key], list):
                            merged_data[key] = list(set(merged_data[key]))
                    
                    print(f"Successfully extracted and merged data from {len(entities)} entities")
                    return merged_data
            
            print("No entities extracted. Document may still be processing.")
            return None
                
        except Exception as e:
            print(f"Error processing resume: {str(e)}")
            return None

    def parse_multiple_resumes(self, file_paths):
        """Parse multiple resume files"""
        results = []
        
        for file_path in file_paths:
            print(f"Processing: {file_path}")
            extracted_data = self.upload_and_parse_resume(file_path)
            print("extracted_data", extracted_data)
            
            if extracted_data:
                results.append({
                    "file_name": os.path.basename(file_path),
                    "extracted_data": extracted_data
                })
        
        return results

    def list_available_instructions(self):
        """List all available extraction instructions"""
        try:
            instructions = self.client.entities.list_instructions()
            return instructions
        except Exception as e:
            print(f"Error listing instructions: {str(e)}")
            return None



