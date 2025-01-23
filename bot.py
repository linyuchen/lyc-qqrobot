import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OB11Adapter
from nonebot.adapters.telegram import Adapter as TGAdapter
from nonebot.adapters.github import Adapter as GHAdapter
from src.common.alembic.group_point.script import upgrade_group_point_db

upgrade_group_point_db()

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(OB11Adapter)
driver.register_adapter(TGAdapter)
driver.register_adapter(GHAdapter)

nonebot.load_plugins("src/plugins")

if __name__ == "__main__":
    nonebot.run()
