# DFT_Panorama

This project analyzes a musical score (encoded as XML, MEI, MusicXML, etc.) by passing a sliding window over the surface and applying the discrete Fourier transform (DFT) to the pitch classes within the window. The result is a numerical representation of the harmonic qualia that can be viewed as tables or as graphical visualizations.

# Instructions

Download or clone all files. In addition to Python 3.8, the following Python packages are required: music21, numpy, pandas, plotly, and tkinter. Use the notebook DFT_Main to run the program and generate visualizations. A small corpus is included, but additional files can be added in DFT_Corpus. Visualizations are interactive plots that are saved as html. The save location can be edited in DFT_Graphing.
