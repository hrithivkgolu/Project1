import openai
import os
import shutil
import tempfile
from git import Repo, GitCommandError
from typing import Dict, Any
from pydantic import BaseModel

class Attachment(BaseModel):
    name: str
    url: str

class EvaluationRequest(BaseModel):
    email: str
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    checks: list[str]
    evaluation_url: str
    attachments: list[Attachment]



# --- Configuration ---
CODE_FILENAME = "index.html"
TEMP_REPO_DIR_PREFIX = "llm_code_repo_"
LLM_MODEL = "gpt-4o-mini" # Using an equivalent fast model for "Copilot" generation

# --- Phase 2: Code Generation (Copilot Equivalent) ---

def _generate_code_from_brief(brief: str, api_key: str) -> str | None:
    """
    Calls the LLM (acting as the Copilot engine) to generate code.
    
    Args:
        brief: The detailed task prompt.
        api_key: The LLM API key passed from the calling function.
    """
    try:
        # Initialize the client using the passed variable (api_key)
        openai_client = openai.OpenAI(api_key=api_key)
    except Exception:
        print("Generation failed: LLM client could not be initialized with the provided key.")
        return None
        
    system_prompt = (
        "You are an expert, minimalist software engineer. Your task is to generate ONLY the raw code content. "
        "Do not include any surrounding markdown formatting (e.g., ```html or ```) or explanations. "
        "Generate the complete, runnable code for the following request, including all HTML, Tailwind CSS, and JavaScript "
        "in a single index.html file. Load Tailwind via the CDN script tag."
    )
    
    try:
        response = openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": brief}
            ],
            temperature=0.2,
            max_tokens=3000
        )
        
        generated_code = response.choices[0].message.content.strip()
        
        # Post-clean: Remove any stubborn markdown wrappers (```...```)
        if generated_code.startswith("```"):
            lines = generated_code.split('\n')
            if len(lines) > 2:
                generated_code = '\n'.join(lines[1:-1]).strip()
        
        return generated_code
        
    except Exception as e:
        print(f"--- ERROR: Copilot Generation Failed: {e} ---")
        return None

# --- Phase 3: GitHub Deployment ---

def _deploy_to_github(repo_url: str, token: str, code_content: str, commit_message: str) -> str | None:
    """
    Clones the repository, commits the code, and pushes using the PAT (secret).
    """
    authenticated_url = f"https://{token}@[github.com/](https://github.com/){repo_url}.git"
    temp_dir = tempfile.mkdtemp(prefix=TEMP_REPO_DIR_PREFIX)
    repo = None
    
    try:
        repo = Repo.clone_from(authenticated_url, temp_dir)
        file_path = os.path.join(temp_dir, CODE_FILENAME)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code_content)
        print(f"Code written to {file_path}")
            
        repo.index.add([CODE_FILENAME])
        repo.index.commit(commit_message)
        
        origin = repo.remote(name='origin')
        origin.push() 

        new_commit_sha = repo.head.commit.hexsha
        commit_url = f"[https://github.com/](https://github.com/){repo_url}/commit/{new_commit_sha}"
        
        return commit_url

    except GitCommandError as e:
        print(f"--- ERROR: Git Command Failed: Check PAT scope/permissions ---")
        # Log the standard error for better debugging on the server side
        print(f"Git Error Details: {getattr(e, 'stderr', str(e))}")
        return None
    except Exception as e:
        print(f"--- ERROR: Deployment Failed: {e} ---")
        return None
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temp directory: {temp_dir}")

# --- Orchestration ---

def run_pipeline(data: Dict[str, Any]):
    """
    The main sequence run as a background task.
    """
    print("\n=======================================================")
    print(f"Pipeline START: Task {data.get('task', 'N/A')}")
    
    # 1. Extract and Validate Input
    brief = data.get('brief')
    secret_token = data.get('secret')
    repo_url = data.get('github_repo')
    
    # --------------------------------------------------------------------------------
    # KEY CHANGE HERE: Fetching the key using the variable name 'vercel'
    # --------------------------------------------------------------------------------
    llm_api_key = os.environ.get("vercel") 
    
    if not all([brief, secret_token, repo_url, llm_api_key]):
        print("Pipeline ABORTED: Missing one or more critical components (brief, secret, repo_url, or LLM API Key).")
        # Print a specific hint for debugging
        if not llm_api_key:
            print(f"Debug Hint: The environment variable 'vercel' was not found.")
        print("=======================================================")
        return 

    commit_msg = f"Task {data.get('task')} (Round {data.get('round')}): Generated solution for {brief[:50]}..."

    # 2. PHASE 2: Generate Code (Copilot-Style)
    print(f"Phase 2: Calling Copilot-equivalent LLM...")
    
    # Pass the key variable directly to the generator function
    generated_code = _generate_code_from_brief(brief, llm_api_key)
    
    if not generated_code:
        print("Pipeline ABORTED: LLM failed to return code.")
        print("=======================================================")
        return

    # 3. PHASE 3: Deploy to GitHub
    print("Phase 3: Deploying code to GitHub...")
    commit_url = _deploy_to_github(
        repo_url=repo_url,
        token=secret_token,
        code_content=generated_code,
        commit_message=commit_msg
    )
    
    if commit_url:
        print(f"\n*** SUCCESS: Code pushed to {commit_url} ***")
    else:
        print("\n*** FAILURE: Deployment was unsuccessful. Check logs above. ***")

    print("=======================================================")