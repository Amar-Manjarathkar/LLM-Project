# Version 1.0

# from src.cleaning.cleaner import IntelCleaner
# from src.models.engine import IntelligenceEngine

# # 1. The Raw Intercept
# raw_data = """
# BREAKING: Kal Pulwama main security forces ne 2 terrorists ko spot kiya. 
# Search operation jaari hai near Main Market. #Kashmir
# """

# # 2. Step 0: Clean
# print("--- STEP 0: CLEANING ---")
# cleaner = IntelCleaner()
# clean_text = cleaner.process(raw_data)
# print(f"Cleaned Text: {clean_text}\n")

# # 3. Step 1: Analyze (The AI)
# print("--- STEP 1: AI INFERENCE ---")
# engine = IntelligenceEngine(model_name="qwen2.5:7b")

# try:
#     report = engine.analyze(clean_text)
    
#     print("\n✅ REPORT GENERATED SUCCESSFULLY")
#     print("=" * 40)
#     print(f"🧠 REASONING: {report.reasoning_trace}")
#     print("-" * 40)
#     print(f"🗣️ LANGUAGE:  {report.detected_language} (Romanized: {report.is_romanized})")
#     print(f"🎯 DOMAIN:    {report.primary_domain}")
#     print(f"📍 LOCATION:  {report.entities.LOCATION}")
#     print(f"👥 PERSON:    {report.entities.PERSON}")
#     print("=" * 40)

# except Exception as e:
#     print(f"❌ ERROR: {e}")

# Version 1.1

# from src.cleaning.cleaner import IntelCleaner
# from src.models.engine import IntelligenceEngine
# import json

# # The same difficult "Hinglish" input
# raw_data = """
# BREAKING: Kal Pulwama main security forces ne 2 terrorists ko spot kiya. 
# Search operation jaari hai near Main Market. #Kashmir
# """

# # Step 0: Clean
# cleaner = IntelCleaner()
# clean_text = cleaner.process(raw_data)

# # Step 1: Analyze
# engine = IntelligenceEngine(model_name="qwen2.5:7b")

# try:
#     report = engine.analyze(clean_text)
    
#     # OUTPUT: Strictly JSON with indentation
#     print("\n" + "="*50)
#     print("FINAL INTELLIGENCE REPORT (STRICT JSON)")
#     print("="*50)
    
#     # We use .model_dump_json() to get the strict schema output
#     print(report.model_dump_json(indent=2))
    
#     print("="*50)

# except Exception as e:
#     print(f"❌ ERROR: {e}")

# Version 1.2

# from src.cleaning.cleaner import IntelCleaner
# from src.models.engine import IntelligenceEngine

# # NEW TEST DATA: Contains specific org ("Rashtriya Rifles") and mixed script
# raw_data = """
# In a major joint operation conducted by the Jammu and Kashmir Police and the Central Reserve Police Force (CRPF) 
# in the early hours of Tuesday, a hideout was busted in the dense forests of Kupwara district. 
# Security forces recovered two AK-47 rifles, five magazines, and a significant amount of ammunition. 
# The operation was launched following specific intelligence inputs regarding the presence of militants in the area.
# """

# cleaner = IntelCleaner()
# clean_text = cleaner.process(raw_data)

# engine = IntelligenceEngine(model_name="qwen2.5:7b")

# try:
#     report = engine.analyze(clean_text)
#     print("\n" + "="*50)
#     print("FINAL INTELLIGENCE REPORT")
#     print("="*50)
#     print(report.model_dump_json(indent=2))
#     print("="*50)
# except Exception as e:
#     print(f"❌ ERROR: {e}")

#Version 1.3

# import json
# from src.cleaning.cleaner import IntelCleaner
# from src.models.engine import IntelligenceEngine

