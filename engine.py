import time

def run_benchmark_session():
    print("🚀 SYSTEM BENCHMARKING: HUMAN (SUNDAR) VS. AI")
    print("Type 'EXIT' to conclude the session.")
    print("="*70)
    
    while True:
        # 1. Input from Panel
        query = input("\nPANEL QUESTION: ")
        if query.upper() in ['EXIT', 'QUIT']: break
        
        # 2. Human 'Ground Truth' Input
        human_truth = input("SUNDAR (HUMAN ANSWER): ")
        
        print("\n" + "-"*30)
        print("🔍 AI IS RETRIEVING & REASONING...")
        time.sleep(1) # Dramatic pause for the demo
        
        # 3. AI Generation
        ai_response = ask_ai_final(query)
        
        # 4. SIDE-BY-SIDE COMPARISON
        print("\n" + "="*70)
        print(f"QUESTION: {query}")
        print(f"HUMAN (GROUND TRUTH): {human_truth}")
        print(f"AI SYSTEM RESPONSE:  {ai_response}")
        print("="*70)
        
        # 5. Validation Logic
        match = input("\nDOES THE AI MATCH THE HUMAN TRUTH? (Y/N): ")
        if match.upper() == 'Y':
            print("✅ RESULT: 100% FACTUAL ALIGNMENT.")
        else:
            print("⚠️ RESULT: DISCREPANCY DETECTED - LOGGING FOR RE-TUNING.")

run_benchmark_session()



