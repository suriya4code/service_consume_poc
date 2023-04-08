import logging
from constants import MAX_ALLOWED_SIZE

log = logging.getLogger(__name__)

def validate_file_size(contents):
    if len(contents) > MAX_ALLOWED_SIZE:
        log.error("File size larger than 1mb")
        raise Exception("Please upload file less than 1 mb")
    pass

