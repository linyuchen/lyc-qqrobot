from enum import StrEnum

from qqsdk.message import FriendMsg, GroupMsg


class CMDPermissions(StrEnum):
    GROUP_ADMIN: str = "群管理"
    SUPER_ADMIN: str = "超级管理员(机器人主人)"

    def __and__(self, other):
        if isinstance(other, CMDPermissions):
            return CMDPermissionGroup() & self & other
        elif isinstance(other, CMDPermissionGroup):
            return other & self
        else:
            raise Exception(f"未知权限类型: {other}")

    def __or__(self, other):
        if isinstance(other, CMDPermissions):
            return CMDPermissionGroup() | self | other
        elif isinstance(other, CMDPermissionGroup):
            return other | self
        else:
            raise Exception(f"未知权限类型: {other}")


class CMDPermissionGroup:
    def __init__(self):
        self.and_permissions: set[CMDPermissions] = set()
        self.or_permissions: set[CMDPermissions] = set()

    def __and__(self, other):
        if isinstance(other, CMDPermissions):
            self.and_permissions.add(other)
        elif isinstance(other, CMDPermissionGroup):
            self.and_permissions |= other.and_permissions
        else:
            raise Exception(f"未知权限类型: {other}")
        return self

    def __or__(self, other):
        if isinstance(other, CMDPermissions):
            self.or_permissions.add(other)
        elif isinstance(other, CMDPermissionGroup):
            self.or_permissions |= other.or_permissions
        else:
            raise Exception(f"未知权限类型: {other}")
        return self


def check_permission(msg: GroupMsg | FriendMsg, permissions: CMDPermissions | CMDPermissionGroup):
    if isinstance(permissions, CMDPermissions):
        permissions = CMDPermissionGroup() & permissions

    # or权限只要有一个满足就行
    for permission in permissions.or_permissions:
        if permission == CMDPermissions.GROUP_ADMIN:
            if isinstance(msg, GroupMsg) and msg.is_from_admin:
                return True
        elif permission == CMDPermissions.SUPER_ADMIN:
            if msg.is_from_super_admin:
                return True
    # or权限没有符合的就检查and权限
    # and权限必须全部满足
    if len(permissions.and_permissions) == 0:
        return False
    for permission in permissions.and_permissions:
        if permission == CMDPermissions.GROUP_ADMIN:
            if not isinstance(msg, GroupMsg):
                return False
            elif not msg.is_from_admin:
                return False
        elif permission == CMDPermissions.SUPER_ADMIN:
            if not msg.is_from_super_admin:
                return False
    return True

