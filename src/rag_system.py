from .document_loader import DocumentLoader
from .text_preprocessor import TextProcessor
from .embeddings import EmbeddingsManager
from .retrieval_system import RetrievalSystem


class RAGSystem:
    def __init__(self, groq_api_key, google_api_key, image_output_dir="/content/"):
        self.groq_api_key = groq_api_key
        self.google_api_key = google_api_key
        self.image_output_dir = image_output_dir
        
        # Initialize components
        self.document_loader = DocumentLoader(image_output_dir)
        self.text_processor = TextProcessor(groq_api_key)
        self.embeddings_manager = EmbeddingsManager(google_api_key)
        self.retrieval_system = None
    
    def process_document(self, pdf_path, img_dir="/content/figures"):
        """Complete pipeline to process a PDF document"""
        
        # 1. Load PDF
        print("Loading PDF...")
        elements = self.document_loader.load_pdf(pdf_path)
        
        # 2. Filter elements
        print("Filtering elements...")
        filtered_elements, table_elements = self.document_loader.filter_elements(elements)
        
        # 3. Chunk text elements
        print("Chunking elements...")
        chunks = self.text_processor.chunk_elements(filtered_elements)
        
        # 4. Combine chunks with tables
        total_chunks = self.text_processor.combine_chunks_and_tables(chunks, table_elements)
        
        # 5. Categorize elements
        print("Categorizing elements...")
        categorized_elements, table_elements_categorized, text_elements_categorized = \
            self.text_processor.categorize_elements(total_chunks)
        
        # 6. Summarize elements
        print("Summarizing elements...")
        table_summaries, text_summaries, tables, texts = \
            self.text_processor.summarize_elements(table_elements_categorized, text_elements_categorized)
        
        # 7. Process images
        print("Processing images...")
        img_summaries = self.document_loader.load_images_from_directory(img_dir, self.google_api_key)
        
        # 8. Store in vector database
        print("Storing in vector database...")
        doc_ids = self.embeddings_manager.process_and_store_content(
            text_summaries, table_summaries, img_summaries, texts, tables
        )
        
        # 9. Initialize retrieval system
        print("Setting up retrieval system...")
        self.retrieval_system = RetrievalSystem(
            self.embeddings_manager.get_vectorstore(),
            self.embeddings_manager.get_docstore(),
            groq_api_key=self.groq_api_key
        )
        
        print("RAG system setup complete!")
        return {
            'elements_processed': len(elements),
            'text_chunks': len(texts),
            'tables': len(tables),
            'images': len(img_summaries),
            'doc_ids': doc_ids
        }
    
    def query(self, question):
        """Query the RAG system"""
        if not self.retrieval_system:
            raise ValueError("No document processed yet. Please process a document first.")
        
        return self.retrieval_system.query(question)
    
    def get_relevant_docs(self, question, k=4):
        """Get relevant documents for debugging/inspection"""
        if not self.retrieval_system:
            raise ValueError("No document processed yet. Please process a document first.")
        
        return self.retrieval_system.get_relevant_docs(question, k)


# Example usage function
def create_rag_system(groq_api_key, google_api_key):
    """Factory function to create a RAG system instance"""
    return RAGSystem(groq_api_key, google_api_key)