
# Version 1.0
# import ollama
# from .schemas import IntelReport

# class IntelligenceEngine:
#     def __init__(self, model_name="qwen2.5:7b"):
#         self.model = model_name

#     def analyze(self, cleaned_text: str) -> IntelReport:
#         """
#         Sends cleaned text to Ollama and enforces the Pydantic Schema.
#         """
#         print(f"⚡ Sending to AI ({self.model})...")
        
#         response = ollama.chat(
#             model=self.model,
#             messages=[
#                 {
#                     'role': 'system',
#                     'content': (
#                         "You are a Senior Intelligence Analyst. "
#                         "Analyze the text for Language, Domain, and Entities. "
#                         "CRITICAL: You must include a 'reasoning_trace' explaining your logic first."
#                     )
#                 },
#                 {
#                     'role': 'user',
#                     'content': cleaned_text
#                 }
#             ],
#             # MAGIC LINE: This forces the model to output valid JSON matching our Schema
#             format=IntelReport.model_json_schema(), 
#             options={'temperature': 0.1}  # Low temp = distinct facts, no creativity
#         )

#         # Parse the raw JSON response into our Python Object
#         raw_json = response['message']['content']
#         return IntelReport.model_validate_json(raw_json)

# Version 1.1


# import ollama
# from .schemas import IntelReport

# class IntelligenceEngine:
#     def __init__(self, model_name="qwen2.5:7b"):
#         self.model = model_name

#     def analyze(self, cleaned_text: str) -> IntelReport:
#         print(f"⚡ Sending to AI ({self.model})...")
        
#         system_prompt = (
#             "You are a Precision Intelligence Analyst. "
#             "Analyze the text strictly following this structure:\n"
#             "1. LANGUAGE: Detect the language. If it is Hindi/Urdu written in English script, set 'is_romanized' to true. "
#             "Explain WHY you chose this language.\n"
#             "2. DOMAIN: Classify the text (Terrorism, Politics, Crime, Military). "
#             "Assign a confidence score (0.0-1.0) and explain WHY.\n"
#             "3. ENTITIES: Extract PERSON, LOCATION, ORGANIZATION. "
#             "For each entity, explain your reasoning and assign a confidence score."
#         )

#         response = ollama.chat(
#             model=self.model,
#             messages=[
#                 {'role': 'system', 'content': system_prompt},
#                 {'role': 'user', 'content': cleaned_text}
#             ],
#             format=IntelReport.model_json_schema(), # <--- Enforces the new Atomic Schema
#             options={'temperature': 0.0} # Zero temp = Maximum Logic, Minimum Hallucination
#         )

#         raw_json = response['message']['content']
#         return IntelReport.model_validate_json(raw_json)

# Version 1.2

# import ollama
# from .schemas import IntelReport

# class IntelligenceEngine:
#     def __init__(self, model_name="qwen2.5:7b"):
#         self.model = model_name

#     def analyze(self, cleaned_text: str) -> IntelReport:
#         print(f"⚡ Sending to AI ({self.model})...")
        
#         system_prompt = (
#             "You are a Precision Intelligence Analyst. Output strictly in JSON.\n"
#             "CONSTRAINTS:\n"
#             "1. REASONING: Must be extremely concise (Max 15 words). No fluff.\n"
#             "2. LANGUAGE: If the text uses English letters for Hindi/Urdu words (e.g. 'kal', 'main'), "
#             "set 'is_romanized' to true.\n"
#             "3. ENTITIES: Extract the FULL specific name. "
#             "   - Bad: 'Police', 'Team'\n"
#             "   - Good: 'UP Police', 'Indian Cricket Team'\n"
#             "   - If a specific name is not present, only then use the generic term.\n"
#             "4. CONFIDENCE: Be strict. If the name is generic, confidence should be lower (0.5-0.7)."
#         )

#         response = ollama.chat(
#             model=self.model,
#             messages=[
#                 {'role': 'system', 'content': system_prompt},
#                 {'role': 'user', 'content': cleaned_text}
#             ],
#             format=IntelReport.model_json_schema(), 
#             options={'temperature': 0.0}
#         )

#         raw_json = response['message']['content']
#         return IntelReport.model_validate_json(raw_json)

# Version 1.3

# import ollama
# from .schemas import IntelReport

# class IntelligenceEngine:
#     def __init__(self, model_name="qwen2.5:7b"):
#         self.model = model_name

#     def analyze(self, cleaned_text: str) -> IntelReport:
#         print(f"⚡ Sending to AI ({self.model})...")
        
