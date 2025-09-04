from unstructured.chunking.title import chunk_by_title
from pydantic import BaseModel
from typing import Any
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class Element(BaseModel):
    type: str
    text: Any


class TextProcessor:
    def __init__(self, groq_api_key=None):
        self.groq_api_key = groq_api_key
        self.model = None
        if groq_api_key:
            self.model = ChatGroq(
                model="gemma2-9b-it", 
                temperature=0, 
                api_key=groq_api_key
            )
    
    def chunk_elements(self, filtered_elements, combine_text_under_n_chars=2000, 
                      max_characters=4000, new_after_n_chars=3800):
        """Chunk elements by title"""
        chunks = chunk_by_title(
            filtered_elements,
            combine_text_under_n_chars=combine_text_under_n_chars,
            max_characters=max_characters,
            new_after_n_chars=new_after_n_chars
        )
        return chunks
    
    def combine_chunks_and_tables(self, chunks, table_elements):
        """Combine text chunks with table elements"""
        total_chunks = chunks + table_elements
        return total_chunks
    
    def categorize_elements(self, total_chunks):
        """Categorize elements into text and table types"""
        categorized_elements = []
        
        for element in total_chunks:
            if "unstructured.documents.elements.Table" in str(type(element)):
                categorized_elements.append(Element(type="table", text=str(element)))
            elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
                categorized_elements.append(Element(type="text", text=str(element)))
        
        # Separate by type
        table_elements = [e for e in categorized_elements if e.type == "table"]
        text_elements = [e for e in categorized_elements if e.type == "text"]
        
        return categorized_elements, table_elements, text_elements
    
    def setup_summarization_chain(self):
        """Setup summarization chain for text and tables"""
        if not self.model:
            raise ValueError("Groq API key required for summarization")
            
        prompt_text = """You are an assistant tasked with summarizing tables and text. \
Give a concise summary of the table or text. Table or text chunk: {element} """
        
        prompt = ChatPromptTemplate.from_template(prompt_text)
        summarize_chain = {"element": lambda x: x} | prompt | self.model | StrOutputParser()
        return summarize_chain
    
    def summarize_elements(self, table_elements, text_elements):
        """Summarize table and text elements"""
        summarize_chain = self.setup_summarization_chain()
        
        # Summarize tables
        tables = [i.text for i in table_elements]
        table_summaries = summarize_chain.batch(tables, {"max_concurrency": 1})
        
        # Summarize texts
        texts = [i.text for i in text_elements]
        text_summaries = summarize_chain.batch(texts, {"max_concurrency": 1})
        
        return table_summaries, text_summaries, tables, texts