# # Sample Data
# samples = [
#     "আগামীকাল কলকাতায় দুর্গapuja উৎসব শুরু হবে। সবাই খুব উত্সাহিত।",
#     "मुंबईत आज महागाईविरोधात भव्य मोर्चा काढण्यात येणार आहे. पोलिसांनी बंदोबस्त वाढवला आहे.",
#     "ਬੀ.ਐਸ.ਐਫ. ਨੇ ਅੰਮ੍ਰਿਤਸਰ ਸਰਹੱਦ ਨੇੜੇ 10 ਕਿਲੋ ਹੈਰੋਇਨ ਬਰਾਮਦ ਕੀਤੀ ਹੈ। ਤਸਕਰ ਪਾਕਿਸਤਾਨ ਵੱਲ ਭੱਜ ਗਏ।"
# ]

# cleaner = IntelCleaner()
# engine = IntelligenceEngine(model_name="qwen2.5:7b")

# print("="*60)
# print("🔎 STARTING MULTI-LINGUAL PIPELINE TEST")
# print("="*60)

# for i, raw_text in enumerate(samples, 1):
#     print(f"\nProcessing Sample #{i}...")
#     clean_text = cleaner.process(raw_text)
    
#     try:
#         report = engine.analyze(clean_text)
        
#         # Dump using 'by_alias' to keep the "1_language..." keys
#         print(report.model_dump_json(by_alias=True, indent=2))
#         print("-" * 60)
        
#     except Exception as e:
#         print(f"❌ Failed: {e}")

# Version 1.4

# import json
# import time
# import sys
# from src.cleaning.cleaner import IntelCleaner
# from src.models.engine import IntelligenceEngine

# def print_separator():
#     print("-" * 80)

# def select_model(engine):
#     """Interactive menu to select a model."""
#     print("\n🔍 Scanning for available Ollama models...")
#     models = engine.get_available_models()
    
#     if not models:
#         print("❌ No models found! Is Ollama running?")
#         return

#     print(f"\nAvailable Models:")
#     for idx, name in enumerate(models, 1):
#         # Mark the current model
#         marker = "(*)" if name == engine.model else "   "
#         print(f"{idx}. {marker} {name}")
    
#     try:
#         choice = input("\nSelect model number (or Press Enter to cancel): ").strip()
#         if choice.isdigit():
#             idx = int(choice) - 1
#             if 0 <= idx < len(models):
#                 engine.set_model(models[idx])
#             else:
#                 print("⚠️ Invalid number.")
#         else:
#             print("🚫 Selection cancelled.")
#     except Exception as e:
#         print(f"⚠️ Error: {e}")

# def main():
#     # Initialize
#     print("⚙️ Initializing Engine...")
#     cleaner = IntelCleaner()
#     engine = IntelligenceEngine(model_name="qwen2.5:7b") # Default start

#     print_separator()
#     print("🔎 UNIFIED PROMPT ENGINEERING FRAMEWORK - INTERACTIVE TERMINAL")
#     print("Commands:")
#     print("  Type text  -> Analyze content")
#     print("  !model     -> Switch AI Model")
#     print("  !exit      -> Quit")
#     print_separator()

#     while True:
#         # Show current model in prompt
#         user_input = input(f"\n[{engine.model}] ➤ ").strip()

#         if not user_input:
#             continue

#         # --- Handle Commands ---
#         if user_input.lower() == "!exit":
#             print("👋 Exiting framework. Jai Hind.")
#             break
        
#         if user_input.lower() == "!model":
#             select_model(engine)
#             continue

#         # --- Process Input ---
#         print(f"\n⏳ Input submitted. Starting timer...")
#         overall_start = time.time()
        
#         try:
#             # 1. Cleaning Phase
#             print("🧹 Cleaning text...")
#             clean_text = cleaner.process(user_input)
            
#             # 2. Analysis Phase (Engine handles its own internal timer too)
#             print(f"⚡ Sending to AI ({engine.model})...")
#             report = engine.analyze(clean_text)

#             overall_end = time.time()
#             total_time = overall_end - overall_start

#             # 3. Output Display
#             print("\n" + "="*30 + " 📄 INTELLIGENCE REPORT " + "="*30)
            
#             # Pretty print the JSON
#             print(report.model_dump_json(by_alias=True, indent=2))
            
#             print("="*80)
            
#             # 4. Timing Breakdown
#             model_time = report.performance.response_time_sec if report.performance else 0
#             overhead = total_time - model_time
            