#         system_prompt = (
#             "You are an Intelligence Analyst. Output strictly in JSON.\n"
#             "GUIDELINES:\n"
#             "1. LANGUAGE: Look for Romanized Hindi/Urdu words like 'hai', 'ki', 'ka', 'mein'. "
#             "   - If present, set 'detected_language' to 'Hindi' or 'Urdu' and 'is_romanized' to true.\n"
#             "2. ORGANIZATIONS: Capture the full specific name. "
#             "   - Example: Capture 'UP Police', NOT just 'Police'.\n"
#             "   - Example: Capture 'Rashtriya Rifles', NOT just 'Rifles'.\n"
#             "3. REASONING: Keep it short (Max 10 words). Use direct facts."
#         )

#         response = ollama.chat(
#             model=self.model,
#             messages=[
#                 {'role': 'system', 'content': system_prompt},
#                 {'role': 'user', 'content': cleaned_text}
#             ],
#             format=IntelReport.model_json_schema(), 
#             options={'temperature': 0.0} 
#         )

#         raw_json = response['message']['content']
#         return IntelReport.model_validate_json(raw_json)

# Version 1.4

# import ollama
# import time
# import psutil
# import os
# import json
# from .schemas import IntelReport, PerformanceDetails

# class IntelligenceEngine:
#     def __init__(self, model_name="qwen2.5:7b"):
#         self.model = model_name
#         # Warmup / Check if model exists
#         try:
#             ollama.show(self.model)
#         except:
#             print(f"⚠️ Model {self.model} not found. Please pull it first.")

#     def _get_system_prompt(self):
#         return """
# You are a Senior Indian Intelligence Analyst. Analyze the text for any of the 22 Indian languages.

# ### ANALYSIS GUIDELINES
# 1. **Language**: Identify if text is Romanized (e.g., 'Bharat mata ki jai').
# 2. **Sentiment**: 'Anti-National' applies if content promotes secession (Azadi), glorifies banned groups (TRF, Hizbul, Maoists), or undermines Indian sovereignty.
# 3. **Domain**: Select ONLY from: [Politics, Military, Extremism in J&K, Terrorism, Crime, Narcotics, Radicalisation, General].
# 4. **Dates**: Use dd/mm/yyyy strictly.

# ### OUTPUT SCHEMA (STRICT JSON)
# You must output a JSON object with keys numbered 1 to 9 exactly as follows:
# {
#     "1_language_detection": { "detected_language": "...", "transliterated": "..." },
#     "2_domain_id": { "domains": ["..."] },
#     "3_ner": { "PERSON": [], "LOCATION": [], "ORGANIZATION": [], "EVENT": [], "PRODUCT": [] },
#     "4_sentiment": "...",
#     "5_event_date": { "dates_found": [{"original_text": "...", "standardized_date": "..."}], "gatherings_participants": [] },
#     "6_country_id": "Indian",
#     "7_relevancy": { "relevant_to": [], "confidence": 0.0, "level": "High/Low" },
#     "8_translation": { "translated_text": "...", "justification": "...", "confidence": 0.0 },
#     "9_summary": "..."
# }
# DO NOT output field "10_performance_metrics", it is calculated externally.
# """

#     def analyze(self, cleaned_text: str) -> IntelReport:
#         # --- 1. Start Performance Metrics ---
#         start_time = time.time()
#         process = psutil.Process(os.getpid())
#         start_cpu = process.cpu_percent(interval=None)
        
#         print(f"⚡ Sending to AI ({self.model})...")

#         # --- 2. Call AI Model ---
#         try:
#             response = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {'role': 'system', 'content': self._get_system_prompt()},
#                     {'role': 'user', 'content': f"Text for analysis: {cleaned_text}"}
#                 ],
#                 format="json", # Force JSON mode
#                 options={'temperature': 0.1} 
#             )
            
#             raw_content = response['message']['content']
            
#             # --- 3. Parse JSON ---
#             try:
#                 data_dict = json.loads(raw_content)
#             except json.JSONDecodeError:
#                 # Fallback if model adds markdown backticks
#                 clean_json = raw_content.replace("```json", "").replace("```", "")
#                 data_dict = json.loads(clean_json)

#             # --- 4. Calculate Metrics ---
#             end_time = time.time()
#             response_time = end_time - start_time
            
#             # Memory & CPU
#             memory_mb = process.memory_info().rss / 1024 / 1024
#             # CPU percent requires a blocking interval or delta; we use a simple snapshot here
#             cpu_usage = psutil.cpu_percent(interval=0.1) 
            
