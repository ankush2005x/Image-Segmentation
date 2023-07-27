import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage

img = Image.open('mri.png').convert('L')  # convert image to 8-bit grayscale
width, height = img.size

data = list(img.getdata()) # convert image data to a list of integers

# convert that to 2D list (list of lists of integers)

data = [data[offset:offset+width] for offset in range(0, width*height, width)]

"""
for row in data:
    print(' '.join('{:3}'.format(value) for value in row))
"""
# Get x-gradient in "sx"
sx = ndimage.sobel(data, axis=0, mode='constant')
# Get y-gradient in "sy"
sy = ndimage.sobel(data, axis=1, mode='constant')
# Get square root of sum of squares
gradient=np.hypot(sx, sy)
gradient = gradient.astype(int)


plt.imshow(gradient, cmap='gray', vmin=0, vmax=255)
plt.show()

"""
# Get 2nd x-gradient in "sx"
sx2 = ndimage.sobel(gradient, axis=0, mode='constant')
# Get y-gradient in "sy"
sy2 = ndimage.sobel(gradient, axis=1, mode='constant')
# Get square root of sum of squares
gradient2=np.hypot(sx2, sy2)
plt.imshow(gradient2, cmap=plt.cm.gray)
plt.show()
"""
print("number of markers:", end = " ")
num = int(input())

result = [0 for _ in range(height * width)]
markers = [[] for _ in range(num)]
parent = [-3 for _ in range(height * width)]
labelPic = gradient.copy()

def find(cell, parent):
    if parent[cell] >= 0:
        parent[cell] = find(parent[cell], parent)
        return parent[cell]
    else:
        return cell

for i in range(height):
    for j in range(width):
        parent[i * width + j] = -3

print("\nEnter coordinates")

for i in range(num):
    print("Marker List ", i+1, end=": ")
    read = list(map(int, input().split()))
#    print(read)
#    print(i)
    for j in range(0, len(read), 2):
#    	print(i, j)
    	markers[i].append([read[j], read[j+1]])
    parent[markers[i][0][0] * width + markers[i][0][1]] = -2
#    for j in range(1, len(markers[i])):
#    	parent[markers[i][j][0] * width + markers[i][j][1]] = markers[i][0][0] * width + markers[i][0][1]

    for j in range(markers[i][0][0]+1, markers[i][1][0]+1):
#    	print(j * width + markers[i][0][1])
    	parent[j * width + markers[i][0][1]] = markers[i][0][0] * width + markers[i][0][1]
    	parent[j * width + markers[i][1][1]] = markers[i][0][0] * width + markers[i][0][1]
    	labelPic[j][markers[i][0][1]] = 255
    	labelPic[j][markers[i][1][1]] = 255
    	
    for j in range(markers[i][0][1]+1, markers[i][1][1]+1):
    	parent[markers[i][1][0] * width + j] = markers[i][0][0] * width + markers[i][0][1]
    	parent[markers[i][0][0] * width + j] = markers[i][0][0] * width + markers[i][0][1]
    	labelPic[markers[i][1][0]][j] = 255
    	labelPic[markers[i][0][0]][j] = 255

plt.imshow(labelPic, cmap='gray', vmin=0, vmax=255)
plt.show()

priority = [(gradient[i][j], i * width + j) for i in range(height) for j in range(width)]
priority.sort()

for i in range(width * height):
    if parent[priority[i][1]] == -3:
        parent[priority[i][1]] = -1

    for c in range(-1, 2):
        for r in range(-1, 2):
       	    if c == 0 and r == 0: continue
	
            neighbour = priority[i][1] + c + r * width
            if (priority[i][1] % width == 0 and c == -1) or (priority[i][1] % width == width - 1 and c == 1):
                continue
            if neighbour < 0 or neighbour >= width * height or parent[neighbour] == -3:
                continue
            else:
                prevRoot = find(neighbour, parent)
                if parent[priority[i][1]] == -2 and parent[prevRoot] == -1:
                    parent[prevRoot] = priority[i][1]
                elif (parent[priority[i][1]] == -2 and parent[prevRoot] == -2) or (priority[i][1]==prevRoot):
                    pass
                else:
                    parent[priority[i][1]] = parent[prevRoot]
                    parent[prevRoot] = priority[i][1]

region = 1
for k in range(width * height - 1, -1, -1):
    p = priority[k][1]
    if parent[p] < 0:
        parent[p] = region
        region += 1
    else:
        parent[p] = parent[parent[p]]


for k in range(width*height-1, -1, -1):
    p = priority[k][1]
    result[p] = (255//(region-1)) * parent[p]

for i in range(height):
    for j in range(width):
        print(result[i*width+j], end=" ")
    print()

#resultArr = np.asarray(result)
#resultArr = np.reshape(resultArr, (height, width))


result = np.reshape(result, (height, width))
#print(resultArr)
result = result.astype(int)
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.imshow(gradient, cmap='gray', alpha=0.2, vmin=0, vmax=255)
plt.show()


