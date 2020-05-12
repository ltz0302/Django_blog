from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Folder,Document
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .form import FolderPostForm, DocumentPostForm
# Create your views here.
def folder_list(request):
    folder_list = Folder.objects.all()
    paginator = Paginator(folder_list, 3)
    page = request.GET.get('page')
    folders = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'folders': folders,
    }

    return render(request, 'doc/folder_list.html', context)

@login_required(login_url='/accounts/login/')
def folder_create(request):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("抱歉，你无权写文章。")
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
        context = {'article_post_form': folder_post_form}
        return render(request, 'doc/folder_create.html', context)