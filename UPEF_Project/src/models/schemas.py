# Version 1.0


# from typing import List, Optional
# from pydantic import BaseModel, Field

# class DomainRank(BaseModel):
#     domain: str = Field(..., description="The category (e.g., Terrorism, Politics, Crime)")
#     confidence: str = Field(..., description="High, Medium, or Low")

# class NERData(BaseModel):
#     PERSON: List[str] = Field(default_factory=list)
#     LOCATION: List[str] = Field(default_factory=list)
#     ORGANIZATION: List[str] = Field(default_factory=list)
#     EVENT: List[str] = Field(default_factory=list)

# class IntelReport(BaseModel):
#     """
#     The Strict Structure for our Intelligence Report.
#     """
#     # Chain of Thought: The model must explain 'why' before deciding
#     reasoning_trace: str = Field(..., description="Step-by-step logic for the classification.")
    
#     # Task 1: Language ID
#     detected_language: str = Field(..., description="e.g. Hindi, English, Roman_Urdu")
#     is_romanized: bool = Field(..., description="True if script is Latin but language is Indic")
    
#     # Task 2: Domain Classification
#     primary_domain: str = Field(..., description="The most relevant domain")
#     domain_ranking: List[DomainRank]
    
#     # Task 3: NER
#     entities: NERData

#Version 1.1

# from typing import List, Literal
# from pydantic import BaseModel, Field

# # --- Base Block for Scored Outputs ---
# class AnalysisBlock(BaseModel):
#     value: str = Field(..., description="The main classification result")
#     confidence: float = Field(..., description="Score between 0.0 and 1.0")
#     reasoning: str = Field(..., description="Specific logic for this single decision")

# # --- Specific Blocks ---
# class LanguageAnalysis(AnalysisBlock):
#     is_romanized: bool = Field(..., description="True if the text uses English/Latin script for Hindi/Urdu")

# class EntityItem(BaseModel):
#     text: str = Field(..., description="The extracted entity text")
#     label: Literal["PERSON", "LOCATION", "ORGANIZATION", "EVENT", "OTHER"]
#     confidence: float
#     reasoning: str = Field(..., description="Why is this an entity?")

# # --- The Master Report ---
# class IntelReport(BaseModel):
#     language: LanguageAnalysis
#     domain: AnalysisBlock
#     entities: List[EntityItem]

#Version 1.2

# from typing import List, Literal
# from pydantic import BaseModel, Field

# # --- 1. Language Schema ---
# class LanguageResult(BaseModel):
#     detected_language: str = Field(..., description="The name of the language (e.g. Hindi, English, Urdu)")
#     is_romanized: bool = Field(..., description="True if Hindi/Urdu words are written in English script (e.g., 'kal', 'hai')")
#     confidence: float = Field(..., description="0.0 to 1.0")
#     reasoning: str = Field(..., description="Brief explanation")

# # --- 2. Domain Schema ---
# class DomainResult(BaseModel):
#     category: str = Field(..., description="Main category: Terrorism, Politics, Crime, Military, Cyber")
#     confidence: float = Field(..., description="0.0 to 1.0")
#     reasoning: str = Field(..., description="Brief explanation")

# # --- 3. Entity Schema ---
# class EntityItem(BaseModel):
#     text: str = Field(..., description="The exact entity text found in the input")
#     label: Literal["PERSON", "LOCATION", "ORGANIZATION", "EVENT", "OTHER"]
#     confidence: float
#     reasoning: str

# # --- Master Report ---
# class IntelReport(BaseModel):
#     language: LanguageResult
#     domain: DomainResult
#     entities: List[EntityItem]

# Version 1.3

from typing import List, Optional, Any
from pydantic import BaseModel, Field

# --- Sub-Models ---

class LanguageDetails(BaseModel):
    detected_language: str
    transliterated: Optional[str] = None

class DomainDetails(BaseModel):
    domains: List[str]

class NerDetails(BaseModel):
    PERSON: List[str] = []
    LOCATION: List[str] = []
    ORGANIZATION: List[str] = []
    EVENT: List[str] = []
    PRODUCT: List[str] = []

class DateDetails(BaseModel):
    original_text: str
    standardized_date: str

class EventDateDetails(BaseModel):
    dates_found: List[DateDetails] = []
    gatherings_participants: List[str] = []

class RelevancyDetails(BaseModel):
    relevant_to: List[str]
    confidence: float
    level: str

class TranslationDetails(BaseModel):
    translated_text: Optional[str] = None
    justification: str
    confidence: float

class PerformanceDetails(BaseModel):
    response_time_sec: float
    throughput_ops_per_sec: float
    memory_usage_mb: float
    cpu_utilization_percent: float

# --- Master Report Schema ---

class IntelReport(BaseModel):
    # We use 'alias' to map the JSON keys (1_...) to Python variables
    language: LanguageDetails = Field(..., alias="1_language_detection")
    domain: DomainDetails = Field(..., alias="2_domain_id")
    ner: NerDetails = Field(..., alias="3_ner")
    sentiment: str = Field(..., alias="4_sentiment")
    event_date: EventDateDetails = Field(..., alias="5_event_date")
    country_id: str = Field(default="Indian", alias="6_country_id")
    relevancy: RelevancyDetails = Field(..., alias="7_relevancy")
    translation: TranslationDetails = Field(..., alias="8_translation")
    summary: str = Field(..., alias="9_summary")
    
    # This field is optional in the AI response because Python calculates it
    performance: Optional[PerformanceDetails] = Field(None, alias="10_performance_metrics")

    class Config:
        populate_by_name = True