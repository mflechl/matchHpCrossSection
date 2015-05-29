import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties as font

################################################
#
# Plotting helper 
#
################################################

green_line = None
blue_line = None
red_line = None
cyan_line = None

def plot_error_bar(num, mean, losigma, upsigma, color):
	global ymin
	global ymax

	if ymin == None:
		ymin = mean
	if ymax == None:
		ymax = mean

	if mean - losigma < ymin:
		ymin = mean - losigma
	if mean + upsigma > ymax:
		ymax = mean + upsigma

	if color == "green":
		num = num - 0.2
	elif color == "blue":
		num = num - 0.1
	elif color == "red":
		num = num
	elif color == "cyan":
		num = num + 0.1

	global green_line
	global blue_line
	global red_line
	global cyan_line

	if losigma == upsigma:
		if color == "green" and not green_line:
			green_line = plt.errorbar([num], [mean], yerr=[losigma], color=color, marker="o", markersize=3.5, fmt="--", ecolor=color, mfc=color, mec=color, label="LO + pdf" )
			return

		if color == "blue" and not blue_line:
			blue_line = plt.errorbar([num], [mean], yerr=[losigma], color=color, marker="o", markersize=3.5, fmt="--", ecolor=color, mfc=color, mec=color, label="NLO + pdf" )
			return

		if color == "red" and not red_line:
			red_line = plt.errorbar([num], [mean], yerr=[losigma], color=color, marker="o", markersize=3.5, fmt="--", ecolor=color, mfc=color, mec=color, label="NLO + pdf + alphas" )
			return

		if color == "cyan" and not cyan_line:
			cyan_line = plt.errorbar([num], [mean], yerr=[losigma], color=color, marker="o", markersize=3.5, fmt="--", ecolor=color, mfc=color, mec=color, label="NLO + pdf + mb" )
			return


		plt.errorbar([num], [mean], yerr=[losigma], color=color, marker="o", markersize=3.5, fmt="--", ecolor=color, mfc=color, mec=color)

		return 

	plt.plot([num], [mean], color=color, marker="o", markersize=3.5, mfc=color, mec=color)
	upper_val = mean+upsigma
	lower_val = mean-losigma
	err_bar_mean = (upper_val + lower_val)/2.0
	err_bar_sigma = (upper_val - lower_val)/2.0
	plt.errorbar([num], [err_bar_mean], yerr=[err_bar_sigma], marker=None, color=color)

def plot_error_tube(plot_x, plot_y, color, legend = None, linestyle="--", tube_style=False, alpha=1.0):
	if tube_style:
		if legend:
			plt.fill_between(plot_x, [i[0] - i[2] for i in plot_y], [i[0] + i[1] for i in plot_y], color=color, alpha=alpha)
			plt.plot([0],[0],color=color, linewidth=3.0, marker=None, label=legend, alpha=alpha)
		else:
			plt.fill_between(plot_x, [i[0] - i[2] for i in plot_y], [i[0] + i[1] for i in plot_y], color=color, alpha=alpha)

	else:
		plt.plot(plot_x, [i[0] for i in plot_y], color, linestyle="-", linewidth=2.0, label=legend, alpha=alpha)
		plt.plot(plot_x, [i[0] +  i[1] for i in plot_y], color, linestyle=linestyle, linewidth=2.0, alpha=alpha)
		plt.plot(plot_x, [i[0] - i[2] for i in plot_y], color, linestyle=linestyle, linewidth=2.0, alpha=alpha)