#             # Throughput (approx chars per second processing)
#             throughput = len(cleaned_text) / response_time if response_time > 0 else 0

#             # --- 5. Inject Metrics into Data ---
#             perf_data = {
#                 "response_time_sec": round(response_time, 4),
#                 "throughput_ops_per_sec": round(1 / response_time, 2), # Ops/sec (1 op = 1 request)
#                 "memory_usage_mb": round(memory_mb, 2),
#                 "cpu_utilization_percent": round(cpu_usage, 1)
#             }
            
#             data_dict["10_performance_metrics"] = perf_data

#             # --- 6. Validate & Return ---
#             return IntelReport.model_validate(data_dict)

#         except Exception as e:
#             print(f"❌ Engine Error: {e}")
#             raise e

# Version 1.5

# import ollama
# import time
# import psutil
# import os
# import json
# from .schemas import IntelReport, PerformanceDetails

# class IntelligenceEngine:
#     def __init__(self, model_name="qwen2.5:7b"):
#         self.model = model_name
#         self._ensure_model_exists()

#     def _ensure_model_exists(self):
#         """Checks if model is available, otherwise warns user."""
#         try:
#             ollama.show(self.model)
#         except:
#             print(f"⚠️ Warning: Model '{self.model}' not found in Ollama library.")

#     def get_available_models(self):
#         """Fetches list of available models from Ollama."""
#         try:
#             models_info = ollama.list()
#             # ollama.list() returns a dict with 'models' key which is a list
#             return [m['model'] for m in models_info.get('models', [])]
#         except Exception as e:
#             print(f"❌ Error fetching models: {e}")
#             return []

#     def set_model(self, new_model_name):
#         """Updates the active model."""
#         self.model = new_model_name
#         print(f"🔄 Model switched to: {self.model}")

#     def _get_system_prompt(self):
#         return """
# You are a Senior Indian Intelligence Analyst. Analyze the text for any of the 22 Indian languages.

# ### ANALYSIS GUIDELINES
# 1. **Language**: Identify if text is Romanized (e.g., 'Bharat mata ki jai').
# 2. **Sentiment**: 'Anti-National' applies if content promotes secession (Azadi), glorifies banned groups (TRF, Hizbul, Maoists), or undermines Indian sovereignty.
# 3. **Domain**: Select ONLY from: [Politics, Military, Extremism in J&K, Terrorism, Crime, Narcotics, Radicalisation, General].
# 4. **Dates**: Use dd/mm/yyyy strictly.

# ### OUTPUT SCHEMA (STRICT JSON)
# You must output a JSON object with keys numbered 1 to 9 exactly as follows:
# {
#     "1_language_detection": { "detected_language": "...", "transliterated": "..." },
#     "2_domain_id": { "domains": ["..."] },
#     "3_ner": { "PERSON": [], "LOCATION": [], "ORGANIZATION": [], "EVENT": [], "PRODUCT": [] },
#     "4_sentiment": "...",
#     "5_event_date": { "dates_found": [{"original_text": "...", "standardized_date": "..."}], "gatherings_participants": [] },
#     "6_country_id": "Indian",
#     "7_relevancy": { "relevant_to": [], "confidence": 0.0, "level": "High/Low" },
#     "8_translation": { "translated_text": "...", "justification": "...", "confidence": 0.0 },
#     "9_summary": "..."
# }
# DO NOT output field "10_performance_metrics", it is calculated externally.
# """

#     def analyze(self, cleaned_text: str) -> IntelReport:
#         # --- 1. Start Performance Metrics ---
#         start_time = time.time()
#         process = psutil.Process(os.getpid())
        
#         # --- 2. Call AI Model ---
#         try:
#             response = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {'role': 'system', 'content': self._get_system_prompt()},
#                     {'role': 'user', 'content': f"Text for analysis: {cleaned_text}"}
#                 ],
#                 format="json", 
#                 options={'temperature': 0.1}
#             )
            
#             raw_content = response['message']['content']
            
#             # --- 3. Parse JSON ---
#             try:
#                 data_dict = json.loads(raw_content)
#             except json.JSONDecodeError:
#                 clean_json = raw_content.replace("```json", "").replace("```", "")
#                 data_dict = json.loads(clean_json)

#             # --- 4. Calculate Metrics ---
#             end_time = time.time()
#             response_time = end_time - start_time
            
#             # Memory & CPU snapshot
#             memory_mb = process.memory_info().rss / 1024 / 1024
#             cpu_usage = psutil.cpu_percent(interval=None) 
            
