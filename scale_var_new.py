from os import path
import re

from tables import search_line, cm_energy

from mh_detail import *

def create_scale_var_new_tables(m_Hs):
	m_Hdata = {}

	jobs = len(m_Hs)*15

#	print ""
	print ""
	print "Creating tables for scale_var_new from %d jobs." % (jobs) 

	for i in range(1, jobs+1):
		if not path.isfile("jobs_%s/job_scale_var_new%d" % (cm_energy, i)):
			print "File job_%s/job_scale_var_new%d missing." % (cm_energy, i)
			continue

#		print "Processing job_%s/job_scale_var_new%d" % (cm_energy, i)
		f = open("jobs_%s/job_scale_var_new%d" % (cm_energy, i), "r")

		M_H = 0.0
		M_t = 0.0

		line, res = search_line(".*M_t\s*=\s*([0-9.]+)", f)
		M_t = float(res.group(1))
		line, res = search_line("\s*M_H\s*=\s*([0-9.]+)", f)
		M_H = float(res.group(1))

		if not M_H in m_Hdata.viewkeys():
			m_Hdata[M_H] = []

		data = m_Hdata[M_H]

		scale = 0.0

#		line, res = search_line("\s*inverse factor for scale\s*:\s*([0-9.]+)", f)
#		line, res = search_line("\s*inverse factor for scale qf qr qb\s*:\s*([0-9.]+)\s*([0-9.]+)", f)
		line, res = search_line("\s*inverse factor for scale qf qr qb\s*:\s*([0-9.]+)\s*([0-9.]+)\s*([0-9.]+)", f)
		scale = (M_H + M_t)/float(res.group(1))
		scale2 = (M_H + M_t)/float(res.group(2))
		scale3 = (M_H + M_t)/float(res.group(3))
                iline=len(data)

		search_line("\s*RESULTS:", f)

		line = f.readline()
		line = line.split()

		# old format: 0: scale, 1: cs lo, 2: integ err lo, 3: cs nlo, 4: integ err nlo, 5:k factor, 6:nlo susy
		# format: 0: iline 1: scale, 2: scale2, 3: scal3, 4: cs lo, 5: integ err lo, 6: cs nlo, 7: integ err nlo, 8:k factor, 9:nlo susy
		data.append((iline, scale, scale2, scale3, float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]), float(line[14])))

		f.close()


	for mass_name in m_Hdata:
		mass = m_Hdata[mass_name]
	#	mass.sort(cmp = lambda x,y: x[0] < y[0])
		mass = sorted(mass, key = lambda x: x[0])

		f = open("tables_%s/scale_var_new_%dGeV" % (cm_energy, mass_name), "w")
		
		f.write("# scale_fac     scale_ren    scale_b       LO            relative_err  NLO           relative_err  K-Factor      NLO(SUSY)\n")

		for d in mass:
			f.write(" %2d %10e  %10e  %10e  %10e  %10e  %10e  %10e  %10e  %10e\n" % d)

		f.close()

def read_scale_var_new_table(name):
	f = open("tables_%s/%s" % (cm_energy, name), "r")

	# drop first line
	for line in f:
		break

	data = []

	for line in f:
		l = line.split()
		data.append((float(l[0]), float(l[1]), float(l[2]), float(l[3]), float(l[4]), float(l[5]), float(l[6]), float(l[7]), float(l[8]), float(l[9])))

	return data

#import matplotlib.pyplot as plt
from plotting import *

m_t = 172.5

def get_sigma_bounds(data):
	upper_lo = max(data, key = lambda x: x[4])[4]
	lower_lo = min(data, key = lambda x: x[4])[4]
	upper_nlo = max(data, key = lambda x: x[6])[6]
	lower_nlo = min(data, key = lambda x: x[6])[6]

	return ((upper_lo, lower_lo), (upper_nlo, lower_nlo))

from math import floor

def get_scale_var_new(m_H):
	data = read_scale_var_new_table("scale_var_new_%dGeV" % m_H)

#	central_scale = (m_t + m_H[0])/m_H[1]

	# Get central value
	central = data[0]
#	print central

	bounds = get_sigma_bounds(data)
#	print bounds
#	print (bounds[1][0]-central[6], bounds[1][1] - central[6])
	return (central[6], central[6] - bounds[1][1], bounds[1][0]-central[6],
		central[4], central[4] - bounds[0][1], bounds[0][0] - central[4])

