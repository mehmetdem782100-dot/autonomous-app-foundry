import os

class DockerSandboxManager:
    def __init__(self):
        pass

    def create_sandbox(self, project_id: str) -> str:
        sandbox_path = f"./sandbox/execution_env/{project_id}"
        os.makedirs(sandbox_path, exist_ok=True)
        return sandbox_path

    def run_code(self, project_id: str, script_name: str) -> dict:
        return {
            "status": "success",
            "stdout": "Kurgusal cikti",
            "stderr": ""
        }
        
    def cleanup_sandbox(self, project_id: str):
        pass
