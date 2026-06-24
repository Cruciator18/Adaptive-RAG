from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_pdf(file_path: str):
    """
    Loads a PDF and splits it into semantic chunks ready for vectorization.
    """
    print(f"--- LOADING PDF: {file_path} ---")
    
    # 1. Load the PDF using the advanced PyMuPDF loader
    # FIX: Changed 'path=' to 'file_path=' and used the passed variable
    loader = PyMuPDFLoader(file_path=file_path)
    pages = loader.load()
    
    print(f"Successfully loaded {len(pages)} pages.")

    # 2. Initialize the Text Splitter
    # We don't want to split a sentence in half, so we use a recursive splitter.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # The maximum number of characters in a chunk
        chunk_overlap=200,     # How much chunks overlap (prevents cutting a concept in half)
        separators=["\n\n", "\n", ".", " ", ""] # The hierarchy of how to break text
    )
    
    # 3. Perform the chunking
    chunks = text_splitter.split_documents(pages)
    
    print(f"Split the PDF into {len(chunks)} chunks.")
    
    # Optional: Print the first chunk just to verify it looks correct
    if chunks:
        print("\n--- SAMPLE CHUNK (First 200 chars) ---")
        print(f"{chunks[0].page_content[:200]}...")
        print(f"Metadata: {chunks[0].metadata}")
        print("--------------------------------------\n")
        
    return chunks

if __name__ == "__main__":
    # Test the function with a local PDF
    sample_pdf_path = r"C:\adaptive_rag\AI_Interview_Question_Bank.pdf"
    
    try:
        document_chunks = load_and_chunk_pdf(sample_pdf_path)
    except FileNotFoundError:
        print(f"Error: Could not find the file '{sample_pdf_path}'. Please check the path.")