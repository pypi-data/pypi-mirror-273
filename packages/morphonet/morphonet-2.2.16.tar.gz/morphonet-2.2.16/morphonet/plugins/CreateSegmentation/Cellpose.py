# -*- coding: latin-1 -*-
import logging
from os.path import join, isfile

from morphonet.plugins import MorphoPlugin
import numpy as np

from ...tools import printv
from ..functions import get_torch_device, read_time_points
from skimage.measure import label

def denoise(denoise_model,rawdata,diameter,t):
    # Denoise rawdata with CellPose3 but not working yet.
    if denoise_model is not None:
        printv("denoise z planes  at " + str(t), 0)
        for z in range(rawdata.shape[2]):
            printv("denoise z planes  " + str(z) + "  at " + str(t), 1)
            rawdata[..., z] = denoise_model.eval(rawdata[..., z], channels=[0, 0], diameter=diameter)[..., 0]
    return rawdata

def predict_3D(model,rawdata,dataset,t,diameter,downsampling,denoise_model=None):
    printv("predict the 3D segmentation masks with diameter " + str(diameter), 0)
    voxel_size = dataset.get_voxel_size(t)
    anisotropy = voxel_size[2] / voxel_size[1]
    printv("found anisotropy at " + str(anisotropy), 1)

    if downsampling > 1: rawdata = rawdata[::downsampling, ::downsampling, ::downsampling]
    if denoise_model is not None: rawdata= denoise(denoise_model,rawdata,diameter,t)

    rawdata=np.swapaxes(np.swapaxes(rawdata, 0, 2), 1, 2) #Cell pose is Z,X,Y
    masks = model.eval(rawdata, diameter=int(diameter / downsampling), anisotropy=anisotropy, do_3D=True)
    masks = np.swapaxes(np.swapaxes(masks[0], 0, 2), 0, 1)  # Cell pose is Z,X,Y
    return masks

def predict_2D(model,rawdata,dataset,t,diameter,downsampling,merge_overlap,denoise_model=None):
    printv("predict the 2D segmentation masks with diameter " + str(diameter), 0)
    if downsampling > 1: rawdata = rawdata[::downsampling, ::downsampling, :]
    data = np.zeros(rawdata.shape, dtype=np.uint16)
    last_id = 0
    if denoise_model is not None: rawdata = denoise(denoise_model, rawdata, diameter, t) #FOR CELLPOSE 3

    for z in range(rawdata.shape[2]):
        printv("Predict plane z=" + str(z) + "  at " + str(t), 1)

        masksz = model.eval( rawdata[..., z] , diameter=int(diameter / downsampling))[0]
        printv(
            "found " + str(len(np.unique(masksz)) - 1) + " cells for plane z=" + str(z) + "/"+str(rawdata.shape[2])+" at " + str(t),
            0)
        masksz[masksz > 0] += last_id
        last_id = np.max(masksz)
        data[..., z] = masksz

    if merge_overlap: #Merge 2D Prediction by connected component
        data=label(np.uint8(data>0))
        print(type(data))
        print(np.unique(data))
    return data