#             # --- 5. Inject Metrics into Data ---
#             perf_data = {
#                 "response_time_sec": round(response_time, 4),
#                 "throughput_ops_per_sec": round(1 / response_time, 2) if response_time > 0 else 0,
#                 "memory_usage_mb": round(memory_mb, 2),
#                 "cpu_utilization_percent": round(cpu_usage, 1)
#             }
            
#             data_dict["10_performance_metrics"] = perf_data

#             # --- 6. Validate & Return ---
#             return IntelReport.model_validate(data_dict)

#         except Exception as e:
#             raise e


# Version 1.6

# import ollama
# import time
# import psutil
# import os
# import json
# from .schemas import IntelReport

# class IntelligenceEngine:
#     def __init__(self, model_name="qwen2.5:7b"):
#         self.model = model_name
#         self._ensure_model_exists()

#     def _ensure_model_exists(self):
#         try:
#             ollama.show(self.model)
#         except:
#             print(f"⚠️ Warning: Model '{self.model}' not found in Ollama library.")

#     def get_available_models(self):
#         try:
#             models_info = ollama.list()
#             return [m['model'] for m in models_info.get('models', [])]
#         except:
#             return []

#     def set_model(self, new_model_name):
#         self.model = new_model_name

#     # --- PROMPT PHASE 1: EXTRACTION (Low Compute) ---
#     def _get_phase1_prompt(self):
#         return """
# You are an expert Data Extraction Engine. Extract structured data from the text.
# OUTPUT JSON ONLY.

# TASKS:
# 1. Language: Detect native language. If Romanized Hindi, label 'Roman_Hindi'.
# 2. Domain: Choose top 3 from [Politics, Military, Extremism in J&K, Terrorism, Crime, Narcotics, Radicalisation, Law & Order, LWE].
# 3. NER: Extract PERSON, LOCATION, ORGANIZATION, EVENT.
# 5. Dates: Extract events and map to dd/mm/yyyy.
# 6. Country: 'Indian' or specific neighbor.

# REQUIRED JSON FORMAT:
# {
#   "1_language_detection": { "detected_language": "...", "transliterated": "..." },
#   "2_domain_id": { "domains": [] },
#   "3_ner": { "PERSON": [], "LOCATION": [], "ORGANIZATION": [], "EVENT": [], "PRODUCT": [] },
#   "5_event_date": { "dates_found": [{"original_text": "...", "standardized_date": "..."}], "gatherings_participants": [] },
#   "6_country_id": "..."
# }
# """

#     # --- PROMPT PHASE 2: ANALYSIS (High Compute) ---
#     def _get_phase2_prompt(self, phase1_context):
#         return f"""
# You are a Senior Indian Intelligence Analyst. Analyze the text using the extracted context below.
# OUTPUT JSON ONLY.

# CONTEXT FROM PHASE 1:
# {json.dumps(phase1_context)}

# TASKS:
# 4. Sentiment: 'Anti-National' if undermining Indian sovereignty, otherwise Positive/Negative/Neutral.
# 7. Relevancy: Score for Indian Security Context (High/Medium/Low).
# 8. Translation: Translate to English if required.
# 9. Summary: Concise 25% summary.

# REQUIRED JSON FORMAT:
# {{
#   "4_sentiment": "...",
#   "7_relevancy": {{ "relevant_to": [], "confidence": 0.0, "level": "..." }},
#   "8_translation": {{ "translated_text": "...", "justification": "...", "confidence": 0.0 }},
#   "9_summary": "..."
# }}
# """

#     def analyze(self, cleaned_text: str, status_callback=None) -> IntelReport:
#         """
#         Runs the 2-step pipeline.
#         status_callback: A function that accepts a string (e.g., set_status("Thinking..."))
#         """
#         start_time = time.time()
#         process = psutil.Process(os.getpid())

#         # Helper to clean JSON
#         def parse_response(response):
#             content = response['message']['content']
#             content = content.replace("```json", "").replace("```", "").strip()
#             return json.loads(content)

#         try:
#             # --- PHASE 1: Extraction ---
#             if status_callback: status_callback("Thinking... Extracting Entities & Metadata")
            
#             resp1 = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {'role': 'system', 'content': self._get_phase1_prompt()},
#                     {'role': 'user', 'content': cleaned_text}
#                 ],
#                 format="json",
#                 options={'temperature': 0.1}
#             )
#             p1_data = parse_response(resp1)

#             # --- PHASE 2: Analysis ---
#             if status_callback: status_callback("Analyzing... Assessing Sentiment & Threat Level")
            
