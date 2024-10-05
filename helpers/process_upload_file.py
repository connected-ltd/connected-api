# import os
# import shutil
# import tempfile
# from pypdf import PdfReader
# from docx import Document
# from weaviate.util import generate_uuid5

# from helpers.weaviate import wv_upload_doc


# def check_if_file_exists(wv_client, wv_class_name, filename):
#     # Generate UUID based on the filename
#     object_uuid = generate_uuid5({"filename": filename})
    
#     # Check if object with the UUID exists
#     file = wv_client.collections.get("filename")
#     file_exists = file.data.exists(object_uuid)
#     # objects = wv_client.data.exists(object_uuid)
#     return file_exists
     


# def process_uploaded_file(file, wv_client, wv_class_name):
#     temp_dir = None
    
#     try:
#         # Check if file already exists in Weaviate
#         file_exists = check_if_file_exists(wv_client, wv_class_name, file.filename)
#         print("File exists", file_exists)
#         if file_exists:
#             return {"message": f"File {file.filename} already exists in Weaviate", "status": "exists"}
        
        
#         #saving the file temporarily
#         temp_dir = tempfile.mkdtemp()
#         temp_file_path = os.path.join(temp_dir, file.filename)
        
#         with open(temp_file_path,"wb") as buffer:
#             shutil.copyfileobj(file, buffer)
            
#         if file.filename.lower().endswith('.pdf'):
#             reader = PdfReader(temp_file_path)
#             text = ""
#             for page in reader.pages:
#                 text += page.extract_text() + "\n\n"
#         elif file.filename.lower().endswith('.docx'):
#             doc = Document(temp_file_path)
#             text = "\n\n".join([paragraph.text for paragraph in doc.paragraphs])
#         else:
#             raise ValueError(f"Unsupported file type: {file.filename}")
        
#         # Upload to Weaviate
#         print("Pass")
#         wv_upload_doc(wv_client, text, wv_class_name, file.filename)
#         print("Success")
        
#         return {"message": f"File {file.filename} processed and uploaded successfully", "status": "success"}, 200
#     except Exception as e:
#         print("Failed")
#         return {"message": f"Error processing file {file.filename}: {str(e)}", "status": "error"}, 500
    
#     finally:
#         # Clean up: close the file and remove the temporary directory
#         if temp_dir:
#             shutil.rmtree(temp_dir)
    