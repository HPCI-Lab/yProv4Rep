import json
import argparse
import os
import subprocess
import sys
import shlex
import uuid
import pathlib
import shutil

from utils import get_output_files_list, check_hashes, find_provenance_file_in_artifact_directory, hash_output_files

def run_with_dockerfile(command, artifact_dir, tag="crate-experiment"):
    build_cmd = f"docker build -t {tag} . --build-arg artifact_dir={artifact_dir}"
    result = subprocess.run(build_cmd, shell=True)
    if result.returncode != 0:
        print("Error: Docker build failed.")
        sys.exit(1)

    container_name = f"temp_container_{uuid.uuid4().hex[:8]}"
    subprocess.run(f"docker run -dit --name {container_name} -v .:/workspace -w /workspace {tag}", shell=True)
    subprocess.run(f"docker exec {container_name} bash -c {shlex.quote(command)}", shell=True)
    subprocess.run(f"docker cp {container_name}:/workspace/prov ./", shell=True)
    subprocess.run(f"docker rm -f {container_name}", shell=True, check=True)

def main(rocrate_path):
    provenance_path = find_provenance_file_in_artifact_directory(rocrate_path)
    with open(provenance_path, 'r') as f:
        provenance = json.load(f)

    main_activity = provenance.get("activity")
    main_activity = main_activity[list(main_activity.keys())[0]]
    source_code = "/".join(["prov"] + main_activity.get("yProv4ML:source_code", None).split("/")[1:])
    command = main_activity.get("prov-ml:execution_command", None)
    
    provenance_src = main_activity.get("yProv4ML:provenance_path", None)
    # if pathlib.Path(provenance_src).exists(): 
    #     shutil.rmtree(provenance_src)

    if not os.path.exists(source_code):
        print(f"Error: Source code file not found at {source_code}")
        sys.exit(1)

    run_with_dockerfile(command, rocrate_path)

    experiment_name = "_".join(main_activity.get("yProv4ML:experiment_name", None).split("_")[:-2])
    experiment_dir = os.path.join(provenance_src, f"{experiment_name}_0")

    reproduced_provenance_file = find_provenance_file_in_artifact_directory(experiment_dir)
    
    print(provenance_path)
    original_outputs = get_output_files_list(provenance_path)
    original_outputs = hash_output_files(original_outputs)

    print(reproduced_provenance_file)
    reproduced_outputs = get_output_files_list(reproduced_provenance_file)
    reproduced_outputs = hash_output_files(reproduced_outputs)

    result = check_hashes(original_outputs, reproduced_outputs)
    print("✅" if result else "❌")

 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Reproduce an experiment from a Provenance directory or yProv4ML-generated RO-Crate'
    )
    parser.add_argument('--rocrate', type=str, required=True, help='Path to the RO-Crate directory')
    args = parser.parse_args()

    main(args.rocrate)
