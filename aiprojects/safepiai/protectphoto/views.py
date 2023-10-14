from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .forms import PhotoForm
from .models import Photo
import os


def upload_file(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            print(request.FILES)
            return redirect('image_list')
    else:
        form = PhotoForm()
    return render(request, 'upload.html', {'form': form})


def image_list(request):
    photos = Photo.objects.all()
    return render(request, 'image_list.html', {'photos': photos})


def download_image(request, pk):
    photo_instance = get_object_or_404(Photo, pk=pk)

    # 이미지 파일 경로를 생성
    image_path = photo_instance.image.path

    # 파일이 존재하는지 확인
    if os.path.exists(image_path):
        with open(image_path, 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="{photo_instance.image.name}"'
        return response

    else:
        # 접근 거부 or 파일이 존재하지 않을 경우 404 오류 반환
        return HttpResponseNotFound('Denied')


def delete_image(request, pk):
    photo_instance = get_object_or_404(Photo, pk=pk)

    # 이미지 파일 경로를 생성
    image_path = photo_instance.image.path

    if os.path.exists(image_path):
        # 이미지 파일 삭제
        os.remove(image_path)

        # 이미지 모델 삭제
        photo_instance.delete()

    # 'upload_file' URL로 리다이렉션
    redirect_url = reverse('upload_file')
    # 'upload_file'은 프로젝트의 URL 패턴 이름에 맞게 변경
    return HttpResponseRedirect(redirect_url)


def download_and_delete_image(request, pk):
    photo_instance = get_object_or_404(Photo, pk=pk)

    # 이미지 다운로드 응답
    image_path = photo_instance.image.path
    with open(image_path, 'rb') as image_file:
        response = HttpResponse(image_file.read(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{photo_instance.image.name}"'

    if os.path.exists(image_path):
        # 이미지 파일 삭제
        os.remove(image_path)

        # 이미지 모델 삭제
        photo_instance.delete()

    return response