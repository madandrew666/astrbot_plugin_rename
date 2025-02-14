from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import sp
from astrbot.api.message_components import At

@register("rename", "黑色灵魂石（空）", "重命名插件，用于更改AI眼中用户的名称", "1.0.0")
class RenamePlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        # 持久化存储，使用 sp 接口加载数据（数据存储为 list，转换为 set 便于处理）
        self.id_name_list = dict(sp.get('id_name_list', []))

    def persist(self):
        """将当前禁用数据持久化保存"""
        sp.put('id_name_list', dict(self.id_name_list))

    def replace_name(self, event: AstrMessageEvent):
        """    """
        qq = str(event.get_sender_id())
        if qq in self.id_name_list.keys():
            event.message_obj.sender.user_id=self.id_name_list[qq]
            return True
        return False

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def filter_replace_name(self, event: AstrMessageEvent):
        """
        全局事件过滤器：
        在消息发送给LLM之前替换用户昵称为已存储名称
        """
        self.replace_name(event)

    @filter.command("rename")
    async def rename_user(self, event: AstrMessageEvent):
        """        """
        sender_id = str(event.get_sender_id())
        newname = event.message_obj.message_str
        if not newname:
            yield event.plain_result("请在 /rename 后输入新名称")
            return

        self.id_name_list[sender_id]=newname
        self.persist()
        yield event.plain_result(f"已更新{sender_id}的昵称为{newname}")


    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("rename-help")
    async def ban_help(self, event: AstrMessageEvent):
        """
        管理员专用命令：显示该插件所有命令列表及功能说明。
        格式：/ban-help
        """
        help_text = (
            "【rename_plugin 插件命令帮助】\n"
            "1. /rename xxx：将此账号的昵称永久更改为xxx\n"
        )
        yield event.plain_result(help_text)

