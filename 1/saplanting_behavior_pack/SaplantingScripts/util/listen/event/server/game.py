# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class AddEntityServerEvent(BaseEvent):
    """服务端侧创建新实体，或实体从存档加载时触发

    - id : str 实体id
    - posX : float 位置x
    - posY : float 位置y
    - posZ : float 位置z
    - dimensionId : int 实体维度
    - isBaby : bool 是否为幼儿
    - engineTypeStr : str 实体类型
    - itemName : str 物品identifier（仅当物品实体时存在该字段）
    - auxValue : int 物品附加值（仅当物品实体时存在该字段）

    """
    pass


class AddServerPlayerEvent(BaseEvent):
    """触发时机：玩家加入时触发该事件。

    - id : str 玩家id
    - isTransfer : bool 是否是切服时进入服务器，仅用于Apollo。如果是True，则表示切服时加入服务器，若是False，则表示登录进入网络游戏
    - isReconnect : bool 是否是断线重连，仅用于Apollo。如果是True，则表示本次登录是断线重连，若是False，则表示本次是正常登录或者转服
    - isPeUser : bool 是否从手机端登录，仅用于Apollo。如果是True，则表示本次登录是从手机端登录，若是False，则表示本次登录是从PC端登录
    - transferParam : str 切服传入参数，仅用于Apollo。调用【TransferToOtherServer】或【TransferToOtherServerById】传入的切服参数
    - uid : int/long 仅用于Apollo，玩家的netease uid，玩家的唯一标识
    - proxyId : int 仅用于Apollo，当前客户端连接的proxy服务器id


    """

    pass


class ChunkAcquireDiscardedServerEvent(BaseEvent):
    """服务端区块即将被卸载时触发

    - dimension : int 区块所在维度
    - chunkPosX : int 区块的x坐标，对应方块X坐标区间为[x * 16, x * 16 + 15]
    - chunkPosZ : int 区块的z坐标，对应方块Z坐标区间为[z * 16, z * 16 + 15]
    - entities : list(str) 随区块卸载而从世界移除的实体id的列表。注意事件触发时已经无法获取到这些实体的信息，仅供脚本资源回收用。
    - blockEntities : list(dict) 随区块卸载而从世界移除的自定义方块实体的坐标的列表，列表元素dict包含posX，posY，posZ三个int表示自定义方块实体的坐标。注意事件触发时已经无法获取到这些方块实体的信息，仅供脚本资源回收用。

    """
    pass


class ChunkGeneratedServerEvent(BaseEvent):
    """触发时机：区块创建完成时触发

    - dimension : int 该区块所在的维度
    - blockEntityData : [{"blockName":str,"posX":int,"posY":int,"posZ":int}...]/None 该区块中的自定义方块实体列表，通常是由自定义特征生成的自定义方块，没有自定义方块实体时该值为None

    """

    pass


class ChunkLoadedServerEvent(BaseEvent):
    """触发时机：服务端区块加载完成时

    - dimension : int 区块所在维度
    - chunkPosX : int 区块的x坐标，对应方块X坐标区间为[x * 16, x * 16 + 15]
    - chunkPosZ : int 区块的z坐标，对应方块Z坐标区间为[z * 16, z * 16 + 15]

    """

    pass


class ClientLoadAddonsFinishServerEvent(BaseEvent):
    """触发时机：客户端mod加载完成时，服务端触发此事件。服务器可以使用此事件，往客户端发送数据给其初始化。

    - playerId : str 玩家id

    """
    pass


class CommandEvent(BaseEvent):
    """玩家请求执行指令时触发

    - entityId : str 玩家ID
    - command : str 指令字符串
    - cancel : bool 是否取消

    该事件是玩家请求执行指令时触发的Hook，该事件不响应命令方块的指令和通过modSDK调用的指令，阻止玩家的该条指令只需要将cancel设置为True
    """
    pass


class DelServerPlayerEvent(BaseEvent):
    """触发时机：删除玩家时触发该事件。

    - id : str 玩家id
    - isTransfer : bool 是否是切服时退出服务器，仅用于Apollo。如果是True，则表示切服时退出服务器；若是False，则表示退出网络游戏
    - uid : int/long 玩家的netease uid，玩家的唯一标识

    玩家离开游戏时，会在PlayerLeftEvent之后触发
    """

    pass


