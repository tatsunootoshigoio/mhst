# mhst - Multiple hysteresis loop data ploter

</hr>

### Process multiple hysteresis files using numpy, matplotlib and pandas recursively

The way it works:

- opens system dialog for you to choose a directory with your .dat files
- puts the data column, by column into a pandas DataFrame
- plots the DataFrame using matplotlib applying an horizontal offset between each of the loops
- exports the DataFrame into .xlsx sheet file


