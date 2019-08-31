#-----------------------------------------------------#
# multi hysteresis ploter v0.4					      #
# author: tatsunootoshigo, 7475un00705hi90@gmail.com  #
#-----------------------------------------------------#

# Imports
from axfmtr import custom_axis_formater
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

# script version
version = '0.4'
version_name = 'mhst' + version + '.py'

# plot labels related
plot_title = 'hysteresis loops'
plot_x_label = r'$H$'  
plot_y_label = r'$M$'
xmin = -1000
xmax = 5400
ymin = -16000
ymax = 16000
xprec = 0
yprec = 0

datasets_name = 'example_data'
# output filnames
out_pdf = 'mhst_plot' + datasets_name + '.pdf'
out_svg = 'mhst_plot' + datasets_name + '.svg'

def mhst_open_in():

	# files counter 
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
	
	# looking only for *.DAT files to caount the total of those
	for file in sorted(glob.glob("*.DAT")):
		
		# count files in dir
		print(file_count, file)
		file_count += 1
		print("----------------");

	# field step iterator
 	i=0
	# loading x,y datasets from all .DAT files in selected dir
	for file in sorted(glob.glob("*.DAT")):
 	
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
		#print(df_xi1)
		i+=1

		df_xi1.columns = [labelx, labely]
		df_xi1.head()
		
		# appending columns to dataframe
		df_xi = pd.concat([df_xi, df_xi1], axis=1)

	return df_xi;
	
hyst_data = mhst_open_in()

# export dataframe to xlsx
hyst_data.to_excel("hyst_out.xlsx")

#print(hyst_data)
#print(np.size(hyst_data)/2)
#print((len(hyst_data.columns)/2))

hyst_labels = hyst_data.columns.values
print(hyst_labels)
#print(hyst_labels[0])


# plotting the dataframe
fig, ax = plt.subplots(figsize=(9, 9))
fig.tight_layout(pad=4.0, w_pad=0.5, h_pad=0.5)
plt.subplots_adjust(left=0.15, bottom=0.1, wspace=0.0, hspace=0.0)
fig.canvas.set_window_title('hysteresis plotter' + ' ' + version_name) 
# plt.subplots_adjust(left=0.15, bottom=0.5, wspace=0.0, hspace=0.0)
plt.figtext(0.90, 0.97, version_name, size=10)

colors = iter(plt.cm.inferno(np.linspace(0.3,0.8,10)))
mfcolors = iter(plt.cm.plasma(np.linspace(0.1,1,10)))

# column index operators init
j = 0	# M
k = 1	# H
# plot data recursively from DataFrame
for i in xrange(0,len(hyst_data.columns)/2):
	
	# generate dataset label
	hyst_label = hyst_labels[j][1:]
	
	#get dataset to plot
	x = hyst_data.iloc[:,j]
	y = hyst_data.iloc[:,k]
	j+=2
	k+=2
	
	#print(pd.DataFrame([x,y]))
	#print(hyst_labels[i]) 
	plt.plot(x, y, 'o', color=next(colors), mfc=next(mfcolors), markersize=6, label=hyst_label)

#plt.legend(loc='best', bbox_to_anchor=(0.94, 1.05), frameon=True, fontsize=9, ncol=len(hyst_data.columns)/2)
plt.legend(loc='top left', frameon=True, fontsize=10, title='Anneal Time')

# format plot
custom_axis_formater(plot_title, plot_x_label, plot_y_label, xmin, xmax, ymin, ymax, xprec, yprec)

# write a pdf file with fig and close
pp = PdfPages(out_pdf)
pp.savefig(fig)
pp.close()

# save as .svg too
fig = plt.savefig(out_svg)

plt.show()
