from pathlib import Path
import subprocess
import time

def write_executors(folder_path, script='geney.pipelines.dask_utils', input_file='/tamir2/nicolaslynn/data/ClinVar/clinvar_oncosplice_input.txt', output_folder='/tamir2/nicolaslynn/data/oncosplice_base/oncosplice/clinvar_benchmarking', default_logging_path='/tamir2/nicolaslynn/temp/logging'):
    executor_path = Path(folder_path)
    executor_path.mkdir(parents=True, exist_ok=True)
    print(executor_path)
    default_logging_path = Path(default_logging_path)
    job_file_content = f'#!/bin/bash\nhostname\nsource /a/home/cc/students/outside/nicolaslynn/.bashrc\ncd {str(executor_path)}\nsource /tamir2/nicolaslynn/venvs/geney_dask/bin/activate\npython -m {script} -n 750 -m 5GB -i {input_file} -r {output_folder}'
    job_file = executor_path / 'job.sh'
    with open(job_file, 'w') as f:
        _ = f.write(job_file_content)
    submit_file_content = f'qsub -q tamirQ -l nodes=1:ppn=1,cput=24:00:00,mem=25000mb,pmem=25000mb,vmem=50000mb,pvmem=50000mb -e {default_logging_path / "err"} -o {default_logging_path / "out"} {executor_path / "job.sh"}'
    submit_file = executor_path / 'submit'
    with open(submit_file, 'w') as f:
        _ = f.write(submit_file_content)
    subprocess.run(['bash', (executor_path / 'submit')])
    # time.sleep(60)
    # job_file.unlink()
    # submit_file.unlink()
    # executor_path.rmdir()
    return None