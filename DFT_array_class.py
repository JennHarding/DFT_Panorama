import numpy as np


class dft_array(object):
    def __init__(self, array, measure_range=None, log_weight=True):
        self.original_array = array
        self.measure_range = measure_range
        if measure_range is not None:
            self.start_measure = measure_range[0]
            self.end_measure = measure_range[1]
        self.log_weight = log_weight
    
    def do_dft(self):
        if self.log_weight is True:
            return np.fft.fft(np.log2(self.original_array + 1))
        else:
            return np.fft.fft(self.original_array)
    
    def mag_dict(self):
        return {f'f{i}' : np.abs(self.do_dft())[i] for i in range(1, 7)}
    
    def phase_dict(self):
        return {f'f{i}' : np.angle(self.do_dft(), deg=True)[i] for i in range(1, 7)}
    
    def rounded_weighted_array(self):
        return np.around(np.log2(self.original_array), decimals=2)
    
    def rounded_original_array(self):
        return np.around(self.original_array, decimals=2)
        
    