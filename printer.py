import emulation

import os.path
import time
from enum import Enum
if not emulation.active():
    import cups
import logging


if not emulation.active():
    conn = cups.Connection()
logger = logging.getLogger("kb.printer")


class JobStatus(Enum):
    PRINTING = 1
    DONE = 2
    FAILED = 3
    CANCELED = 4
    NEED_MAINTENANCE = 5


class Job:
    """
    Create and start a print job
    """
    def __init__(self, filename):
        if not emulation.active():
            self.filename = os.path.abspath(filename)
            printer = first_printer()
            logger.info("Printing %s on %s", self.filename, printer)
            self.id = conn.printFile(printer, self.filename, 'kivybooth', {})# {'media': "Custom.{}x{}cm".format(width, height)}) 
            self.prev_atts = None
            self.last_progress = None

    def status(self):
        if emulation.active():
            return (JobStatus.DONE, 100)
        else:
            atts = conn.getJobAttributes(self.id, ["job-state", "job-media-progress"])
            if self.prev_atts != atts:
                logger.debug("Job %d changed to %s", self.id, atts)
                self.prev_atts = atts
                self.last_progress = time.time()
            state = atts["job-state"]
            if detect_maintenance_needed():
                return (JobStatus.NEED_MAINTENANCE, atts["job-media-progress"])
            if state == 5:
                return (JobStatus.PRINTING, atts["job-media-progress"])
            elif state == 9:
                return (JobStatus.DONE, 100)
            elif state == 7:
                return (JobStatus.CANCELED, 0)
            elif state == 3:
                return (JobStatus.PRINTING, 0)
            else:
                return (JobStatus.FAILED, 100)

    def cancel(self):
        if not emulation.active() and self.status()[0] == JobStatus.PRINTING:
            conn.cancelJob(self.id)


def first_printer():
    id, _ = next(iter(conn.getPrinters().items()))
    return id

def first_job():
    for id, _ in iter(conn.getJobs().items()):
        atts = conn.getJobAttributes(id, ["job-state", "job-media-progress"])
        state = atts["job-state"]
        if state == 5:
            return id
    return None

def print_image(filename, timeout=300):
    status = None
    job = Job(filename)
    logger.info("Started job with ID {}".format(job.id))
    while(timeout > 0):
        status, progress = job.status()
        if status == JobStatus.DONE:
            return
        time.sleep(1)
        timeout -= 1
    logger.error("Job %d did not finish in expected time", job.id)

def detect_maintenance_needed():
    if not hasattr(detect_maintenance_needed, "prev_atts"):
        detect_maintenance_needed.prev_atts = None
    if not hasattr(detect_maintenance_needed, "last_progress"):
        detect_maintenance_needed.last_progress = time.time()
    id = first_job()
    if id is None:
        return False
    atts = conn.getJobAttributes(id, ["job-state", "job-media-progress"])
    if detect_maintenance_needed.prev_atts != atts:
        logging.debug(f"Maintenance detection: First job (#{id}) status changed to {atts}")
        detect_maintenance_needed.last_progress = time.time()
    detect_maintenance_needed.prev_atts = atts
    return atts["job-state"] == cups.IPP_JOB_PROCESSING and \
        atts["job-media-progress"] < 20 and \
        time.time() - detect_maintenance_needed.last_progress > 20

def cancel_all():
    for id, _ in iter(conn.getJobs().items()):
        conn.cancelJob(id)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=int, required=True, help="which test file to print")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)
    print_image(f"res/kivybooth-test-{args.test}.jpg")
