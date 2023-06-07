from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True, verbose_name="标签", help_text="标签")
    create_time = models.CharField(max_length=255, blank=True, verbose_name="添加时间")
    update_time = models.CharField(max_length=255, blank=True, verbose_name="更新时间")

    class Meta:
        db_table = "blog_tag"
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True, verbose_name="分类", help_text="分类")
    create_time = models.CharField(max_length=255, blank=True, verbose_name="添加时间")
    update_time = models.CharField(max_length=255, blank=True, verbose_name="更新时间")

    class Meta:
        db_table = "blog_category"
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class BlogContent(models.Model):
    content = models.TextField(blank=False, null=False, verbose_name="博文内容", help_text="博文内容，html内容格式")
    create_time = models.CharField(max_length=255, blank=True, verbose_name="添加时间")
    update_time = models.CharField(max_length=255, blank=True, verbose_name="更新时间")

    class Meta:
        db_table = "blog_content"
        verbose_name = '本地编写博文内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.content[:20]}..."


class BlogDownloadContent(models.Model):
    source_site_choice = (
        ("csdn", "csdn"),
    )
    source_site = models.CharField(choices=source_site_choice, max_length=255, blank=False, null=False, verbose_name="原始站点", help_text="原始网站，比如csdn，博客园等描述")
    source_url = models.TextField(blank=False, null=False, verbose_name="原始url地址", help_text="原始url地址")
    local_path = models.TextField(blank=True, null=True, verbose_name="博文本地地址", help_text="从网络下载的博文存放在本机的文件地址")
    create_time = models.CharField(max_length=255, blank=True, verbose_name="添加时间")
    update_time = models.CharField(max_length=255, blank=True, verbose_name="更新时间")

    class Meta:
        db_table = "blog_download_content"
        verbose_name = '网络下载博文内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.local_path}"


class Blog(models.Model):
    blog_from_choice = (
        ("local", "本地编辑"),
        ("internet", "网络下载")
    )

    title = models.CharField(max_length=512, blank=False, null=False, verbose_name="博文标题", help_text="博文标题")
    description = models.TextField(max_length=512, blank=False, null=False, verbose_name="博文简要描述", help_text="博文简要描述")
    blog_from = models.CharField(choices=blog_from_choice, max_length=255, blank=False, null=False, verbose_name="来源", help_text="博客来源：本地/网络")
    categories = models.CharField(max_length=255, blank=False, null=False, verbose_name="分类", help_text="博文分类id，填写分类id，只能属于一个分类，不可多对多")
    tags = models.CharField(max_length=255, blank=False, null=False, verbose_name="标签", help_text="博文标签id，填写标签id，多个id以英文逗号隔开")
    content_id = models.CharField(max_length=255, blank=False, null=False, verbose_name="博文内容id", help_text="博文内容id：BlogContentID或者BlogDownloadContentID")
    create_time = models.CharField(max_length=255, blank=True, verbose_name="添加时间")
    update_time = models.CharField(max_length=255, blank=True, verbose_name="更新时间")

    def category_name(self):
        """ 获取分类名称"""
        return Category.objects.get(pk=self.categories).name

    def tags_name(self):
        """ 获取标签名称"""
        tags = [int(__) for __ in self.tags.split(",")]
        tags_obj = Tag.objects.filter(pk__in=tags)
        tags_name_list = [__.name for __ in tags_obj]
        return tags_name_list

    class Meta:
        db_table = "blog"
        verbose_name = '博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title}"
