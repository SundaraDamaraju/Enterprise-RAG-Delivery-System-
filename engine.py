import os
import time
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# ==========================================
# 1. SYSTEM INITIALIZATION (The "Engine")
# ==========================================

# TPM Tip: We use environment variables for security
api_key = os.getenv("GROQ_API_KEY") 

# Load the Manifest (Ensure this filename matches your GitHub exactly)
file_path = "SundarResume.txt" 

if os.path.exists(file_path):
    loader = TextLoader(file_path)
    docs = loader.load()
    
    # Recursive Splitting: Optimized for dense chronological data
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    
    # Vector Infrastructure
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
    print("✅ ENGINE INITIALIZED: Knowledge base is live.")
else:
    print("❌ ERROR: SundarResume.txt not found. Please ensure data manifest is present.")

# ==========================================
# 2. GROUNDED INFERENCE LOGIC
# ==========================================

def ask_ai_final(q):
    # Llama-3-70B via Groq LPU for sub-500ms latency
    llm = ChatGroq(api_key=api_key, model_name="llama3-70b-8192")
    
    # High-Recall Retrieval (k=15)
    docs = vector_db.similarity_search(q, k=15)
    context = "\n\n".join([d.page_content for d in docs])
    
    # Identity-Aware Prompting
    template = """You are the Professional Assistant for Sundara Rao Damaraju. 
    IDENTITY: When the user says "You" or "Your", they are referring to Sundara Rao Damaraju.
    
    INSTRUCTIONS: Use the provided context to answer professionally. 
    If info is missing, say: "I do not have a record of that in my resume."

    Context: {context}
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm
    return chain.invoke({"context": context, "question": q}).content

# ==========================================
# 3. UAT BENCHMARK SESSION (Human vs. AI)
# ==========================================

def run_benchmark_session():
    print("\n🚀 SYSTEM BENCHMARKING: HUMAN (SUNDAR) VS. AI")
    print("Type 'EXIT' to conclude the session.")
    print("-" * 30)
    
    while True:
        query = input("\nPANEL QUESTION: ")
        if query.upper() in ['EXIT', 'QUIT']: break
        
        human_truth = input("SUNDAR (HUMAN ANSWER): ")
        
        print("\n🔍 AI IS RETRIEVING & REASONING...")
        time.sleep(1) # Dramatic pause for the demo
        
        ai_response = ask_ai_final(query)
        
        print("\n" + "="*70)
        print(f"QUESTION: {query}")
        print(f"HUMAN (GROUND TRUTH): {human_truth}")
        print(f"AI SYSTEM RESPONSE:  {ai_response}")
        print("="*70)
        
        match = input("\nDOES THE AI MATCH THE HUMAN TRUTH? (Y/N): ")
        if match.upper() == 'Y':
            print("✅ RESULT: 100% FACTUAL ALIGNMENT.")
        else:
            print("⚠️ RESULT: DISCREPANCY LOGGED.")

if __name__ == "__main__":
    run_benchmark_session()
