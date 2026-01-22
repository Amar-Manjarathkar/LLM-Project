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

import json
from src.cleaning.cleaner import IntelCleaner
from src.models.engine import IntelligenceEngine

# Sample Data
samples = [
    "আগামীকাল কলকাতায় দুর্গapuja উৎসব শুরু হবে। সবাই খুব উত্সাহিত।",
    "मुंबईत आज महागाईविरोधात भव्य मोर्चा काढण्यात येणार आहे. पोलिसांनी बंदोबस्त वाढवला आहे.",
    "ਬੀ.ਐਸ.ਐਫ. ਨੇ ਅੰਮ੍ਰਿਤਸਰ ਸਰਹੱਦ ਨੇੜੇ 10 ਕਿਲੋ ਹੈਰੋਇਨ ਬਰਾਮਦ ਕੀਤੀ ਹੈ। ਤਸਕਰ ਪਾਕਿਸਤਾਨ ਵੱਲ ਭੱਜ ਗਏ।"
]

cleaner = IntelCleaner()
engine = IntelligenceEngine(model_name="qwen2.5:7b")

print("="*60)
print("🔎 STARTING MULTI-LINGUAL PIPELINE TEST")
print("="*60)

for i, raw_text in enumerate(samples, 1):
    print(f"\nProcessing Sample #{i}...")
    clean_text = cleaner.process(raw_text)
    
    try:
        report = engine.analyze(clean_text)
        
        # Dump using 'by_alias' to keep the "1_language..." keys
        print(report.model_dump_json(by_alias=True, indent=2))
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Failed: {e}")