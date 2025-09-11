# from .document_loader import DocumentLoader
# from .text_preprocessor import TextProcessor
# from .embeddings import EmbeddingsManager
# from .retrieval_system import RetrievalSystem


# class RAGSystem:
#     def __init__(self, groq_api_key, google_api_key, image_output_dir="/content/"):
#         self.groq_api_key = groq_api_key
#         self.google_api_key = google_api_key
#         self.image_output_dir = image_output_dir
        
#         # Initialize components
#         self.document_loader = DocumentLoader(image_output_dir)
#         self.text_processor = TextProcessor(groq_api_key)
#         self.embeddings_manager = EmbeddingsManager(google_api_key)
#         self.retrieval_system = None
    
#     def process_document(self, pdf_path, img_dir="/content/figures"):
#         """Complete pipeline to process a PDF document"""
        
#         # 1. Load PDF
#         print("Loading PDF...")
#         elements = self.document_loader.load_pdf(pdf_path)
        
#         # 2. Filter elements
#         print("Filtering elements...")
#         filtered_elements, table_elements = self.document_loader.filter_elements(elements)
        
#         # 3. Chunk text elements
#         print("Chunking elements...")
#         chunks = self.text_processor.chunk_elements(filtered_elements)
        
#         # 4. Combine chunks with tables
#         total_chunks = self.text_processor.combine_chunks_and_tables(chunks, table_elements)
        
#         # 5. Categorize elements
#         print("Categorizing elements...")
#         categorized_elements, table_elements_categorized, text_elements_categorized = \
#             self.text_processor.categorize_elements(total_chunks)
        
#         # 6. Summarize elements
#         print("Summarizing elements...")
#         table_summaries, text_summaries, tables, texts = \
#             self.text_processor.summarize_elements(table_elements_categorized, text_elements_categorized)
        
#         # 7. Process images
#         print("Processing images...")
#         img_summaries = self.document_loader.load_images_from_directory(img_dir, self.google_api_key)
        
#         # 8. Store in vector database
#         print("Storing in vector database...")
#         doc_ids = self.embeddings_manager.process_and_store_content(
#             text_summaries, table_summaries, img_summaries, texts, tables
#         )
        
#         # 9. Initialize retrieval system
#         print("Setting up retrieval system...")
#         self.retrieval_system = RetrievalSystem(
#             self.embeddings_manager.get_vectorstore(),
#             self.embeddings_manager.get_docstore(),
#             groq_api_key=self.groq_api_key
#         )
        
#         print("RAG system setup complete!")
#         return {
#             'elements_processed': len(elements),
#             'text_chunks': len(texts),
#             'tables': len(tables),
#             'images': len(img_summaries),
#             'doc_ids': doc_ids
#         }
    
#     def query(self, question):
#         """Query the RAG system"""
#         if not self.retrieval_system:
#             raise ValueError("No document processed yet. Please process a document first.")
        
#         return self.retrieval_system.query(question)
    
#     def get_relevant_docs(self, question, k=4):
#         """Get relevant documents for debugging/inspection"""
#         if not self.retrieval_system:
#             raise ValueError("No document processed yet. Please process a document first.")
        
#         return self.retrieval_system.get_relevant_docs(question, k)


# # Example usage function
# def create_rag_system(groq_api_key, google_api_key):
#     """Factory function to create a RAG system instance"""
#     return RAGSystem(groq_api_key, google_api_key)


# Api limit
# from .document_loader import DocumentLoader
# from .text_preprocessor import TextProcessor
# from .embeddings import EmbeddingsManager
# from .retrieval_system import RetrievalSystem


# class RAGSystem:
#     def __init__(self, groq_api_key, google_api_key, image_output_dir="/content/"):
#         self.groq_api_key = groq_api_key
#         self.google_api_key = google_api_key
#         self.image_output_dir = image_output_dir
        
#         # Initialize components
#         self.document_loader = DocumentLoader(image_output_dir)
#         self.text_processor = TextProcessor(groq_api_key)
#         self.embeddings_manager = EmbeddingsManager(google_api_key)
#         self.retrieval_system = None
    
#     def process_document(self, pdf_path, img_dir="/content/figures"):
#         """Complete pipeline to process a PDF document"""
        
#         # 1. Load PDF
#         print("Loading PDF...")
#         elements = self.document_loader.load_pdf(pdf_path)
        
#         # 2. Filter elements
#         print("Filtering elements...")
#         filtered_elements, table_elements = self.document_loader.filter_elements(elements)
        