#             resp2 = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {'role': 'system', 'content': self._get_phase2_prompt(p1_data)},
#                     {'role': 'user', 'content': cleaned_text}
#                 ],
#                 format="json",
#                 options={'temperature': 0.2} # Slightly higher creativity for summary
#             )
#             p2_data = parse_response(resp2)

#             # --- MERGE & METRICS ---
#             if status_callback: status_callback("Finalizing Report...")
            
#             final_data = {**p1_data, **p2_data}

#             end_time = time.time()
#             duration = end_time - start_time
            
#             # Metrics
#             perf_data = {
#                 "response_time_sec": round(duration, 4),
#                 "throughput_ops_per_sec": round(1 / duration, 2) if duration > 0 else 0,
#                 "memory_usage_mb": round(process.memory_info().rss / 1024 / 1024, 2),
#                 "cpu_utilization_percent": round(psutil.cpu_percent(), 1)
#             }
#             final_data["10_performance_metrics"] = perf_data

#             return IntelReport.model_validate(final_data)

#         except Exception as e:
#             raise e

# Version 1.7 # 3 shot strategy #best so far

# import ollama
# import time
# import psutil
# import os
# import json
# from .schemas import IntelReport

# class IntelligenceEngine:
#     def __init__(self, model_name="qwen2.5:7b"):
#         self.model = model_name
#         self._ensure_model_exists()

#     def _ensure_model_exists(self):
#         try:
#             ollama.show(self.model)
#         except:
#             print(f"⚠️ Warning: Model '{self.model}' not found in Ollama library.")

#     def get_available_models(self):
#         try:
#             return [m['model'] for m in ollama.list().get('models', [])]
#         except:
#             return []

#     def set_model(self, new_model_name):
#         self.model = new_model_name

#     # =========================================================================
#     # PHASE 1: UNIVERSAL TRANSLATOR
#     # Goal: Convert ANY noise/language into clean, factual English.
#     # =========================================================================
#     # =========================================================================
#     # PHASE 1: UNIVERSAL TRANSLATOR (HARDENED FOR 22 LANGUAGES)
#     # Goal: Handle specific linguistic bottlenecks for Indian languages.
#     # =========================================================================
#     def _get_translator_prompt(self):
#         return """
# You are a Linguistic Expert specializing in the 22 Official Languages of India.
# Your Task: Translate the input text to accurate, neutral English.

# ### 🛡️ LINGUISTIC GUARDRAILS (APPLY STRICTLY):

# 1.  **Dravidian (Tamil/Telugu/Kannada/Malayalam):**
#     * *Bottleneck:* Agglutination (words glued together).
#     * *Fix:* Decompose compound words before translating (e.g., split "Veettirkul" -> "Veedu" + "Il" -> "Inside House").

# 2.  **Indo-Aryan (Hindi/Marathi/Gujarati/Punjabi/Bengali):**
#     * *Bottleneck:* Gender/Honorific Ambiguity.
#     * *Fix:* If gender is ambiguous, default to neutral "They" or the contextually appropriate noun. Maintain "Tu/Tum/Aap" honorific distinctions in tone.
#     * *Script Fix:* Do NOT confuse Bengali 'Ra' with Assamese 'Ro'.

# 3.  **Perso-Arabic (Urdu/Kashmiri/Sindhi):**
#     * *Bottleneck:* RTL/LTR mixing and "Surkhi" (Headline) confusion.
#     * *Fix:* Ensure numbers (1, 2, 3) and English names remain LTR. Do NOT translate "Surkhi" as "Red Alert"; it means "Headline".

# 4.  **Tibeto-Burman & Low Resource (Manipuri/Bodo/Santali/Dogri):**
#     * *Bottleneck:* Hallucination due to low data.
#     * *Fix:* If unsure, output "[Uncertain Translation]" rather than inventing a meaning.

# 5.  **Code-Mixing (Tanglish/Hinglish):**
#     * *Fix:* Treat Romanized script as valid input. Detect the underlying language phonetically.

# ### OUTPUT FORMAT (JSON ONLY):
# {
#     "detected_language": "Language Name (e.g., Tamil, Urdu, Manipuri)",
#     "script_type": "Native/Romanized",
#     "english_text": "The plain English translation...",
#     "correction_note": "Optional: Note if you fixed a specific bottleneck (e.g., 'Fixed agglutination in Tamil')"
# }
# """

#     # =========================================================================
#     # PHASE 2: UNIVERSAL ANALYST
#     # Goal: Apply Intelligence Standards to the clean English text.
#     # =========================================================================
#     def _get_analyst_prompt(self):
#         return """
# You are a Senior Intelligence Officer. Analyze the following ENGLISH Report.

