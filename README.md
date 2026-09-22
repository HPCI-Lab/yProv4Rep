# yProv4Rep

yProv4Rep (Reproducible Experiments with Provenance (or yProv4Reproducibility)) is a lightweight reproducibility verification framework that leverages PROV-JSON to ensure the full traceability and deterministic re-execution of computational workflows. It provides a simple way to confirm whether a job can be rerun in a clean Docker environment and yield exactly the same results.
# Overview

This project is designed to automatically verify the reproducibility of a computational job by comparing its execution inside a controlled Docker container with the provenance data previously captured in a PROV-JSON file. The verification process does not just run the script again—it ensures that every artifact generated during execution matches byte-for-byte with the original outputs, validating that the workflow is truly reproducible.

### How It Works
yProv4Reproducibility begins by checking that all input artifacts referenced in the PROV-JSON file are present in the local working directory. It then launches a Docker container configured to mirror the original runtime environment as closely as possible. The job script is executed within this container, with careful monitoring to detect any runtime errors or deviations.

Once the job completes successfully, the framework computes cryptographic hashes (SHA-256) of all output artifacts generated during the re-execution. These hashes are then compared to those listed in the original PROV-JSON file, which acts as the canonical reference. If all hashes match exactly, the job is deemed reproducible.

In the case of mismatch or errors during execution, detailed diagnostics are provided to help users identify where and why reproducibility may have failed—whether due to missing inputs, environment inconsistencies, or nondeterministic behavior in the script.

### Why This Matters
Reproducibility is a foundational principle of scientific computing and data science. yProv4Reproducibility makes it easy to formalize, test, and verify that a workflow can be reliably rerun—either by yourself in the future, or by others reviewing your work. By using standard provenance representations like PROV-JSON, this tool integrates smoothly with broader workflows and supports long-term reproducibility goals.
