# -*- coding: latin-1 -*-
import logging
from os.path import join, isfile

from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv
from ..functions import fit_bbox_in_shape, _centerInShape


class BinCha(MorphoPlugin):
    """ This plugin create a new segmentation from each barycenters of the selected objects  using a binary threshold on intensity image in the desired channel

    Parameters
    ----------
    Intensity Channel : int, default :0
        The desired channel to apply the binary threshold
    Threshold : int, default :30
        The threshold value using in the intensity image
    Radius : int, default :15
        The radius value of the bounding box around the center of each selected objects
    Intensity channel : int , default 0
        The desired channel to apply the binary threshold
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("BinCha.png")
        self.set_image_name("BinCha.png")
        self.set_name("BinCha : apply a binary threshold on the other channel from selected objects")
        self.add_inputfield("threshold", default=30)
        self.add_inputfield("radius", default=15)
        self.add_inputfield("Intensity Channel", default=0)
        self.set_parent("Create Segmentation")
        self.set_description("This plugin create a new segmentation from each barycenters of the selected objects "
                                "using a binary threshold on intensity image in the desired channel\n \n"
                             "Parameters : \n \n"
                             "- threshold: (float, default 1.) : the theshold value in the intensity images  \n"
                             "- Intensity Channel: (int, default 0.) : The desired channel to apply the binary threshold\n"
                             "- radius: (int, default 30) : radius of the circle inside the bounding box")
    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None

        from skimage.measure import label
        threshold = float(self.get_inputfield("threshold"))
        intensity_channel = int(self.get_inputfield("Intensity Channel"))
        radius = int(self.get_inputfield("radius"))

        cancel = True

        for t in dataset.get_times(objects):  # For each time points in selected object
            cell_updated=[]
            data = dataset.get_seg(t, intensity_channel)
            rawdata = dataset.get_raw(t, intensity_channel)

            if rawdata is None:
                printv("miss raw data at "+str(t), 0)
            elif data is None:
                printv("miss segmentation data at "+str(t), 0)
            else:
                for o in dataset.get_objects_at(objects, t): #For each objects
                    centroid = dataset.get_regionprop("centroid", o) #Get the barycenter
                    centroid=[int(centroid[0]), int(centroid[1]), int(centroid[2])]
                    printv("centroid of "+str(o.id)+" at "+str(o.t)+ " in channel "+str(o.channel)+" is "+str(centroid),2)

                    bbox=[centroid[0]-radius, centroid[1]-radius, centroid[2]-radius,centroid[0]+radius, centroid[1]+radius, centroid[2]+radius] # Get the bounding box with this diameter
                    bbox=fit_bbox_in_shape(bbox,data.shape)#Trunk the box if it gets out of the image shape

                    #CREATE A MASK WITH EXISTING OBJECTS IN THE CHANNEL
                    data_box = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                    raw_box=rawdata[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                    raw_box[data_box>0]=0 #Put at 0 where cells already exist

                    new_data_box = np.uint16(label(np.uint8(raw_box > threshold)))  # Label by connected component
                    new_label=new_data_box[radius,radius,radius]

                    if new_label==0:  # Only background...
                        printv("did not find any new object at this coordinate", 0)
                        printv("the distribution of intensity in this bounding box is "+str(np.unique(rawdata[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]])),1)
                    else:
                        printv("found a new object "+str(o.id)+" at " + str(t) + " for channel "+str(o.channel), 0)
                        data_box[new_data_box == new_label]=o.id
                        cell_updated.append(o.id)
            if len(cell_updated)>0:
                dataset.set_seg(t, data, channel=intensity_channel, cells_updated=cell_updated)  # New ID
                cancel = False

        self.restart(cancel=cancel)




