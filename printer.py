import emulation

import os.path
import time
from enum import Enum
if not emulation.active():
    import cups


if not emulation.active():
    conn = cups.Connection()


class JobStatus(Enum):
    PRINTING = 1
    DONE = 2
    FAILED = 3

def first_printer():
    id, _ = next(iter(conn.getPrinters().items()))
    print("Using printer {}".format(id))
    return id

def job_status(job_id):
    if emulation.active():
        return (JobStatus.DONE, 100)
    else:
        atts = conn.getJobAttributes(job_id, ["job-state", "job-media-progress"])
        if atts["job-state"] == 5:
            return (JobStatus.PRINTING, atts["job-media-progress"])
        elif atts["job-state"] == 9:
            return (JobStatus.DONE, 100)
        elif atts["job-state"] == 3:
            return (JobStatus.PRINTING, 0)
        return atts
    #jobs = conn.getJobs(which_jobs='all', my_jobs=False, limit=-1, first_job_id=job_id, requested_attributes=[])
    #return jobs

def start_job(filename, width=15, height=10):
    if emulation.active():
        return 0
    else:
        filename = os.path.abspath(filename)
        print("Printing {} in size {}x{}cm".format(filename, width, height))
        return conn.printFile(first_printer(), filename, 'kivybooth', {})# {'media': "Custom.{}x{}cm".format(width, height)}) 

def print_image(filename, timeout=60):
    status = None
    job_id = start_job(filename)
    print("Started job with ID {}".format(job_id))
    while(timeout > 0):
        status, progress = job_status(job_id)
        print("Status for job {} is {} ({}%)".format(job_id, status, progress))
        if status == JobStatus.DONE:
            break
        time.sleep(1)
        timeout -= 1

if __name__ == '__main__':
    print_image("res/kivybooth-test.jpg")
