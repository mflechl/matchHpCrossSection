################################################
#
# PDF_ERRORS
#
################################################

pdf_error = {}

from math import sqrt

# Calculate pdf-error with 0th set from data as the central
# value and the other sets the deviation from this
def pdf_error1(data):
	central = data[0]

	sum_lo = 0.0
	sum_lo2 = 0.0
	sum_nlo = 0.0
	sum_nlo2 = 0.0
	sum_susy = 0.0
	sum_susy2 = 0.0

	for d in data:
		# Don't take that!
		if d == central:
			continue

		sum_lo += d[2]
		sum_lo2 += d[2]**2.0
		sum_nlo += d[4]
		sum_nlo2 += d[4]**2.0
		sum_susy += d[7]
		sum_susy2 += d[7]**2.0

	N = float(len(data)-1)

	sum_lo = sum_lo/N
	sum_lo2 = sum_lo2/N
	sum_nlo = sum_nlo/N
	sum_nlo2 = sum_nlo2/N
	sum_susy = sum_susy/N
	sum_susy2 = sum_susy2/N

	return ( sum_lo, sqrt(N * (sum_lo2 - sum_lo**2.0) / ( N - 1)), sqrt(N * (sum_lo2 - sum_lo**2.0) / ( N - 1)),
	         sum_nlo, sqrt(N * (sum_nlo2 - sum_nlo**2.0) / ( N - 1)), sqrt(N * (sum_nlo2 - sum_nlo**2.0) / ( N - 1)),
	         sum_susy, sqrt(N * (sum_susy2 - sum_susy**2.0) / ( N - 1)), sqrt(N * (sum_susy2 - sum_susy**2.0) / ( N - 1)))

#	sum_lo = 0.0
#	sum_nlo = 0.0
#	sum_susy = 0.0
#
#	for d in data:
#		# Don't take that!
#		if d == central:
#			continue
#
#		sum_lo += (d[1] - central[1])**2.0
##		sum_nlo += (d[3] - central[3])**2.0
#		sum_susy += (d[6] - central[6])**2.0
#
#
#	# the -2 in the denominator is due to the fact, that
#	# zeroth date is dropped.
#	return (central[1], ( sum_lo/(len(data)-2) )**(1.0/2.0),
#		central[3], ( sum_nlo/(len(data)-2) )**(1.0/2.0),
#		central[6], ( sum_susy/(len(data)-2) )**(1.0/2.0))


pdf_error["NNPDF23"] = pdf_error1

# Calculate pdf-error with 90% prescription from ct10
# with hepdata method
def pdf_error2(data):
	sum_lop = 0.0
	sum_lom = 0.0
	sum_nlop = 0.0
	sum_nlom = 0.0
	sum_susyp = 0.0
	sum_susym = 0.0

	for i in range(1, int((len(data)+1.0)/2.0)):
		sum_lop += max((data[2*i - 1][2] - data[0][2]), (data[2*i][2]-data[0][2]), 0)**(2.0)
		sum_lom += max((data[0][2] - data[2*i - 1][2]), (data[0][2] - data[2*i][2]), 0)**(2.0)
		sum_nlop += max((data[2*i - 1][4] - data[0][4]), (data[2*i][4]-data[0][4]), 0)**(2.0)
		sum_nlom += max((data[0][4] - data[2*i - 1][4]), (data[0][4] - data[2*i][4]), 0)**(2.0)
		sum_susyp += max((data[2*i - 1][7] - data[0][7]), (data[2*i][7]-data[0][7]), 0)**(2.0)
		sum_susym += max((data[0][7] - data[2*i - 1][7]), (data[0][7] - data[2*i][7]), 0)**(2.0)

	C90 = 1.64485

	return (data[0][2], sqrt(sum_lom)/C90, sqrt(sum_lop)/C90,
	        data[0][4], sqrt(sum_nlom)/C90, sqrt(sum_nlop)/C90,
	        data[0][7], sqrt(sum_susym)/C90, sqrt(sum_susyp)/C90)

pdf_error["CT10"] = pdf_error2

