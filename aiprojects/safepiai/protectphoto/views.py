from django.http import HttpResponseRedirect
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
            for file in request.FILES.getlist('image'):
                # 파일 처리 로직 추가
                Photo.objects.create(image=file)
            print(request.FILES)
            return redirect('image_list')
    else:
        form = PhotoForm()
    return render(request, 'upload.html', {'form': form})

def image_list(request):
    photos = Photo.objects.all()
    return render(request, 'image_list.html', {'photos': photos})

def download_and_delete_image(request):

     # 모든 이미지를 가져옵니다. 이 예제에서는 모든 이미지를 가져오지만 필요에 따라 필터링할 수 있습니다.
    all_images = Photo.objects.all()

    # 다운로드 및 삭제된 이미지 수를 추적하는 변수를 초기화합니다.
    downloaded_images = 0

    for photo_instance in all_images:
        # 이미지 파일 경로를 가져옵니다.
        image_path = photo_instance.image.path

        with open(image_path, 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{photo_instance.image.name}"'

        if os.path.exists(image_path):
            # 이미지 파일 삭제
            os.remove(image_path)

            # 이미지 모델 삭제
            photo_instance.delete()

            downloaded_images += 1

    # 모든 이미지를 처리한 후 응답을 반환합니다.
    return HttpResponse(f'Downloaded and deleted {downloaded_images} images.')
