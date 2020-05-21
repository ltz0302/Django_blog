from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import GalleryPostForm, PhotoPostForm
from photologue.models import Gallery, Photo

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

#TODO site
@login_required(login_url='/accounts/login/')
def gallery_delete(request, id):
    if request.method == 'POST':
        gallery = Gallery.objects.get(id=id)
        gallery.delete()
        return redirect("photologue:gallery-list")
    else:
        return HttpResponse("仅允许post请求")

@login_required(login_url='/accounts/login/')
def photo_add(request):
    superuser = User.objects.get(is_superuser=True)
    if request.user != superuser:
        return HttpResponse("抱歉，你无权上传照片。")
    if request.method == 'POST':
        title = request.FILES.get('image').name
        if Photo.objects.filter(title=title).exists():
            photo = Photo.objects.get(title=title)
        else:
            photo_form = PhotoPostForm(request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.title = title
                photo.save()
            else:
                return HttpResponse("注册表单输入有误。请重新输入~")
        id_gallery = request.POST.get('id_gallery')
        gallery = Gallery.objects.get(id=id_gallery)
        gallery.photos.add(photo)
        return redirect("photologue:gallery-list")
    else:
        gallery = Gallery.objects.all()
        context = {'gallery': gallery}
        return render(request, 'photologue/photo_add.html', context)

@login_required(login_url='/accounts/login/')
def photo_delete(request, id):
    if request.method == 'POST':
        photo = Photo.objects.get(id=id)
        galleries = photo.galleries.all()
        for gallery in galleries:
            photo.galleries.remove(gallery)
        return redirect("photologue:gallery-list")
    else:
        return HttpResponse("仅允许post请求")


class GalleryDateView:
    pass

class PhotoDateView:
    pass
