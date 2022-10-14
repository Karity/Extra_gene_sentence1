import os
import shutil

slices_path = '../slices_images1'
image_path = r'E:\LAPTOP\new_result1'
dst_dir = '../images'
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)
for dir in os.listdir(slices_path):
    for image in os.listdir(os.path.join(slices_path, dir)):
        image = image.split('_')
        img = image[0]+'_'+image[1]+'_'+image[2]+'.jpg'
        image_dir = image[0]
        print(img, image_dir)
        for i in os.listdir(os.path.join(image_path, image_dir, 'img')):
            if i.endswith('jpg'):
                if i == img:
                    imgfile = os.path.join(image_path, image_dir, 'img', i)
                    shutil.copy(imgfile, dst_dir)
                print('1:', i)