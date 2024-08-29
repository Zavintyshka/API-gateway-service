from logging import getLogger, FileHandler, StreamHandler, Formatter, INFO

fastapi_logger = getLogger("flask_logger")
fastapi_logger.setLevel(INFO)

output_formatter = Formatter("%(asctime)s - [%(levelname)s] - %(message)s")

console_handler = StreamHandler()
user_file_handler = FileHandler("./logs/user_logs.log")

console_handler.setFormatter(output_formatter)
user_file_handler.setFormatter(output_formatter)

fastapi_logger.addHandler(console_handler)
fastapi_logger.addHandler(user_file_handler)
