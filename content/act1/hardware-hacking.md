+++
title = 'Hardware Hacking 101'
date = 2024-11-17T14:19:45+01:00
draft = true
weight = 3
+++


In the hint section I found this helpful hint: 

> On the Cutting Edge
> From: Morcel Nougat
> Terminal: Hardware Part 1
> Hey, I just caught wind of this neat way to piece back shredded paper! It's a fancy heuristic detection technique—sharp as an elf’s wit, I tell ya! Got a sample Python script right here, courtesy of Arnydo. Check it out when you have a sec: [heuristic_edge_detection.py](https://gist.github.com/arnydo/5dc85343eca9b8eb98a0f157b9d4d719)."

I downloaded the script: 

```python
import os
import numpy as np
from PIL import Image

def load_images(folder):
    images = []
    filenames = sorted(os.listdir(folder))
    for filename in filenames:
        if filename.endswith('.png') or filename.endswith('.jpg'):
            img = Image.open(os.path.join(folder, filename)).convert('RGB')
            images.append(np.array(img))
    return images

def calculate_difference(slice1, slice2):
    # Calculate the sum of squared differences between the right edge of slice1 and the left edge of slice2
    return np.sum((slice1[:, -1] - slice2[:, 0]) ** 2)

def find_best_match(slices):
    n = len(slices)
    matched_slices = [slices[0]]
    slices.pop(0)

    while slices:
        last_slice = matched_slices[-1]
        differences = [calculate_difference(last_slice, s) for s in slices]
        best_match_index = np.argmin(differences)
        matched_slices.append(slices.pop(best_match_index))

    return matched_slices

def save_image(images, output_path):
    heights, widths, _ = zip(*(i.shape for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_image = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for img in images:
        pil_img = Image.fromarray(img)
        new_image.paste(pil_img, (x_offset, 0))
        x_offset += pil_img.width

    new_image.save(output_path)

def main():
    input_folder = "/mnt/c/Users/Roger Johnsen/Downloads/HHC2024/shreds/slices"
    output_path = "/mnt/c/Users/Roger Johnsen/Downloads/HHC2024/assembled_image.png"

    slices = load_images(input_folder)
    matched_slices = find_best_match(slices)
    save_image(matched_slices, output_path)

if __name__ == '__main__':
    main()
```

I only changed the "_input_folder_" and "_output_path_" variables and ran the script. Once finished, it assembled the pieced into this image:

![Hardware hacking 101 assembled image](/images/act1/Hardware-Hacking-101-assembled_image.png)

Image isn't particularly easy to read. Thus some manual work needs to be done: 

1. Image assembled are mirrored. In order to mirror it readable, I used this site which offers basic image editing tools: https://www.resizepixel.com/
2. After mirroring the image, I used https://www.photopea.com/ to rearrange the elements in the picture, making the whole lot readable: 

![Hardware hacking 101 fixed image ](/images/act1/Hardware-Hacking-101-assembled_image-mirrored.png)