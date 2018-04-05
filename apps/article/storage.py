# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/04/05 13:51'

from django.core.files.storage import FileSystemStorage


class ImageStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super().__init__(location, base_url)

    # 重写 _save方法
    def _save(self, name, content):
        import os, time, random
        # 文件扩展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0, 100)
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        # 调用父类方法
        return super()._save(name, content)