class EntityRemoveEvent(BaseEvent):
    """实体被删除时触发

    - id : str 实体id

    触发情景：实体从场景中被删除，例如：生物死亡，生物被清除 (opens new window)，玩家退出游戏，船/盔甲架被破坏，掉落物/经验球被捡起或清除

    当生物随区块卸载时，不会触发该事件，而是ChunkAcquireDiscardedServerEvent事件

    关于生物的清除：当生物离玩家大于wiki所说的距离，并且还在玩家的模拟距离内时，会被清除。也就是说，如果玩家瞬间传送到远处，原处的生物马上离开了模拟距离，并不会被清除

    玩家退出游戏时，PlayerLeftEvent，EntityRemoveEvent，DelServerPlayerEvent按顺序依次触发
    """
    id = None  # type: str
    """实体id"""


class ExplosionServerEvent(BaseEvent):
    """
    当发生爆炸时触发。

    - blocks : list[[x,y,z,cancel],...] 爆炸涉及到的方块坐标(x,y,z)，cancel是一个bool值
    - victims : list/None 受伤实体id列表，当该爆炸创建者id为None时，victims也为None
    - sourceId : str/None 爆炸创建者id
    - explodePos : list 爆炸位置[x,y,z]
    - dimensionId : int 维度id

    通过设置blocks中cancel的bool值为True可以将该方块的爆炸取消，例如(x,y,z,True)

    某些情况下爆炸创建者id为None，此时受伤实体id列表也为None，比如爬行者所造成的爆炸。
    """

    pass


class LoadServerAddonScriptsAfter(BaseEvent):
    """服务器加载完mod时触发"""

    pass


class NewOnEntityAreaEvent(BaseEvent):
    """触发时机：通过RegisterEntityAOIEvent注册过AOI事件后，当有实体进入或离开注册感应区域时触发该事件。

    - name : str 注册感应区域名称
    - enteredEntities : list[str] 进入该感应区域的实体id列表
    - leftEntities : list[str] 离开该感应区域的实体id列表

    """
    pass


class OnCommandOutputServerEvent(BaseEvent):
    """Command命令执行成功事件

    - command : str 命令名称
    - message : str 命令返回的消息

    """

    pass


class OnContainerFillLoottableServerEvent(BaseEvent):
    """触发时机：随机奖励箱第一次打开根据loottable生成物品时

    - loottable : str 奖励箱子所读取的loottable的json路径
    - playerId : str 打开奖励箱子的玩家的playerId
    - itemList : list 掉落物品列表，每个元素为一个itemDict，格式可参考物品信息字典
    - dirty : bool 默认为False，如果需要修改掉落列表需将该值设为True

    """

    pass


class OnLightningLevelChangeServerEvent(BaseEvent):
    """打雷强度发生改变

    - oldLevel : float 改变前的打雷强度
    - newLevel : float 改变后的打雷强度

    """

    pass


class OnLocalLightningLevelChangeServerEvent(BaseEvent):
    """独立维度天气打雷强度发生改变时触发

    - oldLevel : float 改变前的打雷强度
    - newLevel : float 改变后的打雷强度
    - dimensionId : int 独立天气维度id

    """
    pass


class OnLocalRainLevelChangeServerEvent(BaseEvent):
    """独立维度天气下雨强度发生改变时触发

    - oldLevel : float 改变前的下雨强度
    - newLevel : float 改变后的下雨强度
    - dimensionId : int 独立天气维度id

    """
    pass


class OnRainLevelChangeServerEvent(BaseEvent):
    """下雨强度发生改变

    - oldLevel : float 改变前的下雨强度
    - newLevel : float 改变后的下雨强度

    """
    pass


class OnScriptTickServer(BaseEvent):
    """服务器tick时触发,1秒有30个tick"""

    pass


class PlaceNeteaseStructureFeatureEvent(BaseEvent):
    """触发时机：首次生成地形时，结构特征即将生成时服务端抛出该事件。

    - structureName : str 结构名称
    - x : int 结构坐标最小方块所在的x坐标
    - y : int 结构坐标最小方块所在的y坐标
    - z : int 结构坐标最小方块所在的z坐标
    - biomeType : int 该feature所放置区块的生物群系类型
    - biomeName : str 该feature所放置区块的生物群系名称
    - dimensionId : int 维度id
    - cancel : bool 设置为True时可阻止该结构的放置

    """
    pass


