import re
import json

raw_input = "{sender: help@retailbiz.org,message: I don't understand the breakdown in our last bill. Can someone explain the extra charges?,customer_id: R8842}"

# Step 1: Add quotes around keys and string values
def fix_to_json(s):
    s = re.sub(r'([{,]\s*)(\w+)\s*:', r'\1"\2":', s)  # keys
    s = re.sub(r':\s*([^",{}]+)', r': "\1"', s)       # values (if not already quoted)
    return s

fixed_json_str = fix_to_json(raw_input)
parsed = json.loads(fixed_json_str)

print(parsed)
