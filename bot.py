import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.load_plugins("src/plugins")

if __name__ == "__main__":
    nonebot.run()