# ### CRITICAL LOGIC FRAMEWORK:
# 1. **Domain Selection**:
#    - **Military/Terrorism**: ONLY if weapons, soldiers in combat, IEDs, or militants are mentioned.
#    - **Law & Order**: Riots, protests, police actions.
#    - **General**: Weather, civilian accidents (even involving soldiers), stock market, politics.
   
# 2. **Sentiment Analysis**:
#    - **Anti-National**: ONLY if the text explicitly promotes secession, insurrection, or attacks India's sovereignty.
#    - **Negative**: Tragedies, accidents, deaths, economic loss. (Tragedy is NOT Anti-National).
#    - **Neutral**: Factual reporting, weather.

# 3. **Date Standardization**: Convert all dates to 'dd/mm/yyyy'.

# ### OUTPUT SCHEMA (STRICT JSON):
# {
#   "2_domain_id": { "domains": ["Rank 1", "Rank 2", "Rank 3"] },
#   "3_ner": { "PERSON": [], "LOCATION": [], "ORGANIZATION": [], "EVENT": [], "PRODUCT": [] },
#   "4_sentiment": "Positive/Negative/Neutral/Anti-National",
#   "5_event_date": { "dates_found": [{"original_text": "...", "standardized_date": "..."}], "gatherings_participants": [] },
#   "6_country_id": "Indian/Abroad/Neighbor",
#   "7_relevancy": { "relevant_to": ["Topic 1"], "confidence": 0.0, "level": "High/Medium/Low" },
#   "9_summary": "Concise 3-sentence summary of the event."
# }
# """

#     def analyze(self, raw_text: str, status_callback=None) -> IntelReport:
#         start_time = time.time()
#         process = psutil.Process(os.getpid())

#         # JSON Parser with fallback
#         def parse_json(response_obj):
#             try:
#                 content = response_obj['message']['content']
#                 # Strip markdown code blocks if present
#                 clean = content.replace("```json", "").replace("```", "").strip()
#                 return json.loads(clean)
#             except Exception:
#                 return {}

#         try:
#             # --- STEP 1: NORMALIZE (Translate) ---
#             if status_callback: status_callback("Phase 1: Normalizing Data (Translation)...")
            
#             # We use temperature=0.0 to force the model to be boring and factual
#             resp1 = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {'role': 'system', 'content': self._get_translator_prompt()},
#                     {'role': 'user', 'content': raw_text}
#                 ],
#                 format="json",
#                 options={'temperature': 0.0} 
#             )
#             t_data = parse_json(resp1)
            
#             english_content = t_data.get("english_text", raw_text)
#             detected_lang = t_data.get("detected_language", "Unknown")

#             # --- STEP 2: ANALYZE (Intelligence Logic) ---
#             if status_callback: status_callback("Phase 2: Applying Intelligence Framework...")
            
#             # We use temperature=0.2 for slight flexibility in summary, but strict logic
#             resp2 = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {'role': 'system', 'content': self._get_analyst_prompt()},
#                     {'role': 'user', 'content': english_content}
#                 ],
#                 format="json",
#                 options={'temperature': 0.2}
#             )
#             a_data = parse_json(resp2)

#             # --- STEP 3: MERGE & REPORT ---
#             final_data = {
#                 # Map Phase 1 outputs
#                 "1_language_detection": {
#                     "detected_language": detected_lang,
#                     "transliterated": detected_lang # We skip transliteration for speed
#                 },
#                 "8_translation": {
#                     "translated_text": english_content,
#                     "justification": "Normalized for analysis",
#                     "confidence": 1.0
#                 },
#                 # Map Phase 2 outputs
#                 **a_data
#             }

#             # Performance Calculation
#             end_time = time.time()
#             duration = end_time - start_time
            
#             final_data["10_performance_metrics"] = {
#                 "response_time_sec": round(duration, 4),
#                 "throughput_ops_per_sec": round(1 / duration, 2) if duration > 0 else 0,
#                 "memory_usage_mb": round(process.memory_info().rss / 1024 / 1024, 2),
#                 "cpu_utilization_percent": round(psutil.cpu_percent(), 1)
#             }

#             return IntelReport.model_validate(final_data)

#         except Exception as e:
#             # Pass the error up to the UI
#             raise e


# Version 1.9
# import time
# import json
# import psutil
# import ollama
# import os
# from .schemas import IntelReport

# class IntelligenceEngine:
#     def __init__(self, model_name="qwen2.5:32b"):
#         """
#         Initialized with High-RAM Model (32b/70b).
#         """
#         self.model = model_name