class Cellpose(MorphoPlugin):
    """ This plugin uses an intensity image of the membranes from a local dataset at a specific time point, to compute a segmentation of the membranes,
    using the 3D Cellpose deep learning algorithm.

    Parameters
    ----------
    Intensity Channel: int, default : 0
        in case of multiples channel, this correspond to the intensity images channel

    dimension : 3D or 2D :
        to applied CellPose in 2D or 3D

    time points: string (current, begin:end, time1;time2;...)
        on which time point to train

    downsampling : int, default :2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality

    model type : list of models
        The model used to compute segmentations. A detailed documentation on models can be found https://cellpose.readthedocs.io/en/latest/models.html

    model filename: string
        the full filename path to for pretraind model

    diameter: int, default :30
        the average cell size diameter

    Reference : Stringer, C., Wang, T., Michaelos, M. et al. Cellpose: a generalist algorithm for cellular segmentation.
    Nat Methods 18, 100?106 (2021). https://doi.org/10.1038/s41592-020-01018-x
    https://www.cellpose.org
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Cellpose.png")
        self.set_image_name("Cellpose.png")
        self.set_name("CellPose : Perform cell segmentation on intensity images")
        self.add_inputfield("Intensity Channel", default=0)
        self.add_inputfield("downsampling", default=1)
        self.add_inputfield("diameter", default=30)
        self.add_dropdown("model type",['cyto','nuclei','tissuenet','livecell', 'cyto2', 'general','CP', 'CPx', 'TN1', 'TN2', 'TN3', 'LC1', 'LC2', 'LC3', 'LC4'])
        self.add_filepicker("pretrained model",default=None,Optional=True)
        self.add_toggle("merge 2D overlap", default=True)
        self.add_dropdown("dimension", ['3D', '2D'])
        self.add_inputfield("time points", default="current")
        #self.add_dropdown("denoise model type",['no-denoising', 'denoise-cyto3', 'deblur-cyto3', 'upsample-cyto3', 'denoise-nuclei','deblur-nuclei', 'upsample-nuclei'])
        self.set_parent("Create Segmentation")
        self.set_description( "This plugin use the CellPose algorithm to compute cell segmentation on intensity image  "
                              "If you first select objects, CellPose will run on the bounding box defined by theses objects "
                              "otherwise, CellPose will run on the full 3D images at the given times points.\n \n"
                             "Parameters : \n \n "
                               "- Intensity Channel:  in case of multiples channel, this correspond to the intensity images channel on which CellPose will be applied \n"
                             "- downsampling (numeric,default:2) : he resolution reduction applied to each axis of the "
                              "input image before performing segmentation, 1 meaning that no reduction is applied. "
                              "Increasing the reduction factor may reduce segmentation quality \n"
                             "- diameter: (float, default 30.) : the average cell size diameter (Use Measurement in Tools to define it). \n" 
                             "- model type : The model used to compute segmentations. A detailed documentation on models"
                              " can be found https://cellpose.readthedocs.io/en/latest/models.html \n"
                              "- dimension: apply Cellpose in 3D or 2D . \n" 
                               "- merge 2D overlap: when cellpose is applied in 2D, do you want to merge the objects detected in z by overlapping? \n" 
                              "- pretrained model: choose a file if you want to use a pretrained model (model type will not be used)\n" 
                            "- time points : apply CellPose at the current time point or specify the number or specify the begin:end")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None
        #import scipy.special._cdflib
        from cellpose import models
        from skimage.transform import resize
        import logging
        logging.basicConfig(level=logging.INFO) #To have cellpose log feedback on the terminalk

        which, device = get_torch_device()
        printv("CellPose  will run on " + which, 1)

        downsampling = int(self.get_inputfield("downsampling"))
        intensity_channel= int(self.get_inputfield("Intensity Channel"))
        diameter = int(self.get_inputfield("diameter"))
        dimension = self.get_dropdown("dimension")
        model_type = self.get_dropdown("model type")
        merge_overlap=self.get_toggle("merge 2D overlap")

        denoise_model = None
        '''For Cellpose 3 which not working yet ...
        denoise_model_type = self.get_dropdown("denoise model type")
        if denoise_model_type != "no-denoising":
            from cellpose.denoise import DenoiseModel
            denoise_model = DenoiseModel(model_type=denoise_model_type.replace("-", "_"), gpu=True)
        '''
        pretrained_model=self.get_filepicker("pretrained model")
        if pretrained_model!="" and isfile(pretrained_model):
            printv("load the pretrained model " + pretrained_model, 0)
            model = models.CellposeModel(gpu=which == "GPU", device=device, pretrained_model=pretrained_model)
        else:
            printv("load the model " + model_type, 0)
            model = models.CellposeModel(gpu=which == "GPU", device=device, model_type=model_type)

        cancel = True
        #If objects are selected, we run cellpose on the global bounding box of the object
        if len(objects)>=1 and objects[0]!="":
            for t in dataset.get_times(objects):  # Get all times in the labeled objects list
                rawdata = dataset.get_raw(t, intensity_channel)
                data = dataset.get_seg(t, intensity_channel)
                if rawdata is not None and data is not None:

                    bbox = None  # Get the bounding box arround the selected cells
                    for o in dataset.get_objects_at(objects, t):
                        printv("add object " + str(o.id) + " at " + str(o.t),1)
                        bb = dataset.get_regionprop("bbox", o)
                        if bbox is None: bbox=bb
                        else:   bbox=[min(bb[0],bbox[0]),min(bb[1],bbox[1]),min(bb[2],bbox[2]),max(bb[3],bbox[3]),max(bb[4],bbox[4]),max(bb[5],bbox[5])]

                    rawdata_box = rawdata[bbox[0]:bbox[3]+1, bbox[1]:bbox[4]+1, bbox[2]:bbox[5]+1]
                    if dimension == "3D":  data_box = predict_3D(model,rawdata_box,dataset,t,diameter,1,denoise_model=denoise_model) #We do not apply downsampling for selected objectss
                    else:   data_box = predict_2D(model,rawdata_box,dataset,t,diameter,1,merge_overlap,denoise_model=denoise_model)

                    cells=np.unique(data_box)
                    nb_cells = len(cells)
                    if nb_cells == 1:  # Only background...
                        printv("did not find any cells ", 0)
                    else:
                        cells_updated = []
                        printv("found " + str(nb_cells) + " cells  at " + str(t), 0)

                        #Now We have to merge this new segmentation inside the selected masks
                        data_mask=np.zeros(rawdata_box.shape,dtype=np.uint16)
                        for o in dataset.get_objects_at(objects, t):
                            cells_updated.append(o.id)
                            coords = dataset.np_where(o)
                            data_mask[coords[0] -bbox[0], coords[1] -bbox[1],coords[2] -bbox[2]] = True
                        data_box[data_mask==False]=0 #Cut everything out of this masks

                        #Now we have to give the new cells ids
                        last_id = dataset.get_last_id(t)
                        data_box[data_box>0]+=last_id
                        data[bbox[0]:bbox[3]+1, bbox[1]:bbox[4]+1, bbox[2]:bbox[5]+1][data_mask==True]=data_box[data_mask==True]
                        for c in cells:
                            if c>0:
                                cells_updated.append(c+last_id)
                        print(" --> cells_updated="+str(cells_updated))
                        dataset.set_seg(t, data, channel=intensity_channel, cells_updated=cells_updated)  # ALL
                        cancel = False

        else: #Predict on the full images
            times = read_time_points(self.get_inputfield("time points"), t)
            if len(times) == 0:
                printv("No time points", 0)
            else:
                for t in  times:
                    rawdata = dataset.get_raw(t,intensity_channel)
                    init_shape = rawdata.shape
                    if rawdata is not None:
                        if dimension=="3D":
                            data = predict_3D(model,rawdata,dataset,t,diameter,downsampling,denoise_model=denoise_model)
                        else:
                            data = predict_2D(model,rawdata,dataset,t,diameter,downsampling,merge_overlap,denoise_model=denoise_model)
                        if dataset.background != 0:
                            data[data==0] = dataset.background
                        nb_cells = len(np.unique(data))
                        if nb_cells == 1:  # Only background...
                            printv("did not find any cells", 0)
                        else:
                            printv("found " + str(nb_cells) + " cells  at " + str(t), 0)
                            if downsampling > 1: data = resize(data, init_shape, preserve_range=True, order=0)
                            dataset.set_seg(t, data, channel=intensity_channel, cells_updated=None)  # ALL
                            cancel = False



        logging.basicConfig(level=logging.WARNING)
        self.restart(cancel=cancel)




