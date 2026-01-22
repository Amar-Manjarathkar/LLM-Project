import re
import unicodedata
from cleantext import clean

class IntelCleaner:
    """
    Step 0: Data Cleaning Pipeline for Indian Intelligence Context.
    Handles 'Hinglish', Unicode normalization, and noise reduction.
    """

    def __init__(self):
        # Regex patterns specific to Indian digital intel
        self.patterns = {
            'urls': r'http\S+|www\.\S+',
            'html': r'<.*?>',
            # Matches "12/05/23, 8:41 pm - " WhatsApp style headers
            'whatsapp_meta': r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s', 
            'hashtags': r'[@#]\w+',
            'excess_whitespace': r'\s+'
        }

    def global_clean(self, text: str) -> str:
        """
        Stage 1: Sanitization (Structural Repairs)
        Fixes broken Unicode and removes dangerous artifacts (HTML).
        """
        if not text:
            return ""

        # 1. Unicode Normalization (NFKC)
        # Critical for Devanagari/Urdu scripts to be consistent
        text = unicodedata.normalize('NFKC', text)
        
        # 2. Remove HTML Tags (Noise)
        text = re.sub(self.patterns['html'], ' ', text)
        
        # 3. Remove Metadata/Headers (WhatsApp/Telegram logs)
        text = re.sub(self.patterns['whatsapp_meta'], '', text)
        
        return text

    def temp_clean(self, text: str) -> str:
        """
        Stage 2: Context Prep (LLM Optimization)
        Optimizes text for the Prompt without losing linguistic signal.
        """
        if not text:
            return ""

        # 1. URL Handling: Don't delete, replace with <LINK> token
        # This keeps the context that a link *existed* (often suspicious)
        text = re.sub(self.patterns['urls'], ' <LINK> ', text)

        # 2. Clean-Text Library: "Soft" cleaning
        # lower=False -> Keep Case (Important for NER: 'Apple' vs 'apple')
        # no_numbers=False -> Keep dates/times (Critical for intel)
        # no_emoji=True -> Remove visual noise
        text = clean(
            text, 
            fix_unicode=True, 
            to_ascii=False, # Keep Devanagari/Hindi characters!
            lower=False, 
            no_line_breaks=False,
            no_urls=False, 
            no_emails=False, 
            no_phone_numbers=False,
            no_numbers=False, 
            no_digits=False, 
            no_currency_symbols=False, 
            no_punct=False, 
            no_emoji=True
        )

        # 3. Final Polish: Collapse Whitespace
        # Turns "Hello    World" into "Hello World"
        text = re.sub(self.patterns['excess_whitespace'], ' ', text).strip()
        
        return text

    def process(self, raw_text: str) -> str:
        """Run the full pipeline"""
        step1 = self.global_clean(raw_text)
        final = self.temp_clean(step1)
        return final