from src.cleaning.cleaner import IntelCleaner

# Simulated noisy intel intercept
raw_data = """
12/10/24, 9:00 pm -  ⚠️ ALERT!!! ⚠️  
Kal raat Pulwama sector (33.8N) me suspicious movement dekhi gayi.  
Check this link: http://bit.ly/secure-comms  <div class="hidden">ignore</div>
"""

cleaner = IntelCleaner()
result = cleaner.process(raw_data)

print("-" * 30)
print("ORIGINAL:")
print(raw_data)
print("-" * 30)
print("CLEANED (Ready for LLM):")
print(result)
print("-" * 30)