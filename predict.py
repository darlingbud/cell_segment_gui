from asyncio import transports
from operator import mod
from random import random
from subprocess import STARTF_USESTDHANDLES
from tkinter import image_names
from tkinter.ttk import LabelFrame
from unet2 import UNetStar
import torch
import cv2 as cv
import numpy as np
from stardist import non_maximum_suppression,polygons_to_label
from monai.transforms import ScaleIntensity
MODEL_WRIGHTS_PATH="./unet2/model_weights.t7"

def draw(label):
    number=np.max(label)
    random_coler={}
    for i in range(1,number+1):
        bgr = np.random.randint(0, 255, 3, dtype=np.int32)
        random_coler[i]=bgr
    ret=np.zeros((label.shape[0],label.shape[1],3),dtype=np.int32)
    for i in range(label.shape[0]):
        for j in range(label.shape[1]):
            if label[i][j]>0:
                ret[i][j][:]=random_coler[label[i][j]]
    return ret




def st_segmentation(img):
    model=UNetStar(1,32)
    #checkpoint=torch.load(MODEL_WRIGHTS_PATH,map_location=torch.device('cpu'))
    model.load_state_dict(torch.load(MODEL_WRIGHTS_PATH,map_location=torch.device('cpu')))
    print("Distance weights loaded")
    #格式变换
    transpose=ScaleIntensity()
    img=transpose(img)
    img=torch.tensor(img)
    img=img.unsqueeze(0).unsqueeze(0)
    dist,prob=model(img)
    dist=dist.detach().cpu().numpy().squeeze()
    prob=prob.detach().cpu().numpy().squeeze()
    dist=dist.transpose((1,2,0))
    points,prob,dists=non_maximum_suppression(dist,prob,prob_thresh=0.4,nms_thresh=0.3)
    image_shape=img.shape[2:4]
    star_label=polygons_to_label(dists,points,image_shape,prob)
    return star_label
    #label=draw(star_label)
    return label
