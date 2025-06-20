import logging
import json

from pathlib import Path

class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_obj = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
            return json.dumps(log_obj)
        
def setup_logging() -> None:
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    log_path = f"{logs_dir}/app.log"

    if logging.getLogger().hasHandlers():
        return

    json_formatter = JsonFormatter()

    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(json_formatter)
    
    logger = logging.getLogger("root")
    logger.setLevel(logging.DEBUG) # Must set loggers base level, can reduce with handler
    logger.addHandler(file_handler)