from pdfs import *
from tables import *
from mh_detail import *

from scale_var import *
from scale_var_new import *
from scaleplot import *
from grid import *

def create_all_tables():
	create_tables("pdf_error", pdfs_pdf_err, m_Hs[cm_energy])
	create_tables("ct10_alphas", pdfs_als_err[0:1], m_Hs[cm_energy])
	create_tables("mstw_alphas", pdfs_als_err[1:3], m_Hs[cm_energy])
	create_tables("nnpdf_alphas", pdfs_als_err[3:], m_Hs[cm_energy], as_name = True)
	create_tables("mstw_mb", pdfs_mb_err[0:1], m_Hs[cm_energy])
	create_tables("nnpdf_mb", pdfs_mb_err[1:], m_Hs[cm_energy], mb_name = True)
##	create_scale_var_tables(m_Hs[cm_energy])
	create_scale_var_new_tables(m_Hs[cm_energy])
##	create_scaleplot_tables(m_Hs[cm_energy])
	create_tanbeta_tables(m_Hs[cm_energy])

from pdf_error import *
from alphas_pdf_error import *
from mb_pdf_error import *
from combined_error import *

pdf_data = None


latex_res = None

def init_data_struct():
	# create tables for every pdf and make a 
	# data point for every mass in m_Hs
	global pdf_data

	if pdf_data != None:
		return

#	pdf_data = {
#		"MSTW2008" : [],
#		"NNPDF23" : [],
#		"CT10" : [],
#		"combined" : []
#	}

	pdf_data = {
		"CT10" : [],
#		"NNPDF21" : [],
		"NNPDF23" : [],
		"MSTW2008" : [],
		"combined" : []
	}

	for pdf in pdf_data:
		for i in range(0, len(m_Hs[cm_energy])):
			pdf_data[pdf].append({})

def pdf_error():
	init_data_struct()
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	print_pdf_error(pdf_data, m_Hs[cm_energy])

def alphas_pdf_error():
	init_data_struct()
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_alphas_pdf_errors(pdf_data, m_Hs[cm_energy])
	print_alphas_pdf_error(pdf_data, m_Hs[cm_energy])

def mb_pdf_error():
	init_data_struct()
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_mb_pdf_errors(pdf_data, m_Hs[cm_energy])
	print_mb_pdf_error(pdf_data, m_Hs[cm_energy])

from plotting import * 

def difference_plot(no_show = False):
	init_data_struct()
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_alphas_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_mb_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_combined_errors(pdf_data, m_Hs[cm_energy])

	x = [m_H[0] for m_H in m_Hs[cm_energy]]
	scale_var = [get_scale_var(m) for m in x]

	plot_data = {}

	for pdf in pdf_data:
		data = pdf_data[pdf]
