#-----------------------------------------------------#
# multi hysteresis plotter v0.4			      #
# author: tatsunootoshigo, 7475un00705hi90@gmail.com  #
#-----------------------------------------------------#

# Imports
from axfmtr import custom_axis_formater
from matplotlib.widgets import CheckButtons, Button
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

# field step
H_step = 500

datasets_name = 'example_data'
# output filnames
out_pdf = 'mhst_plot' + datasets_name + '.pdf'
out_svg = 'mhst_plot' + datasets_name + '.svg'


def mhst_open_in():
	""" The Function crates the DataFrame from all the .DAT files in the user selected directory """

	# file counter 
	file_count = 0

	# dir selection popup gui
	dirname = easygui.diropenbox()
	
	print('loaded datasets from dir: ' + dirname)
	print("----------------");
	os.chdir(dirname)
	
	# creating empty dataframe 
	df_xi = pd.DataFrame()
	

		
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
		#print(dataset_label)
		
		# create column labes for dataframe
		labelx = 'H' + np.str(dataset_label)
		labely = 'M' + np.str(dataset_label)

		# writing dataframe columns to be appended

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
print('A total of' + ' ' + str(len(hyst_data.columns)/2) + ' datasets in DataFrame,')
print('generated DataFrame with column names:')
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

# collect plot objects here
hyst_plots = []

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
	hyst_plot = plt.plot(x+i*H_step, y, 'o', color=next(colors), mfc=next(mfcolors), markersize=6, label=hyst_label, visible=True)
	hyst_plots = np.concatenate([hyst_plots, hyst_plot], axis=0)

#plt.legend(loc='best', bbox_to_anchor=(0.94, 1.05), frameon=True, fontsize=9, ncol=len(hyst_data.columns)/2)
plt.legend(loc='upper left', frameon=True, fontsize=10, title='Anneal Time')

# format plot
custom_axis_formater(plot_title, plot_x_label, plot_y_label, xmin, xmax, ymin, ymax, xprec, yprec)

# a list of Line2D objects for check button to play with
#print(hyst_plots)

# initialize checkbuttons with all visable plots
chk_ax = plt.axes([0.0, 0.2, 0.2, 0.2], frameon=False)
labels = [str(plot.get_label()) for  plot in hyst_plots]
visibility = [plot.get_visible() for plot  in hyst_plots]
chk_btn = CheckButtons(chk_ax, labels, visibility)

# add check button action (toggle/enable plots visibility)
def chk_plot(label):
    index = labels.index(label)
    hyst_plots[index].set_visible(not hyst_plots[index].get_visible())
    plt.draw()

chk_btn.on_clicked(chk_plot)

# add plot selected datasets button and event
def plot_selected(event):
	print(CheckButtons.get_status(chk_btn))
	print('Plotting selected datasets...')

	chk_btn_status = CheckButtons.get_status(chk_btn)

	# empty dataframe 
	hyst_data_cut = pd.DataFrame()

	# column index operators init
	j = 0	# M
	k = 1	# H

	# Construct DataFrame containig only selected (checkboxed) datastes
	for i in xrange(0,len(hyst_data.columns)/2):
	
		# generate dataset label
		#hyst_label = hyst_labels[j][1:]
		if chk_btn_status[i] == True:
			#get dataset to plot
			x = hyst_data.iloc[:,j]
			y = hyst_data.iloc[:,k]
			hyst_data_icut = pd.DataFrame([x,y]).T
			hyst_data_cut = pd.concat([hyst_data_cut, hyst_data_icut], axis=1)
		j+=2
		k+=2

	hyst_labels_cut = hyst_data_cut.columns.values
	print(hyst_data_cut)
	print('A total of' + ' ' + str(len(hyst_data_cut.columns)/2) + ' datasets in DataFrame were selected,')
	print('generated a new DataFrame with column names:')
	print(hyst_labels_cut)
	# plotting the dataframe
	fig1, ax1 = plt.subplots(figsize=(9, 9))
	fig1.tight_layout(pad=4.0, w_pad=0.5, h_pad=0.5)
	plt.subplots_adjust(left=0.15, bottom=0.1, wspace=0.0, hspace=0.0)
	fig1.canvas.set_window_title('hysteresis plotter' + ' ' + version_name) 
	# plt.subplots_adjust(left=0.15, bottom=0.5, wspace=0.0, hspace=0.0)
	plt.figtext(0.90, 0.97, version_name, size=10)

	colors = iter(plt.cm.inferno(np.linspace(0.3,0.8,10)))
	mfcolors = iter(plt.cm.plasma(np.linspace(0.1,1,10)))

	# collect plot objects here
	hyst_plots_cut = []

	# column index operators init
	j = 0	# M
	k = 1	# H
	# plot data recursively from DataFrame
	for i in xrange(0,len(hyst_data_cut.columns)/2):
	
		# generate dataset label
		hyst_label_cut = hyst_labels_cut[j][1:]
	
		#get dataset to plot
		x = hyst_data_cut.iloc[:,j]
		y = hyst_data_cut.iloc[:,k]
		j+=2
		k+=2

		hyst_plot_cut = plt.plot(x+i*H_step, y, 'o', color=next(colors), mfc=next(mfcolors), markersize=6, label=hyst_label_cut, visible=True)
		#hyst_plots_cut = np.concatenate([hyst_plots_cut, hyst_plot_cut], axis=0)

	plt.legend(loc='upper left', frameon=True, fontsize=10, title='Anneal Time')

	# format plot
	custom_axis_formater(plot_title, plot_x_label, plot_y_label, xmin, xmax, ymin, ymax, xprec, yprec)
	plt.show()

	# export dataframe to xlsx
	hyst_data_cut.to_excel("hyst_out_cut.xlsx")

btn_ax = plt.axes([0.01, 0.17, 0.06, 0.03], frameon=True)
plot_btn = Button(btn_ax, 'Plot', color='0.85', hovercolor='0.95')
plot_btn.on_clicked(plot_selected)

# write a pdf file with fig and close
pp = PdfPages(out_pdf)
pp.savefig(fig)
pp.close()

# save as .svg too
fig = plt.savefig(out_svg)

plt.show()
