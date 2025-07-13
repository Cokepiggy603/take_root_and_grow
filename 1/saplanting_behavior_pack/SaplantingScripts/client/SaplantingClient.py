# -*- coding: utf-8 -*-
from random import random

import mod.client.extraClientApi as clientApi

from .BaseClientSystem import BaseClientSystem
from ..config.heyconfig import ClientSetting
from ..config.sapling import default_saplings
from ..util.common import Singleton
from ..util.listen import Listen

compFactory = clientApi.GetEngineCompFactory()#获取游戏引擎组件工厂
engineName = clientApi.GetEngineNamespace()#获取当前游戏引擎的命名空间
engineSystem = clientApi.GetEngineSystemName()#获取当前游戏引擎的系统名称


class ClientMasterSetting(object):#在这个类的整个进程中只有一个实例
    __metaclass__ = Singleton#该类在此程序的生命周期永远只有一个实例
    wait_time_range = 5 #默认等待时间5秒
    check_time_range = 15   #默认检查时间15秒

    def __init__(self):#构造函数，在第一次实例化时被调用
        self.saplings = default_saplings  #将default_saplings中默认树苗配置存到self.saplings
        self.min_wait_time = 3 #最小等待时间3秒
        self.check_min_wait_time = 15 + self.min_wait_time #检查最小等待时间

    def load_config(self, data):#从外部中加载配置
        if "saplings" in data:#判断saplings列表是否data字典里
            self.saplings = set(tuple(value) for value in data["saplings"])#将saplings列表先转成元组再转集合
        if "min_wait_time" in data:#判断最小等待时间是否在data字典里
            self.min_wait_time = max(0, data["min_wait_time"])#限制下限为0
            self.check_min_wait_time = 15 + self.min_wait_time#基于最小等待时间计算

    def get_wait_time(self):#获取等待时间
        return random() * self.wait_time_range + self.min_wait_time#把随机等待时间区间加上最小等待时间的值返回

    def get_check_wait_time(self):#获取检查等待时间
        return random() * self.check_time_range + self.check_min_wait_time#把随机检查等待时间区间加上最小等待时间的值返回


class SaplantingClient(BaseClientSystem):#SaplantingClient继承父类BaseClientSystem
    def __init__(self, namespace, name):#构造函数，传入namespace和name两个参数，初始化SaplingClient实例
        super(SaplantingClient, self).__init__(namespace, name)#调用SaplantingClient父类构造函数，完成系统注册
        self.game_comp = compFactory.CreateGame(self.levelId)#前面获取到的compFactory创建游戏组件
        self.master_setting = ClientMasterSetting()#取得全局唯一配置单例，并绑定到self.master_setting
        self.item_entities = {}#创建一个空字典
        self.client_setting = ClientSetting()#创建ClientSetting的实例保存到self.client_setting

    @Listen.on("LoadClientAddonScriptsAfter")#当所有客户端脚本加载完毕事件后，会立即触发下面的函数
    def on_enabled(self, event=None):#定义事件回调函数
        self.client_setting.load()#把本地客户端配置文件读取内存中
        comp = clientApi.CreateComponent(self.levelId, "HeyPixel", "Config")#尝试创建一个第三方组件，命名空间HeyPixel，组件名Config
        if comp:#是否创建comp
            from ..config.heyconfig import register_config#从上级目录配置文件导入到register_config 函数
            comp.register_config(register_config)#把本模组的配置描述交给HeyPixel的组件

    @Listen.on("UiInitFinished")#UI初始化完成事件
    def on_local_player_stop_loading(self, event=None):#当本地玩家加载完毕就触发
        self.NotifyToServer("SyncPlayerTreeFallingState", {"playerId": self.playerId, "state": self.client_setting.tree_felling})#向服务器发送一条“一键砍树开关”状态

    def reload_client_setting(self):#定义重新加载客户端设置函数
        self.client_setting.load()#本地配置文件重新读进内存，覆盖当前客户端设置
        self.NotifyToServer("SyncPlayerTreeFallingState", {"playerId": self.playerId, "state": self.client_setting.tree_felling})#把玩家设置“一键砍树开关的状态同步给服务器，实时更新一键砍树开关状态

    @Listen.server("SyncMasterSetting")#当服务器收到"SyncMasterSetting"，即调用下面函数
    def on_sync_master_setting(self, data):#定义回调函数
        self.master_setting.load_config(data)#把字典里的字段直接覆盖到单例属性

    @Listen.on("AddEntityClientEvent")#客户端世界内生成任何实体事件，会触发此方法
    def on_add_sapling_item(self, event):#定义回调哈函数
        # todo 已知event的文档如右侧连接 ：    https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%B8%96%E7%95%8C.html?key=AddEntityClientEvent&docindex=2&type=0
        # todo 已存在 self.master_setting.saplings 为树苗的枚举

        if event["entityId"] in self.item_entities:#判断是否实体
            # 请继续完成此方法的判断
            if event["entityType"] in self.master_setting.saplings:#判断掉落物是否树苗

                entityId = event["id"]#把事件的实体id取出
                self.item_entities[entityId] = entityId#把当前掉落物实体id作为键存入字典self.item_entities
                self.game_comp.AddTimer(self.master_setting.get_check_wait_time(), self.check_on_ground, entityId)#游戏引擎随机延迟，自动调用去判断树苗的掉落物是否已经在地面

    @Listen.on("RemoveEntityClientEvent")#客户端世界内移除任何实体事件，会触发此方法
    def on_remove_entity(self, event):#定义移除实体的函数
        entityId = event["id"]#把删除的实体id取出

        if entityId in self.item_entities:#判断实体id是否在字典里
            self.item_entities.pop(entityId)#将实体从self.item_entities字典中删除

    @Listen.on("OnGroundClientEvent")#实体掉落事件，就会触发下面方法
    def on_sapling_on_ground(self, event):#事件回调
        entityId = event["id"]#取出落地的实体id
        if entityId in self.item_entities:#判断是否是掉落地上的树苗
            self.game_comp.AddTimer(self.master_setting.get_wait_time(), self.on_ground_notify, entityId)#随机等待一会，自动调用on_ground_notify(entityId)去种植实体

    def on_ground_notify(self, entityId):#定义树苗掉落在地面函数
        if entityId in self.item_entities:#判断实体是否在字典里
            itemName, auxValue = self.item_entities[entityId]#按实体id取出赋值给itemName和auxValue
            # print "notify sapling item on ground", entityId
            self.NotifyToServer("onSaplingOnGround", {"playerId": self.playerId, "entityId": entityId, "itemName": itemName, "auxValue": auxValue})#把玩家的树苗已落地的消息实时推给服务器，触发服务器决定做后续处理

    def check_on_ground(self, entityId):#定义检查树苗掉落在地面函数
        if entityId in self.item_entities:#实时判断实体是否已落地
            if compFactory.CreateAttr(entityId).isEntityOnGround():#利用Attr组件实时查询实体是否落地
                self.on_ground_notify(entityId)#实体id的树苗掉落已落地，，立即执行后续处理
            else:
                self.game_comp.AddTimer(self.master_setting.get_check_wait_time(), self.check_on_ground, entityId)#安排一个随机延迟后，再次调用 check_on_ground(entityId)检查树苗掉落物是否已经落地

    def reload_master_setting(self):#定义重载主配置，无额外参数一个实例方法
        self.NotifyToServer("ReloadMasterSetting", {})#通知服务器重新加载并同步全局主配置
