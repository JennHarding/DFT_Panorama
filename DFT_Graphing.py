import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import sin



rgb_colors = {'f1_colors' : ['rgba(130,202,252,0.4)', 'rgba(61,122,253,0.6)', 'rgba(30,72,143,1)'], 
              'f2_colors' : ['rgba(255,223,34,0.4)', 'rgba(242,171,21,0.6)', 'rgba(127,78,30,1)'], 
              'f3_colors' : ['rgba(99,171,21,0.4)', 'rgba(105,131,57,0.6)', 'rgba(5,71,42,1)'],
              'f4_colors' : ['rgba(207,98,117,0.4)', 'rgba(212,106,126,0.6)', 'rgba(117,8,81,1)'], 
              'f5_colors' : ['rgba(196,142,253,0.4)', 'rgba(133,103,152,0.6)', 'rgba(67,5,65,1)'], 
              'f6_colors' : ['rgba(211,182,131,0.4)', 'rgba(127,104,78,0.6)', 'rgba(65,2,0,1)']}


def make_panorama(df, color_dict=rgb_colors, title=None, savehtml=None):
    """Makes master panorama interactive plot with all magnitudes, all phases, and all quantized phases.

    Arguments:
        df {dataFrame} -- pandas dataframe 

    Keyword Arguments:
        color_dict {dictionary} -- dictionary of rgba colors (default: {rgb_colors})
        title {string} -- title of the plot (default: {None})
        savehtml {string} -- save location for the html file (default: {None})
    """
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.update_layout(autosize=False, width=1000, height=400)
    
    for i in range(1, 7):

        fig.add_trace(go.Scatter(
            y=df['Phases'][f'f{i} Phase'], 
            mode='lines', 
            name=f'f{i} Phase',
            line=dict(color=color_dict[f'f{i}_colors'][1]),
            text=df['General']['Original Array'],
            customdata=df['General']['Measure Range'],
            hovertemplate = 
            "Measure Range: %{customdata} <br>"+
            "Phase: %{y}<br>"+
            "Original Array: %{text}",   
            visible='legendonly',
        ), secondary_y=False)
        
        fig.add_trace(go.Scatter(
            y=df['QuantizedPhases'][f'f{i} Quantized Phase'], 
            mode='lines', 
            name=f'f{i} Quantized Phase',
            line=dict(color=color_dict[f'f{i}_colors'][2]),   
            text=df['General']['Original Array'],
            customdata=df['General']['Measure Range'],
            hovertemplate = 
            "Measure Range: %{customdata} <br>"+
            "Quantized Phase: %{y}<br>"+
            "Original Array: %{text}",
            visible='legendonly',
        ), secondary_y=False)
        
        fig.add_trace(go.Scatter(    
            y=df['Magnitudes'][f'f{i} Magnitude'], 
            mode='lines', 
            fill='tozeroy', 
            fillcolor=color_dict[f'f{i}_colors'][0], 
            name=f'f{i} Magnitude', 
            line=dict(color=color_dict[f'f{i}_colors'][0]), 
            y0=0,
            dy=2,            
            text=df['General']['Original Array'],
            customdata=df['General']['Measure Range'],
            hovertemplate = 
            "Measure Range: %{customdata} <br>"+
            "Magnitude: %{y}<br>"+
            "Original Array: %{text}",  
        ), secondary_y=True)

    fig.update_yaxes(secondary_y=False, 
                     nticks=13, 
                     tick0=-180, 
                     dtick=30, 
                     overwrite=True, 
                     title='Phase',
                     showgrid=True,
                     gridcolor='rgb(222,222,222)')
    
    fig.update_yaxes(secondary_y=True, 
                     nticks=6, 
                     showgrid=False, 
                     title='Magnitude' )
    
    fig.update_xaxes(tick0=1, 
                     dtick=10, 
                     showgrid=False, 
                     title='Window Number')
    
    fig.update_layout(hoverlabel=dict(font_size=16), 
                      font=dict(family='Courier New, monospace', size=16),
                      title=title, 
                      plot_bgcolor='rgb(255,255,255)')

    
    if savehtml == None:
        fig.show()
    else:
        fig.write_html(f'{savehtml}_Panorama.html')


