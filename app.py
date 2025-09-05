import os
from src.rag_system import RAGSystem
    
if __name__ == "__main__":
    
    # Get API keys - you can either set these as environment variables or hardcode them here
    groq_api_key = os.getenv('GROQ_API_KEY', 'your_groq_api_key_here')
    google_api_key = os.getenv('GOOGLE_API_KEY', 'your_google_api_key_here')
    
    if groq_api_key == 'your_groq_api_key_here' or google_api_key == 'your_google_api_key_here':
        print("⚠️  Please set your API keys!")
        print("Either:")
        print("1. Set environment variables: GROQ_API_KEY and GOOGLE_API_KEY")
        print("2. Or edit this file and replace the placeholder keys")
        exit(1)
    
    # Initialize RAG system
    print("🚀 Initializing RAG system...")
    rag = RAGSystem(
        groq_api_key=groq_api_key,
        google_api_key=google_api_key,
        image_output_dir="./data/images/"
    )
    
    # For Kaggle - use a predefined PDF path (you need to upload your PDF to Kaggle)
    # Change this path to your uploaded PDF file in Kaggle
    pdf_path = "/kaggle/input/your-dataset/your-document.pdf"  # Update this path
    
    # Alternative: You can also hardcode a path if you know where your PDF is
    # pdf_path = "./sample.pdf"
    
    print(f"📄 Using PDF file: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found at {pdf_path}")
        print("Please upload your PDF file to Kaggle dataset or update the pdf_path variable")
        exit(1)
    
    try:
        print(f"📊 Processing document: {pdf_path}")
        results = rag.process_document(pdf_path, "./data/images/")
        
        print("\n" + "="*60)
        print("✅ DOCUMENT PROCESSING COMPLETE!")
        print("="*60)
        print(f"📑 Elements processed: {results['elements_processed']}")
        print(f"📝 Text chunks: {results['text_chunks']}")
        print(f"📊 Tables: {results['tables']}")
        print(f"🖼️  Images: {results['images']}")
        print("="*60)
        
        # Predefined questions for Kaggle testing (no interactive input)
        predefined_questions = [
            "What is the main topic or subject of this document?",
            "What are the key findings or conclusions mentioned?",
            "Are there any numerical data, statistics, or performance metrics discussed?"
        ]
        
        print("\n🤖 Testing RAG system with predefined questions...")
        print("="*60)
        
        for i, question in enumerate(predefined_questions, 1):
            try:
                print(f"\n📋 Question {i}: {question}")
                print("🔍 Searching for answer...")
                answer = rag.query(question)
                print(f"💡 Answer: {answer}")
                print("-" * 50)
                
            except Exception as e:
                print(f"❌ Error processing question {i}: {e}")
                print("-" * 50)
        
        print("\n✅ All test questions completed!")
        print("🎉 RAG system is working correctly on Kaggle!")
    
    except Exception as e:
        print(f"❌ Error processing document: {e}")
        print("Make sure your PDF file is valid and API keys are correct.")
        print("For Kaggle, ensure you've uploaded your PDF as a dataset.")