#         # 3. Chunk text elements
#         print("Chunking elements...")
#         chunks = self.text_processor.chunk_elements(filtered_elements)
        
#         # 4. Combine chunks with tables
#         total_chunks = self.text_processor.combine_chunks_and_tables(chunks, table_elements)
        
#         # 5. Categorize elements
#         print("Categorizing elements...")
#         categorized_elements, table_elements_categorized, text_elements_categorized = \
#             self.text_processor.categorize_elements(total_chunks)
        
#         # 6. Summarize elements
#         print("Summarizing elements...")
#         table_summaries, text_summaries, tables, texts = \
#             self.text_processor.summarize_elements(table_elements_categorized, text_elements_categorized)
        
#         # 7. Process images
#         print("Processing images...")
#         img_summaries = self.document_loader.load_images_from_directory(img_dir, self.google_api_key)
        
#         # 8. Store in vector database
#         print("Storing in vector database...")
#         doc_ids = self.embeddings_manager.process_and_store_content(
#             text_summaries, table_summaries, img_summaries, texts, tables
#         )
        
#         # 9. Initialize retrieval system
#         print("Setting up retrieval system...")
#         self.retrieval_system = RetrievalSystem(
#             self.embeddings_manager.get_vectorstore(),
#             self.embeddings_manager.get_docstore(),
#             groq_api_key=self.groq_api_key
#         )
        
#         print("RAG system setup complete!")
#         return {
#             'elements_processed': len(elements),
#             'text_chunks': len(texts),
#             'tables': len(tables),
#             'images': len(img_summaries),
#             'doc_ids': doc_ids
#         }
    
#     def query(self, question):
#         """Query the RAG system"""
#         if not self.retrieval_system:
#             raise ValueError("No document processed yet. Please process a document first.")
        
#         return self.retrieval_system.query(question)
    
#     def get_relevant_docs(self, question, k=4):
#         """Get relevant documents for debugging/inspection"""
#         if not self.retrieval_system:
#             raise ValueError("No document processed yet. Please process a document first.")
        
#         return self.retrieval_system.get_relevant_docs(question, k)


# # Example usage function
# def create_rag_system(groq_api_key, google_api_key):
#     """Factory function to create a RAG system instance"""
#     return RAGSystem(groq_api_key, google_api_key)


