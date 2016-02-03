import itertools
import os
import reprlib
from collections import defaultdict

def lc_reader(filename):
    lclist=[]
    facetlist=[]
    facetvalues =[]
    with open(filename) as fp:
        for idx, line in enumerate(fp):
            if line.find('#')==0 and idx == 0:
                facetlist.append([f for f in line.strip().split()])
            elif line.find('#')==0 and idx == 1:
                facetvalues.append([f for f in line.strip().split()])
                facet = dict(zip(facetlist[0], facetvalues[0]))
            if line.find('#')!=0:
                lclist.append([float(f) for f in line.strip().split()])
    return lclist, facet
                

class LightCurve:
    
    def __init__(self, data, metadict):
        self._time = [x[0] for x in data]
        self._amplitude = [x[1] for x in data]
        self._error = [x[2] for x in data]
        self.metadata = metadict
        self.filename = None
    
    @classmethod
    def from_file(cls, filename):
        lclist, metadict = lc_reader(filename)
        instance = cls(lclist, metadict)
        instance.filename = filename
        return instance
    
    def __repr__(self):
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self.timeseries,0,10)))
        components = components[components.find('['):]
        return '{}({})'.format(class_name, components)        
        
    #your code here
    @property
    def time(self):
        return self._time
    
    @property
    def amplitude(self):
        return self._amplitude

    @property
    def timeseries(self):
        return zip(self._time,self._amplitude)
    
    
    def __len__(self):
        return len(self._time)

    def __getitem__(self, index):
        return self._time[index], self._amplitude[index]


class LightCurveDB:
    
    def __init__(self):
        self._collection={}
        self._field_index=defaultdict(list)
        self._tile_index=defaultdict(list)
        self._color_index=defaultdict(list)
    
    def populate(self, folder):
        for root,dirs,files in os.walk(folder): # DEPTH 1 ONLY
            for file in files:
                if file.find('.mjd')!=-1:
                    the_path = root+"/"+file
                    self._collection[file] = LightCurve.from_file(the_path)
    
    def index(self):
        for f in self._collection:
            lc, tilestring, seq, color, _ = f.split('.')
            field = int(lc.split('_')[-1])
            tile = int(tilestring)
            self._field_index[field].append(self._collection[f])
            self._tile_index[tile].append(self._collection[f])
            self._color_index[color].append(self._collection[f])
     
    def retrieve(self, facet, value):
        if facet == 'tile':
            return self._tile_index[value]
        elif facet == 'field':
            return self._field_index[value]
        elif facet == 'color':
            return self._color_index[value]
        