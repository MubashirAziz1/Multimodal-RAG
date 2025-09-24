# API limit issue

import uuid
from langchain.storage import InMemoryStore
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document


class EmbeddingsManager:
    def __init__(self, google_api_key):
        self.google_api_key = google_api_key
        self.id_key = "doc_id"
        
        # Initialize vectorstore with Google embeddings
        self.vectorstore = Chroma(
            collection_name="summaries",
            embedding_function=GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=google_api_key
            )
        )
        
    
        self.store = InMemoryStore()
    
    def create_documents_from_summaries(self, summaries, original_content, prefix=""):
        """Create Document objects from summaries with metadata"""
        doc_ids = [str(uuid.uuid4()) for _ in summaries]
        
        summary_docs = [
            Document(page_content=s, metadata={self.id_key: doc_ids[i]}) for i, s in enumerate(summaries)
        ]
        
        return summary_docs, doc_ids, original_content
    
    def add_documents_to_vectorstore(self, summary_docs):
        """Add summary documents to vectorstore"""
        self.vectorstore.add_documents(summary_docs)
    
    def store_original_content(self, doc_ids, original_content):
        """Store original content in docstore"""
        self.store.mset(list(zip(doc_ids, original_content)))
    
    def process_and_store_content(self, text_summaries, table_summaries, img_summaries,
                                 texts, tables):
        
        # Process text content
        text_summary_docs, text_doc_ids, _ = self.create_documents_from_summaries(
            text_summaries, texts, "text"
        )
        self.add_documents_to_vectorstore(text_summary_docs)
        self.store_original_content(text_doc_ids, texts)
        
        # Process table content
        table_summary_docs, table_doc_ids, _ = self.create_documents_from_summaries(
            table_summaries, tables, "table"
        )
        self.add_documents_to_vectorstore(table_summary_docs)
        self.store_original_content(table_doc_ids, tables)
        
        # Process image content
        img_summary_docs, img_doc_ids, _ = self.create_documents_from_summaries(
            img_summaries, img_summaries, "image"
        )
        self.add_documents_to_vectorstore(img_summary_docs)
        # Store the image summary as the raw document
        self.store_original_content(img_doc_ids, img_summaries)
        
        return {
            'text_ids': text_doc_ids,
            'table_ids': table_doc_ids, 
            'img_ids': img_doc_ids
        }
    
    def get_vectorstore(self):
        return self.vectorstore
    
    def get_docstore(self):
        return self.store


