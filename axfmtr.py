#-----------------------------------------------------#
# custom plot style formatter v0.5					  #
# author: tatsunootoshigo, 7475un00705hi90@gmail.com  #
#-----------------------------------------------------#

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator, FormatStrFormatter

mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams["font.serif"] = "STIX"
mpl.rcParams["mathtext.fontset"] = "stix"

# axes labels for plots
axis_label_th = r'$thickness\, / \, nm$'
axis_label_theta = r'$\theta$'
axis_label_volt = r'$V$'
axis_label_ohm = r'$R\;/\;\Omega$'
axis_label_points = r'$point\;no.$'
#axis_label_rr0 = r'$R_{xx}^{(z\rightarrow y)}\;/\;R_{0}$' 
axis_label_rr0 = r'$R_{xx}\;/\;R_{xx}^{0}$'

#def custom_axis_formater(custom_title, custom_x_label, custom_y_label, xmin, xmax, ymin, ymax, xprec, yprec):
def custom_axis_formater(custom_title, custom_x_label, custom_y_label, xmin, xmax, ymin, ymax, xprec, yprec):

	# get axes and tick from plot 
	ax = plt.gca()
	# set the number of major and minor bins for x,y axes
	# prune='lower' --> remove lowest tick label from x axis
	xmajorLocator = MaxNLocator(12, prune='lower') 
	xmajorFormatter = FormatStrFormatter('%.'+ np.str(xprec) + 'f')
	xminorLocator = MaxNLocator(12) 
	
	ymajorLocator = MaxNLocator(10) 
	ymajorFormatter = FormatStrFormatter('%.'+ np.str(yprec) + 'f')
	yminorLocator = MaxNLocator(20)
	
	# format major and minor ticks width, length, direction 
	ax.tick_params(which='both', width=1, direction='in', labelsize=14)
	ax.tick_params(which='major', length=6)
	ax.tick_params(which='minor', length=4)

	# set axes thickness
	ax.spines['top'].set_linewidth(1.5)
	ax.spines['bottom'].set_linewidth(1.5)
	ax.spines['right'].set_linewidth(1.5)
	ax.spines['left'].set_linewidth(1.5)

	ax.xaxis.set_major_locator(xmajorLocator)
	ax.yaxis.set_major_locator(ymajorLocator)

	ax.xaxis.set_major_formatter(xmajorFormatter)
	ax.yaxis.set_major_formatter(ymajorFormatter)

	# for the minor ticks, use no labels; default NullFormatter
	ax.xaxis.set_minor_locator(xminorLocator)
	ax.yaxis.set_minor_locator(yminorLocator)

	# grid and axes are drawn below the data plot
	ax.set_axisbelow(True)

	# convert x axis units to radians
	#ax.convert_xunits(radians)

	# add x,y grids to plot area
	ax.xaxis.grid(True, zorder=0, color='lightgray', linestyle='-', linewidth=1)
	ax.yaxis.grid(True, zorder=0, color='lightgray', linestyle='-', linewidth=1)

	# set axis labels
	ax.set_xlabel(custom_x_label, fontsize=16)
	ax.set_ylabel(custom_y_label, fontsize=16)

	plt.xlim(xmin, xmax)
	plt.ylim(ymin, ymax)
	# set plot title
	#ax.set_title(custom_title, loc='right', fontsize=12)

	return;