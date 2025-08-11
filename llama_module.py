from llama_cpp import Llama

# Initialize once (adjust model_path to your actual file)
llm = Llama(model_path=r"F:\models\llama2-7b-q4_K_M.bin")

def get_llama_response(email_body: str, bert_message: str) -> str:
    prompt = (
        "You are an expert customer support agent with excellent communication skills. "
        "Write a clear, professional, empathetic, and helpful response email addressing the customer's concern. "
        "Do not repeat the customer's email or analysis; only provide the response text.\n\n"
        "Customer Email:\n"
        f"{email_body}\n\n"
        "Analysis:\n"
        f"{bert_message}\n\n"
        "Response:"
    )
    
    response = llm(prompt=prompt, max_tokens=150)
    return response['choices'][0]['text'].strip()