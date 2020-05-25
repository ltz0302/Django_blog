from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Folder, Document
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from .form import FolderPostForm, DocumentPostForm
from django.conf import settings
from django.utils.http import urlquote
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging


# Create your views here.
def folder_list(request):
    folder_list = Folder.objects.all()
    paginator = Paginator(folder_list, 10)
    page = request.GET.get('page')
    folders = paginator.get_page(page)

    context = {
        'folders': folders,
    }

    return render(request, 'doc/folder_list.html', context)


@login_required(login_url='/accounts/login/')
def folder_create(request):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("权限不够")
    if request.method == "POST":
        folder_post_form = FolderPostForm(data=request.POST)
        if folder_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_folder = folder_post_form.save(commit=False)
            new_folder.save()
            return redirect("doc:folder_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        folder_post_form = FolderPostForm()
        context = {'folder_post_form': folder_post_form}
        return render(request, 'doc/folder_create.html', context)


@login_required(login_url='/accounts/login/')
def folder_delete(request, id):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("权限不够")
    if request.method == 'POST':
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        config = CosConfig(Region=settings.RERION, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY)
        client = CosS3Client(config)

        docs = Document.objects.filter(folder_id=id)
        #COS删除文件夹下的所有文件
        for doc in docs:
            client.delete_object(
                Bucket='doc-1302212491',
                Key=doc.title
            )
        #删除数据库中的记录
        folder = Folder.objects.get(id=id)
        folder.delete()
        return redirect("doc:folder_list")
    else:
        return HttpResponse("仅允许post请求")


def doc_list(request, folder):
    doc_list = Document.objects.filter(folder=folder)
    paginator = Paginator(doc_list, 10)
    page = request.GET.get('page')
    docs = paginator.get_page(page)

    context = {
        'docs': docs,
    }

    return render(request, 'doc/doc_list.html', context)


@login_required(login_url='/accounts/login/')
def doc_add(request):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("权限不够")
    if request.method == "POST":
        doc_post_form = DocumentPostForm(request.POST)
        if doc_post_form.is_valid():
            title = request.FILES.get('file').name
            if Document.objects.filter(title=title):
                return HttpResponse("文件名已存在")
            else:
                logging.basicConfig(level=logging.INFO, stream=sys.stdout)
                config = CosConfig(Region=settings.RERION, SecretId=settings.COS_SECRET_ID,
                                   SecretKey=settings.COS_SECRET_KEY)
                client = CosS3Client(config)
                # 保存数据，但暂时不提交到数据库中
                new_doc = doc_post_form.save(commit=False)
                # 在表单给定的文件夹下添加文件
                folder_id = request.POST.get("folder_id")
                folder = Folder.objects.get(id=folder_id)
                new_doc.folder = folder

                new_doc.title = title
                #TODO 大文件上传完后不能正确刷新
                response= client.put_object(
                    Bucket='doc-1302212491',
                    Body=request.FILES.get('file'),
                    Key=new_doc.title
                )
                print(response['ETag'])
                new_doc.save()
                return redirect("doc:folder_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        folders = Folder.objects.all()
        context = {'folders': folders}
        return render(request, 'doc/doc_add.html', context)


@login_required(login_url='/accounts/login/')
def doc_delete(request,id):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("权限不够")
    if request.method == 'POST':
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        config = CosConfig(Region=settings.RERION, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY)
        client = CosS3Client(config)

        doc = Document.objects.get(id=id)
        folder_id = doc.folder_id
        client.delete_object(
            Bucket='doc-1302212491',
            Key=doc.title
        )

        doc.delete()
        return redirect("doc:doc_list", folder_id)
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/accounts/login/')
def doc_download(request,id):
    if request.method == 'GET':
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        config = CosConfig(Region=settings.RERION, SecretId=settings.COS_SECRET_ID, SecretKey=settings.COS_SECRET_KEY)
        client = CosS3Client(config)

        doc = Document.objects.get(id=id)
        cos_response = client.get_object(
            Bucket='doc-1302212491',
            Key=doc.title
        )
        response = FileResponse(cos_response['Body'].get_raw_stream())
        # 指定响应格式为二进制流
        response['Content-Type'] = 'application/octet-stream'
        #TODO 服务端会抛出异常
        #指定下载时的设定 attachment表示以附件下载,urlquote对文件中包含的中文编码
        response['Content-Disposition'] = 'attachment;filename="%s' % (urlquote(doc.title))
        return response
    else:
        return HttpResponse("仅允许post请求")



