# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class Match(MorphoPlugin):
    """ This plugin allows you to match the elements of same object across several channels.

    Parameters
    ----------
    Objects:
        The selected or labeled objects on MorphoNet
    """

    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Match.png")
        self.set_image_name("Match.png")
        self.set_name("Match : Match the selected objects")
        self.set_parent("Edit Objects")
        self.set_description("This plugin allows you to match the elements of same object across several channels."
                             "If multiple objects are selected , they are fused together at the current time point. "
                             "Else if objects are labeled it will apply a fusion between all objects sharing the same "
                             "label (for each individual time points)")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        for t in dataset.get_times(objects):  # For each time points in selected object
            tomatch = {}
            for o in dataset.get_objects_at(objects, t):  # Get the list of ids to match  , split with the differents selections (each selection will be match)
                if o.s not in tomatch:   tomatch[o.s] = []
                tomatch[o.s].append(o)

            cells_updated_by_channels={}
            for s in tomatch:  # For each selected group of cells to match together
                if len(tomatch[s]) > 1:  # match only if we have multiple objects

                    last_id=dataset.get_last_id(t) + 1
                    printv("Match objects " + str(tomatch[s]) + " at " + str(t) + " into object " + str(last_id), 0)
                    for o in tomatch[s]:
                        dataset.set_cell_value(o,last_id)
                        dataset.del_cell_from_properties(o)
                        if o.channel not in cells_updated_by_channels:cells_updated_by_channels[o.channel]=[]
                        if o.id not in cells_updated_by_channels[o.channel]:  cells_updated_by_channels[o.channel].append(o.id)
                        if last_id not in cells_updated_by_channels[o.channel]: cells_updated_by_channels[o.channel].append(last_id)

                        # Create a new object for Lineage Modification
                        nc=dataset.get_object(t,last_id,o.channel)
                        for m in o.mothers:
                            dataset.del_mother(o,m)
                            dataset.add_mother(nc,m)

                        for d in o.daughters:
                            dataset.del_daughter(o, d)
                            dataset.add_daughter(nc,d)


            if len(cells_updated_by_channels)>0: #Update the segmentation
                for channel in cells_updated_by_channels:
                    dataset.set_seg(t,dataset.get_seg(t,channel),channel=channel,cells_updated=cells_updated_by_channels[channel])

        self.restart()   #Send data to morphonet
