import os
import subprocess
import tempfile
import shutil
import threading

from resonate import Resonate
from resonate import Context
from resonate.stores.remote import RemoteStore
from resonate.task_sources.poller import Poller

resonate = Resonate(store=RemoteStore(), task_source=Poller(group="gpu"))


@resonate.register()
def execute(ctx: Context, script_content, script_id):
    """
    Executes given Python script content in a sandboxed environment and saves output to [id].txt

    Args:
        script_content (str): Python code to execute
        script_id (str): Unique identifier for output file
    """
    # Create a temporary directory for sandboxing
    temp_dir = tempfile.mkdtemp()
    output_filename = f"{script_id}.sout"
    errput_filename = f"{script_id}.eout"
    print("executing script...")

    err = None
    output = None
    try:
        # Create script file in temporary directory
        script_path = os.path.join(temp_dir, f"sandboxed_script-{script_id}.py")
        with open(script_path, "w") as f:
            f.write(script_content)

        # Execute script with security measures
        result = subprocess.run(
            ["python", "-I", "-S", script_path],  # Isolated mode with minimal imports
            cwd=temp_dir,  # Contain files in temp directory
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120,  # Prevent infinite loops
            check=True,
        )

        output = result.stdout
        err = result.stderr

    except subprocess.TimeoutExpired:
        err = "Error: Execution timed out after 5 seconds"
    except subprocess.CalledProcessError as e:
        err = f"Error: Process returned {e.returncode}\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
    except Exception as e:
        err = f"Unexpected error: {str(e)}"
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("Done executing")
    print("Writing out results")

    # Write output to result file
    with open(output_filename, "w") as f:
        if output:
            f.write(output)

    with open(errput_filename, "w") as f:
        if err:
            f.write(err)


    print("Done!")
    return output_filename


if __name__ == "__main__":
    print("Running worker")
    threading.Event().wait()
