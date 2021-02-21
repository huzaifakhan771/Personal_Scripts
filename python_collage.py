import random
from PIL import Image, ImageDraw, ImageFont
import sys
import cv2
import os
import pandas as pd
import math


def create_collage(img_names, img_folder,image_path, out_path, sku_imgs_occr, sku_img_keys):
    w, h = 400, 400
    size = w, h
    
    collage_width = w*3+10
    collage_height = math.ceil(len(img_names)/3)*h
    new_image = Image.new('RGB', (collage_width, collage_height))
    cursor = (0,0)
    for i, image in enumerate(img_names):

        paste_img = Image.open(os.path.join(image_path, img_folder[image]))
        paste_img, _ = exif_transpose(paste_img)
        paste_img.thumbnail(size, Image.ANTIALIAS)
        new_image.paste(paste_img, cursor)

        # w, h = paste_img.size
        # add name
        text = f"Img: {image+1}, Occr: {sku_imgs_occr[i]}, SKU: {sku_img_keys[i]}"
        insert_name(new_image, text, cursor)

        # move cursor
        y = cursor[1]
        x = cursor[0] + w+5
        if cursor[0] >= (collage_width - w-10):
            y = cursor[1] + h
            x = 0
        cursor = (x, y)

    new_image.save(os.path.join(out_path, str(img_names[0]+1) + ".jpg"))

def insert_name(image, name, cursor):
    draw = ImageDraw.Draw(image, 'RGBA')
    font = ImageFont.truetype('arialbd.ttf', size=12)
    x = cursor[0]
    y = cursor[1]
    draw.rectangle([(x, y), (x+400, y+20)], (255, 255, 255, 123))
    draw.text((x, y), name, (0, 0, 0), font=font)


def create_collage_each_image(image_path, out_path, basamh_path, fp_conflicts_path):
    img_folder = os.listdir(image_path)
    img_folder.sort(key=lambda f: int(os.path.splitext(f)[0]))   # split filename, convert to int then sort
    
    basamh = pd.read_csv(os.path.join(basamh_path, "Basamh.csv"))
    fp_conflicts = pd.read_csv(os.path.join(fp_conflicts_path, "fp_conflicts.csv"))

    for _, row in fp_conflicts.iterrows():
        img_names = []
        orig_img = row['gt_class']
        sku_imgs = eval(row['conflicted_skus'])
        sku_imgs_dict = {k: v for k, v in sorted(sku_imgs.items(), key=lambda item: item[1], reverse = True)}
        sku_img_keys = list(sku_imgs_dict.keys())
        sku_imgs_occr = list(sku_imgs_dict.values())
        sku_imgs_occr.insert(0,"Original")

        if orig_img not in basamh['ShortNames'].tolist():
            continue
        img_names.append(basamh.index[basamh['ShortNames'] == orig_img].tolist()[0])

        filtered_sku_img_keys = [orig_img]
        popped = 0
        for idx, sku_img in enumerate(sku_img_keys):
            if sku_img not in basamh['ShortNames'].tolist():
                sku_imgs_occr.pop(idx+1-popped)
                popped += 1
                continue
            img_names.append(basamh.index[basamh['ShortNames'] == sku_img].tolist()[0])
            filtered_sku_img_keys.append(sku_img)
        # sku_img_keys.insert(0, orig_img)
        # if img_names[0] == 105:
        #     print("getcsv", img_names, sku_imgs_occr, sku_img_keys)
        #     break
        create_collage(img_names, img_folder,image_path, out_path, sku_imgs_occr, filtered_sku_img_keys)
        print("----------------")

tag_map = {
    1 : '0 degrees: the correct orientation, no adjustment is required.',
    2 : '0 degrees, mirrored: image has been flipped back-to-front.',
    3 : '180 degrees: image is upside down.',
    4 : '180 degrees, mirrored: image has been flipped back-to-front and is upside down.',
    5 : '90 degrees: image has been flipped back-to-front and is on its side.',
    6 : '90 degrees, mirrored: image is on its side.',
    7 : '270 degrees: image has been flipped back-to-front and is on its far side.',
    8 : '270 degrees, mirrored: image is on its far side.'
    }

def exif_transpose(img):
    if not img:
        return img

    exif_orientation_tag = 274

    # Check for EXIF data (only present on some files)
    if hasattr(img, "_getexif") and isinstance(img._getexif(), dict) and exif_orientation_tag in img._getexif():
        exif_data = img._getexif()
        orientation = exif_data[exif_orientation_tag]

        # Handle EXIF Orientation
        if orientation == 1:
            # Normal image - nothing to do!
            pass
        elif orientation == 2:
            # Mirrored left to right
            img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # Rotated 180 degrees
            img = img.rotate(180)
        elif orientation == 4:
            # Mirrored top to bottom
            img = img.rotate(180).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
            # Mirrored along top-left diagonal
            img = img.rotate(-90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            # Rotated 90 degrees
            img = img.rotate(-90, expand=True)
        elif orientation == 7:
            # Mirrored along top-right diagonal
            img = img.rotate(90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            # Rotated 270 degrees
            img = img.rotate(90, expand=True)
    else:
        orientation = 1

    return img,orientation

def main():
    image_path = "packshot_images"
    out_path = "out_path"
    basamh_path = "."
    fp_conflicts_path = "."
    create_collage_each_image(image_path, out_path, basamh_path, fp_conflicts_path)

if __name__ == "__main__":
    main()