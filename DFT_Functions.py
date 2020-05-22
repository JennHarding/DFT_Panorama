
from music21 import stream, note, pitch, chord, meter, corpus, converter
import numpy as np

import DFT_Corpus as CP
from DFT_array_class import dft_array


def quantize_array(array, quant=12):
    """Quantizes the values of an array to the nearest of 12 "nodes."

    Arguments:
        array {numpy array} -- Numpy array with the phase values for each component

    Keyword Arguments:
        quant {int} -- Number of nodes around the component circle (default: {12})

    Returns:
        numpy array -- Numpy array with the quantized phase values for each component
    """
    spacing = 360/quant
    q = np.around(array/spacing)
    return q * spacing
  

def parse_score(score_string, excerpt=None):
    """Converts an encoded musical score into a music21 stream object.

    Arguments:
        score_string {string} -- path to file

    Keyword Arguments:
        excerpt {tuple} -- beginning and ending measures if it is an excerpt (default: {None})

    Returns:
        stream -- music21 stream object
    """
    if score_string in CP.music21_corpus:
        working_score = corpus.parse(score_string)
    elif score_string in CP.local_corpus:
        working_score = converter.parse(score_string)

    if excerpt:
        return working_score.measures(excerpt[0], excerpt[1])
    else:
        return working_score


def split_time_signature(numerator):
    """Divides the numerator of a time signature into its beat groupings; e.g. 11 becomes 3+3+3+2.

    Arguments:
        numerator {int} -- numerator of a time signature

    Returns:
        list -- all of the beat groupings
    """
    if numerator < 4:
        return [numerator]
    elif numerator == 4:
        return [2, 2]
    else: 
        return [3, *split_time_signature(numerator-3)]


def convert_time_signature(ts):
    """Changes a time signature object to a meter sequence object.

    Arguments:
        ts {time signature (music21)} -- music21 time signature object

    Returns:
        meter sequence (music21) -- music21 meter sequence object divided into beat groupings
    """
    ms = meter.MeterSequence(ts.ratioString)
    if ms.numerator in [2, 3, 4]:
        ms.partitionByCount(ms.numerator)
    else:
        partition_list = split_time_signature(ts.numerator)
        ms.partitionByList(partition_list)
    return ms


def get_beat_offsets_from_score(score):
    """Finds the offset of every beat in the score.

    Arguments:
        score {stream (music21)} -- music21 string object

    Returns:
        list -- list of all offsets that are beats
    """
    time_signature_list = []
    meter_sequence_list = []
    offset_list = [0]
    for m in score.semiFlat.getElementsByClass('Measure'):
        if m.timeSignature is not None:
            time_signature_list.append(m.timeSignature)
        else:
            time_signature_list.append(m.getContextByClass('TimeSignature'))
        
    for ts in time_signature_list:
        meter_sequence_list.extend(convert_time_signature(ts))
        
    duration_list = [m.duration for m in meter_sequence_list]

    for idx, i in enumerate(duration_list):
        offset_list.append(i.quarterLength + offset_list[idx])
    
    return offset_list


def update_array(array, note_, strategy):
    """Increments the array at a particular pitch class's position based on the requested strategy.

    Arguments:
        array {array} -- array with 12 positions representing the 12 pitch classes
        note_ {note (music21)} -- music21 note object
        strategy {string} -- option of 'Onset', 'Duration', or 'Flat'

    Returns:
        arra -- array after incrementation
    """
    if strategy == 'Onset':
        array[note_.pitch.pitchClass] += 1
    elif strategy == 'Duration':
        array[note_.pitch.pitchClass] += note_.quarterLength
    elif strategy == 'Flat':
        array[note_.pitch.pitchClass] = 1
    return array


def get_measure_number(score, offset):
    """Finds the measure number of an object given its offset in the score

    Arguments:
        score {stream (music21)} -- music21 stream object
        offset {float} -- distance from the beginning of the piece measured in quarter-note lengths

    Returns:
        int -- the measure number
    """
    beat_measure_tuple = score.beatAndMeasureFromOffset(offset)
    measure_number = beat_measure_tuple[1].number
    return measure_number
    
    
def sliding_window(score, beat_offset_list, window_size, strategy, log=True, edo=12):
    """Runs the sliding window across the score and generates arrays of pitch classes to be used as DFT inputs.

    Arguments:
        score {stream (music21)} -- music21 stream object
        beat_offset_list {list} -- list of the offsets of all beats
        window_size {int} -- length of sliding window measured in beats (NOT quarter-lengths)
        strategy {string} -- strategy options are 'Onset', 'Duration', and 'Flat'

    Keyword Arguments:
        log {bool} -- applies a logarithmic weight to the array (default: {True})
        edo {int} -- number of pitches that equally divide the octave (default: {12})

    Returns:
        list -- list of all multiset arrays
    """
    all_arrays = []
    for idx, window_begin in enumerate(beat_offset_list[:-window_size]):
        window_end = beat_offset_list[idx + window_size]
        current_array = np.array([0.0]*12)
        measure1 = get_measure_number(score=score, offset=window_begin)
        if window_end == beat_offset_list[-1]:
            measure2 = get_measure_number(score=score, offset=beat_offset_list[-2])
        else:
            measure2 = get_measure_number(score=score, offset=window_end)
        
        for elem in score.semiFlat.getElementsByOffset(
            offsetStart=window_begin, 
            offsetEnd=window_end, 
            includeEndBoundary=False).getElementsByClass(['Note', 'Chord']):
            
            if isinstance(elem, chord.Chord):
                for a in elem.notes:
                    current_array = update_array(
                        array=current_array, 
                        note_=a, 
                        strategy=strategy)
            elif isinstance(elem, note.Note):
                current_array = update_array(
                    array=current_array, 
                    note_=elem, 
                    strategy=strategy)

        all_arrays.append(dft_array(
            array=current_array, 
            log_weight=log, 
            measure_range=(measure1, measure2)))
        
    return all_arrays


def score_to_data(config):  
    """Generates all multisets by sliding a window over the score

    Arguments:
        config {tuple} -- all user inputs

    Returns:
        list -- all multisets
    """
    repertoire, excerpt, window, strat, log = config
    parsed_score = parse_score(score_string=repertoire, excerpt=excerpt)
    beat_offset_list = get_beat_offsets_from_score(score=parsed_score.parts[0])

    if strat == "Duration":
        adjusted_score = parsed_score.sliceByBeat(addTies=False)
    else:
        adjusted_score = parsed_score.stripTies(retainContainers=True)
    
    multisets = sliding_window(
        score=adjusted_score, 
        beat_offset_list=beat_offset_list, 
        window_size=window, 
        strategy=strat, 
        log=log)

    return multisets