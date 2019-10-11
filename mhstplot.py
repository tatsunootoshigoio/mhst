#-----------------------------------------------------#
# multi hysteresis plotter v0.4			      #
# author: tatsunootoshigo, 7475un00705hi90@gmail.com  #
#-----------------------------------------------------#

# Imports
import glob, os
import easygui
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
from sklearn.preprocessing import MinMaxScaler as sklscl
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator, MultipleLocator, FormatStrFormatter

def mhst_open_in():

	# file counter 
	file_count = 0

	# field step
	H_step = 500
	
	# dir selection popup gui
	dirname = easygui.diropenbox()
	
	print('loaded datasets from dir: ' + dirname)
	print("----------------");
	os.chdir(dirname)
	
	# creating empty dataframe 
	df_xi = pd.DataFrame()
	
	# looking only for *.DAT files to count the total of these in the selected directory
	for file in glob.glob("*.DAT"):
		
		# count files in dir
		print(file_count, file)
		file_count += 1
		print("----------------");

	# field step iterator
 	i=0
	
	# loading x,y datasets from all .DAT files in selected dir
	for file in glob.glob("*.DAT"):
 	
		# read dataset skipping 6 lines of header 	
		xi, yi = np.genfromtxt(file, usecols=(0,1), skip_header=6, skip_footer=1, unpack=True)
	
		# read input file for column labels
		dataset_label = np.genfromtxt(file, dtype=str, usecols=(2), skip_footer=len(xi)+6, unpack=None)
		print(dataset_label)
		
		# create column labes for dataframe
		labelx = 'H' + np.str(dataset_label)
		labely = 'M' + np.str(dataset_label)

		# writing dataframe columns to be appended
		df_xi1 = pd.DataFrame([xi+i*H_step,yi]).T
		print(df_xi1)
		i+=1

		df_xi1.columns = [labelx, labely]
		df_xi1.head()
		
		# appending columns to dataframe
		df_xi = pd.concat([df_xi, df_xi1], axis=1)

	return df_xi;
	
hyst_data = mhst_open_in()
print(hyst_data)
hyst_data.to_excel("hyst_out.xlsx")
