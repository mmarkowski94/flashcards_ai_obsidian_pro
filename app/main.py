import logging.config

from app.logging_setup import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
	setup_logging()


if __name__ == "__main__":
	main()