import uuid
import time
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
        
        # Initialize storage for parent documents
        self.store = InMemoryStore()
    
    def create_documents_from_summaries(self, summaries, original_content, prefix=""):
        """Create Document objects from summaries with metadata"""
        # Filter out empty summaries first
        valid_summaries = []
        valid_original = []
        
        for i, summary in enumerate(summaries):
            if summary and str(summary).strip():  # Check if not empty
                valid_summaries.append(str(summary).strip())
                if i < len(original_content):
                    valid_original.append(original_content[i])
        
        if not valid_summaries:
            print(f"⚠️ Warning: No valid {prefix} summaries found")
            return [], [], []
        
        doc_ids = [str(uuid.uuid4()) for _ in valid_summaries]
        
        summary_docs = [
            Document(page_content=s, metadata={self.id_key: doc_ids[i]})
            for i, s in enumerate(valid_summaries)
        ]
        
        print(f"📝 Created {len(summary_docs)} valid {prefix} documents")
        return summary_docs, doc_ids, valid_original
    
    def add_documents_to_vectorstore_with_retry(self, summary_docs, max_retries=3):
        """Add summary documents to vectorstore with rate limiting and retry logic"""
        if not summary_docs:
            print("⚠️ No documents to add to vectorstore")
            return
        
        # Process in small batches to avoid rate limits
        batch_size = 3  # Very small batch size for Google API
        total_batches = (len(summary_docs) + batch_size - 1) // batch_size
        
        print(f"📊 Processing {len(summary_docs)} documents in {total_batches} batches of {batch_size}")
        
        for batch_idx in range(0, len(summary_docs), batch_size):
            batch = summary_docs[batch_idx:batch_idx + batch_size]
            batch_num = batch_idx // batch_size + 1
            
            for attempt in range(max_retries):
                try:
                    print(f"🔄 Processing batch {batch_num}/{total_batches} (attempt {attempt + 1})")
                    
                    # Validate batch documents
                    valid_batch = []
                    for doc in batch:
                        if doc.page_content and doc.page_content.strip():
                            valid_batch.append(doc)
                    
                    if valid_batch:
                        self.vectorstore.add_documents(valid_batch)
                        print(f"✅ Successfully added batch {batch_num}: {len(valid_batch)} documents")
                    
                    # Success - break out of retry loop
                    break
                    
                except Exception as e:
                    error_str = str(e)
                    
                    if "429" in error_str or "quota" in error_str.lower():
                        # Rate limit error
                        if attempt < max_retries - 1:
                            wait_time = min(60 * (2 ** attempt), 300)  # Exponential backoff, max 5 minutes
                            print(f"⚠️ Rate limit hit for batch {batch_num}. Waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                        else:
                            print(f"❌ Max retries exceeded for batch {batch_num}. Skipping this batch.")
                            print(f"Error: {e}")
                    else:
                        # Other error
                        print(f"❌ Error processing batch {batch_num}: {e}")
                        break
            
            # Add delay between successful batches to respect rate limits
            if batch_idx + batch_size < len(summary_docs):
                print("⏳ Waiting 10 seconds between batches to respect rate limits...")
                time.sleep(10)
    
    def add_documents_to_vectorstore(self, summary_docs):
        """Add summary documents to vectorstore with rate limiting"""
        self.add_documents_to_vectorstore_with_retry(summary_docs)
    
    def store_original_content(self, doc_ids, original_content):
        """Store original content in docstore"""
        if doc_ids and original_content:
            self.store.mset(list(zip(doc_ids, original_content)))
    
    def process_and_store_content(self, text_summaries, table_summaries, img_summaries,
                                 texts, tables):
        """Process and store all content types (texts, tables, images)"""
        
        print("🔍 Content analysis:")
        print(f"   Text summaries: {len(text_summaries) if text_summaries else 0}")
        print(f"   Table summaries: {len(table_summaries) if table_summaries else 0}")
        print(f"   Image summaries: {len(img_summaries) if img_summaries else 0}")
        
        # Check if we have any content at all
        total_content = (len(text_summaries) if text_summaries else 0) + \
                       (len(table_summaries) if table_summaries else 0) + \
                       (len(img_summaries) if img_summaries else 0)
        
        if total_content == 0:
            print("❌ ERROR: No content summaries to process!")
            return {'text_ids': [], 'table_ids': [], 'img_ids': []}
        
        print(f"📊 Total content items to process: {total_content}")
        print("🌐 Using Google Embeddings with rate limiting...")
        
        all_doc_ids = {'text_ids': [], 'table_ids': [], 'img_ids': []}
        
        # Process text content
        if text_summaries and texts:
            try:
                print("\n📝 Processing text summaries...")
                text_summary_docs, text_doc_ids, filtered_texts = self.create_documents_from_summaries(
                    text_summaries, texts, "text"
                )
                if text_summary_docs:
                    self.add_documents_to_vectorstore(text_summary_docs)
                    self.store_original_content(text_doc_ids, filtered_texts)
                    all_doc_ids['text_ids'] = text_doc_ids
            except Exception as e:
                print(f"❌ Error processing text content: {e}")
        
        # Process table content
        if table_summaries and tables:
            try:
                print("\n📊 Processing table summaries...")
                table_summary_docs, table_doc_ids, filtered_tables = self.create_documents_from_summaries(
                    table_summaries, tables, "table"
                )
                if table_summary_docs:
                    self.add_documents_to_vectorstore(table_summary_docs)
                    self.store_original_content(table_doc_ids, filtered_tables)
                    all_doc_ids['table_ids'] = table_doc_ids
            except Exception as e:
                print(f"❌ Error processing table content: {e}")
        
        # Process image content
        if img_summaries:
            try:
                print("\n🖼️ Processing image summaries...")
                img_summary_docs, img_doc_ids, filtered_img_summaries = self.create_documents_from_summaries(
                    img_summaries, img_summaries, "image"
                )
                if img_summary_docs:
                    self.add_documents_to_vectorstore(img_summary_docs)
                    self.store_original_content(img_doc_ids, filtered_img_summaries)
                    all_doc_ids['img_ids'] = img_doc_ids
            except Exception as e:
                print(f"❌ Error processing image content: {e}")
        
        # Summary
        total_processed = len(all_doc_ids['text_ids']) + len(all_doc_ids['table_ids']) + len(all_doc_ids['img_ids'])
        if total_processed > 0:
            print(f"\n✅ Successfully processed {total_processed} items with Google embeddings")
        else:
            print(f"\n⚠️ WARNING: No content was successfully processed!")
        
        return all_doc_ids
    
    def get_vectorstore(self):
        """Get the vectorstore instance"""
        return self.vectorstore
    
    def get_docstore(self):
        """Get the document store instance"""
        return self.store