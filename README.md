# Image-Segmentation
Performing marker based image segmentation by implementing Watershed algorithm using disjoint set union data structure.

I have implemented the watershed algorithm as described in the [research paper](https://www.sciencedirect.com/science/article/pii/S092359650500086X) using python. Check out [results.pdf](https://github.com/ankush2005x/Image-Segmentation/blob/main/Results.pdf) for the comparison between results of my implementation of the algorithm and that shown in the research paper.

Input required:
1) Number of markers : Each marker marks a seperate object.
2) Enter coordinates : For each marker, enter four numbers, which correspond to x1, y1, x2, y2. This selects all pixels on the rectangle with two opposite corners at (x1,y1) & (x2,y2), and all these selected points one the perimeter of this rectangle make up a single marker.

As the algorithm progresses, the markers expand to cover the whole object, as a result of which the image is divided into different parts and the result is obtained.

Output: 
Image depicting segmentation of the original image into constituent parts.
