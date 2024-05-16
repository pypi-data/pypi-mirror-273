# -*- coding: latin-1 -*-
import logging
from os.path import join, isfile, basename, abspath,dirname

from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv, imsave, mkdir, cp, rmrf,normalize
from ..functions import get_torch_device, read_time_points
from skimage.measure import regionprops


def denoise_train(denoise_model,rawdata,data,t):
    #Denoise rawdata with CellPose3 but not working yet.
    if denoise_model is not None:
        printv("denoise z planes  at " + str(t), 0)
        for z in range(rawdata.shape[2]):
            regions=regionprops(data[...,z])
            diameter=0.0
            nbdiameter=0
            for r in regions:
                if r['label']!=0:
                    diameter+=r['equivalent_diameter_area']
                    nbdiameter+=1
            if nbdiameter>0:   diameter/=nbdiameter
            else : diameter=30 #Default value
            printv("denoise z planes  " + str(z) + "  at " + str(t)+ " with average diameter "+str(diameter), 1)
            rawdata[..., z] = denoise_model.eval(rawdata[..., z], channels=[0, 0], diameter=diameter)[..., 0]
    return rawdata


class CellposeTrain(MorphoPlugin):
    """ This plugin uses an intensity image of the membranes from a local dataset at a specific time point, to compute a segmentation of the membranes,
    using the 3D Cellpose deep learning algorithm.

    Parameters
    ----------
    Intensity Channel: int, default : 0
        in case of multiples channel, this correspond to the intensity images channel

    epochs : int, default : 20
        number of epochs of training

    dimension : 3D or 2D :
        For 2D: use XY planes to train
        For 3D: extract XY, YZ,YX planes to train

    time points: string (current, begin:end, time1;time2;...)
        on which time point to train

    number 2D images per epochs: int, default : 8
        batch size

    downsampling : int, default :2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality

    model type : list of models
        The model used to compute segmentations. A detailed documentation on models can be found https://cellpose.readthedocs.io/en/latest/models.html

    model filename: string
        full filename path to save the model

    Reference : Stringer, C., Wang, T., Michaelos, M. et al. Cellpose: a generalist algorithm for cellular segmentation.
    Nat Methods 18, 100?106 (2021). https://doi.org/10.1038/s41592-020-01018-x
    https://www.cellpose.org
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("CellposeTrain.png")
        self.set_image_name("CellposeTrain.png")
        self.set_name("CellPose Train  : Train the CellPose model on your own data")
        self.add_inputfield("Intensity Channel", default=0)
        self.add_inputfield("downsampling", default=1)
        self.add_inputfield("epochs", default=20)
        self.add_dropdown("dimension", ['2D', '3D'])
        self.add_dropdown("model type",['cyto','nuclei','tissuenet','livecell', 'cyto2', 'general','CP', 'CPx', 'TN1', 'TN2', 'TN3', 'LC1', 'LC2', 'LC3', 'LC4'])
        self.add_inputfield("time points", default="current")
        self.add_inputfield("number 2D images per epochs", default=8)
        #self.add_dropdown("denoise model type",['no-denoising', 'denoise-cyto3', 'deblur-cyto3', 'upsample-cyto3', 'denoise-nuclei','deblur-nuclei', 'upsample-nuclei'])
        self.add_filesaver("model filename")
        self.set_parent("Create Segmentation")
        self.set_description("This plugin train the CellPose algorithm on your own data (based on the model type) \n \n"
                             "Parameters : \n \n "
                             "- downsampling (numeric,default:2) : he resolution reduction applied to each axis of the "
                             "input image before performing segmentation, 1 meaning that no reduction is applied. "
                             "Increasing the reduction factor may reduce segmentation quality \n"
                             "- epochs: ( default 20.) : the number of epochs to train the algorithm \n"
                             "- model type : The model used to compute segmentations. A detailed documentation on models"
                             " can be found https://cellpose.readthedocs.io/en/latest/models.html \n"
                             "- dimension: train Cellpose on the 3 axes (XY,XZ and YZ) for 3D or only on XY planes (2D). \n"
                             "- number 2D images per epochs: batch size, depending on your image size, decrease it in case of memory issue.  \n"
                             "- Intensity Channel:  in case of multiples channel, this correspond to the intensity images channel on which CellPose will be train \n"
                             "- time points : apply CellPose at the current time point or specify the number or specify the begin:end\n"
                             "- model filename : choose a file to save to model")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        from cellpose import models
        import logging
        logging.basicConfig(level=logging.INFO) #To have cellpose log feedback on the terminalk

        which,device=get_torch_device(mps=False) #Seems that we cannot train when MPS architecture is active ...
        printv("CellPose Train will run on " + which, 1)

        intensity_channel= int(self.get_inputfield("Intensity Channel"))
        downsampling = int(self.get_inputfield("downsampling"))
        model_type = self.get_dropdown("model type")
        n_epochs = int(self.get_inputfield("epochs"))
        nimg_per_epoch=int(self.get_inputfield("number 2D images per epochs"))
        dimension = self.get_dropdown("dimension")

        #We first same the model in a temporary Path
        model_filename=self.get_filesaver("model filename")
        train_dir = dataset.parent.temp_path
        model_name=basename(model_filename)

        denoise_model = None
        '''
        #FOR CELLPOSE 3 but not working yet ...
        denoise_model_type = self.get_dropdown("denoise model type")
        if denoise_model_type != "no-denoising":
            from cellpose.denoise import DenoiseModel
            denoise_model = DenoiseModel(model_type=denoise_model_type.replace("-", "_"), gpu=True)
        '''
        learning_rate = 0.1
        weight_decay = 0.0001
        channels = [0,0]

        times=read_time_points(self.get_inputfield("time points"),t)
        if len(times)==0:
            printv("No time points",0)
        else:
            printv(" Train on "+str(times)+ " time point",2)

            #Colllect the selected data at the given time point
            train_data = []
            train_labels = []

            for t in times:
                rawdata = dataset.get_raw(t, intensity_channel)
                data = dataset.get_seg(t, intensity_channel)
                nb_image=0
                nb_cells=0
                if dimension=="3D":
                    if downsampling > 1:
                        data = data[::downsampling, ::downsampling, ::downsampling]
                        rawdata = rawdata[::downsampling, ::downsampling, ::downsampling]
                    if dataset.background != 0: data[   data == dataset.background] = 0  # We do it after the rescaling to go faster
                    if denoise_model is not None: rawdata = denoise_train(denoise_model, rawdata,data,t)

                    for dim in range(3):
                        for c in range(data.shape[dim]): #ADD Slicdes
                            if dim==0:
                                rawslice=rawdata[c,...]
                                segslice=data[c,...]
                            elif dim==1:
                                rawslice = rawdata[:,c,:]
                                segslice = data[:,c,:]
                            else:
                                rawslice = rawdata[...,c]
                                segslice = data[...,c]

                            im = np.reshape(rawslice, (1,) + rawslice.shape)
                            cells = np.unique(segslice)
                            if len(cells) > 5:  # Minimum Required by Cell Pose
                                train_data.append(im)
                                train_labels.append(segslice)
                                nb_image+=1
                                nb_cells += len(cells) - 1
                else: #2D
                    if downsampling>1:
                        data=data[::downsampling,::downsampling,:]
                        rawdata = rawdata[::downsampling, ::downsampling, :]

                    if dataset.background != 0: data[data == dataset.background] = 0  # We do it after the rescaling to go faster
                    if denoise_model is not None: rawdata = denoise_train(denoise_model, rawdata,data,t)

                    for c in range(data.shape[2]):  # ADD Slicdes
                        segslice = data[..., c]
                        cells=np.unique(segslice)
                        if len(cells) > 5:  # Minimum Required by Cell Pose
                            train_data.append(rawdata[..., c])
                            train_labels.append(segslice)
                            nb_image+=1
                            nb_cells+=len(cells)-1
                printv(str(nb_cells)+" "+dimension+" cells added at " + str(t), 0)

            if len(train_data)==0:
                printv("ERROR Cannot Train with not images",0)
            else:
                printv("Start Train CellPose on " + str(len(train_data)) + " 2D images from model : "+model_type,0)
                if isfile(model_filename): #Continue to train
                    printv("Found a pretrained model, continue to train on "+model_filename,1)
                    model = models.CellposeModel(gpu=which=="GPU", device=device, pretrained_model=model_filename)
                else:
                    model = models.CellposeModel(gpu=which=="GPU", device=device, model_type=model_type)

                #CELLPOSE 3
                #from cellpose import train
                #model_path = train.train_seg(model.net, train_data=train_data, train_labels=train_labels,  channels=channels,   save_path=train_dir,   n_epochs=n_epochs,   normalize=True,    learning_rate=learning_rate,   weight_decay=weight_decay,   nimg_per_epoch=nimg_per_epoch,  model_name=model_name)

                #CELLPOSE 2
                model_path = model.train(train_data, train_labels,
                                         channels=channels,
                                         save_path=train_dir,
                                         n_epochs=n_epochs,
                                         normalize=True,
                                         learning_rate=learning_rate,
                                         weight_decay=weight_decay,
                                         nimg_per_epoch=nimg_per_epoch,
                                         model_name=model_name)


                if not isfile(join(train_dir,"models",model_name)): #CellPose automaticaly add "models"
                    printv("Error miss temporary model  "+str(join(train_dir,"models",model_name)),0)
                else:
                    cp(join(train_dir,"models",model_name),dirname(abspath(model_filename)))
                    if not isfile(model_filename):
                        printv("Error miss  model  " +model_filename, 0)
                        printv("look in the temporary folder "+str(join(train_dir,"models",model_name)),1)
                    else:
                        printv("Model Saved into "+model_filename,0)
                        rmrf(join(train_dir,"models"))  #Delete temporary folder

        logging.basicConfig(level=logging.WARNING)
        self.restart(cancel=True) #We do not change anything




