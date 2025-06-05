def build_few_shot_prompt(user_text: str) -> str:
    return f"""You are an expert in detecting the document format and business intent.

Classify the following message into:
 Format: [PDF, JSON, Email]
 Intent: [RFQ, Complaint, Invoice, Regulation, Fraud Risk]

Examples:

Message: "Please send a quotation for 200 power adapters."
Format: Email
Intent: RFQ

Message: "The attached invoice has incorrect tax values."
Format: Email
Intent: Complaint

Message: {{
  "sender": "system",
  "type": "alert",
  "message": "High fraud risk detected on account 3095"
}}
Format: JSON
Intent: Fraud Risk

Message: "Please find attached the invoice for this month’s services totaling $11,800."
Format: PDF
Intent: Invoice

Message: "{user_text}"
Format:"""

