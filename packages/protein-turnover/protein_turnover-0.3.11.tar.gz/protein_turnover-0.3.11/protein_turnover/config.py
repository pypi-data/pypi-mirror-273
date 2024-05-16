from __future__ import annotations

from sys import byteorder

# change this to cache bust
VERSION = 1

EXT = "parquet"
PEPXML = f".pep-v{VERSION}.{EXT}"
PROTXML = f".prot-v{VERSION}.{EXT}"
MZMAP = f".{byteorder}-v{VERSION}.mzi"
DINOSAUR = f".features-v{VERSION}.{EXT}"
MZML = f".mzml-v{VERSION}.{EXT}"
EICS = f".eics-v{VERSION}.{EXT}"
RESULT_EXT = ".sqlite"  # {EXT}"  # f".v{VERSION}.{EXT}"


MIN_RT = 2
ABUNDANCE_CUTOFF = 0.01
# split jobs into this many spectra
# set to zero to not split
NSPECTRA = 10000
# quadrature limit for estimating area under curve (unused now)
QUAD_LIMIT = 500
# https://docs.python.org/3/library/logging.html#logrecord-attributes
LOG_FORMAT = "%(levelname)s|[%(asctime)s]|%(process)d| %(message)s"

XCMS_STEP = 0.0
PEPXML_CHUNKS = 1000

# also group on retention_time_sec
GROUP_RT = False

dpi = 96
FIGSIZE = (1056.0 / dpi, 768.0 / dpi)

MAIL_SUBJECT = "turnover pipeline"
# default "from" sender
MAIL_TURNOVER = "turnover-pipeline@uwa.edu.au"
# set to None or 'none' to stop any emailing
MAIL_SERVER = "antivirus.uwa.edu.au"

# e.g. "https://protein-turnover.plantenergy.org/inspect/{jobid}"
INSPECT_URL = None
MAIL_TEXT = """Protein Turnover Job "{job.job_name}" has <b>finished</b>!{url}."""
# set to True for production version (hides debug click commands)
PRODUCTION = True
INTERPOLATE_INTENSITY = True

# Dinosaur
JAVA_PATH = "java"
DINOSAUR_JAR = None
