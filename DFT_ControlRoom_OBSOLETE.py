#%%
import pandas as pd
from functools import partial

import DFT_UserInputs as UI
import DFT_Functions as Funcs
import DFT_Graphing as Graph

user_inputs = UI.get_user_input()

score_data = Funcs.score_to_data(user_inputs.values())

# %%
general_info = {'Window Number' : [x for x in range(1, len(score_data) + 1)],
         'Weighted Array' : [str(a.round_log_array()) for a in score_data],
         'Original Array' : [str(a.round_original_array()) for a in score_data],
         'Measure Range' : [f'Measures {a.start_measure}–{a.end_measure}' for a in score_data]
         }

phases = {f'f{i} Phase' : [a.make_phase_dict()[f'f{i}'] for a in score_data] for i in range(1, 7)}
quantized_phases = {f'f{i} Quantized Phase' : map(partial(Funcs.quantize_list), [a.make_phase_dict()[f'f{i}'] for a in score_data]) for i in range(1, 7)}
magnitudes = {f'f{i} Magnitude' : [a.make_mag_dict()[f'f{i}'] for a in score_data] for i in range(1, 7)}

master_dict = {**general_info, **phases, **quantized_phases, **magnitudes}

general_df = pd.DataFrame(general_info)
phase_df = pd.DataFrame(phases)
quant_phase_df = pd.DataFrame(quantized_phases)
mag_df = pd.DataFrame(magnitudes)
master_df = pd.concat(dict(General = general_df, Magnitudes = mag_df, Phases = phase_df, QuantizedPhases = quant_phase_df), axis=1)
#%%

save_info = f"NAME_{user_inputs['window']}beat_{user_inputs['strategy']}"
title = f"NAME: {user_inputs['window']}-Beat Window, {user_inputs['strategy']}"

#%%
Graph.make_panorama(df=master_df, title=title, savehtml=None)

#%%

Graph.individual_panorama(df=master_df, coefficient=3, color_dict=Graph.rgb_colors, title=title, savehtml=None)

# %%

Graph.magnitudes_panorama(df=master_df, color_dict=Graph.rgb_colors, title=title, savehtml=None)

# %%
