from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq


class RetrievalSystem:
    def __init__(self, vectorstore, docstore, id_key="doc_id", groq_api_key=None):
        self.vectorstore = vectorstore
        self.docstore = docstore
        self.id_key = id_key
        self.groq_api_key = groq_api_key
        
        # Initialize retriever
        self.retriever = MultiVectorRetriever(
            vectorstore=vectorstore,
            docstore=docstore,
            id_key=id_key,
        )
        
        # Initialize model if API key provided
        self.model = None
        if groq_api_key:
            self.model = ChatGroq(
                model="gemma2-9b-it",
                temperature=0,
                api_key=groq_api_key
            )
    
    def setup_rag_chain(self):
        """Setup RAG chain for question answering"""
        if not self.model:
            raise ValueError("Groq API key required for RAG chain")
            
        # Prompt template
        template = """Answer the question based only on the following context, which can include text and tables:

{context}

Question: {question}
"""
        prompt = ChatPromptTemplate.from_template(template)
        
        # RAG pipeline
        chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.model
            | StrOutputParser()
        )
        
        return chain
    
    def query(self, question):
        """Query the RAG system with a question"""
        chain = self.setup_rag_chain()
        return chain.invoke(question)
    
    def get_relevant_docs(self, question, k=4):
        """Get relevant documents for a question"""
        return self.retriever.get_relevant_documents(question, k=k)
    
    def update_retriever_stores(self, new_vectorstore=None, new_docstore=None):
        """Update the retriever with new stores if needed"""
        if new_vectorstore:
            self.retriever.vectorstore = new_vectorstore
        if new_docstore:
            self.retriever.docstore = new_docstore