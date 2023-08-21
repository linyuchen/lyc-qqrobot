import datetime
import logging
from pathlib import Path
base_dir = Path(__file__).parent.parent.parent / "logs"
# 创建logger对象
logger = logging.getLogger('robot_plugin')
logger.setLevel(logging.DEBUG)

# 创建一个用于写入error级别日志的handler
error_handler = logging.FileHandler(base_dir / f'error-{datetime.datetime.now().date()}.log', encoding='utf-8')
error_handler.setLevel(logging.ERROR)

# 创建一个用于写入所有级别日志的handler
all_handler = logging.FileHandler(base_dir / 'all.log')
all_handler.setLevel(logging.DEBUG)

# 定义日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 将格式应用到handler
error_handler.setFormatter(formatter)
all_handler.setFormatter(formatter)

# 将handler添加到logger对象中
logger.addHandler(error_handler)
logger.addHandler(all_handler)
