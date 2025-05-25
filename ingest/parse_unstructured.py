import os
import json
import fitz
import uuid
from datetime import datetime
from email import policy
from email.parser import BytesParser

def parse_pdf(file_path):
    try:
        doc_id = str(uuid.uuid4())
        created_at = datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
        
        with fitz.open(file_path) as doc:
            title = doc.metadata.get('title', os.path.basename(file_path))
            text = ""
            
            for page in doc:
                text += page.get_text()
        
        return {
            "doc_id": doc_id,
            "source_type": "pdf",
            "title": title,
            "body": text,
            "filename": os.path.basename(file_path),
            "created_at": created_at
        }
    except Exception as e:
        print(f"Error parsing PDF {file_path}: {e}")
        return None

def parse_email(file_path):
    try:
        doc_id = str(uuid.uuid4())
        created_at = datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
        
        with open(file_path, 'rb') as fp:
            msg = BytesParser(policy=policy.default).parse(fp)
        subject = msg.get('subject', '(No Subject)')
        from_address = msg.get('from', '(No Sender)')
        body = ""

        if msg.is_multipart():
            for part in msg.iter_parts():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body += part.get_content()
        else:
            body = msg.get_content()
            
        return {
            "doc_id": doc_id,
            "source_type": "email",
            "title": subject,
            "sender": from_address,
            "body": body,
            "filename": os.path.basename(file_path),
            "created_at": created_at
        }
    except Exception as e:
        print(f"Error parsing email {file_path}: {e}")
        return None

def process_directory(directory, output_file='data/parsed_docs.jsonl'):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'a') as out_file:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if not os.path.isfile(file_path):
                continue
                
            result = None
            if filename.lower().endswith('.pdf'):
                result = parse_pdf(file_path)
            elif filename.lower().endswith('.eml'):
                result = parse_email(file_path)
                
            if result:
                out_file.write(json.dumps(result) + '\n')
                print(f"Processed: {filename}")

if __name__ == "__main__":
    process_directory('data/pdfs')
    process_directory('data/emls')
    print("Done")