# Calculate pdf-error from mstw with hepdata method
def pdf_error3(data):
	sum_lop = 0.0
	sum_lom = 0.0
	sum_nlop = 0.0
	sum_nlom = 0.0
	sum_susyp = 0.0
	sum_susym = 0.0

	for i in range(1, int((len(data))/2.0)):
		sum_lop += max((data[2*i - 1][2] - data[0][2]), (data[2*i][2]-data[0][2]), 0)**(2.0)
		sum_lom += max((data[0][2] - data[2*i - 1][2]), (data[0][2] - data[2*i][2]), 0)**(2.0)
		sum_nlop += max((data[2*i - 1][4] - data[0][4]), (data[2*i][4]-data[0][4]), 0)**(2.0)
		sum_nlom += max((data[0][4] - data[2*i - 1][4]), (data[0][4] - data[2*i][4]), 0)**(2.0)
		sum_susyp += max((data[2*i - 1][7] - data[0][7]), (data[2*i][7]-data[0][7]), 0)**(2.0)
		sum_susym += max((data[0][7] - data[2*i - 1][7]), (data[0][7] - data[2*i][7]), 0)**(2.0)
		if 2*i == 41:
			raise RuntimeError("MSTW set 41 is irregular!")


	return (data[0][2], sqrt(sum_lom), sqrt(sum_lop),
	        data[0][4], sqrt(sum_nlom), sqrt(sum_nlop),
	        data[0][7], sqrt(sum_susym), sqrt(sum_susyp))

pdf_error["MSTW2008"] = pdf_error3

##################################################################
#
# Actual analysis and plotting 
#
##################################################################

from mh_detail import *
from tables import read_table as read_table

ct10warning = False
mstwwarning = False

def get_pdf_error(pdf, m_H):
	if not pdf in pdf_error:
#		return
		raise ValueError("Don't have a pdf-error-function for %s" % pdf)

	err_fun = pdf_error[pdf]

	data = read_table("%s_%dGeV" % (pdf, m_H))
	res = err_fun(data)

	# Hack for CT10, cteq6ll doesn't provide error sets, 
	# take CT10 errors
	if pdf == "CT10":
		global ct10warning
		if not ct10warning:
			print "WARNING: Using CT10-pdf-error from nlo for lo also."
			ct10warning = True
		res = (res[0], res[4], res[5], res[3], res[4], res[5], res[6], res[7], res[8])
	# Hack for MSTW2008, alphas is not 0.118, use prescription
	if pdf == "MSTW2008":
		global mstwwarning
		if not mstwwarning:
			print "WARNING: Using pdf-error from alphas(MZ)=0.120/0.139 from MSTW for calculation with alphas(MZ)=0.118"
			mstwwarning = True
		res = ( data[41][2], res[1], res[2],
		        data[41][4], res[4], res[5],
		        data[41][7], res[7], res[8])


	return res

def calc_pdf_errors(pdf_data, m_Hs):
	for pdf in pdf_data:
		if pdf == "combined":
			continue
#		if pdf == "NNPDF21":
#			continue
		data_set = pdf_data[pdf]
		# Traverse Higgs-masses
		for i in range(0, len(m_Hs)):
			data_point = data_set[i]
			res = get_pdf_error(pdf, m_Hs[i][0])

			# Try to find problems
			if "central_lo" in data_point and data_point["central_lo"] != res[0]:
				print "WARNING for PDF %s with m_H = %d: Previously calculated value for central_lo %10e differs from the value %10e calculated now." % (pdf, m_Hs[i][0], data_point["central_lo"], res[0]) 
			if "central_nlo" in data_point and data_point["central_nlo"] != res[0]:
				print "WARNING for PDF %s with m_H = %d: Previously calculated value for central_nlo %10e differs from the value %10e calculated now." % (pdf, m_Hs[i][0], data_point["central_nlo"], res[0]) 

			data_point["central_lo"] = res[0]
			data_point["pdf_central_lo"] = res[0]
			data_point["pdflo_lo"] = res[1]
			data_point["pdfup_lo"] = res[2]
			data_point["central_nlo"] = res[3]
			data_point["pdf_central_nlo"] = res[3]
			data_point["pdflo_nlo"] = res[4]
			data_point["pdfup_nlo"] = res[5]

	if not "combined" in pdf_data:
		return

	data_set = pdf_data["combined"]
	for i in range(0, len(m_Hs)):
	#	mean_lo = 0.0
		lo_sigma_lo = None
		up_sigma_lo = None
	#	mean_nlo = 0.0
		lo_sigma_nlo = None
		up_sigma_nlo = None

		count = 0
		for pdf in pdf_data:
			if pdf == "combined":
				continue
