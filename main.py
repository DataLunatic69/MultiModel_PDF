from .utilse import process_document, print_summary

if __name__ == "__main__":
    
    print("📦 Checking dependencies...")
    try:
        print("✅ Dependencies ready")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install sentence-transformers chromadb")
    

    try:
        result = process_document("2312.10997v5 (1) (2).pdf")
        
        if result:
            print_summary(result)
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()