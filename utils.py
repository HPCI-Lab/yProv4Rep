
import hashlib
import os
import json
import pathlib

def compute_sha256_from_file(file_path):
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_output_files_list(prov_file): 
    with open(prov_file, 'r') as f:
        provenance = json.load(f)
    all_entities = provenance.get("entity")

    outputs = []
    for entity in all_entities: 
        if isinstance(all_entities[entity], dict): 
            if all_entities[entity].get("yProv4ML:role", None) == "output": 
                outputs.append(all_entities[entity])
        elif isinstance(all_entities[entity], list):
            for e in all_entities[entity]: 
                if e.get("yProv4ML:role", None) == "output": 
                    outputs.append(e)
        else: 
            raise NotImplemented 
        
    return outputs

def find_provenance_file_in_artifact_directory(directory_path: str): 
    provenance_path = None
    for f in os.listdir(directory_path): 
        if f.endswith(".json"): 
            provenance_path = os.path.join(directory_path, f)
            break
    
    if provenance_path is None: 
        raise Exception("Provenance file not found")
    return provenance_path

def hash_output_files(outputs): 
    for output in outputs: 
        path = output.get("yProv4ML:path", None)
        label = output.get("yProv4ML:label", None)
        if path and label: 
            if pathlib.Path(path).is_file() and not path.endswith(".zarr"): 
                h = compute_sha256_from_file(path)
                print("Done for ", label)
                output["yProv4ML:hash"] = h
    return outputs

def check_hashes(original_outputs, reproduced_outputs): 
    for o_output in original_outputs: 
        o_lbl = o_output.get("yProv4ML:label", None)
        if o_lbl is not None: 
            for r_output in reproduced_outputs: 
                r_lbl = r_output.get("yProv4ML:label", None)
                if o_lbl == r_lbl: 
                    o_hash = o_output.get("yProv4ML:hash", None)
                    r_hash = r_output.get("yProv4ML:hash", None)
                    
                    print("Checked: ", o_lbl, "\nHashes:\n", o_hash, "\n", r_hash)
                    if o_hash != r_hash: 
                        print("Error on: ", o_lbl)
                        return False
                    
    return True