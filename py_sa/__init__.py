def submit_aegea_job(cmd, expected_output, rdb=None, alocation=None, verbose=False):
    """
    Submit the cmd to aegea, capture the jobID, and store the jobID at ~/aegea_logs.txt

    v1.0 - 1/26/21

    aegea 2.6.9
    """
    from datetime import datetime
    import subprocess

    if alocation is None:
        alocation = '/home/mattolm/.aegea_logs.txt'

    # 1) Check it output already exists
    if check_s3_file(result):
        if verbose:
            print(f"{result} already exists")
        return None

    # 2) Check if job is already running

    # Get list of running jobs
    if rdb is None:
        rdb = load_running_aegea(verbose=False)
    running_jobs = set(rdb[rdb['job_status'].isin(['RUNNING', 'RUNNABLE', 'STARTING'])]['job_ID'].tolist())
    if verbose:
        print(f"{len(running_jobs)} jobs are running")

    # Get output -> job key
    adb = pd.read_csv(alocation, sep='\t', names=['job_ID', 'output', 'time', 'cmd'])
    cdb = adb[adb['output'] == expected_output]
    if len(cdb) > 0:
        db = cdb[cdb['job_ID'].isin(running_jobs)]
    else:
        db = pd.DataFrame()
    if verbose:
        print(
            f"Captured {len(adb)} aegea logs, {len(running_jobs)} running jobs, {len(cdb)} previous attempts, {len(db)} currently running attempts")

    if len(db) > 0:
        if verbose:
            print(f"{expected_output} is currently running (job={db['job_ID'].tolist()})")
        return None

    # 3) Run job
    out = subprocess.check_output(cmd, shell=True, text=True)
    ID = eval(out)['jobId']

    # 4) Store job ID
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    with open(alocation, 'a') as o:
        o.write(f"\n{ID}\t{expected_output}\t{dt_string}\t{cmd}")

    # 5) Finish
    if verbose:
        print(f"Job {ID} is launched to create {expected_output}")
    return ID


def load_running_aegea(queue="novome_spot", tries=20, verbose=True):
    """
    Return a list of running aegea jobs

    v1.2 - 10/11/21
    * If no queue is specified, dont do a queue

    v1.1 - 3/15/21
    * Better printing of status while running showq

    v1.0 - 1/26/21

    aegea 2.6.9
    """
    import subprocess
    print("Running showq...")
    if queue != "":
        cmd = f"aegea batch ls --queue {queue}"
    else:
        cmd = f"aegea batch ls"
    while tries >= 0:
        try:

            raw_out = subprocess.check_output(cmd, shell=True, text=True)
            break
        except:
            # print(f"showq failed for {queue}, try # {tries}")
            tries = tries - 1
    print("Showq succeeded")

    table = {'job_ID': [], 'job_status': [], 'image': []}
    lines = len(raw_out.split('\n'))
    for j, line in enumerate(raw_out.split('\n')):
        # Skip header
        if j >= 3:

            lw = line.strip().split('│')

            # Skip weird lines
            if len(lw) != 14:
                continue

            table['job_ID'].append(lw[1].strip())
            table['job_status'].append(lw[4].strip())
            table['image'].append(lw[8].strip())

    db = pd.DataFrame(table)

    if verbose:
        print(f"{len(db[db['job_status'] == 'RUNNING'])} aegea jobs are currently running")

    return db