class PlayerIntendLeaveServerEvent(BaseEvent):
    """触发时机：即将删除玩家时触发该事件，此时可以通过各种API获取玩家的当前状态。

    - playerId : str 玩家id

    与【DelServerPlayerEvent】事件不同，此时可以通过各种API获取玩家的当前状态。
    """

    pass


class PlayerJoinMessageEvent(BaseEvent):
    """触发时机：准备显示“xxx加入游戏”的玩家登录提示文字时服务端抛出的事件。

    - id : str 玩家实体id
    - name : str 玩家昵称
    - cancel : bool 是否显示提示文字，允许修改。True：不显示提示
    - message : str 玩家加入游戏的提示文字，允许修改

    """
    pass


class PlayerLeftMessageServerEvent(BaseEvent):
    """触发时机：准备显示“xxx离开游戏”的玩家离开提示文字时服务端抛出的事件。

    - id : str 玩家实体id
    - name : str 玩家昵称
    - cancel : bool 是否显示提示文字，允许修改。True：不显示提示
    - message : str 玩家加入游戏的提示文字，允许修改
    """

    pass


class ServerChatEvent(BaseEvent):
    """玩家发送聊天信息时触发

    - username : str 玩家名称
    - playerId : str 玩家id
    - message : str 玩家发送的聊天消息内容
    - cancel : bool 是否取消这个聊天事件，若取消可以设置为True
    - bChatById : bool 是否把聊天消息发送给指定在线玩家，而不是广播给所有在线玩家，若只发送某些玩家可以设置为True
    - bForbid : bool 是否禁言，仅apollo可用。true：被禁言，玩家聊天会提示“你已被管理员禁言”。
    - toPlayerIds : list(str) 接收聊天消息的玩家id列表，bChatById为True时生效

    """
    username = None  # type: str
    """玩家名称"""
    playerId = None  # type: str
    """玩家id"""
    message = None  # type: str
    """玩家发送的聊天消息内容"""
    cancel = None  # type: bool
    """是否取消这个聊天事件，若取消可以设置为True"""
    bChatById = None  # type: bool
    """是否把聊天消息发送给指定在线玩家，而不是广播给所有在线玩家，若只发送某些玩家可以设置为True"""
    bForbid = None  # type: bool
    """是否禁言，仅apollo可用。true：被禁言，玩家聊天会提示“你已被管理员禁言”。"""
    toPlayerIds = None  # type: list[str]
    """接收聊天消息的玩家id列表，bChatById为True时生效"""


class ServerPostBlockPatternEvent(BaseEvent):
    """触发时机：用方块组合生成生物，生成生物之后触发该事件。

    - entityId : str 生成生物的id
    - entityGenerated : str 生成生物的名字，如"minecraft:pig"
    - x : int 方块x坐标
    - y : int 方块y坐标
    - z : int 方块z坐标
    - dimensionId : int 维度id

    """

    pass


class ServerPreBlockPatternEvent(BaseEvent):
    """触发时机：用方块组合生成生物，在放置最后一个组成方块时触发该事件。

    - enable : bool 是否允许继续生成。若设为False，可阻止生成生物
    - x : int 方块x坐标
    - y : int 方块y坐标
    - z : int 方块z坐标
    - dimensionId : int 维度id
    - entityWillBeGenerated : str 即将生成生物的名字，如"minecraft:pig"

    """
    pass


class ServerSpawnMobEvent(BaseEvent):
    """游戏内自动生成怪物时触发

    - identifier : str 生成实体的命名空间
    - type : int 生成实体的类型，参考EntityType
    - baby : bool 生成怪物是否是幼年怪
    - x : float 生成实体坐标x
    - y : float 生成实体坐标y
    - z : float 生成实体坐标z
    - dimensionId : int 生成实体的维度，默认值为0（0为主世界，1为地狱，2为末地）
    - realIdentifier : str 生成实体的命名空间，通过MOD API生成的生物在这个参数也能获取到真正的命名空间，而不是以custom开头的
    - cancel : bool 是否取消生成该实体

    """
    pass
