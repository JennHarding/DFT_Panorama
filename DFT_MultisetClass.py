import math
import numpy as np


class MultiSetArray(object):
    def __init__(self, array, measure_range=None, log_weight=True):
        self.original_array = array
        self.measure_range = measure_range
        if measure_range is not None:
            self.start_measure = measure_range[0]
            self.end_measure = measure_range[1]
        self.log_weight = log_weight

    def log_weighting(self):
        return [math.log(element + 1, 2) for element in self.original_array]
    
    def all_complex(self):
        if self.log_weight is True:
            return np.fft.fft(self.log_weighting())
        else:
            return np.fft.fft(self.original_array)
    
    def all_magnitudes(self):
        return list(np.abs(self.all_complex()))
    
    def all_phases(self):
        return list(np.angle(self.all_complex(), deg=True))
    
    def make_mag_dict(self):
        return {f'f{i}' : self.all_magnitudes()[i] for i in range(1, 7)}
    
    def make_phase_dict(self):
        return {f'f{i}' : self.all_phases()[i] for i in range(1, 7)}
    
    def round_log_array(self):
        return[round(x, 2) for x in self.log_weighting()]
    
    def round_original_array(self):
        return [round(x, 2) for x in self.original_array]
    
    def __repr__(self):
        return '<'+str([round(x, 2) for x in self.original_array])+'>'

    