from PIL import Image
import os

cwd = os.getcwd()
filesDir = os.path.join(cwd, "texturesFolder")
files = os.scandir(filesDir)

blocksrgb = {}

for i in files:
    if os.path.splitext(i)[1] == ".png":
        imgobj = Image.open(os.path.join(i)).convert('RGBA')
        r=0
        g=0
        b=0
        alpha_present = False
        for pixel in imgobj.getdata():
            if pixel[3] != 255:
                print(i, "has alpha")
                os.remove(os.path.join(i))
                alpha_present = True
                break
        if not alpha_present:
            if imgobj.size != (16, 16):
                print(i, "is not 16x16")
                os.remove(os.path.join(i))
        for pixel in imgobj.getdata():
            r = r + pixel[0]
            g = g + pixel[1]
            b = b + pixel[2]
        rgb = [r/256, g/256, b/256]
        blocksrgb.update({os.path.basename(i): rgb})
# print(blocksrgb)

# load source image
img = Image.open("source.png")

# create a new blank image with same size
# new_img = Image.new('RGB', img.size)

# pick blocks of nxn pixels from source image
n=8
# paste mxm blocks into new image
m=16

new_img = Image.new('RGB', (img.size[0]*m//n, img.size[1]*m//n))
bit_depth = 2**1
for i in range(0, img.size[0], n):
    print(str(int(i/img.size[0]*100)) + "%")
    for j in range(0, img.size[1], n):
        # get the average color of the block
        r=0
        g=0
        b=0
        for k in range(n):
            for l in range(n):
                # check if pixel is inside the image
                if i+k >= img.size[0] or j+l >= img.size[1]:
                    continue
                pixel = img.getpixel((i+k, j+l))
                r = r + pixel[0]
                g = g + pixel[1]
                b = b + pixel[2]
        rgb = [r/(n*n), g/(n*n), b/(n*n)]
        # convert rgb to low bit depth
        # rgb = [round(rgb[0]/(256/bit_depth))*(256/bit_depth), round(rgb[1]/(256/bit_depth))*(256/bit_depth), round(rgb[2]/(256/bit_depth))*(256/bit_depth)]

        # find the closest block color
        closest = 0
        closest_dist = 1000000
        for key in blocksrgb:
            dist = (rgb[0]-blocksrgb[key][0])**2 + (rgb[1]-blocksrgb[key][1])**2 + (rgb[2]-blocksrgb[key][2])**2
            if dist < closest_dist:
                closest = key
                closest_dist = dist

        # grab image of closest block color and paste it into the new image
        block = Image.open(os.path.join(filesDir, closest))
        # resize block to n x n
        block = block.resize((m, m))
        new_img.paste(block, (i*m//n, j*m//n))
        # new_img.paste(block, (i, j))

# save the new image
new_img.save("output.png")
