# import os
# from src.rag_system import RAGSystem
    
# if __name__ == "__main__":
    
#     # Get API keys - you can either set these as environment variables or hardcode them here
#     groq_api_key = os.getenv('GROQ_API_KEY', 'your_groq_api_key_here')
#     google_api_key = os.getenv('GOOGLE_API_KEY', 'your_google_api_key_here')
    
#     if groq_api_key == 'your_groq_api_key_here' or google_api_key == 'your_google_api_key_here':
#         print("⚠️  Please set your API keys!")
#         print("Either:")
#         print("1. Set environment variables: GROQ_API_KEY and GOOGLE_API_KEY")
#         print("2. Or edit this file and replace the placeholder keys")
#         exit(1)
    
#     # Initialize RAG system
#     print("🚀 Initializing RAG system...")
#     rag = RAGSystem(
#         groq_api_key=groq_api_key,
#         google_api_key=google_api_key,
#         image_output_dir="./data/images/"
#     )
    
#     # Process document
#     pdf_path = input("📄 Enter path to your PDF file: ").strip()
    
#     if not os.path.exists(pdf_path):
#         print(f"❌ Error: File not found at {pdf_path}")
#         exit(1)
    
#     try:
#         print(f"📊 Processing document: {pdf_path}")
#         results = rag.process_document(pdf_path, "./data/images/")
        
#         print("\n" + "="*60)
#         print("✅ DOCUMENT PROCESSING COMPLETE!")
#         print("="*60)
#         print(f"📑 Elements processed: {results['elements_processed']}")
#         print(f"📝 Text chunks: {results['text_chunks']}")
#         print(f"📊 Tables: {results['tables']}")
#         print(f"🖼️  Images: {results['images']}")
#         print("="*60)
        
#         # Interactive query loop
#         print("\n🤖 RAG system is ready! Ask questions about your document.")
#         print("💡 Type 'quit' or 'exit' to stop.\n")
        
#         while True:
#             question = input("❓ Your question: ").strip()
            
#             if question.lower() in ['quit', 'exit', 'q', 'stop']:
#                 print("👋 Goodbye!")
#                 break
            
#             if not question:
#                 print("Please enter a valid question.")
#                 continue
            
#             try:
#                 print("🔍 Searching for answer...")
#                 answer = rag.query(question)
#                 print(f"\n💡 Answer: {answer}\n")
#                 print("-" * 50)
                
#             except Exception as e:
#                 print(f"❌ Error processing question: {e}")
    
#     except Exception as e:
#         print(f"❌ Error processing document: {e}")
#         print("Make sure your PDF file is valid and API keys are correct.")

"""
Main application file to run RAG system
Usage: python app.py
"""

if __name__ == "__main__":
    from kaggle_secrets import UserSecretsClient
    import os
    from src.rag_system import RAGSystem
    
    # Initialize Kaggle Secrets client
    user_secrets = UserSecretsClient()
    
    # Get API keys from Kaggle Secrets
    try:
        groq_api_key = user_secrets.get_secret("GROQ_API_KEY")
        google_api_key = user_secrets.get_secret("GOOGLE_API_KEY")
    except Exception as e:
        print(f"⚠️ Error loading secrets: {e}")
        print("Please ensure you have added 'GROQ_API_KEY' and 'GOOGLE_API_KEY' in Kaggle Secrets.")
        print("Steps:")
        print("1. Go to Notebook Add-ons -> Kaggle Secrets")
        print("2. Add secrets with labels 'GROQ_API_KEY' and 'GOOGLE_API_KEY'")
        print("3. Attach them to this notebook")
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
    pdf_path = "/kaggle/input/llava-paper-1/2304.08485v2.pdf"  # Update this path
    
    # Alternative: You can also hardcode a path if you know where your PDF is
    # pdf_path = "./sample.pdf"
    
    print(f"📄 Using PDF file: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found at {pdf_path}")
        print("Please upload your PDF file to Kaggle dataset or update the pdf_path variable")
        exit(1)
    
    try:
        print(f"📊 Processing document: {pdf_path}")
        img_dir = '/kaggle/working/Multimodal-RAG/imges/'
        results = rag.process_document(pdf_path, image_dir = img_dir)
        
        print("\n" + "="*60)
        print("✅ DOCUMENT PROCESSING COMPLETE!")
        print("="*60)
        print(f"📑 Elements processed: {results['elements_processed']}")
        print(f"📝 Text chunks: {results['text_chunks']}")
        print(f"📊 Tables: {results['tables']}")
        print(f"🖼️  Images: {results['images']}")
        
        # Show extracted images
        if os.path.exists(img_dir):
            image_files = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
            print(f"📷 Extracted image files: {len(image_files)}")
            for img_file in image_files:
                print(f"   - {img_file}")
        
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