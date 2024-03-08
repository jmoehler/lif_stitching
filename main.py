from lif_processer import lif_processer

channel = 0 #channel to use, adjust here
source = './src' #source folder adjust if needed

# run the pipeline for all .lif files in the src folder
lif_processer(channel, source)