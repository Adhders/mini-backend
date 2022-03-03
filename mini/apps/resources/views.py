import json
from datetime import datetime
from django import http
from django.views import View
from .models import Image, Video, Article, Author, ImageGroup, VideoGroup, ArticleGroup
from store.models import Store
from utils.response_code import RETCODE
from qiniu import Auth, BucketManager, build_batch_delete

# 需要填写你的 Access Key 和 Secret Key
access_key = 'qzwEr-xaXDxPHOxXAhPs6ofGA4HzCp8UQ1Jslvuo'
secret_key = 'w3UaRyqtpD9pdtAkv-ruIlrxnGPr0JXdfjsch9UW'

# 构建鉴权对象
q = Auth(access_key, secret_key)
bucket = BucketManager(q)


# Create your views here.
class ImageView(View):
    """添加图片"""
    def post(self, request, pid, store_id):
        """
        用户注册实现
        :param request:
        :return:
        """
        # 1.接受参数
        img = json.loads(request.body)

        # 1.创建新的图片对象
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            Image.objects.create(
                store=store,
                title=img['title'],
                format=img['format'],
                size=img['size'],
                fileSize=img['fileSize'],
                src=img['src'],
                group=img['group'],
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid, store_id):
        # 1.接受参数
        # 1.创建新的图片对象
        print(pid, store_id)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            res = store.all_image.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'imgList': list(res)})

    def delete(self, request, pid, store_id, bucket_name):
        data = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.all_image.filter(src__in=data).delete()
            build_batch_delete(bucket_name, data)
        except:
            http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})

    def put(self, request, pid, store_id, mode):
        updateData = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            if mode == 'group':
                images = store.all_image.filter(src__in=updateData['data'])
                for image in images:
                    image.group = updateData['group']
                    image.update_time = datetime.now()
                Image.objects.bulk_update(images, fields=['group'])
            if mode == 'title':
                store.all_image.filter(id=updateData['id']).update(title=updateData['title'], update_time=datetime.now())
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


class ImageGroupView(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            group = store.image_group
            if group.exists():
                res = group.first().group
            else:
                res = [{'group': "全部图像", 'children': [{'group': '默认分组', 'id': 1163614357, 'num': 0}], 'id': 1,
                        'num': 0}]
                ImageGroup.objects.create(
                    store=store,
                    group=res,
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'imageGroup': res})

    def post(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.image_group.update(group=json.loads(request.body.decode()))
        except Exception as e:
            print(request.body.decode(),e)
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})


class VideoView(View):
    def post(self, request, pid, store_id):
        video = json.loads(request.body)
        store = Store.objects.get(pid=pid, id=store_id)
        try:
            Video.objects.create(
                store=store,
                title=video['title'],
                format=video['format'],
                size=video['size'],
                fileSize=video['fileSize'],
                src=video['src'],
                url=video['url'],
                group=video['group'],
                playTime=video['playTime'],
                textarea=video['textarea']
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid, store_id):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            res = store.all_video.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'videoList': list(res)})

    def delete(self, request, pid, store_id, bucket_name):
        data = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.all_video.filter(src__in=data).delete()
            build_batch_delete(bucket_name, data)
        except:
            http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})

    def put(self, request, pid, store_id, mode):
        updateData = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            if mode == 'group':
                videos = store.all_video.filter(src__in=updateData['data'])
                for video in videos:
                    video.group = updateData['group']
                    video.update_time = datetime.now()
                Video.objects.bulk_update(videos, fields=['group'])
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


class VideoGroupView(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            group = store.video_group
            if group.exists():
                res = group.first().group
            else:
                res = [
                    {'group': "全部视频", 'children': [{'group': '默认分组', 'id': 1163614357, 'num': 0}], 'id': 1, 'num': 0}]
                VideoGroup.objects.create(
                    store=store,
                    group=res,
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'videoGroup': res})

    def post(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.video_group.update(group=json.loads(request.body.decode()))
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})


class ArticleView(View):
    def post(self, request, pid, store_id):
        article = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            Article.objects.create(
                store=store,
                title=article['title'],
                totalRead=article['totalRead'],
                totalLike=article['totalLike'],
                review=article['review'],
                author=article['author'],
                caption=article['caption'],
                profile=article['profile'],
                content=article['content'],
                groupList=json.dumps(article['groupList']),
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid, store_id):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            res = store.all_article.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'articleList': list(res)})

    def delete(self, request, pid, store_id):
        data = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.all_article.filter(id__in=data).delete()
        except:
            http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})

    def put(self, request, pid, store_id, mode):
        article = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            if mode == 'edit':
                store.all_article.filter(id=article['id']).update(
                    title=article['title'],
                    totalRead=article['totalRead'],
                    totalLike=article['totalLike'],
                    review=article['review'],
                    author=article['author'],
                    caption=article['caption'],
                    profile=article['profile'],
                    content=article['content'],
                    update_time=datetime.now(),
                    groupList=json.dumps(article['groupList']),
                )
            elif mode == 'state':
                store.all_article.filter(id=article['id']).update(
                    top=article['top'],
                    conceal=article['conceal'],
                    update_time=datetime.now()
                )
            elif mode == 'read':
                store.all_article.filter(id=article['id']).update(
                    totalRead=article['totalRead'],
                    totalLike=article['totalLike'],
                    update_time=datetime.now()
                )
            elif mode == 'author':
                articles = store.all_article.filter(id__in=article['data'])
                for page in articles:
                    page.author = article['author']
                    page.update_time = datetime.now()
                Article.objects.bulk_update(articles, fields=['author'])

            else:
                articles = store.all_article.filter(id__in=article.keys())
                for page in articles:
                    page.groupList = json.dumps(article[str(page.id)])
                    page.update_time = datetime.now()
                Article.objects.bulk_update(articles, fields=['groupList'])
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


class AuthorView(View):
    def post(self, request, pid, store_id):
        author = json.loads(request.body)
        store = Store.objects.get(pid=pid, id=store_id)
        try:
            Author.objects.create(
                store=store,
                profile=author['profile'],
                author=author['author'],
                remark=author['remark']
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid, store_id):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            res = store.all_author.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'authorList': list(res)})

    def delete(self, request, pid, store_id, authorId):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.all_author.filter(id=authorId).delete()
        except Exception as e:
            http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})

    def put(self, request, pid, store_id, mode):
        updateData = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            if mode == 'edit':
                store.all_author.filter(id=updateData['id']).update(
                    profile=updateData['profile'],
                    author=updateData['author'],
                    remark=updateData['remark'],
                    update_time=datetime.now()
                )
            elif mode == 'status':
                store.all_author.filter(id=updateData['id']).update(
                    active=updateData['active'],
                    update_time=datetime.now()
                )
            else:
                authors = store.all_author.filter(id__in=updateData.keys())
                for author in authors:
                    author.article = updateData[str(author.id)]
                    author.update_time = datetime.now()
                Author.objects.bulk_update(authors, fields=['article'])
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


class ArticleGroupView(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            group = store.article_group
            if group.exists():
                res = group.first().group
            else:
                res = [{'group': '默认', 'article': 0}]
                ArticleGroup.objects.create(
                    store=store,
                    group=res,
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'articleGroup': res})

    def post(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.article_group.update(group=json.loads(request.body.decode()))
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})


class GetToken(View):
    def get(self, request, bucket_name):
        # 生成上传 Token，可以指定过期时间等
        try:
            token = q.upload_token(bucket_name)
        except:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'token': token})
