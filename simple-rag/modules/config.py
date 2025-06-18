from pathlib import Path

from experiment_config import capture_config

_config = capture_config()

# Directories
EFS_DIR = "./datasets/pytorch"
ROOT_DIR = Path(__file__).parent.parent.absolute()
DB_CONNECTION_STRING = "dbname=postgres user=postgres host=localhost password=postgres"