#     def _get_master_linguist_prompt(self):
#         """
#         Hybrid Single-Shot Prompt: Combines Deep Linguistics with 9-Step Analytics.
#         """
#         return (
#             "You are a Master Linguist and Senior Indian Intelligence Analyst. "
#             "You support all Indic Languages: [Hindi, Tamil, Telugu, Kannada, Malayalam, Punjabi, Gujarati, Bengali, Odia, Marathi].\n\n"
            
#             "### SYSTEM INSTRUCTIONS\n"
#             "1. **Traceability**: You must return the 'original_input' field exactly as received.\n"
#             "2. **Reasoning**: Perform detailed internal Chain-of-Thought, but only output a short 'reasoning_summary'.\n"
#             "3. **Strict JSON**: Output valid JSON only. No Markdown. No comments.\n\n"
            
#             "### 10-STEP INTELLIGENCE PIPELINE\n\n"
            
#             "1. **Language Detection**: Detect native language. If Romanized (e.g., 'Hum aarahe hai'), identify as 'Roman_<Lang>'.\n"
#             "2. **Domain Identification**: Rank top 3: [Politics, Crime, Military, Terrorism, Radicalisation, Extremism in J&K, Law and Order, Narcotics, Left Wing Extremism]. Use 'General' if unrelated.\n"
#             "3. **NER (Rich Extraction)**: \n"
#             "   - Extract entities in their **ORIGINAL SCRIPT** (e.g., 'ಬೆಂಗಳೂರು', 'ਪੰਜਾਬ').\n"
#             "   - Provide the English transliteration.\n"
#             "   - Format: `{'original': '...', 'english': '...', 'confidence': 0.9}`.\n"
#             "   - Categories: PERSON, LOCATION, ORGANIZATION, EVENT, PRODUCT.\n"
#             "4. **Sentiment**: 'Positive', 'Negative', 'Neutral', or 'Anti-National' (undermining Indian sovereignty).\n"
#             "5. **Event & Date**: Standardize dates to dd/mm/yyyy. List gathering participants.\n"
#             "6. **Country**: 'Indian', 'Abroad', or specific neighbor [Pakistan, China, Bangladesh, Nepal, Sri Lanka, Afghanistan].\n"
#             "7. **Relevancy**: Score 'High 85 and above', 'Medium 50 to 84.9', 'Low 0 to 49.9'. List topics.\n"
#             "8. **Translation**: Translate to English if not already English/General. Justification required.\n"
#             "9. **Summary**: Concise 3-4 sentences (approx 25% length).\n"
#             "10. **Performance**: (System will inject this).\n\n"
            
#             "### JSON OUTPUT KEYS\n"
#             "Ensure keys match exactly: "
#             "'original_input', 'reasoning_summary', '1_language_detection', '2_domain_identification', '3_ner', "
#             "'4_sentiment_analysis', '5_event_date_mapping', '6_country_identification', '7_relevancy', "
#             "'8_translation', '9_summary'."
#         )

#     def analyze(self, cleaned_text: str, status_callback=None) -> IntelReport:
#         """
#         Executes Single-Pass Deep Analysis and injects metrics.
#         """
#         start_time = time.time()
#         process = psutil.Process(os.getpid())
        
#         if status_callback:
#             status_callback(f"🧠 Loading {self.model} for Deep Linguistic Analysis...")

#         try:
#             # 1. AI Inference
#             response = ollama.chat(
#                 model=self.model,
#                 messages=[
#                     {'role': 'system', 'content': self._get_master_linguist_prompt()},
#                     {'role': 'user', 'content': cleaned_text}
#                 ],
#                 format="json", # Forces valid JSON structure
#                 options={
#                     'temperature': 0.1, # Precise extraction
#                     'num_ctx': 8192     # High context for reasoning
#                 }
#             )

#             # 2. Parse AI Output
#             ai_content = response['message']['content']
#             try:
#                 data_dict = json.loads(ai_content)
#             except json.JSONDecodeError:
#                 # Fallback clean-up
#                 clean_json = ai_content.replace("```json", "").replace("```", "").strip()
#                 data_dict = json.loads(clean_json)

#             # 3. Inject System Data (Traceability & Metrics)
#             end_time = time.time()
#             duration = end_time - start_time
            
#             # Force original input to match exactly what we sent (traceability)
#             data_dict["original_input"] = cleaned_text
            
