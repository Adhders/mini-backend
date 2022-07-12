from django.db import models


# Create your models here.
class Image(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_image', verbose_name='店铺')
    title = models.CharField(max_length=50, verbose_name='名称')
    format = models.CharField(max_length=10, verbose_name='格式')
    size = models.CharField(null=False, max_length=20, verbose_name='图像尺寸')
    fileSize = models.CharField(max_length=20, verbose_name='图像大小')
    src = models.CharField(max_length=100, verbose_name='链接地址')
    group = models.CharField(max_length=20, verbose_name='分组名称')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_image'
        # admin只使用第一个字段进行排序
        ordering = ['-update_time', '-create_time', 'title']
        verbose_name = '图片详情'
        verbose_name_plural = verbose_name


class Video(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_video', verbose_name='店铺')
    title = models.CharField(max_length=50, verbose_name='名称')
    format = models.CharField(max_length=10, verbose_name='格式')
    size = models.CharField(null=False, max_length=20, verbose_name='视频尺寸')
    fileSize = models.CharField(max_length=20, verbose_name='视频大小')
    playTime = models.CharField(max_length=10, verbose_name='播放时长')
    src = models.CharField(max_length=100, verbose_name='视频地址')
    url = models.CharField(max_length=100, verbose_name='封面地址')
    textarea = models.CharField(max_length=500, verbose_name='视频简介')
    group = models.CharField(max_length=20, verbose_name='分组名称')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")
    class Meta:
        db_table = 'tb_video'
        # admin只使用第一个字段进行排序
        ordering = ['-update_time', '-create_time', 'title']
        verbose_name = '视频详情'
        verbose_name_plural = verbose_name


class Article(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_article', verbose_name='店铺')
    title = models.CharField(max_length=50, verbose_name='名称')
    totalRead = models.IntegerField(verbose_name='阅读量')
    totalLike = models.IntegerField(verbose_name='点赞数')
    review = models.IntegerField(verbose_name='评论数')
    author = models.CharField(max_length=10, verbose_name='作者')
    caption = models.CharField(max_length=100, verbose_name='插图')
    profile = models.CharField(max_length=100, verbose_name='肖像')
    content = models.TextField(verbose_name='文章内容')
    groupList = models.CharField(max_length=80, verbose_name='分组列表')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")
    top = models.BooleanField(default=False, null=True, verbose_name='勾选')
    conceal = models.BooleanField(default=False, null=True, verbose_name='勾选')

    class Meta:
        db_table = 'tb_article'
        verbose_name = '文章详情'
        verbose_name_plural = verbose_name


class Author(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_author', verbose_name='店铺')
    profile = models.CharField(max_length=100, verbose_name='肖像')
    author = models.CharField(max_length=10, verbose_name='作者')
    article = models.IntegerField(verbose_name='文章数', default=0)
    active = models.BooleanField(default=True, verbose_name='激活')
    remark = models.CharField(max_length=100, verbose_name='标签', null=True)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_author'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name


class ArticleGroup(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='article_group',
                              verbose_name='店铺')
    group = models.JSONField(verbose_name='文章分组')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_article_group'
        verbose_name = '文章分组'
        verbose_name_plural = verbose_name


class ImageGroup(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='image_group',
                              verbose_name='店铺')
    group = models.JSONField(max_length=1000, verbose_name='视频分组')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_image_group'
        verbose_name = '图像分组'
        verbose_name_plural = verbose_name


class VideoGroup(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='video_group',
                              verbose_name='店铺')
    group = models.JSONField(verbose_name='图片分组')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_video_group'
        verbose_name = '视频分组'
        verbose_name_plural = verbose_name
