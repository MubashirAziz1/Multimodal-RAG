import os
from src.rag_system import RAGSystem
    
if __name__ == "__main__":
    
    groq_api_key = os.getenv('GROQ_API_KEY', 'your_groq_api_key_here')
    google_api_key = os.getenv('GOOGLE_API_KEY', 'your_google_api_key_here')
    
    if groq_api_key == 'your_groq_api_key_here' or google_api_key == 'your_google_api_key_here':
        print(" Please set your API keys!")
        exit(1)
    
    print("🚀 Initializing RAG system...")
    rag = RAGSystem(
        groq_api_key=groq_api_key,
        google_api_key=google_api_key,
        image_output_dir="./data/images/"
    )
    
    # Process document
    pdf_path = input("Enter path to your PDF file: ").strip()
    
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        exit(1)
    
    try:
        print(f"Processing document: {pdf_path}")
        results = rag.process_document(pdf_path, "./data/images/")
        
        print("\n" + "="*60)
        print("DOCUMENT PROCESSING COMPLETE!")
        print("="*60)
        print(f"Elements processed: {results['elements_processed']}")
        print(f"Text chunks: {results['text_chunks']}")
        print(f"Tables: {results['tables']}")
        print(f"Images: {results['images']}")
        
        # Interactive query loop
        print("\nRAG system is ready! Ask questions about your document.")
        print("Type 'quit' or 'exit' to stop.\n")
        
        while True:
            question = input("Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q', 'stop']:
                print("Goodbye!")
                break
            
            if not question:
                print("Please enter a valid question.")
                continue
            
            try:
                print("Searching for answer...")
                answer = rag.query(question)
                print(f"\n Answer: {answer}\n")
                print("-" * 50)
                
            except Exception as e:
                print(f"Error processing question: {e}")
    
    except Exception as e:
        print(f"Error processing document: {e}")
        print("Make sure your PDF file is valid and API keys are correct.")

