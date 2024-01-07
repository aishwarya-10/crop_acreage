import rasterio as rio
from rasterio.plot import show
from rasterio.plot import reshape_as_image
import matplotlib.pyplot as plt
import numpy as np
import earthpy.plot as ep # RGB visualization
import cv2

# Visualization 
def plot_img(img1, title: str):
    plt.figure()
    plt.imshow(img1, cmap='gray')
    plt.axis('on')
    plt.title(title)
    plt.show()

def plot_two_img(img1, img2, title: str):
  fig, axs = plt.subplots(1, 2, figsize=(50,50))
  for i in range(2):
    plot_img = [img1, img2]
    axs[i].imshow(plot_img[i], cmap='gray')
    axs[i].axis('off')
  # Overall title
  fig.suptitle(title)
  plt.show()


#---------------------Spectral indices-----------------------#
# Vegetation
def NDVI(RED, NIR):
  """
  NDVI-Normalized Difference Vegetation Index
    ARGS: RED, NIR
    RETURN: NDVI map
  """
  NDVI = (NIR.astype(float) - RED.astype(float))/(NIR + RED)
  return NDVI


#-----------------------------Data--------------------------#
# path = "C://Users//Aishwarya//OneDrive - AZISTA INDUSTRIES PVT LTD//VS CODE//Crop_acreage//Data//"
# stack = path + "S2_SR_B4_GAgri_2018.tif"

stack = "Data\S2_SR_B4_GAgri_2018.tif"

with rio.open(stack) as src:
  RGB_im=src.read([3,2,1])
  blue = src.read(1)
  green = src.read(2)
  red = src.read(3)
  nir = src.read(4)

# RGB Visualization
RGB_im = cv2.normalize(RGB_im, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
show(RGB_im)


#--------------------Calculate spectral index--------------------#
# Calculate NDVI
ndvi = NDVI(red, nir)

# Define the "spectral index var" name to get statistics and visualize
def stats_and_visualize(SpectralIndex, title_caps):
  """
  To print statistics of the spectral index and visualize the index map
  ARGS: Spectral Index, 
        Title: in caps & within " " 
  RETURN: Statistics, Plot
  """
  print("Statistics: ")
  print("Minimum: ", np.nanmin(SpectralIndex))
  print("Maximum: ", np.nanmax(SpectralIndex))

  plt.figure()
  plt.title(title_caps)
  plt.imshow(SpectralIndex)
  plt.colorbar()
  plt.show()

# stats_and_visualize(ndvi, "NDVI")

# Agriculture lands
lower_lmt = 0.2
upper_lmt = 0.4

ndvi_agri = (ndvi > lower_lmt) & (ndvi < upper_lmt)

stats_and_visualize(ndvi_agri, "NDVI")


#-------------- Pixel area calculation------------------#
# Convert uint16 to uint8
im_uint8 = np.uint8(ndvi_agri)

# Number of non-zero pixels
pixels = cv2.countNonZero(im_uint8)
im_area = im_uint8.shape[0]*im_uint8.shape[1]

# Print area of the image
# Area = pixelCount * (Resolution_x * Resolution_y) 
print("Pixel Area in sq.km: ", pixels*100/1e6) 
print("Image area in sq.km: ", im_area*100/1e6)


#-----------------------------Write--------------------------#
# meta = src.meta.copy() # input
# meta.update(count=3) # count implies no. of bands
# with rio.open("Data//RGB.tif", 'w', **meta) as dst:
#     dst.write(RGB_im) # output
