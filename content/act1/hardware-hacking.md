+++
title = 'Hardware Hacking 101'
date = 2024-11-17T14:19:45+01:00
draft = false
weight = 3
+++

## Objective (main)

> Ready your tools and sharpen your wits—only the cleverest can untangle the wires and unlock Santa’s hidden secrets!

## Hardware Hacking 101 Part 1

### Objective

> Jingle all the wires and connect to Santa's Little Helper to reveal the merry secrets locked in his chest!

### Solution for silver

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

Opening the task itself, we are presented a book: 

![Hardware hacking 101 part 1 part 1](/images/act1/hardware-hacking-101-part-1-1.png)

And by closing the book we are presented with a nifty play area: 

![Hardware hacking 101 part 1 part 2](/images/act1/hardware-hacking-101-part-1-2.png)

Connecting the wires game! The way I solved was to 

1. Power up the controller (upper right corner)
2. Enter the values from the shredded note (see controllers screen)
3. Conenct USB from controller to UART bridge.
4. Connecting the wires completely willy-nillingly from UART bridge.
5. Selecting a port on the controller. 
6. Hit "S" button on the controller to see if it worked.

Well. That was the general recipe. In real life, though, I had forgotten to flip the 5V switch over to 3V - so things got a bit toasty here and there. And I also had to cycle the com ports before eventually landing on using USB0. 

![Hardware hacking 101 part 1 part 3](/images/act1/hardware-hacking-101-part-1-3.png)

And by this silver was won! 

![Hardware hacking 101 part 1 part 4](/images/act1/hardware-hacking-101-part-1-4.png)

### Solution for gold

For going for gold, I first found the Iframe source:

![Hardware hacking 101 part 1 part 5](/images/act1/hardware-hacking-101-part-1-5.png)

Then ran that URL through BurpSuite Browser, where I found a reference to V1 of the API. This hint was located in "main.js" script file. 

![Hardware hacking 101 part 1 part 6](/images/act1/hardware-hacking-101-part-1-6.png)

Having captured the post request to solve the game using V2 of the API (basically the same as the GUI game), I just changed the text to refer to V1 of the API: 

![Hardware hacking 101 part 1 part 7](/images/act1/hardware-hacking-101-part-1-7.png)

Done.

## Hardware Hacking 101 Part 2

> Santa’s gone missing, and the only way to track him is by accessing the Wish List in his chest—modify the access_cards database to gain entry!