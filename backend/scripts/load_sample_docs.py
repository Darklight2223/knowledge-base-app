#!/usr/bin/env python3
"""
Script to load sample documents into the knowledge base.
Run this after setting up the backend to initialize with sample data.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_service import document_service

def load_sample_documents():
    """Load all sample documents from the sample_docs directory"""
    sample_docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_docs')
    
    if not os.path.exists(sample_docs_dir):
        print(f"❌ Sample docs directory not found: {sample_docs_dir}")
        return
    
    print("🚀 Loading sample documents into knowledge base...\n")
    
    for filename in os.listdir(sample_docs_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(sample_docs_dir, filename)
            
            try:
                print(f"📄 Processing: {filename}")
                
                # Read file content
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add to knowledge base
                doc_id = document_service.add_document(
                    filename=filename,
                    content=content,
                    doc_type='text',
                    metadata={'source': 'sample_data'}
                )
                
                print(f"✅ Loaded: {filename} (ID: {doc_id})")
                
            except Exception as e:
                print(f"❌ Error loading {filename}: {str(e)}")
    
    print("\n✨ Sample documents loaded successfully!")
    print("You can now query the knowledge base with questions like:")
    print("  - What are the pricing plans?")
    print("  - How do I integrate the API?")
    print("  - What's the refund policy?")

if __name__ == "__main__":
    load_sample_documents()