#  		        if pdf == "NNPDF21":
#			        continue

			res = pdf_data[pdf][i]

			count += 1

	#		mean_lo += res["central_lo"]
	#		mean_nlo += res["central_nlo"]

			if lo_sigma_lo == None:
				lo_sigma_lo = res["central_lo"]
			if up_sigma_lo == None:
				up_sigma_lo = res["central_lo"]

			if lo_sigma_nlo == None:
				lo_sigma_nlo = res["central_nlo"]
			if up_sigma_nlo == None:
				up_sigma_nlo = res["central_nlo"]

			if res["central_lo"] - res["pdflo_lo"] < lo_sigma_lo:
				lo_sigma_lo = res["central_lo"]-res["pdflo_lo"]
			if res["central_lo"] + res["pdfup_lo"] > up_sigma_lo:
				up_sigma_lo = res["central_lo"]+res["pdfup_lo"]

			if res["central_nlo"] - res["pdflo_nlo"] < lo_sigma_nlo:
				lo_sigma_nlo = res["central_nlo"]-res["pdflo_nlo"]
			if res["central_nlo"] + res["pdfup_nlo"] > up_sigma_nlo:
				up_sigma_nlo = res["central_nlo"] + res["pdfup_nlo"]

	#	mean_lo = mean_lo/count
	#	mean_nlo = mean_nlo/count

		mean_lo = (up_sigma_lo + lo_sigma_lo)/2.0
		mean_nlo = (up_sigma_nlo + lo_sigma_nlo)/2.0

		lo_sigma_lo = mean_lo - lo_sigma_lo
		up_sigma_lo = up_sigma_lo - mean_lo
		lo_sigma_nlo = mean_nlo - lo_sigma_nlo
		up_sigma_nlo = up_sigma_nlo - mean_nlo

		data_point = data_set[i]

		# Try to find problems
		if "central_lo" in data_point and data_point["central_lo"] != mean_lo:
			print "WARNING for combined with m_H = %d: Previously calculated value for central_lo %10e differs from the value %10e calculated now." % (m_Hs[i][0], data_point["central_lo"], mean_lo) 
		if "central_nlo" in data_point and data_point["central_nlo"] != mean_nlo:
			print "WARNING for combined with m_H = %d: Previously calculated value for central_nlo %10e differs from the value %10e calculated now." % (m_Hs[i][0], data_point["central_nlo"], mean_nlo) 


		data_point["central_lo"] = mean_lo
		data_point["central_nlo"] = mean_nlo
		data_point["pdf_central_lo"] = mean_lo
		data_point["pdf_central_nlo"] = mean_nlo
		data_point["pdflo_lo"] = lo_sigma_lo
		data_point["pdfup_lo"] = up_sigma_lo
		data_point["pdflo_nlo"] = lo_sigma_nlo
		data_point["pdfup_nlo"] = up_sigma_nlo


def print_pdf_error(pdf_data, m_Hs):
	print ""
	print "****************************"
	print "*  PDF - Errors            *"
	print "****************************"


	# Traverse Higgs-masses
	for i in range(0, len(m_Hs)):
		start = True
		print ""
		print "        M_H            LO     pdf_error           NLO     pdf_error" 
		print "-----------------------------------------------------------------------"

		for pdf in pdf_data:
			if pdf == "combined":
				continue
			res = pdf_data[pdf][i]

			print " %10s  %3e        +%3e         %3e        +%3e           %s" % (("%s" % (m_Hs[i][0] if start else "")), res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], pdf)
			print " %10s  %5s               -%3e         %5s               -%3e           %s" % ("", "", res["pdflo_lo"], "", res["pdflo_nlo"], "")

			start = False

		res = pdf_data["combined"][i]

		print ""
		print "  Combination:    LO + pdf: %3e    +%3e" % (res["central_lo"], res["pdfup_lo"])
		print "                                            -%3e" % res["pdflo_nlo"]
		print "                 NLO + pdf: %3e    +%3e" % (res["central_nlo"], res["pdfup_nlo"])
		print "                                            -%3e" % res["pdflo_nlo"] 
