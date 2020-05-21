from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Folder, Document
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from .form import FolderPostForm, DocumentPostForm
from django.conf import settings
import os
from django.utils.http import urlquote

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
    if request.method == 'POST':
        folder = Folder.objects.get(id=id)
        if request.user != superuser:
            return HttpResponse("权限不够")
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
        folder_id = request.POST.get("folder_id")
        folder = Folder.objects.get(id=folder_id)
        doc_post_form = DocumentPostForm(request.POST, request.FILES)
        if doc_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_doc = doc_post_form.save(commit=False)
            new_doc.folder = folder
            new_doc.title = request.FILES.get('file').name
            new_doc.save()
            return redirect("doc:folder_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        folders = Folder.objects.all()
        context = {'folders': folders}
        return render(request, 'doc/doc_add.html', context)


@login_required(login_url='/accounts/login/')
def doc_delete(request, id):
    superuser = User.objects.get(is_superuser=True)
    if request.method == 'POST':
        doc = Document.objects.get(id=id)
        if request.user != superuser:
            return HttpResponse("权限不够")
        folder_id = doc.folder_id
        doc.delete()
        return redirect("doc:doc_list", folder_id)
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/accounts/login/')
def doc_download(request, id):
    if request.method == 'GET':
        doc = Document.objects.get(id=id)
        name = str(doc.file)
        filepath = os.path.join(settings.MEDIA_ROOT, name)

        response = FileResponse(open(filepath, 'rb'))
        #指定响应格式为二进制流
        response['Content-Type'] = 'application/octet-stream'
        #TODO 客户端中断连接时 服务端会抛出异常
        #指定下载时的设定 attachment表示以附件下载,urlquote对文件中包含的中文编码
        response['Content-Disposition'] = 'attachment;filename="%s' % (urlquote(doc.title))
        return response
    else:
        return HttpResponse("仅允许post请求")


