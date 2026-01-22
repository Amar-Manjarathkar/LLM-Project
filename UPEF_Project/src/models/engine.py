
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

import ollama
import time
import psutil
import os
import json
from .schemas import IntelReport, PerformanceDetails

class IntelligenceEngine:
    def __init__(self, model_name="qwen2.5:7b"):
        self.model = model_name
        # Warmup / Check if model exists
        try:
            ollama.show(self.model)
        except:
            print(f"⚠️ Model {self.model} not found. Please pull it first.")

    def _get_system_prompt(self):
        return """
You are a Senior Indian Intelligence Analyst. Analyze the text for any of the 22 Indian languages.

### ANALYSIS GUIDELINES
1. **Language**: Identify if text is Romanized (e.g., 'Bharat mata ki jai').
2. **Sentiment**: 'Anti-National' applies if content promotes secession (Azadi), glorifies banned groups (TRF, Hizbul, Maoists), or undermines Indian sovereignty.
3. **Domain**: Select ONLY from: [Politics, Military, Extremism in J&K, Terrorism, Crime, Narcotics, Radicalisation, General].
4. **Dates**: Use dd/mm/yyyy strictly.

### OUTPUT SCHEMA (STRICT JSON)
You must output a JSON object with keys numbered 1 to 9 exactly as follows:
{
    "1_language_detection": { "detected_language": "...", "transliterated": "..." },
    "2_domain_id": { "domains": ["..."] },
    "3_ner": { "PERSON": [], "LOCATION": [], "ORGANIZATION": [], "EVENT": [], "PRODUCT": [] },
    "4_sentiment": "...",
    "5_event_date": { "dates_found": [{"original_text": "...", "standardized_date": "..."}], "gatherings_participants": [] },
    "6_country_id": "Indian",
    "7_relevancy": { "relevant_to": [], "confidence": 0.0, "level": "High/Low" },
    "8_translation": { "translated_text": "...", "justification": "...", "confidence": 0.0 },
    "9_summary": "..."
}
DO NOT output field "10_performance_metrics", it is calculated externally.
"""

    def analyze(self, cleaned_text: str) -> IntelReport:
        # --- 1. Start Performance Metrics ---
        start_time = time.time()
        process = psutil.Process(os.getpid())
        start_cpu = process.cpu_percent(interval=None)
        
        print(f"⚡ Sending to AI ({self.model})...")

        # --- 2. Call AI Model ---
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self._get_system_prompt()},
                    {'role': 'user', 'content': f"Text for analysis: {cleaned_text}"}
                ],
                format="json", # Force JSON mode
                options={'temperature': 0.1} 
            )
            
            raw_content = response['message']['content']
            
            # --- 3. Parse JSON ---
            try:
                data_dict = json.loads(raw_content)
            except json.JSONDecodeError:
                # Fallback if model adds markdown backticks
                clean_json = raw_content.replace("```json", "").replace("```", "")
                data_dict = json.loads(clean_json)

            # --- 4. Calculate Metrics ---
            end_time = time.time()
            response_time = end_time - start_time
            
            # Memory & CPU
            memory_mb = process.memory_info().rss / 1024 / 1024
            # CPU percent requires a blocking interval or delta; we use a simple snapshot here
            cpu_usage = psutil.cpu_percent(interval=0.1) 
            
            # Throughput (approx chars per second processing)
            throughput = len(cleaned_text) / response_time if response_time > 0 else 0

            # --- 5. Inject Metrics into Data ---
            perf_data = {
                "response_time_sec": round(response_time, 4),
                "throughput_ops_per_sec": round(1 / response_time, 2), # Ops/sec (1 op = 1 request)
                "memory_usage_mb": round(memory_mb, 2),
                "cpu_utilization_percent": round(cpu_usage, 1)
            }
            
            data_dict["10_performance_metrics"] = perf_data

            # --- 6. Validate & Return ---
            return IntelReport.model_validate(data_dict)

        except Exception as e:
            print(f"❌ Engine Error: {e}")
            raise e