#             perf_metrics = {
#                 "response_time_sec": round(duration, 4),
#                 "throughput_ops_per_sec": round(1 / duration, 2) if duration > 0 else 0.0,
#                 "memory_usage_mb": round(process.memory_info().rss / 1024 / 1024, 2),
#                 "cpu_utilization_percent": round(psutil.cpu_percent(), 1)
#             }
#             data_dict["10_performance_metrics"] = perf_metrics

#             # 4. Validate against Version 1.6 Schema
#             report = IntelReport.model_validate(data_dict)
#             return report

#         except Exception as e:
#             raise RuntimeError(f"Analysis Failed: {str(e)}")


# Version 2.0
import time
import json
import psutil
import ollama
import os
from .schemas import IntelReport

class IntelligenceEngine:
    def __init__(self, model_name="qwen2.5:32b"):
        self.model = model_name

    def _get_master_linguist_prompt(self):
        # We explicitly show the model the target JSON structure
        return (
            "You are a Master Linguist and Senior Indian Intelligence Analyst. "
            "Output VALID JSON ONLY. No markdown. No intro.\n\n"
            
            "### JSON STRUCTURE (STRICTLY FOLLOW THIS SKELETON):\n"
            "{\n"
            '  "original_input": "(Leave blank, system fills this)",\n'
            '  "reasoning_summary": "One sentence logic trace",\n'
            '  "1_language_detection": {\n'
            '      "detected_language": "Hindi/Tamil/etc",\n'
            '      "transliterated": "native script if input was romanized, else null"\n'
            '  },\n'
            '  "2_domain_identification": {\n'
            '      "domains": ["Politics", "Security"]\n'
            '  },\n'
            '  "3_ner": {\n'
            '      "PERSON": [{"original": "NameInNative", "english": "NameInEnglish", "confidence": 0.9}],\n'
            '      "LOCATION": [{"original": "...", "english": "...", "confidence": 0.9}],\n'
            '      "ORGANIZATION": [],\n'
            '      "EVENT": [],\n'
            '      "PRODUCT": []\n'
            '  },\n'
            '  "4_sentiment_analysis": "Negative",\n'
            '  "5_event_date_mapping": {\n'
            '      "events": [{"event": "Brief desc", "date": "dd/mm/yyyy"}],\n'
            '      "gatherings_participants": []\n'
            '  },\n'
            '  "6_country_identification": "Indian",\n'
            '  "7_relevancy": {\n'
            '      "relevant_to": ["UP Politics", "Elections"],\n'
            '      "level": "High 85 and above",\n'
            '      "confidence": 0.9\n'
            '  },\n'
            '  "8_translation": {\n'
            '      "translated_text": "Full English translation here...",\n'
            '      "justification": "Translating Hindi to English",\n'
            '      "confidence": 0.95\n'
            '  },\n'
            '  "9_summary": "Brief summary..."\n'
            "}\n\n"

            "### INSTRUCTIONS\n"
            "1. **NER**: Use 'original' (native script) and 'english' keys.\n"
            "2. **Relevancy Level**: Must be EXACTLY: 'High 85 and above', 'Medium 50 to 84.9', or 'Low 0 to 49.9'.\n"
            "3. **Sentiment**: 'Positive', 'Negative', 'Neutral', 'Anti-National'.\n"
        )

    def analyze(self, cleaned_text: str, status_callback=None) -> IntelReport:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        
        if status_callback:
            status_callback(f"🧠 Loading {self.model} for Deep Linguistic Analysis...")

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self._get_master_linguist_prompt()},
                    {'role': 'user', 'content': cleaned_text}
                ],
                format="json", 
                options={'temperature': 0.1, 'num_ctx': 8192}
            )

            # Parse Output
            ai_content = response['message']['content']
            try:
                data_dict = json.loads(ai_content)
            except json.JSONDecodeError:
                clean_json = ai_content.replace("```json", "").replace("```", "").strip()
                data_dict = json.loads(clean_json)

            # Inject Traceability & Metrics
            end_time = time.time()
            duration = end_time - start_time
            
            data_dict["original_input"] = cleaned_text
            data_dict["10_performance_metrics"] = {
                "response_time_sec": round(duration, 4),
                "throughput_ops_per_sec": round(1 / duration, 2) if duration > 0 else 0.0,
                "memory_usage_mb": round(process.memory_info().rss / 1024 / 1024, 2),
                "cpu_utilization_percent": round(psutil.cpu_percent(), 1)
            }

            return IntelReport.model_validate(data_dict)

        except Exception as e:
            # Detailed error logging helps debug Pydantic issues
            raise RuntimeError(f"Analysis Failed: {str(e)}")