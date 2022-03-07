from django.db import models


# Create your models here.
class Goods(models.Model):
    """自定义商品模型类"""
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_goods', verbose_name='店铺')
    spu = models.ForeignKey('goods.SPU', on_delete=models.CASCADE, related_name='all_skus',verbose_name='店铺', null=True)
    sku = models.CharField(max_length=20, verbose_name='商品sku', null=True)
    title = models.CharField(max_length=30, verbose_name='商品名称')
    slogan = models.CharField(max_length=50, verbose_name='标语', null=True)
    goodsType = models.CharField(max_length=5, verbose_name='商品类型')
    sellModelType = models.CharField(max_length=5, verbose_name='销售类型')
    category = models.JSONField(verbose_name="商品类别", null=True)
    price = models.CharField(max_length=10, verbose_name='价格', )
    costPrice = models.CharField(max_length=10, verbose_name='成本价', null=True)
    salesNum = models.IntegerField(verbose_name='销量', default=0)
    sortNum = models.IntegerField(verbose_name='权重', default=0)
    originalPrice = models.CharField(max_length=10, verbose_name='原价', null=True)
    stock = models.IntegerField(verbose_name='库存', default=100)
    isPutAway = models.BooleanField(verbose_name='是否上架', default=True)
    sellUnit = models.CharField(max_length=5, verbose_name='单位', null=True)
    videoUrl = models.CharField(max_length=100, verbose_name='视频封面', null=True)
    videoImage = models.CharField(max_length=100, verbose_name='视频链接', null=True)
    goodsImageUrls = models.JSONField(verbose_name="商品图片", null=True)
    goodsCertificateUrls = models.JSONField(verbose_name="商品资质", null=True)
    defaultImageUrl = models.CharField(max_length=100, verbose_name="商品图片", null=True)
    detail = models.TextField(verbose_name='商品详情', null=True)
    goodsLimitVo = models.JSONField(verbose_name='限量', null=True)
    selectedTag = models.JSONField(verbose_name='商品标签', null=True)
    selectedClassifyList = models.JSONField(verbose_name="商品分组", null=True)
    selectedGoodsAttrList = models.JSONField(verbose_name="商品属性", null=True)
    selectedGoodsPropList = models.JSONField(verbose_name="商品参数", null=True)
    selectedGoodsRightsList = models.JSONField(verbose_name="商品服务", null=True)
    putAwayDate = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    # 模型已经迁移建表,并且表中已经有数据之后,再给表/模型新增字段时,必须给默认值或可以为空,不然迁移就报错
    class Meta:
        db_table = 'tb_goods'
        verbose_name = '商品'
        ordering = ['-sortNum']
        verbose_name_plural = verbose_name


class SPU(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_spus', verbose_name='店铺')
    defaultImageUrl = models.CharField(max_length=100, verbose_name="商品图片", null=True)
    spu = models.CharField(max_length=50, verbose_name='spu编码')
    reviews = models.IntegerField(verbose_name='评论数', default=0)
    sales = models.IntegerField(verbose_name='销量', default=0)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_spu'
        verbose_name = 'spu'
        ordering = ['-sales']
        verbose_name_plural = verbose_name


class GoodsReview(models.Model):
    spu = models.ForeignKey('goods.SPU', on_delete=models.CASCADE, related_name='all_reviews', verbose_name='评论')
    customer = models.ForeignKey('customer.Customer', to_field='openid', on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', to_field='orderNum', on_delete=models.CASCADE, null=True)
    star = models.IntegerField(verbose_name='星数', default=5)
    likes = models.IntegerField(verbose_name='点赞量', default=0)
    reviews = models.IntegerField(verbose_name='评论数', default=0)
    children = models.JSONField(verbose_name='子评论', null=True, default=list)
    name = models.CharField(max_length=50, verbose_name='用户名')
    msg = models.CharField(max_length=250, verbose_name='评论')
    specs = models.CharField(max_length=200, verbose_name='规格')
    avatar = models.CharField(max_length=250, verbose_name='用户头像')
    imgs = models.JSONField(verbose_name="评论图片", null=True)
    additional = models.JSONField(verbose_name="追加评论", null=True)
    videoUrl = models.CharField(max_length=100, verbose_name='视频封面', null=True)
    videoImage = models.CharField(max_length=100, verbose_name='视频链接', null=True)
    anonymous = models.BooleanField(verbose_name="匿名的", default=False)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'tb_goods_review'
        verbose_name = 'tb_goods_review'
        ordering = ['-star']
        verbose_name_plural = verbose_name


class GoodsGroup(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='goods_group',
                              verbose_name='店铺')
    group = models.JSONField(verbose_name='商品分组')
    system_group = models.BooleanField(verbose_name="系统分组", default=True)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_goods_group'
        verbose_name = '商品分组'
        verbose_name_plural = verbose_name


class GoodsTag(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='goods_tag',
                              verbose_name='店铺')
    tags = models.JSONField(verbose_name='商品标签')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_goods_tags'
        verbose_name = '商品标签'
        verbose_name_plural = verbose_name


class GoodsProperty(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='goods_property',
                              verbose_name='店铺')
    property = models.JSONField(verbose_name='商品属性')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_goods_property'
        verbose_name = '商品属性'
        verbose_name_plural = verbose_name