#             print(f"⏱️  TIMING REPORT:")
#             print(f"   • AI Inference Time : {model_time:.4f} sec")
#             print(f"   • Pipeline Overhead : {overhead:.4f} sec (Cleaning + Parsing)")
#             print(f"   • TOTAL TIME TAKEN  : {total_time:.4f} sec")
#             print("="*80)

#         except Exception as e:
#             print(f"\n❌ PROCESSING FAILED: {e}")

# if __name__ == "__main__":
#     main()

# Version 1.5

import time
import sys
import threading
import itertools
from src.cleaning.cleaner import IntelCleaner
from src.models.engine import IntelligenceEngine

# --- UI UTILITIES ---

class LoadingSpinner:
    """Runs a spinner and timer in a separate thread to keep UI alive."""
    def __init__(self):
        self.stop_event = threading.Event()
        self.status_message = "Initializing..."
        self.start_time = 0
        self.thread = None

    def _spin(self):
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        while not self.stop_event.is_set():
            elapsed = time.time() - self.start_time
            sys.stdout.write(f"\r{next(spinner)} [{elapsed:.1f}s] {self.status_message}   ")
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self.stop_event.clear()
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()

    def update_status(self, msg):
        """Updates the text next to the spinner"""
        self.status_message = msg

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        sys.stdout.write("\r" + " "*60 + "\r") # Clear line
        sys.stdout.flush()

# --- MAIN LOGIC ---

def select_model(engine):
    print("\n🔍 Scanning for available Ollama models...")
    models = engine.get_available_models()
    if not models:
        print("❌ No models found!")
        return
    
    print(f"\nAvailable Models:")
    for idx, name in enumerate(models, 1):
        marker = "(*)" if name == engine.model else "   "
        print(f"{idx}. {marker} {name}")
    
    choice = input("\nSelect model number (Enter to cancel): ").strip()
    if choice.isdigit() and 0 < int(choice) <= len(models):
        engine.set_model(models[int(choice)-1])
    else:
        print("🚫 Cancelled.")

def main():
    print("⚙️  Initializing Engine...")
    cleaner = IntelCleaner()
    # Ensure qwen2.5:7b is pulled, or fallback to what you have
    engine = IntelligenceEngine(model_name="qwen2.5:7b") 
    
    print("-" * 80)
    print("🔎 UNIFIED PROMPT FRAMEWORK - INTERACTIVE CONSOLE")
    print("Commands: Type text to analyze | !model to switch | !exit to quit")
    print("-" * 80)

    spinner_ui = LoadingSpinner()

    while True:
        user_input = input(f"\n[{engine.model}] ➤ ").strip()
        
        if not user_input: continue
        if user_input.lower() == "!exit": break
        if user_input.lower() == "!model": 
            select_model(engine)
            continue

        # --- PROCESS ---
        report = None
        error = None

        # Wrapper to run engine in thread
        def run_analysis():
            nonlocal report, error
            try:
                # We pass the spinner's update method as a callback
                report = engine.analyze(
                    clean_text, 
                    status_callback=spinner_ui.update_status
                )
            except Exception as e:
                error = e

        try:
            # 1. Cleaning
            print("🧹 Cleaning text...")
            clean_text = cleaner.process(user_input)

            # 2. AI Inference (Threaded)
            spinner_ui.start()
            analysis_thread = threading.Thread(target=run_analysis)
            analysis_thread.start()
            analysis_thread.join() # Wait for it to finish
            spinner_ui.stop()

            # 3. Result Display
            if error:
                print(f"❌ ERROR: {error}")
            elif report:
                print("\n" + "="*30 + " 📄 INTELLIGENCE REPORT " + "="*30)
                print(report.model_dump_json(by_alias=True, indent=2))
                print("="*80)
                
                # Timing
                perf = report.performance
                print(f"⏱️  TIMING: AI Inference: {perf.response_time_sec}s | Memory: {perf.memory_usage_mb}MB")
                print("="*80)

        except KeyboardInterrupt:
            spinner_ui.stop()
            print("\n🚫 Operation Interrupted.")

if __name__ == "__main__":
    main()