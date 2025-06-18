import os
import shutil
import sys
import subprocess

#allow importing all other files
sys.path.append("/ptmp/mpa/ankitad/athenapk")

import replace_input  
import replace_job

def make_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        print("Directory '{}' created successfully.".format(path))
    except Exception as e:
        print("Error creating directory '{}': {}".format(path, e))

def copy_selected_files(src_dir, dest_dir, files_to_copy):
    try:
        for filename in files_to_copy:
            full_src_path = os.path.join(src_dir, filename)
            full_dest_path = os.path.join(dest_dir, filename)
            if os.path.isfile(full_src_path):
                shutil.copy(full_src_path, full_dest_path)
                print("Copied '{}'.".format(filename))
            else:
                print("File '{}' not found in source directory.".format(filename))
    except Exception as e:
        print("Error copying files: {}".format(e))

def replace_tags_in_template(sim_dir, template_filename, output_filename):
    template_path = os.path.join(sim_dir, template_filename)
    output_path = os.path.join(sim_dir, output_filename)

    try:
        with open(template_path, 'r') as f:
            data = f.read()

        updated_data = replace_input.athinput_replace(data)

        with open(output_path, 'w') as f:
            f.write(updated_data)

        print("Input file written to '{}'.".format(output_path))
    except Exception as e:
        print("Error during tag replacement: {}".format(e))

def generate_job_script(sim_dir, template_name, output_name, tag_values):
    job_input = tag_values["job_input"]
    sim_dir = tag_values["sim_dir"]
    inputfile = tag_values["inputfile"]

    template_path = os.path.join(sim_dir, template_name)
    output_path = os.path.join(sim_dir, output_name)

    try:
        with open(template_path, 'r') as f:
            data = f.read()

        updated = replace_job.jobscript_replace(data, job_input, sim_dir, inputfile)

        with open(output_path, 'w') as f:
            f.write(updated)

        print(f"Job script written to '{output_path}'")
    except Exception as e:
        print(f"Error creating job script: {e}")

def submit_job(sim_dir, script_name):
    job_path = os.path.join(sim_dir, script_name)
    try:
        result = subprocess.run(["sbatch", job_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Job submitted successfully.")
        print(result.stdout.decode("utf-8").strip())
        
    except Exception as e:
        print(f"Failed to submit job: {e}")

if __name__ == "__main__":
    new_dir = "/ptmp/mpa/ankitad/athenapk/nc_rst_256_075"
    template_dir = "/ptmp/mpa/ankitad/athenapk/turb_template"

    files_to_copy = [
        "turb_input_ver1.in",
        "input.py",
        "job_input.py",
        "temp_job.sh",
    ]

    make_directory(new_dir)
    copy_selected_files(template_dir, new_dir, files_to_copy)
    replace_tags_in_template(new_dir, "turb_input_ver1.in", "athinput.turb")

    job_input = replace_job.load_job_input(new_dir)
    generate_job_script(
        sim_dir=new_dir,
        template_name="temp_job.sh",
        output_name="created_job_script.sh",
        tag_values={
            "job_input": job_input,
            "sim_dir": new_dir,
            "inputfile": os.path.join(new_dir, "athinput.turb"),
        }
    )

    submit_job(new_dir, "created_job_script.sh")