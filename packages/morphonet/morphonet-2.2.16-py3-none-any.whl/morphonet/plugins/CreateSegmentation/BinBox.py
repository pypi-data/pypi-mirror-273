# -*- coding: latin-1 -*-
import logging
from os.path import join, isfile

from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv
from ..functions import fit_bbox_in_shape, _centerInShape,get_seeds_in_image


class BinBox(MorphoPlugin):
    """ This plugin apply a threshold to intensity image on a bouding box and create label by connected component

    Parameters
    ----------
    Threshold : int, default :1
        The threshold value
    Time points : basestring , default:current
        The time range for binarization
    radius : int , default : 15
        The radius value of the bounding box around the center of each selected objects
    Intensity channel : int , default 0
        The desired channel to apply the binary threshold

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("BinBox.png")
        self.set_image_name("BinBox.png")
        self.set_name("BinBox : apply a threshold to intensity image inside a Bounding Box")
        self.add_inputfield("threshold", default=1)
        self.add_coordinates("Add a Seed")
        self.add_inputfield("radius", default=15)
        self.add_inputfield("Intensity Channel", default=0)
        self.set_parent("Create Segmentation")
        self.set_description("This plugin apply a threshold to intensity image on a bouding box and label each binary objects by connected component\n"
                             "Parameters : \n \n"
                             "- threshold: (float, default 1.) : the theshold value in the intensity images  \n"
                             "- Seed:  : seed added in the GUI  \n"
                             "- radius: (int, default 30) : radius of the circle inside the bounding box   \n"
                             "- intensity channel: (int, default 0) : The desired channel to apply the binary threshold  \n"
                             "- time points : apply CellPose at the current time point or specify the number or specify the begin:end")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        from skimage.measure import label
        threshold = float(self.get_inputfield("threshold"))
        intensity_channel = int(self.get_inputfield("Intensity Channel"))
        radius = int(self.get_inputfield("radius"))

        seeds = self.get_coordinates("Add a Seed")  # Get list of seeds coordinates from MorphoNet seed system
        if len(seeds) != 1:
            printv("only one seed is require for this plugin", 0)
            self.restart(cancel=True)
            return None
        seeds = get_seeds_in_image(dataset, seeds) # Get coordinates of the seeds in the image (coordinates in morphonet != coordinates in images)
        data = dataset.get_seg(t, intensity_channel)
        rawdata = dataset.get_raw(t, intensity_channel)



        if rawdata is None :
            printv("miss raw data ",0)
            self.restart(cancel=True)
            return None
        if data is None:
            printv("miss segmentation data ", 0)
            self.restart(cancel=True)
            return None

        cancel = True
        for seed in seeds: # For each seed
            if not _centerInShape(seed, data.shape): # if seed is in image
                printv("the seed "+str(seed)+" is not in the image", 0)
            else:
                bbox=[seed[0]-radius, seed[1]-radius, seed[2]-radius,seed[0]+radius, seed[1]+radius, seed[2]+radius] # Get the bounding box with this diameter
                bbox=fit_bbox_in_shape(bbox,data.shape)

                new_data_box = label(np.uint8(rawdata[bbox[0]:bbox[3],bbox[1]:bbox[4],bbox[2]:bbox[5]] > threshold))  # Label by connected component
                new_cells = np.unique(new_data_box)

                if len(new_cells) == 1:  # Only background...
                    printv("did not find any cells", 0)
                else:
                    cells_updated = []

                    printv("found " + str(len(new_cells))+ " cells  at " + str(t), 0)
                    last_id = dataset.get_last_id(t)
                    for c in new_cells:
                        if c>0:
                            cells_updated.append(c+last_id)

                    data_box = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                    data_mask=new_data_box > 0
                    cells = np.unique(data_box[data_mask])
                    for c in cells:
                        if c != dataset.background:
                            printv("this cell" + str(c) + " already exist in the bounding box will be modify", 0)
                            cells_updated.append(c)

                    data_box[data_mask]=new_data_box[data_mask]+last_id
                    dataset.set_seg(t, data, channel=intensity_channel, cells_updated=cells_updated)  # ALL
                    cancel = False

        self.restart(cancel=cancel)




