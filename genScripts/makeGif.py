import glob
from PIL import Image

# filepaths
fp_in = "./CICADAPUPlots/anomalyScore_*A.png"
fp_out = "./anomalyScoreA.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
imgs = (Image.open(f) for f in sorted(glob.glob(fp_in)))
img = next(imgs)  # extract first image from iterator
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=400, loop=0)