#		if pdf != "CT10":
#			complete_err = [(data[i]["central_nlo"], data[i]["mbpdfup_nlo"] + scale_var[i][2], data[i]["mbpdflo_nlo"] + scale_var[i][1]) for i in range(0, len(m_Hs))]
#		else:
#			complete_err = [(data[i]["central_nlo"], data[i]["alphaspdfup_nlo"] + scale_var[i][2], data[i]["alphaspdflo_nlo"] + scale_var[i][1]) for i in range(0, len(m_Hs))]
	
		complete_err = [(data[i]["central_nlo"], data[i]["combinedup_nlo"], data[i]["combinedlo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]

		plot_data[pdf] = complete_err
	
	for pdf in plot_data:
		if pdf == "combined":
			continue
	
		for i in range(0, len(plot_data[pdf])):
			plot_data[pdf][i] = (plot_data[pdf][i][0]/plot_data["combined"][i][0], plot_data[pdf][i][1]/plot_data["combined"][i][0], plot_data[pdf][i][2]/plot_data["combined"][i][0])

	pdf = "combined"
	for i in range(0, len(plot_data[pdf])):
		plot_data[pdf][i] = (plot_data[pdf][i][0]/plot_data["combined"][i][0], plot_data[pdf][i][1]/plot_data["combined"][i][0], plot_data[pdf][i][2]/plot_data["combined"][i][0])


	#plt.title("Deviation of gb->Ht-cross-sections for different pdfs to combined results for %s." % cm_energy)

	colors = ["red", "green", "blue", "black"]

	for pdf in plot_data:
		if pdf == "combined":
			continue
		plot_error_tube(x, plot_data[pdf], colors[0], legend = "%s - cross section + total-error" % pdf)

		del colors[0]
	

	plot_error_tube(x, plot_data["combined"], colors[0], legend = "%s - cross section + total-error" % "combined")


	plt.subplots_adjust(left = 0.05, right = 0.96, top = 0.95, bottom = 0.06)

#	plt.legend(loc = "best", prop=font(size=30))

#	if cm_energy == "8TeV":
#		plt.legend(bbox_to_anchor = (0,0,1,0.72), prop=font(size=24))
#	else:
#		plt.legend(bbox_to_anchor = (0,0,1,0.8), prop=font(size=24))
	plt.xlabel("$M_H$ [GeV]", fontdict={"size":30})
	plt.ylabel(r"$\sigma/\sigma_{\mathrm{combined}}$ [pb]", fontdict={"size":30})
#	plt.semilogy()

	plt.xlim(200, 500)
#	if cm_energy == "14TeV":
#		plt.ylim(0.07, 1.5)

	plt.grid(which="major", linestyle="-")
	#plt.minorticks_on()
	#plt.grid(which="minor", linestyle="--")

	set_ax_size()

	if not no_show:
		plt.show()

def set_ax_size():
	fontsize = 16

	ax = plt.gca()
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(16)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(16)

def error_plot(no_show = False):
	init_data_struct()
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_alphas_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_mb_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_combined_errors(pdf_data, m_Hs[cm_energy])

	x = [m_H[0] for m_H in m_Hs[cm_energy]]
	scale_var = [get_scale_var(m) for m in x]

	plot_data = {}

	for pdf in pdf_data:
		data = pdf_data[pdf]
#		if pdf != "CT10":
#			complete_err = [(data[i]["central_nlo"], data[i]["mbpdfup_nlo"] + scale_var[i][2], data[i]["mbpdflo_nlo"] + scale_var[i][1]) for i in range(0, len(m_Hs))]
#		else:
#			complete_err = [(data[i]["central_nlo"], data[i]["alphaspdfup_nlo"] + scale_var[i][2], data[i]["alphaspdflo_nlo"] + scale_var[i][1]) for i in range(0, len(m_Hs))]
		complete_err = [(data[i]["central_nlo"], data[i]["combinedup_nlo"], data[i]["combinedlo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]

		plot_data[pdf] = complete_err
	

#	plt.title("Errors of gb->Ht-cross-sections for different pdfs and combined results for %s." % cm_energy)

	plt.subplots_adjust(left = 0.05, right = 0.96, top = 0.95, bottom = 0.06)

	colors = ["blue", "green", "red", "black"]

	pdfs = ["MSTW2008", "NNPDF23", "CT10"]

#	for pdf in plot_data:
	for pdf in pdfs:
		if pdf == "combined":
			continue
		plot_error_tube(x, plot_data[pdf], colors[0], tube_style=True, alpha=0.5)
		plot_error_tube(x, plot_data[pdf], colors[0], legend = "%s" % pdf)
#		plot_error_tube(x, plot_data[pdf], colors[0], tube_style=True, alpha=0.5)

#		plot_error_tube(x, plot_data[pdf], colors[0], legend = "%s NLO + total-error" % pdf, alpha=0.5)
		del colors[0]
	

	plot_error_tube(x, plot_data["combined"], colors[0], legend = "%s" % "combined")
	#plot_error_tube(x, plot_data["combined"], colors[0], legend = "%s - NLO + total-error" % "combined")

	data = pdf_data["combined"]
#	pdf_err_lo = [(data[i]["central_lo"], data[i]["pdfup_lo"], data[i]["pdflo_lo"]) for i in range(0, len(m_Hs))]
#	plot_error_tube(x, pdf_err_lo, "gray", legend = "%s - LO + PDF-error" % "combined")


	plt.legend(loc = "best", prop=font(size=24))
	plt.xlabel("$M_H$ [GeV]", fontdict={"size":30})
	plt.ylabel("$\sigma$ [pb]", fontdict={"size":30})
	plt.semilogy()
	
	plt.xlim(200, 500)
	if cm_energy == "14TeV":
		plt.ylim(0.07, 1.5)
	if cm_energy == "8TeV":
		plt.ylim(0.01, 0.3)

	plt.grid(which="major", linestyle="-")
	plt.minorticks_on()
	plt.grid(which="minor", linestyle="--")

	set_ax_size()

	if not no_show:
		plt.show()


def combined2():
	plt.subplots(1,2)
	ax = plt.subplot(1,2,1)
	error_plot(True)
	plt.text(0.05, 0.1, "pp $\\rightarrow$ $H^-$t at %s at NLO\ncalculated in 2HDM\n$M_t$ = 172.5 GeV\n$M_b$ = 4.75 GeV\n$\\alpha_s$ = 0.118\n$\\tan \\beta$ = 30.0" % cm_energy, transform= ax.transAxes, fontdict={"size":"36"})
	plt.subplot(1,2,2)
	difference_plot(True)
	plt.show()




def pdf_data_for(name):
	pdf_data = { name : [] }
	for i in range(0, len(m_Hs[cm_energy])):
		pdf_data[name].append({})
	return pdf_data


##########################################
#
#  CT10
#
##########################################

def ct10_analysis():
	pdf_data = pdf_data_for("CT10")
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_alphas_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_combined_errors(pdf_data, m_Hs[cm_energy])

	print ""
	print "***************************************"
	print "*  CT10-Results for %5s             *" % cm_energy
	print "***************************************"

	x = [m_H[0] for m_H in m_Hs[cm_energy]]
	scale_var = [get_scale_var_new(m) for m in x]  #mf!

	def print_line(pdf_data, pdf, i, start):
		res = pdf_data[pdf][i]

#		print " %4s   %8s   %.2e   %.2e     +%.2e       +%.2e       +%.2e       +%.2e"  % ((m_Hs[cm_energy][i][0] if start else ""), pdf, res["central_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphasup_nlo"], scale_var[i][2], res["combinedup_nlo"])
#		print "                                           -%.2e       -%.2e       -%.2e       -%.2e" % (res["pdflo_nlo"], res["alphaslo_nlo"], scale_var[i][1], res["combinedlo_nlo"])
		print " %4s   %8s   %.2e   %.2e     +%.2e       +%.2e       +%.2e       +%.2e"  % ((m_Hs[cm_energy][i][0] if start else ""), pdf, res["central_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphasup_nlo"], scale_var[i][2], res["combinedup_nlo"]+scale_var[i][2])
		print "                                           -%.2e       -%.2e       -%.2e       -%.2e" % (res["pdflo_nlo"], res["alphaslo_nlo"], scale_var[i][1], res["combinedlo_nlo"]+scale_var[i][1])

		if latex_res:
			latex_res.writelines([
				r"%s & %.2e & %.2e & +%.2e & +%.2e & +%.2e & +%.2e \\" % (m_Hs[cm_energy][i][0], res["central_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphasup_nlo"], scale_var[i][2], res["combinedup_nlo"]) + "\n",
			r" & & & -%.2e & -%.2e & -%.2e & -%.2e \\" % (res["pdflo_nlo"], res["alphaslo_nlo"], scale_var[i][1], res["combinedlo_nlo"]) + "\n",
			r"\hline" + "\n"])

	print ""
	print "  M_H    pdf-set         LO       NLO      pdf_error       as_error       scale_var     total_error"
	print "--------------------------------------------------------------------------------------------------------"

	if latex_res:
		latex_res.write(r"\begin{tabular}{|c|r|r|r|r|r|r|}" + "\n")
		latex_res.write(r"\hline" + "\n")
		latex_res.write(r"$M_{H^-}$ [GeV] & \mySigma{LO} [pb] & \mySigma{NLO} [pb] & \mySigma{PDF} [pb] & \mySigma{$\alpha_s$} [pb] & \mySigma{Scale} [pb] & \mySigma{total} [pb] \\" + "\n")
		latex_res.write(r"\hline" + "\n")


	for i in range(0, len(m_Hs[cm_energy])):
		start = True

		print_line(pdf_data, "CT10", i, start)
		start = False

	if latex_res:
		latex_res.write(r"\end{tabular}" + "\n")
		latex_res.close()
        exit()

	count = 0

	data = pdf_data["CT10"]
#	lo = [(data[i]["central_lo"], data[i]["combinedup_lo"], data[i]["combinedlo_lo"]) for i in range(0, len(m_Hs))]
	pdf_err = [(data[i]["central_nlo"], data[i]["pdfup_nlo"], data[i]["pdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
	als_pdf_err = [(data[i]["central_nlo"], data[i]["alphaspdfup_nlo"], data[i]["alphaspdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
	complete_err = [(data[i]["central_nlo"], data[i]["combinedup_nlo"], data[i]["combinedlo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
		
#	plt.title("Results for CT10")

	ax = plt.subplot(1,1,1)

	plt.subplots_adjust(left = 0.05, right = 0.96, top = 0.95, bottom = 0.06)


#	plt.plot(x, lo, "gray", label="LO")
#	plot_error_tube(x, pdf_err, "red", linestyle="-.", legend = "PDF-error")
#	plot_error_tube(x, als_pdf_err, "green", legend = "$\\alpha_s$-error+PDF-error")
#	plot_error_tube(x, complete_err, "black", legend = "NLO + total error")

	plot_error_tube(x, complete_err, "black", tube_style=True, legend="total uncertainty")
#	plot_error_tube(x, als_pdf_err, "yellow", legend = "$\\alpha_s$-error+PDF-error", tube_style=True)
	plot_error_tube(x, pdf_err, "red", linestyle="-.", legend = "PDF-uncertainty", tube_style=True)
#	plot_error_tube(x, lo, "gray", linestyle="-.", legend = "total uncertainty in LO", tube_style=True)
#	plt.plot(x, lo, "gray", label="LO")
	plt.text(0.05, 0.1, "pp $\\rightarrow$ $H^-$t at %s at NLO\ncalculated with CT10 in 2HDM\n$M_t$ = 172.5 GeV\n$M_b$ = 4.75 GeV\n$\\alpha_s$ = 0.118\n$\\tan \\beta$ = 30.0" % cm_energy, transform= ax.transAxes, fontdict={"size":"36"})
#	plt.text(0.1, 0.1, "gb $\\rightarrow$ $H^-$ t at 8 GeV", transform = ax.transAxes, fontdict={"size":"18"})
	plt.plot(x, [c[0] for c in complete_err], "black")


	plt.legend(loc = "best", prop=font(size=30))
	plt.xlabel("$M_{H^-}$ [GeV]", fontdict={"size":30})
	plt.ylabel("$\sigma$ [pb]", fontdict={"size":30})
	plt.semilogy()
	plt.xlim(200, 500)
	if cm_energy == "14TeV":
		plt.ylim(0.07, 1)
	if cm_energy == "8TeV":
		plt.ylim(0.01, 0.3)
		

	plt.grid(which="major", linestyle="-")
	plt.minorticks_on()
	plt.grid(which="minor", linestyle="--")

#	if latex_res:
#		latex_res.write(r"\end{tabular}" + "\n")
#		latex_res.close()

	set_ax_size()

	plt.show()


##########################################
#
#  MSTW2008 
#
##########################################

def mstw_analysis():
	pdf_data = pdf_data_for("MSTW2008")
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_alphas_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_mb_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_combined_errors(pdf_data, m_Hs[cm_energy])

	print ""
	print "***************************************"
	print "*  MSTW2008-Results for %5s         *" % cm_energy
	print "***************************************"

	x = [m_H[0] for m_H in m_Hs[cm_energy]]
	scale_var = [get_scale_var_new(m) for m in x]  #mf!

	def print_line(pdf_data, pdf, i, start):
		res = pdf_data[pdf][i]

#		print " %4s   %8s   %.2e   +%.2e  %.2e    +%.2e      +%.2e      +%.2e      +%.2e      +%.2e"  % ((m_Hs[cm_energy][i][0] if start else ""), pdf, res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphasup_nlo"], res["mbup_nlo"], scale_var[i][2], res["combinedup_nlo"])
#		print "                              -%.2e              -%.2e      -%.2e      -%.2e      -%.2e      -%.2e" % (res["pdflo_lo"], res["pdflo_nlo"], res["alphaslo_nlo"], res["mblo_nlo"], scale_var[i][1], res["combinedlo_nlo"])
		print " %4s   %8s   %.2e   +%.2e  %.2e    +%.2e      +%.2e      +%.2e      +%.2e      +%.2e"  % ((m_Hs[cm_energy][i][0] if start else ""), pdf, res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphasup_nlo"], res["mbup_nlo"], scale_var[i][2], res["combinedup_nlo"]+scale_var[i][2])
		print "                              -%.2e              -%.2e      -%.2e      -%.2e      -%.2e      -%.2e" % (res["pdflo_lo"], res["pdflo_nlo"], res["alphaslo_nlo"], res["mblo_nlo"], scale_var[i][1], res["combinedlo_nlo"]+scale_var[i][1])

		if latex_res:
			latex_res.writelines([
				r"%s & %.2e & +%.2e & %.2e & +%.2e & +%.2e & +%.2e & +%.2e & +%.2e\\" % (m_Hs[cm_energy][i][0], res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphasup_nlo"], res["mbup_nlo"], scale_var[i][2], res["combinedup_nlo"]) + "\n",
			r" & & -%.2e & & -%.2e & -%.2e & -%.2e & -%.2e & -%.2e \\" % (res["pdflo_lo"],res["pdflo_nlo"], res["alphaslo_nlo"], res["mblo_nlo"], scale_var[i][1], res["combinedlo_nlo"]) + "\n",
			r"\hline" + "\n"])

	print ""
	print "  M_H    pdf-set         LO    pdf_error      NLO    pdf_error       as_error       mb_error      scale_var    total_error"
	print "--------------------------------------------------------------------------------------------------------------------------"

	if latex_res:
		latex_res.write(r"\begin{tabular}{|c|r|r|r|r|r|r|r|r|}" + "\n")
		latex_res.write(r"\hline" + "\n")
		#latex_res.write(r"$M_{H^-}$ [GeV] & \mySigma{LO} [pb] & \mySigma{PDF} [pb] & \mySigma{NLO} [pb] & \mySigma{PDF} [pb] & \mySigma{$\alpha_s$} [pb] & \mySigma{$M_b$} [pb] & \mySigma{Scale} [pb] & \mySigma{total} [pb] \\" + "\n")
		latex_res.write(r"$M_{H^-}$ & \mySigma{LO} [pb] & \mySigma{PDF} [pb] & \mySigma{NLO} [pb] & \mySigma{PDF} [pb] & \mySigma{$\alpha_s$} [pb] & \mySigma{$M_b$} [pb] & \mySigma{Scale} [pb] & \mySigma{total} [pb] \\" + "\n")
		latex_res.write(r" [GeV] & & & & & & & & \\" + "\n")
		latex_res.write(r"\hline" + "\n")


	for i in range(0, len(m_Hs[cm_energy])):
		start = True

		print_line(pdf_data, "MSTW2008", i, start)
		start = False

	if latex_res:
		latex_res.write(r"\end{tabular}" + "\n")
		latex_res.close()
        exit()

	count = 0

	data = pdf_data["MSTW2008"]
	pdf_err_lo = [(data[i]["central_lo"], data[i]["pdfup_lo"], data[i]["pdflo_lo"]) for i in range(0, len(m_Hs[cm_energy]))]
	pdf_err = [(data[i]["central_nlo"], data[i]["pdfup_nlo"], data[i]["pdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
	als_pdf_err = [(data[i]["central_nlo"], data[i]["alphaspdfup_nlo"], data[i]["alphaspdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
	mb_pdf_err = [(data[i]["central_nlo"], data[i]["mbpdfup_nlo"], data[i]["mbpdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
	complete_err = [(data[i]["central_nlo"], data[i]["combinedup_nlo"], data[i]["combinedlo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]

	ax = plt.subplot(1,1,1)
		

	plt.subplots_adjust(left = 0.05, right = 0.96, top = 0.95, bottom = 0.06)


#	plot_error_tube(x, pdf_err_lo, "gray", legend="LO + PDF-error", tube_style="True")
#	plot_error_tube(x, pdf_err, "red", linestyle="-.", legend = "PDF-error in NLO", tube_style="True")
#	plot_error_tube(x, als_pdf_err, "green", legend = "$\\alpha_s$+PDF-error in NLO", tube_style="True")
#	plot_error_tube(x, mb_pdf_err, "blue", legend = "$M_b$+PDF-error in NLO", tube_style="True")
#	plot_error_tube(x, complete_err, "black", legend = "NLO + total error", tube_style="True")

	plot_error_tube(x, complete_err, "black", legend = "total uncertainty", tube_style="True")
	plot_error_tube(x, mb_pdf_err, "blue", legend = "$M_b$+PDF-uncertainty", tube_style="True")
#	plot_error_tube(x, als_pdf_err, "yellow", legend = "$\\alpha_s$+PDF-error in NLO", tube_style="True")
	plot_error_tube(x, pdf_err, "red", linestyle="-.", legend = "PDF-uncertainty", tube_style="True")
#	plot_error_tube(x, pdf_err_lo, "magenta", legend="LO + PDF-error")
	plt.plot(x, [c[0] for c in complete_err], "black", linestyle="-")

	plt.legend(loc = "best", prop=font(size=30))
	plt.xlabel("$M_{H^-}$ [GeV]", fontdict={"size":30})
	plt.ylabel("$\sigma$ [pb]", fontdict={"size":30})
	plt.text(0.05, 0.1, "pp $\\rightarrow$ $H^-$t at %s at NLO\ncalculated with MSTW2008 in 2HDM\n$M_t$ = 172.5 GeV\n$M_b$ = 4.75 GeV\n$\\alpha_s$ = 0.118\n$\\tan \\beta$ = 30.0" % cm_energy, transform= ax.transAxes, fontdict={"size":"36"})
	plt.semilogy()
	plt.xlim(200, 500)
	if cm_energy == "14TeV":
		plt.ylim(0.07, 1.1)
	if cm_energy == "8TeV":
		plt.ylim(0.01, 0.3)
		

	plt.grid(which="major", linestyle="-")
	plt.minorticks_on()
	plt.grid(which="minor", linestyle="--")

#	if latex_res:
#		latex_res.write(r"\end{tabular}" + "\n")
#		latex_res.close()


	set_ax_size()

	plt.show()

##########################################
#
#  NNPDF23 
#
##########################################

def nnpdf_analysis():
	pdf_data = pdf_data_for("NNPDF23")
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_alphas_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_mb_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_combined_errors(pdf_data, m_Hs[cm_energy])

	print ""
	print "***************************************"
	print "*  NNPDF23-Results for %5s          *" % cm_energy
	print "***************************************"

	x = [m_H[0] for m_H in m_Hs[cm_energy]]
	scale_var = [get_scale_var_new(m) for m in x]  #mf!

	def print_line(pdf_data, pdf, i, start):
		res = pdf_data[pdf][i]

		print " %4s   %8s   %.2e   +%.2e  %.2e    +%.2e      +%.2e      +%.2e      +%.2e      +%.2e"  % ((m_Hs[cm_energy][i][0] if start else ""), pdf, res["pdf_central_lo"], res["pdfup_lo"], res["pdf_central_nlo"], res["pdfup_nlo"], res["alphaspdfup_nlo"], res["mbpdfup_nlo"], scale_var[i][2], res["combinedup_nlo"]+scale_var[i][2])
		print "                              -%.2e              -%.2e      -%.2e      -%.2e      -%.2e      -%.2e" % (res["pdflo_lo"], res["pdflo_nlo"], res["alphaspdflo_nlo"], res["mbpdflo_nlo"], scale_var[i][1], res["combinedlo_nlo"]+scale_var[i][1])

		if latex_res:
			latex_res.writelines([
				r"%s & %.2e & +%.2e & %.2e & +%.2e & +%.2e & +%.2e & +%.2e & +%.2e \\" % (m_Hs[cm_energy][i][0], res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphaspdfup_nlo"], res["mbpdfup_nlo"], scale_var[i][2], res["combinedup_nlo"]) + "\n",
			r" & & -%.2e  & & -%.2e & -%.2e & -%.2e & -%.2e & -%.2e \\" % (res["pdflo_lo"], res["pdflo_nlo"], res["alphaslo_nlo"], res["mblo_nlo"], scale_var[i][1], res["combinedlo_nlo"]) + "\n",
			r"\hline" + "\n"])

	print ""
	print "  M_H    pdf-set         LO    pdf_error      NLO    pdf_error   as_pdf_error   mb_pdf_error      scale_var    total_error"
	print "--------------------------------------------------------------------------------------------------------------------------"

	if latex_res:
		latex_res.write(r"\begin{tabular}{|c|r|r|r|r|r|r|r|r|}" + "\n")
		latex_res.write(r"\hline" + "\n")
#		latex_res.write(r"$M_{H^-}$ [GeV] & $\sigma_{LO}$ [pb] & $\sigma_{PDF}$ [pb] & $\sigma_{NLO}$ [pb] & $\sigma_{PDF}$ [pb] & $\sigma_{PDF+\alpha_s}$ [pb] & $\sigma_{PDF+M_b}$ [pb] & $\sigma_{Scale}$ [pb] & $\sigma_{total}$ [pb] \\" + "\n")
		#latex_res.write(r"$M_{H^-}$ [GeV] & \mySigma{LO} [pb] & \mySigma{PDF} [pb] & \mySigma{NLO} [pb] & \mySigma{PDF} [pb] & \mySigma{PDF+$\alpha_s$} [pb] & \mySigma{PDF+$M_b$} [pb] & \mySigma{Scale} [pb] & \mySigma{total} [pb] \\" + "\n")
		latex_res.write(r"$M_{H^-}$ & \mySigma{LO} [pb] & \mySigma{PDF} [pb] & \mySigma{NLO} [pb] & \mySigma{PDF} [pb] & \mySigma{PDF+$\alpha_s$} [pb] & \mySigma{PDF+$M_b$} [pb] & \mySigma{Scale} [pb] & \mySigma{total} [pb] \\" + "\n")
		latex_res.write(r"[GeV] & & & & & & & & \\" + "\n")
		latex_res.write(r"\hline" + "\n")


	for i in range(0, len(m_Hs[cm_energy])):
		start = True

		print_line(pdf_data, "NNPDF23", i, start)
		start = False

	if latex_res:
		latex_res.write(r"\end{tabular}" + "\n")
		latex_res.close()
        exit()

	count = 0

	data = pdf_data["NNPDF23"]
	pdf_err_lo = [(data[i]["pdf_central_lo"], data[i]["pdfup_lo"], data[i]["pdflo_lo"]) for i in range(0, len(m_Hs[cm_energy]))]
	pdf_err = [(data[i]["pdf_central_nlo"], data[i]["pdfup_nlo"], data[i]["pdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
	als_pdf_err = [(data[i]["pdf_central_nlo"], data[i]["alphaspdfup_nlo"], data[i]["alphaspdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
	mb_pdf_err = [(data[i]["pdf_central_nlo"], data[i]["mbpdfup_nlo"], data[i]["mbpdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
	complete_err = [(data[i]["pdf_central_nlo"], data[i]["combinedup_nlo"], data[i]["combinedlo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]


	ax = plt.subplot(1,1,1)
		
	plt.subplots_adjust(left = 0.05, right = 0.96, top = 0.95, bottom = 0.06)


#	plot_error_tube(x, pdf_err_lo, "gray", legend="LO + PDF-error")
#	plot_error_tube(x, als_pdf_err, "green", legend = "$\\alpha_s$+PDF-error in NLO")
#	plot_error_tube(x, mb_pdf_err, "blue", legend = "$M_b$+PDF-error in NLO")
#	plot_error_tube(x, pdf_err, "red", legend = "PDF-error in NLO")
#	plot_error_tube(x, complete_err, "black", legend = "NLO + total error")

	plot_error_tube(x, complete_err, "black", legend = "cross section + total error", tube_style=True)
	plot_error_tube(x, mb_pdf_err, "blue", legend = "$M_b$+PDF-error", tube_style=True)
	plot_error_tube(x, pdf_err, "red", legend = "PDF-error", tube_style=True)
	plot_error_tube(x, als_pdf_err, "yellow", legend = "$\\alpha_s$+PDF-error in NLO", tube_style=True)
#	plot_error_tube(x, pdf_err_lo, "gray", legend="LO + PDF-error")
	plt.plot(x, [c[0] for c in complete_err], "black", linestyle="-")


	plt.legend(loc = "best", prop=font(size=30))
	plt.xlabel("$M_{H^-}$ [GeV]", fontdict={"size":30})
	plt.ylabel("$\sigma$ [pb]", fontdict={"size":30})
	plt.text(0.05, 0.1, "pp $\\rightarrow$ $H^-$t at %s at NLO\ncalculated with NNPDF23 in 2HDM\n$M_t$ = 172.5 GeV\n$M_b$ = 4.75 GeV\n$\\alpha_s$ = 0.118\n$\\tan \\beta$ = 30.0" % cm_energy, transform= ax.transAxes, fontdict={"size":"36"})
	plt.semilogy()
	plt.xlim(200, 500)
	if cm_energy == "14TeV":
		plt.ylim(0.08, 1.1)
	if cm_energy == "8TeV":
		plt.ylim(0.01, 0.3)
		

	plt.grid(which="major", linestyle="-")
	plt.minorticks_on()
	plt.grid(which="minor", linestyle="--")

#	if latex_res:
#		latex_res.write(r"\end{tabular}" + "\n")
#		latex_res.close()

	plt.show()



#################################################
#                                               #
#    COMBINED                                   #
#                                               #
#################################################

def combined_analysis():
	init_data_struct()
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_alphas_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_mb_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_combined_errors(pdf_data, m_Hs[cm_energy])

	print "\n\n"

	print latex_res

	print ""
	print "***************************************"
	print "*  Combined-Results for %5s         *" % cm_energy
	print "***************************************"

	x = [m_H[0] for m_H in m_Hs[cm_energy]]
#	scale_var = [get_scale_var_new(m) for m in x]  #mf!
	scale_var = [get_scale_var_new(m) for m in x]  #mf!!

	def print_line(pdf_data, pdf, i, start):
		res = pdf_data[pdf][i]

		print " %4s   %8s   %.2e   +%.2e  %.2e    +%.2e"  % ((m_Hs[cm_energy][i][0] if start else ""), pdf, res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["combinedup_nlo"])
		print "                              -%.2e              -%.2e      " % (res["pdflo_lo"], res["combinedlo_nlo"])

		if latex_res:
			latex_res.writelines([
				r"%s & %.2e & $\pm$%.2e & %.2e & $\pm$%.2e \\" % (m_Hs[cm_energy][i][0], res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["combinedup_nlo"]) + "\n",
	#		r" & & -%.2e  & & -%.2e \\" % (res["pdflo_lo"], res["combinedlo_nlo"]) + "\n",
			r"\hline" + "\n"])

	print ""
	print "  M_H    pdf-set         LO    pdf_error      NLO    total_error"
	print "----------------------------------------------------------------"

	if latex_res:
		latex_res.write(r"\begin{tabular}{|c|r|r|r|r|}" + "\n")
		latex_res.write(r"\hline" + "\n")
#		latex_res.write(r"$M_{H^-}$ [GeV] & $\sigma_{LO}$ [pb] & $\sigma_{PDF}$ [pb] & $\sigma_{NLO}$ [pb] & $\sigma_{PDF}$ [pb] & $\sigma_{PDF+\alpha_s}$ [pb] & $\sigma_{PDF+M_b}$ [pb] & $\sigma_{Scale}$ [pb] & $\sigma_{total}$ [pb] \\" + "\n")
		latex_res.write(r"$M_{H^-}$ [GeV] & \mySigma{LO} [pb] & \mySigma{PDF} [pb] & \mySigma{NLO} [pb] & \mySigma{total} [pb] \\" + "\n")
		latex_res.write(r"\hline" + "\n")


	for i in range(0, len(m_Hs[cm_energy])):
		start = True

		print_line(pdf_data, "combined", i, start)
		start = False

	if latex_res:
		latex_res.write(r"\end{tabular}" + "\n")
		latex_res.close()
        exit()

	count = 0

	data = pdf_data["combined"]

	pdf_err_lo = [(data[i]["central_lo"], data[i]["pdfup_lo"], data[i]["pdflo_lo"]) for i in range(0, len(m_Hs[cm_energy]))]
	#pdf_err = [(data[i]["central_nlo"], data[i]["pdfup_nlo"], data[i]["pdflo_nlo"]) for i in range(0, len(m_Hs))]
	#als_pdf_err = [(data[i]["central_nlo"], data[i]["alphaspdfup_nlo"], data[i]["alphaspdflo_nlo"]) for i in range(0, len(m_Hs))]
	#mb_pdf_err = [(data[i]["central_nlo"], data[i]["mbpdfup_nlo"], data[i]["mbpdflo_nlo"]) for i in range(0, len(m_Hs))]
	complete_err = [(data[i]["central_nlo"], data[i]["combinedup_nlo"], data[i]["combinedlo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
		
	plt.subplots_adjust(left = 0.05, right = 0.96, top = 0.95, bottom = 0.06)


#	plot_error_tube(x, pdf_err_lo, "gray", legend="LO + PDF-error")
#	plot_error_tube(x, als_pdf_err, "green", legend = "$\\alpha_s$+PDF-error in NLO")
#	plot_error_tube(x, mb_pdf_err, "blue", legend = "$M_b$+PDF-error in NLO")
#	plot_error_tube(x, pdf_err, "red", legend = "PDF-error in NLO")
#	plot_error_tube(x, complete_err, "black", legend = "NLO + total error")

	plot_error_tube(x, complete_err, "black", legend = "cross section + total error")
	plot_error_tube(x, pdf_err_lo, "gray", legend="LO + PDF-error")
#	plt.plot(x, [c[0] for c in complete_err], "black", linestyle="-")


	plt.legend(loc = "best", prop=font(size=30))
	plt.xlabel("$M_{H^-}$ [GeV]", fontdict={"size":30})
	plt.ylabel("$\sigma$ [pb]", fontdict={"size":30})
	#plt.text(0.05, 0.1, "pp $\\rightarrow$ $H^-$t at %s in NLO\ncombined results from CT10,MSTW2008,NNPDF23\n$M_t$ = 172.5 GeV\n$M_b$ = 4.75 TeV\n$\\tan \\beta$ = 30.0" % cm_energy, transform= ax.transAxes, fontdict={"size":"36"})
	plt.semilogy()
	plt.xlim(200, 500)
	if cm_energy == "14TeV":
		plt.ylim(0.08, 1.1)
	if cm_energy == "8TeV":
		plt.ylim(0.01, 0.3)
		

	plt.grid(which="major", linestyle="-")
	plt.minorticks_on()
	plt.grid(which="minor", linestyle="--")

#	if latex_res:
#		latex_res.write(r"\end{tabular}" + "\n")
#		latex_res.close()


	set_ax_size()

	plt.show()


#################################################
#                                               #
#    ALL                                        #
#                                               #
#################################################


def analysis_all():
	init_data_struct()
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_alphas_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_mb_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_combined_errors(pdf_data, m_Hs[cm_energy])

	print ""
	print "***************************************"
	print "*  Complete Results for %5s         *" % cm_energy
	print "***************************************"


	x = [m_H[0] for m_H in m_Hs[cm_energy]]
	scale_var = [get_scale_var_new(m) for m in x]  #mf!

	def print_line(pdf_data, pdf, i, start):
		res = pdf_data[pdf][i]


		if pdf != "CT10":
			print " %4s   %8s   %.2e  +%.2e   %.2e    +%.2e      +%.2e      +%.2e   +%.2e      +%.2e"  % ((m_Hs[cm_energy][i][0] if start else ""), pdf, res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphaspdfup_nlo"], res["mbpdfup_nlo"], scale_var[i][2], res["combinedup_nlo"])
#			print " %4s   %8s   %e  +%e   %e    +%e      +%e      +%e   +%e      +%e"  % ((m_Hs[i][0] if start else ""), pdf, res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphaspdfup_nlo"], res["mbpdfup_nlo"], scale_var[i][2], res["combinedup_nlo"])
			print "                             -%.2e               -%.2e      -%.2e      -%.2e   -%.2e      -%.2e" % (res["pdflo_lo"], res["pdflo_nlo"], res["alphaspdflo_nlo"], res["mbpdflo_nlo"], scale_var[i][1], res["combinedlo_nlo"])
#			print "                             -%e               -%e      -%e      -%e   -%e      -%e" % (res["pdflo_lo"], res["pdflo_nlo"], res["alphaspdflo_nlo"], res["mbpdflo_nlo"], scale_var[i][1], res["combinedlo_nlo"])
		else:
			print " %4s   %8s   %.2e  +%.2e   %.2e    +%.2e      +%.2e                  +%.2e      +%.2e"  % ((m_Hs[cm_energy][i][0] if start else ""), pdf, res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphaspdfup_nlo"], scale_var[i][2], res["combinedup_nlo"])
			print "                             -%.2e               -%.2e      -%.2e                  -%.2e      -%.2e" % (res["pdflo_lo"], res["pdflo_nlo"], res["alphaspdflo_nlo"], scale_var[i][1], res["combinedlo_nlo"])


	print ""
	print "  M_H    pdf-set         LO  pdf_error        NLO    pdf_error   as_pdf_error   mb_pdf_error   scale_var    total_error"
	print "-----------------------------------------------------------------------------------------------------------------------"

	for i in range(0, len(m_Hs[cm_energy])):
		start = True

		for pdf in pdf_data:
			if pdf == "combined":
				continue

			print_line(pdf_data, pdf, i, start)
			start = False

		print_line(pdf_data, "combined", i, start)
		print ""

	
	count = 0

	for pdf in pdf_data:
		count += 1
		data = pdf_data[pdf]
		pdf_err = [(data[i]["central_nlo"], data[i]["pdfup_nlo"], data[i]["pdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
		als_pdf_err = [(data[i]["central_nlo"], data[i]["alphaspdfup_nlo"], data[i]["alphaspdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
		mb_pdf_err = [(data[i]["central_nlo"], data[i]["mbpdfup_nlo"], data[i]["mbpdflo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
		#if pdf != "CT10":
		#	complete_err = [(data[i]["central_nlo"], data[i]["mbpdfup_nlo"] + scale_var[i][2], data[i]["mbpdflo_nlo"] + scale_var[i][1]) for i in range(0, len(m_Hs))]
		#else:
		#	complete_err = [(data[i]["central_nlo"], data[i]["alphaspdfup_nlo"] + scale_var[i][2], data[i]["alphaspdflo_nlo"] + scale_var[i][1]) for i in range(0, len(m_Hs))]
		complete_err = [(data[i]["central_nlo"], data[i]["combinedup_nlo"], data[i]["combinedlo_nlo"]) for i in range(0, len(m_Hs[cm_energy]))]
		
		plt.subplot(2, 2, count)
		plt.title(pdf)

		plot_error_tube(x, als_pdf_err, "green", legend = "NLO + alphas+pdf-error")
		if pdf != "CT10":
			plot_error_tube(x, mb_pdf_err, "blue", legend = "NLO + mb+pdf-error")
		plot_error_tube(x, pdf_err, "red", legend = "NLO + pdf-error")
		plot_error_tube(x, complete_err, "black", legend = "NLO + total-error")


		plt.legend(loc = "best")
		plt.semilogy()
		plt.xlim(200, 500)
		if cm_energy == "14TeV":
			plt.ylim(0.07, 1.5)
		if cm_energy == "8TeV":
			plt.ylim(0.01, 0.3)
		

		plt.grid(which="major", linestyle="-")
		plt.minorticks_on()
		plt.grid(which="minor", linestyle="--")

	plt.show()


	"""
	colors = ["red", "green", "blue", "black"]

	for pdf in pdf_data:
		data = pdf_data[pdf]
		pdf_err = [(data[i]["central_nlo"], data[i]["pdfup_nlo"], data[i]["pdflo_nlo"]) for i in range(0, len(m_Hs))]
		als_pdf_err = [(data[i]["central_nlo"], data[i]["alphaspdfup_nlo"], data[i]["alphaspdflo_nlo"]) for i in range(0, len(m_Hs))]
		mb_pdf_err = [(data[i]["central_nlo"], data[i]["mbpdfup_nlo"], data[i]["mbpdflo_nlo"]) for i in range(0, len(m_Hs))]
		
		plt.title("Check LHC-Errors.")

#		plot_error_tube(x, als_pdf_err, "green", legend = "pdf")
#		if pdf != "CT10":
#			plot_error_tube(x, mb_pdf_err, "blue", legend = "NLO + mb+pdf-error")
		color = colors[0]
		del colors[0]
		plot_error_tube(x, mb_pdf_err, color, legend = pdf)

		plt.legend(loc = "best")
		plt.semilogy()
		plt.ylim(0.07, 1.5)
		plt.xlim(200, 500)
	

	plt.show()
	"""



######################################################## 
#
# create output for santander matching
#
######################################################## 
	
def santander_output():
	init_data_struct()
	calc_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_alphas_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_mb_pdf_errors(pdf_data, m_Hs[cm_energy])
	calc_combined_errors(pdf_data, m_Hs[cm_energy])

	data = pdf_data["combined"]

	f = open("santander_out_%s" % cm_energy, "w") 

	f.write("# M_H    NLO        sigma_+     sigma_-\n")

	for i in range(0, len(m_Hs[cm_energy])):
		f.write(" %4s    %.2e   %.2e    %.2e\n" % (m_Hs[cm_energy][i][0], data[i]["central_nlo"], data[i]["combinedup_nlo"], data[i]["combinedlo_nlo"]))

	f.close()




import sys

if __name__ == "__main__":
	if len(sys.argv) > 1:
		if len(sys.argv) >= 4:
			if sys.argv[2] == "-l":
				latex_res = open(sys.argv[3], "w")

		if sys.argv[1] == "scale_var":
			scale_var_analysis(m_Hs[cm_energy], latex_res)
			exit()
		elif sys.argv[1] == "scale_var_new":
			scale_var_new_analysis(m_Hs[cm_energy], latex_res)
			exit()
		elif sys.argv[1] == "scaleplot":
			scaleplot_analysis(m_Hs[cm_energy], latex_res)
			exit()
		elif sys.argv[1] == "tables":
			create_all_tables()
			exit()
		elif sys.argv[1] == "pdf_error":
			pdf_error()
			exit()
		elif sys.argv[1] == "alphas_pdf_error":
			alphas_pdf_error()
			exit()
		elif sys.argv[1] == "mb_pdf_error":
			mb_pdf_error()
			exit()
		elif sys.argv[1] == "difference":
			difference_plot()
			exit()
		elif sys.argv[1] == "error":
			error_plot()
			exit()
		elif sys.argv[1] == "CT10":
			ct10_analysis()
			exit()
		elif sys.argv[1] == "MSTW":
			mstw_analysis()
			exit()
		elif sys.argv[1] == "NNPDF":
			nnpdf_analysis()
			exit()
		elif sys.argv[1] == "combined":
			combined_analysis()
			exit()
		elif sys.argv[1] == "combined2":
			combined2()
			exit()
		elif sys.argv[1] == "santander":
			santander_output()
			exit()
		else:
			print "Unknown param: %s" % sys.argv[1]
			exit()

	analysis_all()

