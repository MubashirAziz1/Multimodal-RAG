from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import (
    CompositeElement, Table, Header, Footer, Image, FigureCaption, Formula
)
import os
import glob
import google.generativeai as genai


class DocumentLoader:
    def __init__(self, image_output_dir="/content/"):
        self.image_output_dir = image_output_dir
    
    def load_pdf(self, file_path):
        """Load and partition PDF document into elements"""
        elements = partition_pdf(
            filename=file_path,
            extract_images_in_pdf=True,
            infer_table_structure=True,
            image_output_dir_path=self.image_output_dir,
        )
        return elements
    
    def filter_elements(self, elements):
        """Filter out headers, footers, images, captions, formulas"""
        filtered_elements = [
            el for el in elements 
            if not isinstance(el, (Header, Footer, Image, FigureCaption, Formula, Table))
        ]
        
        table_elements = [
            el for el in elements 
            if "unstructured.documents.elements.Table" in str(type(el))
        ]
        
        return filtered_elements, table_elements
    
    def get_element_stats(self, elements):
        category_counts = {}
        for element in elements:
            category = str(type(element))
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1
        return category_counts
    
    def load_images_from_directory(self, img_dir="/content/figures", api_key=None):
        """Load and process images using Gemini Vision API"""
        if not api_key:
            raise ValueError("Gemini API key is required")
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Get image paths
        image_paths = glob.glob(os.path.join(img_dir, "*.jpg"))
        img_summaries = []
        
        for img_path in image_paths:
            with open(img_path, "rb") as img_file:
                image_data = img_file.read()
            
            # Send image + prompt to Gemini
            response = model.generate_content([
                "Describe the image in detail. Be specific about graphs, such as bar plots.",
                {
                    "mime_type": "image/jpeg",
                    "data": image_data
                }
            ])
            
            # Collect the cleaned text
            summary_text = response.text.strip()
            img_summaries.append(summary_text)
            
            # Save summary to file
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            output_path = os.path.join(img_dir, base_name + ".txt")
            with open(output_path, "w") as out_file:
                out_file.write(summary_text)
        
        return img_summaries