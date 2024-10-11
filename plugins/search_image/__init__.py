from nonebot.plugin import PluginMetadata
from zhenxun.configs.utils import PluginExtraData, RegisterConfig

__plugin_meta__ = PluginMetadata(
    name="识图",
    description="以图搜图，看破本源",
    usage="""
    识别图片 [二次元图片]
    指令：
        识图 [图片] 
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1-2a2e785",
        menu_type="一些工具",
        configs=[
            RegisterConfig(
                key="MAX_FIND_IMAGE_COUNT",
                value=3,
                help="搜索动漫返回的最大数量",
                default_value=3,
                type=int,
            ),
            RegisterConfig(
                key="API_KEY",
                value=None,
                help="Saucenao的API_KEY，通过 https://saucenao.com/user.php?page=search-api 注册获取",
            ),
        ],
    ).dict(),
)
