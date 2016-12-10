#coding=UTF8

import os
import sys

import cmdaz
import plugin
import rpg

cur_path = os.path.dirname(__file__) or "."
sys.path.append(cur_path + "/../group_point")
import grouppluginbase

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
rpggame = rpg
game = rpg.RPG

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群游戏：RPG
    """
    def __init__(self):

        self.name = u"group_gamble"
        self.cmdGetState = CMD(u"我的状态")
        self.cmdGetGoods = CMD(u"我的物品")
        self.cmdGetEquip = CMD(u"我的装备")
        self.cmdGetMagic = CMD(u"我的技能")
        self.cmdResurgence = CMD(u"复活")
        self.cmdAttack = CMD(u"攻击", hasParam=True)
        self.cmdAttack2Die = CMD(u"单挑", hasParam=True)
        self.cmdUseGoods = CMD(u"使用物品", hasParam=True)
        self.cmdUseMagic = CMD(u"使用技能", hasParam=True)

        self.cmdPoint2Gold = CMD(u"活跃度兑换金币", hasParam=True)
        self.cmdGold2Point = CMD(u"金币兑换活跃度", hasParam=True)

        self.cmdShop = CMD(u"购买", hasParam=True)
        self.cmdSell = CMD(u"卖掉", hasParam=True)
        self.cmdShopMagic = CMD(u"购买技能", hasParam=True)

        self.cmdShowGoodsList = CMD(u"物品商店")
        self.cmdShowEquipsList = CMD(u"装备商店")
        self.cmdShowMagicList = CMD(u"技能商店")
        self.cmdGetMagic = CMD(u"我的技能")

        self.cmdRank = CMD(u"争霸排名")
        self.cmdLeveling = CMD(u"练级")
        #self.cmdStart = CMD(u"我的状态", hasParam=True)
        self.groupInstances = {} # key groupQQ, value instanvc

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样

    def getGameInstance(self, groupQQ):

        if self.groupInstances.has_key(groupQQ):
            groupPlugin = self.groupInstances[groupQQ]
        else:
            groupPlugin = game()
            self.groupInstances[groupQQ] = groupPlugin

        return groupPlugin

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        groupQQ = msg.group.qq
        member = msg.groupMember

        self.rpg_game = game = self.getGameInstance(groupQQ)

        game.change_current_person(member.qq, member.nick)

        result = ""
        if self.cmdGetState.az(msg.msg):
            result += game.get_state()

        elif self.cmdGetGoods.az(msg.msg):
            result += game.get_knapsacks("g")

        elif self.cmdGetEquip.az(msg.msg):
            result += game.get_knapsacks("e")

        elif self.cmdGetMagic.az(msg.msg):
            result += game.get_knapsacks("m")

        elif self.cmdAttack.az(msg.msg):
            param = self.cmdAttack.get_param_list()[0]
            result += game.attack(param)
 
        elif self.cmdAttack2Die.az(msg.msg):
            param = self.cmdAttack.get_param_list()[0]
            result += game.attack2die(param)

        elif self.cmdResurgence.az(msg.msg):
            result += game.resurgence()
        
        elif self.cmdUseMagic.az(msg.msg):
            param = self.cmdUseMagic.get_original_param()
            result += game.use_magic(param)

        elif self.cmdUseGoods.az(msg.msg):
            param = self.cmdUseGoods.get_original_param()
            result += game.use_goods(param)

        elif self.cmdPoint2Gold.az(msg.msg):
            param = self.cmdPoint2Gold.get_param_list()[0]
            result += self.point2rpg_gold(groupQQ, member.qq, member.nick, param)
        elif self.cmdGold2Point.az(msg.msg):
            param = self.cmdGold2Point.get_param_list()[0]
            result += self.rpg_gold2point(groupQQ, member.qq, member.nick, param)

        elif self.cmdShop.az(msg.msg):
            param = self.cmdShop.get_original_param()
            result += game.shop_goods(param)

        elif self.cmdSell.az(msg.msg):
            param = self.cmdSell.get_original_param()
            result += game.sell_goods(param)

        elif self.cmdShopMagic.az(msg.msg):
            param = self.cmdShopMagic.get_original_param()
            result += game.shop_magic(param)

        elif self.cmdShowGoodsList.az(msg.msg):
            result += game.show_store_goods_list("g")

        elif self.cmdShowEquipsList.az(msg.msg):
            result += game.show_store_goods_list("e")

        elif self.cmdShowMagicList.az(msg.msg):
            result += game.show_store_goods_list("m")

        elif self.cmdRank.az(msg.msg):
            result += game.level_rank()

        elif self.cmdLeveling.az(msg.msg):

            result += game.random_attack2die()

        if result:
            msg.reply(result)
            msg.destroy()


    def point2rpg_gold(self, groupQQ, memberQQ, memberName, gold):
        
        if not gold.isdigit():
            return u"命令有误"
        gold = int(gold)
        group_plugin = grouppluginbase.GroupPluginBase(groupQQ)
        point = group_plugin._get_point(memberQQ)
        need_point = gold * 10 # 需要的活跃度
        if point < need_point:
            return u"【%s】您的%s不足%d，无法兑换！"%(memberName, u"活跃度",need_point)
        self.rpg_game.current_person.attrs[rpggame.gold_str_g] += gold
        point = group_plugin._add_point(memberQQ, memberName, -need_point)
        self.rpg_game.current_person.save()
        return u"【%s】花费了%d %s 兑换了%d %s"%(memberName, need_point,u"活跃度",gold,rpggame.currency_name_str_g)

    def rpg_gold2point(self, groupQQ, memberQQ, memberName, gold):

        group_plugin = grouppluginbase.GroupPluginBase(groupQQ)
        if not gold.isdigit():
            return u"命令有误"
        gold = int(gold)
        if gold > self.rpg_game.current_person.attrs[rpggame.gold_str_g]:
            return u"【%s】的%s不足%d，兑换%s失败"%(memberName, rpggame.currency_name_str_g,gold,u"活跃度")
        point = gold * 8 # 兑换出来的活跃度
        self.rpg_game.current_person.attrs[rpggame.gold_str_g] -= gold
        self.rpg_game.current_person.save()
        group_plugin._add_point(memberQQ, memberName, point)

        return u"【%s】花费了%d%s兑换了%d%s"%(memberName, gold,rpggame.currency_name_str_g,point,u"活跃度")

# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



