# llama_module.py

from llama_cpp import Llama
import os

# Change only this path when switching models
MODEL_PATH = r"F:\models\mistral-7b-instruct-v0.2.Q4_K_M.gguf"
# MODEL_PATH = r"F:\models\llama2-7b-q4_K_M.bin"

# Initialize LLaMA/Mistral model once
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,          # Larger context window (default might be too small)
    n_threads=8,         # Adjust to your CPU
    n_batch=512          # Improves speed
)

def get_llama_response(
    subject: str,
    body: str,
    bert_message: str,
    relevant_qa_pairs: list[dict]
) -> str:
    """
     Generate a professional and empathetic customer support response
    using either LLaMA or Mistral based on model file.
    """

    # Build knowledge base context string (limit to first 2 pairs)
    kb_context = ""
    for i, qa in enumerate(relevant_qa_pairs[:2], start=1):
        kb_context += f"Q{i}: {qa['question']}\nA{i}: {qa['answer']}\n\n"

    # Compose the prompt with clear instructions and examples
    instructions = f"""
    You are a professional and empathetic customer support agent.

    Knowledge Base: {kb_context}
    Customer Email Subject: {subject}
    Customer Email Body: {body}
    Customer Sentiment: {bert_message}

    Instructions:
    - Address the customer's issue clearly and specifically.
    - Use polite, empathetic, and professional language.
    - Do NOT mention or refer to the knowledge base explicitly.
    - Do NOT use placeholders such as [Customer], [Agent], or similar.
    - Do NOT repeat the prompt, instructions, or knowledge base.
    - Do NOT include unrelated information, internal notes, or metadata.
    - Do NOT write any code, markdown, or script.
    - Keep your reply concise.
    - If the customer mentions a billing error, apologize and assure quick resolution.
    - If the customer reports a wrong item, acknowledge and promise a fix.
    - If unsure how to help, ask politely for more information.
    - Do not use html codes in the response.

    Begin your customer support email response below (plain text only):
    """
    # Detect if it's Mistral (filename contains 'mistral')
    if "mistral" in os.path.basename(MODEL_PATH).lower():
        prompt = f"[INST]{instructions}[/INST]"
        temperature = 0.5  # Mistral performs well around 0.4–0.6
    else:
        prompt = instructions
        temperature = 0.25  # LLaMA2 was tuned to be more deterministic

    # Query model
    response = llm(
        prompt=prompt,
        max_tokens=800,
        temperature=temperature,
        stop=["\n\nInstructions:", "###"]
    )

    return response['choices'][0]['text'].strip()
    