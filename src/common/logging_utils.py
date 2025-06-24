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

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
         logging.Formatter(
              fmt="{asctime} {levelname} {name} {message}",
              style="{",
              datefmt="%Y-%m-%d %H:%M:%S",
         )
    )
    
    logger = logging.getLogger("root")
    logger.setLevel(logging.DEBUG) # Must set loggers base level, can reduce with handler
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)