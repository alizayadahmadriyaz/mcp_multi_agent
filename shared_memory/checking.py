from memory import SharedMemory

memory = SharedMemory()

# 1. Write classification result
memory.write(
    entry_id="msg-20250601-001",
    input_source="email",
    format="Email",
    intent="Complaint",
    extracted_fields={"sender": "client@domain.com"},
    trace=["ClassifierAgent → detected Email/Complaint"]
)


# 2. Email Agent adds more info
memory.append_trace("msg-20250601-001", "EmailAgent → tone: angry, urgency: high")
memory.write(
    entry_id="msg-20250601-001",
    input_source="email",
    format="Email",
    intent="Complaint",
    extracted_fields={
        "sender": "client@domain.com",
        "urgency": "high",
        "tone": "angry"
    },
)
memory.update_action("msg-20250601-001", "POST /crm/escalate")
memory.append_trace("msg-20250601-001", "ActionRouter → triggered CRM escalation")

# 4. Read final 

entry=memory.read("msg-20250601-001")
print(entry)