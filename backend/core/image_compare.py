#!/usr/local/bin/python3
import glob
import os,sys
import cv2
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import pprint

cwd = os.getcwd()

os.chdir('/Users/griffin/Dropbox/Scripts-random/image_projects/EmojiColors/')

# Globals ;)
histogram_types = {
    "Correlation": cv2.HISTCMP_CORREL,
    "Chi-Squared": cv2.HISTCMP_CHISQR,
    "Intersection": cv2.HISTCMP_INTERSECT,
    "Hellinger": cv2.HISTCMP_BHATTACHARYYA
}

args = {}               # dictionary of command line args
imagesList = []         # list of image names with path
imagesFolder = None     # folder name combined with path
cvimagesList = {}       # dictionary of cv images with filename as key
histogramsList = {}     # dictionary of histograms with filename as key
targetName = None       # the target image name with path
targetHist = None       # the target histogram to compare against
targetCv = None

"""
Description:
    Opens a filepath and reads into a cvimage type.
Params:
    image_name [string]: filename and path to image
Return:
    a color opencv image 
"""
def load_cv_image(image_name,colors=0):
    if os.path.isfile(image_name):
        cvimage = cv2.imread(image_name)
        if colors > 0:
            cvimage = reduce_colors(cvimage,colors)
        return cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
    else:
        error("cv_image: image_name not an actual file.")
        return None

"""
Description:
    Generates an opencv histogram from a given opencv image.
Params:
    cv_image [cv image type]
Return:
    flattened histogram
"""
def cv_histogram(cv_image):
    # extract a 3D RGB color histogram from the image,
    # using 8 bins per channel, normalize, and update the index
    hist = cv2.calcHist([cv_image], [0, 1, 2], None, [8, 8, 8],[0, 256, 0, 256, 0, 256])
    return cv2.normalize(hist, hist).flatten()

"""
Description:
    Loads two dictionaries with opencv images and opencv histograms. Uses 3 global variables :)
Params:
    What? Global vars :)
Return:
    Seriously? Globals :)
"""
def load_data_lists(colors=0):
    global cvimagesList
    global histogramsList
    global imagesList

    histograms = {}
    # loop over the image paths
    for image in imagesList:

        # load global array of cvimages
        filename = image[image.rfind("/") + 1:]
        
        # get cv images and then histograms for each of them
        cvimagesList[filename] = load_cv_image(image,colors)
        histogramsList[filename] = cv_histogram(cvimagesList[filename])

"""
Description:
    Compare the target histogram to the array of histograms and keep the
    N closest difference scores and return them.
Params:
    method_name [string] : name of comparison method to access 'histogram_types' and get proper opencv value
    target_hist [histogram] : histogram of target image
    keep_closest [int]: keep this many closest images (if that many results) and return list
Return:
    list of tuples (score,image_name) => (0.32774427625335206, 'leopard.png')
"""
def compare_image(method_name,target_hist,keep_closest=5):

    # initialize the results dictionary and the sort
    # direction
    reverse = False
    results = {}

    # if we are using the correlation or intersection
    # method, then sort the results in reverse order
    if method_name in ("Correlation", "Intersection"):
        reverse = True

    for (k, hist) in histogramsList.items():
        # compute the distance between the two histograms
        # using the method and update the results dictionary
        d = cv2.compareHist(target_hist, hist, histogram_types[method_name])
        results[k] = d

    # sort the results
    results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)

    # return N closest (minus the first one since its == target)
    if keep_closest+1 <= len(results):
        return results[1:keep_closest+1]
    else:
        return results


def plot_results(targetName,results,imagesFolder,rows,cols):
    
    cols += 2

    fig, axs = plt.subplots(rows, cols)

    print(os.path.basename(targetName))

    #target = mpimg.imread(targetName)
    target = cvimagesList[os.path.basename(targetName)]

    fig.set_size_inches(8, 5, forward=True)

    row = 0
    for hist_type,hlist in results.items():
        print(hist_type)
        ax = axs[row, 0]
        ax.text(-0.5, 0.5, hist_type, family='monospace',horizontalalignment='left')
        ax.axis('off')
        ax = axs[row, 1]
        ax.imshow(target, alpha=1)
        ax.axis('off')
        col = 2
        for val,image_name in hlist:
            print(val,image_name)
            ax = axs[row, col]
            #img = mpimg.imread(os.path.join(imagesFolder,image_name))
            img = cvimagesList[image_name]
            ax.imshow(img, alpha=1)
            ax.axis('off')
            name,ext = image_name.split('.')
            ax.text(30, 0, str(name), fontsize=12,horizontalalignment='center',verticalalignment='bottom')
            col += 1
        row += 1
    plt.show()

def reduce_colors(image,K=4):

    
    (h, w) = image.shape[:2]
    
    # convert the image from the RGB color space to the L*a*b*
    # color space -- since we will be clustering using k-means
    # which is based on the euclidean distance, we'll use the
    # L*a*b* color space where the euclidean distance implies
    # perceptual meaning
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # reshape the image into a feature vector so that k-means
    # can be applied
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    
    # apply k-means using the specified number of clusters and
    # then create the quantized image based on the predictions
    clt = MiniBatchKMeans(n_clusters = K)
    labels = clt.fit_predict(image)
    quant = clt.cluster_centers_.astype("uint8")[labels]
    
    # reshape the feature vectors to images
    quant = quant.reshape((h, w, 3))
    
    # convert from L*a*b* to RGB
    quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)

    return quant
    
"""
Description:
    Makes sure necessary arguments are on command line
Params:
    None
Return:
    a tuple with (string,string) => (targets image name, folder of images to read)
"""
def check_args():

    # populate args dict with key value pairs
    for arg in sys.argv:
        if "=" in arg:
            k,v = arg.split('=')
            args[k] = v

    targetName = args.get('target',None)
    imagesFolder = args.get('folder',None)
    colors= args.get('colors',0)

    if targetName == None:
        error("Need a target image.")
    
    if imagesFolder == None:
        error("Need a folder of images to read.")

    if not os.path.isdir(imagesFolder):
        error("%s is not a folder ..." % folder)

    if not os.path.isfile(targetName):
        if not os.path.isfile(os.path.join(imagesFolder,targetName)):
            error("Error: %s is not a file ..." % targetName)
        else:
            targetName = os.path.join(imagesFolder,targetName)

    return (targetName,imagesFolder,int(colors))

"""
Simple error function that print usage then exits
"""
def error(msg):
    print("Error: %s" % msg)
    usage()
    sys.exit()

"""
Called from error to print .......... the usage!
"""
def usage():
    print("image_compare.py target=image.png folder=./foldername")
    print("   target: the image you want to compare against")
    print("   folder: a folder of images you want to get the closest matches from")

   
if __name__=='__main__':

    rows = len(histogram_types)
    cols = 5

    # check necessary arguments are on command line
    targetName,imagesFolder,colors = check_args()    

    # load up image names with paths into list
    imagesList = glob.glob(imagesFolder+'/*')
    
    # open images and generate histograms
    load_data_lists(colors)

    # load target image into opencv world
    targetCv = load_cv_image(targetName)

    # generate histogram from previous load_cv_imagd
    targetHist = cv_histogram(targetCv)

    results = {}

    for htype in histogram_types:
        results[htype] = compare_image(htype,targetHist,cols)
        # print(htype)
        # print(compare_image(htype,targetHist))

    plot_results(targetName,results,imagesFolder,rows,cols)

    #pprint.pprint(results)
    sys.exit()


