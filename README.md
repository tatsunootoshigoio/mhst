# mhst - Multiple hysteresis loop data plotter (python 2.7)

</hr>

### Process multiple hysteresis files using numpy, matplotlib and pandas recursively

The way it works:

1. opens system dialog for you to choose a directory with your .dat files
2. puts the data column, by column into a pandas DataFrame
3. plots the DataFrame using matplotlib applying an horizontal offset between each of the loops
4. exports the DataFrame into .xlsx sheet file

</hr>

TODO:

- [ ] add a slider to dynamically adjust hysteresis loop spacing
- [ ] add save to .pdf file button
- [ ] add export to .xlsx sheet button


