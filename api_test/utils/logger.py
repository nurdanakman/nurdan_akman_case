import logging

# Configure logging
logging.basicConfig(
    filename="reports/logs/api_test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_logger():
    return logging.getLogger(__name__)