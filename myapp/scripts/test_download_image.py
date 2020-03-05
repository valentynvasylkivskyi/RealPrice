import wget
import os

dir = r'C:\Users\vasilkovskiy\PycharmProjects\realprice\media\images'
url = 'https://i1.rozetka.ua/goods/15292145/copy_asus_90nr02a1_m01210_5dd6c4955a399_images_15292145534.jpg'
url2 = 'https://i.citrus.ua/imgcache/size_500/uploads/shop/5/5/5533198c217ea9a4280fdf804df8f088.jpg'


filename = wget.download(url2)
os.rename(filename, os.path.join(dir, filename))

print(filename)


