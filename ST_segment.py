from stardist.models import StarDist2D
import numpy as np
from stardist.data import test_image_nuclei_2d
from stardist.plot import render_label
from csbdeep.utils import normalize
import matplotlib.pyplot as plt
from tifffile import imread

def st_segmentation(img):
    StarDist2D.from_pretrained()
    model = StarDist2D.from_pretrained('2D_versatile_fluo')
    # img = test_image_nuclei_2d()
    labels,_= model.predict_instances(normalize(img))
    np.save('lables.npy',labels)
    return labels