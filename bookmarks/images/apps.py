from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
        """
        应用的初始化
        """
        # 导入signal处理器
        import images.signals
