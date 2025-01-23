from nonebot import on_type, on
from nonebot.adapters.github import ReleasePublished

on_released = on_type(
    (ReleasePublished,), block=True
)


@on_released.handle()
def _(event: ReleasePublished):
    pass
