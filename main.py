from brightestZ import get_brightestZ
from mergeZstack import merge_z_stack
from stitching import stitch_images


#read file
img = '../src/20230927_ID361_USV_neuercfos_ak.lif'
channel = 0 #channel to use
#get the brightest z-stack for each mosaic tile
k = get_brightestZ(img,channel)
#print(k)
#merge the brightest z-stack for each mosaic tile
merge_z_stack(img,k)
stitch_images('out/tiles/20230927_ID361_USV_neuercfos_ak/')