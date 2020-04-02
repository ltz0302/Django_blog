from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import GalleryPostForm
from photologue.models import Gallery
# Create your views here.
@login_required(login_url='/accounts/login/')
def gallery_create(request):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("抱歉，你无权新建相册。")
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        gallery_post_form = GalleryPostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if gallery_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_gallery = gallery_post_form.save(commit=False)
            new_gallery.save()
            return redirect("photologue:gallery-list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        gallery_post_form = GalleryPostForm()
        context = {'gallery_post_form': gallery_post_form}
        return render(request, 'photologue/gallery_create.html', context)


@login_required(login_url='/accounts/login/')
def gallery_delete(request, id):
    if request.method == 'POST':
        gallery = Gallery.objects.get(id=id)
        gallery.delete()
        return redirect("photologue:gallery-list")
    else:
        return HttpResponse("仅允许post请求")