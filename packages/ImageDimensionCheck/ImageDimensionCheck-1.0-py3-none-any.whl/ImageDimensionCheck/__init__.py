import glob
import cv2
import os
def CheckImageDimension(path,extension=['jpg','png']):
    path = path + "//"
    for ext in extension:
        pattern = path + '*.' + f'{ext}'
        files = glob.glob(pattern)
        print(f'The number of {ext} files:', files)

    image_files = os.listdir(path)
    if not image_files:
        print("No images found in the specified directory.")
        return

    image_NotExist = True
    j = 0
    while image_NotExist:
         first_image = cv2.imread(path + image_files[j])
         point = j
         if first_image is not None:
             image_NotExist = False
         else:
             j = j+1

    if image_NotExist==True:
        print('No valid images are present in the dataset')
    else:
       ref_width,ref_height,_ = first_image.shape

    image_files = image_files[point:]
    flag = 0
    for i,img in enumerate(image_files):
        if i%1000 == 0:
            print(f'{i} images have been processed.....')
        img_to_compare = cv2.imread(path + img)
        compare_width,compare_height,_ = img_to_compare.shape

        if (ref_width,ref_height)!=(compare_width,compare_height):
            flag = 1
            break

    if flag==1:
        print('Different dimensions detected')
        return False
    else:
        print('All images have same dimensions')
        return True