def individual_panorama(df, coefficient, color_dict=rgb_colors, title=None, savehtml=None):
    """Makes panorama interactive plot for an individual component with its magnitude, phase, and quantized phase.

    Arguments:
        df {dataFrame} -- pandas dataframe 
        coefficient {int} -- Fourier coefficient for the component to be plotted

    Keyword Arguments:
        color_dict {dictionary} -- dictionary of rgba colors (default: {rgb_colors})
        title {string} -- title of the plot (default: {None})
        savehtml {string} -- save location for the html file (default: {None})
    """
    i = coefficient
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.update_layout(autosize=False, width=1000, height=400)

    fig.add_trace(go.Scatter(
        # x=df['General']['Window Number'], 
        y=df['Phases'][f'f{i} Phase'], 
        mode='lines', 
        name=f'f{i} Phase',
        line=dict(color=color_dict[f'f{i}_colors'][1]),
        text=df['General']['Original Array'],
        customdata=df['General']['Measure Range'],
        hovertemplate = 
        "Measure Range: %{customdata} <br>"+
        "Phase: %{y}<br>"+
        "Original Array: %{text}",   
        visible='legendonly',
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        # x=df['General']['Window Number'], 
        y=df['QuantizedPhases'][f'f{i} Quantized Phase'], 
        mode='lines', 
        name=f'f{i} Quantized Phase',
        line=dict(color=color_dict[f'f{i}_colors'][2]),   
        text=df['General']['Original Array'],
        customdata=df['General']['Measure Range'],
        hovertemplate = 
        "Measure Range: %{customdata} <br>"+
        "Quantized Phase: %{y}<br>"+
        "Original Array: %{text}",
        visible='legendonly',
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(    
        # x=df['General']['Window Number'], 
        y=df['Magnitudes'][f'f{i} Magnitude'], 
        mode='lines', 
        fill='tozeroy', 
        fillcolor=color_dict[f'f{i}_colors'][0], 
        name=f'f{i} Magnitude', 
        line=dict(color=color_dict[f'f{i}_colors'][0]), 
        y0=0,
        dy=2,            
        text=df['General']['Original Array'],
        customdata=df['General']['Measure Range'],
        hovertemplate = 
        "Measure Range: %{customdata} <br>"+
        "Magnitude: %{y}<br>"+
        "Original Array: %{text}",  
    ), secondary_y=True)

    fig.update_yaxes(secondary_y=False, 
                    nticks=13, 
                    tick0=-180, 
                    dtick=30, 
                    overwrite=True, 
                    title='Phase',
                    showgrid=True,
                    gridcolor='rgb(222,222,222)')
    
    fig.update_yaxes(secondary_y=True, 
                    nticks=6, 
                    showgrid=False, 
                    title='Magnitude' )
    
    fig.update_xaxes(tick0=1, 
                    dtick=10, 
                    showgrid=False, 
                    title='Window Number')
    
    conv = lambda i : i or ''
    fig.update_layout(hoverlabel=dict(font_size=16), 
                    font=dict(family='Courier New, monospace', size=16),
                    title=''.join([f'{conv(title)}', f', f{i}']), 
                    plot_bgcolor='rgb(255,255,255)')

        
    if savehtml == None:
        fig.show()
    else:
        fig.write_html(f'{savehtml}_-_f{i}.html')


def magnitudes_panorama(df, color_dict=rgb_colors, title=None,savehtml=None):
    """Makes panorama interactive plot with all magnitudes.

    Arguments:
        df {dataFrame} -- pandas dataframe 

    Keyword Arguments:
        color_dict {dictionary} -- dictionary of rgba colors (default: {rgb_colors})
        title {string} -- title of the plot (default: {None})
        savehtml {string} -- save location for the html file (default: {None})
    """
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.update_layout(autosize=False, width=1000, height=400)
    
    for i in range(1, 7):

        fig.add_trace(go.Scatter(    
            # x=df['General']['Window Number'], 
            y=df['Magnitudes'][f'f{i} Magnitude'], 
            mode='lines', 
            fill='tozeroy', 
            fillcolor=color_dict[f'f{i}_colors'][0], 
            name=f'f{i} Magnitude', 
            line=dict(color=color_dict[f'f{i}_colors'][0]), 
            y0=0,
            dy=2,            
            text=df['General']['Original Array'],
            customdata=df['General']['Measure Range'],
            hovertemplate = 
            "Measure Range: %{customdata} <br>"+
            "Magnitude: %{y}<br>"+
            "Original Array: %{text}",  
        ))
    
    fig.update_yaxes(nticks=6, 
                     showgrid=False, 
                     title='Magnitude' )
    
    fig.update_xaxes(tick0=1, 
                     dtick=10, 
                     showgrid=False, 
                     title='Window Number')
    
    conv = lambda i : i or ''
    fig.update_layout(hoverlabel=dict(font_size=16), 
                      font=dict(family='Courier New, monospace', size=16),
                      title=''.join([f'{conv(title)}', f'Magnitudes']), 
                      plot_bgcolor='rgb(255,255,255)')

    
    if savehtml == None:
        fig.show()
    else:
        fig.write_html(f'{savehtml}_-_Magnitudes.html')
