import importlib.util
import os

def load_job_input(template_dir):
    job_input_path = os.path.join(template_dir, "job_input.py")
    spec = importlib.util.spec_from_file_location("job_input", job_input_path)
    job_input = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(job_input)
    return job_input

def tag_replace(filedata, tag, value):
    return filedata.replace(tag, str(value))

def jobscript_replace(template_data, job_input, sim_dir, inputfile):
    tag_map = {
        "JOBNAME": job_input.jobname,
        "PARTITION": job_input.partition,
        "GPU_TYPE": job_input.gpu_type,
        "NUM_GPUS": job_input.num_gpus,
        "NODES": job_input.nodes,
        "NTASKS": job_input.ntasks,
        "WALLTIME": job_input.walltime,
        "EXECUTABLE": job_input.executable,
        "INPUTFILE": inputfile,
        "WORKDIR": sim_dir,
    }
    for tag, val in tag_map.items():
        template_data = tag_replace(template_data, f"!!{tag}!!", val)
    return template_data