def scale_var_new_analysis(m_Hs, latex_res):

	num = 0

	print ""
	print "*****************************************"
	print "*  Scale-Variation-error for %5s      *" % cm_energy
	print "*****************************************"
	print ""

	print " M_H    sigma_scale_lo+   sigma_scale_lo-       sigma_scale_nlo+  sigma_scale_nlo-   central_nlo"
	print "-----------------------------------------------------------------------------------------------"

	if latex_res:
		latex_res.write(r"\begin{tabular}{|c|r|r|r|r|r|r|r|r|}" + "\n")
		latex_res.write(r"\hline" + "\n")
		latex_res.write(r"$M_H$ [GeV] & $\myMathSigma{LO}$ [pb]& $\myMathSigma{Scale,LO}^+$ [pb] & $\myMathSigma{Scale,LO}^-$ [pb] & $\myMathSigma{NLO}$ [pb] & $\myMathSigma{Scale, NLO}^+$ [pb] & $\myMathSigma{Scale,NLO}^-$ [pb] \\" + "\n")
		latex_res.write(r"\hline" + "\n")



	plt.subplots(2, 4)
	plt.subplots_adjust(hspace = 0.2, wspace = 0.3, left=0.05, right=0.97)

	data_lo = []
	data_nlo = []
	data_x = []

	for m_H in m_Hs: 
		data = read_scale_var_new_table("scale_var_new_%dGeV" % m_H[0])
		
		scale_var_new = get_scale_var_new(m_H[0])

		print " %4d      +%.2e         -%.2e             +%.2e         -%.2e   %.2e" % (m_H[0], scale_var_new[5], scale_var_new[4], scale_var_new[2], scale_var_new[1], scale_var_new[0])
		if latex_res:
			latex_res.write(r" %s & %.2e & +%.2e & -%.2e & %.2e & +%.2e & -%.2e \\" % (m_H[0], scale_var_new[3], scale_var_new[5], scale_var_new[4], scale_var_new[0], scale_var_new[2], scale_var_new[1]) + "\n")
			latex_res.write(r"\hline")


		data_x.append(m_H[0])
		data_nlo.append((1.0, scale_var_new[2]/scale_var_new[0], scale_var_new[1]/scale_var_new[0]))
		data_lo.append((1.0, scale_var_new[5]/scale_var_new[3], scale_var_new[4]/scale_var_new[3]))


##UGLY!!!	if not m_H in [m_Hs[0], m_Hs[5], m_Hs[10], m_Hs[15]]:
#		if not m_H in [m_Hs[0], m_Hs[5]]:
#			continue

		num += 1

		central_scale = (m_t + m_H[0])/m_H[1]

		ax = plt.subplot(2,4,num)
		plt.plot([d[0]/central_scale for d in data], [d[1] for d in data], "g-", marker = None, label="LO")
		plt.plot([d[0]/central_scale for d in data], [d[3] for d in data], "b-", marker = None, label="NLO")
#		plt.legend(loc="best", prop=font(size=24)) 
#		plt.title("g b > H- t for M_H = %dGeV" % m_H[0])
		plt.xlabel(r"$\mu/\mu_0$", fontdict = {"size":20})
		plt.ylabel(r"$\sigma$ [pb]", fontdict = {"size":20})
		plt.text(0.4, 0.2, r"$M_H$ = %dGeV" % m_H[0], transform = ax.transAxes, fontdict={"size":18})

	#	left_bound = central_scale / 2.0
	#	right_bound = central_scale * 2.0

		plt.axvline(1.0, linestyle="-", color="black")
	#	plt.axvline(left_bound, linestyle="-.", color="black")
	#	plt.axvline(right_bound, linestyle="-.", color="black")

	#	sigma_bounds = get_sigma_bounds(data, left_bound, right_bound)
		sigma_bounds = get_sigma_bounds(data)

		plt.axhline(sigma_bounds[0][0], linestyle="--", color="green")
		plt.axhline(sigma_bounds[0][1], linestyle="--", color="green")
		plt.axhline(sigma_bounds[1][0], linestyle="--", color="blue")
		plt.axhline(sigma_bounds[1][1], linestyle="--", color="blue")

			
		plt.xlim(0.2, 3.2)
		#plt.minorticks_on()
		plt.xticks([1.0/3.0, 1.0, 3.0], ["1/3", "1", "3"])


#		xmin,xmax = plt.xlim()
#		xspan = xmax - xmin
#		ymin,ymax = plt.ylim()
#		yspan = ymax-ymin

	#	plt.text( 0.1, "%4f" % sigma_bounds[0][0])
		#plt.figtext(0.9, sigma_bounds[0][0]/yspan, "%4f" % sigma_bounds[0][0])
		#plt.figtext(0.9, sigma_bounds[0][1]/yspan, "%4f" % sigma_bounds[0][1])
		#plt.figtext(0.9, sigma_bounds[1][0]/yspan, "%4f" % sigma_bounds[1][0])
	#	plt.figtext(0.9, sigma_bounds[1][1]/yspan, "%4f" % sigma_bounds[1][1])

		fontsize = 16

		ax = plt.gca()
		for tick in ax.xaxis.get_major_ticks():
			tick.label1.set_fontsize(16)
		for tick in ax.yaxis.get_major_ticks():
			tick.label1.set_fontsize(16)

	if latex_res:
		latex_res.write(r"\end{tabular}" + "\n")
		latex_res.close()

        exit()

	plt.subplot2grid((2,4), (1,0), colspan = 4)

	if cm_energy == "14TeV":
		plt.show()
		plt.subplots(1, 1)

	plt.subplots_adjust(hspace = 0.2, wspace = 0.3, left=0.05, right=0.97)
	plot_error_tube(data_x, data_lo, "green", legend="LO")
	plot_error_tube(data_x, data_nlo, "blue", legend="NLO")
	plt.xlabel("$M_{H^-}$ [GeV]", fontdict = {"size":30})
	plt.ylabel("$\sigma/\sigma_{central}$", fontdict = {"size":30})
#	plt.legend(loc="best", prop=font(size=24)) 



	plt.show()


import sys

if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.argv[1] == "tables":
			create_scale_var_new_tables(m_Hs)
			exit()
		else:
			print "Unknown param: %s" % sys.argv[1]
			exit()

	scale_var_new_analysis()
		
