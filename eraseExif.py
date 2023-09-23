from PIL import Image

def remove_exif(image_path, output_path, tags_to_remove):
    image = Image.open(image_path)

    # bring exif data of image
    exif_data = image.info.get('exif')

    # exif data 필터링 하기
    if exif_data is not None:
        filtered_exif_data = {tag: exif_data[tag] for tag in exif_data if tag not in tags_to_remove}
        image.info['exif'] = filtered_exif_data


    # 수정된 이미지 저장
    image.save(output_path)

if __name__ == "__main__":
    input_image_path = "C:\kisia\example_img.jpg"
    output_image_path = "C:\kisia\example_result_img.jpg"
    tags_to_remove = ["Exif.Image.DateTimeOriginal", "Exif.Image.DateTime",
                    "Exif.GPSInfo", "Exif.Photo.CameraOwnerName" ]

    remove_exif(input_image_path, output_image_path,tags_to_remove)