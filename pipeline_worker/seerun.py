# pipeline_worker/seerun.py - Code Generation Pipeline Logic

import os
import time
import json
from pydantic import BaseModel, Field
import openai
from typing import List, Optional

# --- Pydantic Schema for Incoming Task Data ---

class Attachment(BaseModel):
    name: str
    url: str

class EvaluationRequest(BaseModel):
    # Core identifying fields
    email: str
    secret: str = Field(description="GitHub PAT or similar token.")
    task: str
    round: int
    nonce: str
    
    # Task definition fields
    brief: str = Field(description="The natural language task description.")
    checks: List[str]
    evaluation_url: str = Field(description="URL to post completion status.")
    attachments: List[Attachment]

    # Note: github_repo field removed as Git functionality is no longer needed.

# --- LLM Code Generation (Copilot Equivalent) ---

def _generate_code_from_brief(brief: str, api_key: str) -> Optional[str]:
    """
    Calls the LLM API to generate the requested code based on the brief.
    
    Args:
        brief: The detailed task description.
        api_key: The OpenAI API key.
        
    Returns:
        The generated code as a single string, or None if generation fails.
    """
    try:
        # Initialize client with the API key variable
        openai_client = openai.OpenAI(api_key=api_key) 
    except Exception as e:
        print(f"ERROR: Failed to initialize OpenAI client: {e}")
        return None
        
    system_prompt = (
        "You are an expert software engineer specialized in creating single-file, "
        "production-ready web applications (HTML, React, or Python). "
        "Your task is to generate the COMPLETE, single-file code that fulfills the user's brief. "
        "ALWAYS enclose the code in a single markdown block starting with the correct language identifier "
        "and NEVER include any commentary outside of the markdown block. "
        "Do not use external CSS/JS files. Use Tailwind CSS for styling in HTML/React."
    )
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Task Brief: {brief}\n\nGenerate the complete, single-file solution."}
            ],
            temperature=0.7,
        )
        # Extract the text content
        generated_code = response.choices[0].message.content
        return generated_code
    except Exception as e:
        print(f"ERROR: LLM Generation failed: {e}")
        return None

# --- Main Pipeline Execution (Now simplified to Code Generation only) ---

def run_pipeline(data_dict: dict):
    """
    The main background task execution function. 
    It generates code and logs the result instead of deploying to Git.
    """
    print("--- PIPELINE STARTING ---")
    start_time = time.time()
    
    # 1. Configuration & Key Retrieval
    # Key name is 'vercel' as per user's custom environment variable setup
    llm_api_key = os.environ.get("vercel") 
    
    if not llm_api_key:
        print("FATAL ERROR: 'vercel' environment variable (LLM API Key) not found.")
        print("--- PIPELINE FAILED ---")
        return

    brief = data_dict.get('brief', 'No brief provided.')
    task_id = data_dict.get('task', 'N/A')
    
    print(f"Task ID: {task_id}")
    print(f"Brief: {brief}")
    
    # 2. Code Generation
    print("STATUS: Initiating code generation (Copilot-style LLM call)...")
    generated_code = _generate_code_from_brief(brief, llm_api_key)
    
    if not generated_code:
        print("STATUS: Code generation FAILED.")
        print("--- PIPELINE FAILED ---")
        return

    # 3. Log the Generated Code (Fulfilling the user's request to 'get the generated code as json')
    # We print it clearly so the user sees the output in their Vercel logs.
    
    # We use JSON formatting for clarity in the logs.
    log_output = {
        "task_status": "Code Generated Successfully",
        "task_id": task_id,
        "time_taken_seconds": f"{time.time() - start_time:.2f}",
        # The generated code is included here
        "generated_code_content": generated_code,
    }
    
    print("--- GENERATED CODE OUTPUT ---")
    print(json.dumps(log_output, indent=2))
    print("--- PIPELINE FINISHED ---")
