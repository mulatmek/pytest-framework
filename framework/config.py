from framework.utils.paths_handler import get_project_root

LOG_DIR = get_project_root() / "logs"
LOG_FILE_NAME = "framework.log"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5
DEFAULT_TIMEOUT = 30  # seconds
REPORTS_DIR = get_project_root() / "reports"
