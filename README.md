# lif_stitching

How to run the script:
- drop your .lif files in the src folder
- run the main.py
- done. you find the results in the out folder




understanding a lif file:


every file contains two image folders

image folder img.get_image(0) contains all partial scanns
image folder img.get_image(1) contains a stitched/merged scann.


every patial image ( in img_get_image(0)) is identifiably by its number m

every image m contains 
- a stack of z images (vertical)
- a stack of t images (time) (in our cas only t=0 is available)
- several channals c (c-fos,gad67,vglut)

the infividual frame can be accesed through 

img.get_image(0).get_frame(z=int, t= int, c=int,m=int)
