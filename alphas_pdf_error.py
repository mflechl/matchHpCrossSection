################################################
#
# PDF + ALPHAS ERRORS
#
################################################

alphas_pdf_error = {}

from math import sqrt
from math import exp

as_nnpdfwarning = False
as_nnpdfgaussian = False

# Calculate alphas + pdf error for nnpdf
def alphas_pdf_error1(m_H):
	# Create bins for gaussian peak around 0.118

	N_repl = [ (i, int(round(exp( (-( i - 0.118)**2) / (2.0*((0.0012)**2)) ) * 100))) for i in [0.114, 0.115, 0.116, 0.117, 0.118, 0.119, 0.120, 0.121, 0.122, 0.123, 0.124]]

	sum_lo = 0.0
	sum_lo2 = 0.0
	sum_nlo = 0.0
	sum_nlo2 = 0.0
	sum_susy = 0.0
	sum_susy2 = 0.0

#	N_repl = [(0.120, 100)]

	global as_nnpdfgaussian
	if not as_nnpdfgaussian:
		print "Gaussian-bins for as: %s" % N_repl
		as_nnpdfgaussian = True


	N = 0

	for repl in N_repl:
		data = read_table("NNPDF23_as0%d_%dGeV" % (repl[0]*1000, m_H))
#		print "Reading %d entries of NNPDF23_as0%d_%dGeV" % (repl[1], repl[0]*1000, m_H)
		N += repl[1]
		for i in range(1, repl[1] + 1):
			d = data[i]

			sum_lo += d[2]
			sum_lo2 += d[2]**2.0
			sum_nlo += d[4]
			sum_nlo2 += d[4]**2.0
			sum_susy += d[7]
			sum_susy2 += d[7]**2.0

#	N = float(len(data)-1)
#	print "Total number of replicas: %d" % N

	sum_lo = sum_lo/N
	sum_lo2 = sum_lo2/N
	sum_nlo = sum_nlo/N
	sum_nlo2 = sum_nlo2/N
	sum_susy = sum_susy/N
	sum_susy2 = sum_susy2/N

	global as_nnpdfwarning
	if not as_nnpdfwarning:
		print "WARNING: No LO alphas+pdf-error for NNPDF."
		as_nnpdfwarning = True

#	return ( sum_lo, sqrt(N * (sum_lo2 - sum_lo**2.0) / ( N - 1)), sqrt(N * (sum_lo2 - sum_lo**2.0) / ( N - 1)),
	return ( sum_lo, 0.0, 0.0,
	         sum_nlo, sqrt(N * (sum_nlo2 - sum_nlo**2.0) / ( N - 1)), sqrt(N * (sum_nlo2 - sum_nlo**2.0) / ( N - 1)),
	         sum_susy, sqrt(N * (sum_susy2 - sum_susy**2.0) / ( N - 1)), sqrt(N * (sum_susy2 - sum_susy**2.0) / ( N - 1)), 0.0, 0.0
		 , 0.0, 0.0)

alphas_pdf_error["NNPDF23"] = alphas_pdf_error1

from pdf_error import get_pdf_error

as_ct10warning = False

# Calculate pdf-error with 90% prescription from ct10
# with hepdata method
def alphas_pdf_error2(m_H):
	pdf_err = get_pdf_error("CT10", m_H)

	ct10 = read_table("CT10_%dGeV" % m_H) 
	ct10as = read_table("CT10as_%dGeV" % m_H) 

	C59 = 5.0/6.0

	err_m_nlo = (ct10as[4][4] - ct10[0][4]) / C59
	err_p_nlo = (ct10as[6][4] - ct10[0][4]) / C59

	if err_m_nlo > 0:
		if err_m_nlo > err_p_nlo:
			err_p_nlo = err_m_nlo
		err_m_nlo = 0
	if err_p_nlo < 0:
		if err_p_nlo < err_m_nlo:
			err_m_nlo = err_p_nlo
		err_p_nlo = 0

	if err_m_nlo == 0.0:
		err_m_nlo = -0.0

	# Using nlo error for lo and susy
	combined_m_lo = sqrt(err_m_nlo**2 + pdf_err[1]**2)
	combined_p_lo = sqrt(err_p_nlo**2 + pdf_err[2]**2)
	combined_m_susy = sqrt(err_m_nlo**2 + pdf_err[7]**2)
	combined_p_susy = sqrt(err_p_nlo**2 + pdf_err[8]**2)

	combined_m_nlo = sqrt(err_m_nlo**2 + pdf_err[4]**2)
	combined_p_nlo = sqrt(err_p_nlo**2 + pdf_err[5]**2)

	global as_ct10warning
	if not as_ct10warning:
		print "WARNING: No LO alphas+pdf-error for CT10."
		as_ct10warning = True

	return (pdf_err[0], 0.0, 0.0,
	        pdf_err[3], combined_m_nlo, combined_p_nlo,
	        pdf_err[6], combined_m_susy, combined_p_susy, 
		-1.0*err_m_nlo, err_p_nlo)

alphas_pdf_error["CT10"] = alphas_pdf_error2

as_mstwwarning = False

# Calculate pdf-error from mstw with hepdata method
def alphas_pdf_error3(m_H):
	pdf_err = get_pdf_error("MSTW2008", m_H)

	mstw_p = read_table("MSTW2008+as_%dGeV" % m_H)
	mstw_m = read_table("MSTW2008-as_%dGeV" % m_H)
	mstw = read_table("MSTW2008_%dGeV" % m_H) 

	C79 = 5.0/4.0

#	print "%e   %e   %e" % (mstw_p[0][4], mstw_m[0][4], mstw[0][4])

	err_p_nlo = mstw_p[0][4] - mstw[0][4]
	err_m_nlo = (mstw_m[0][4] - mstw[0][4]) / C79

	if err_m_nlo > 0:
		if err_m_nlo > err_p_nlo:
			err_p_nlo = err_m_nlo
		err_m_nlo = 0
	if err_p_nlo < 0:
		if err_p_nlo < err_m_nlo:
			err_m_nlo = err_p_nlo 
		err_p_nlo = 0

	if err_m_nlo == 0.0:
		err_m_nlo = -0.0

	# Using nlo error for lo and susy
	combined_m_lo = sqrt(err_m_nlo**2 + pdf_err[1]**2)
	combined_p_lo = sqrt(err_p_nlo**2 + pdf_err[2]**2)
	combined_m_susy = sqrt(err_m_nlo**2 + pdf_err[7]**2)
	combined_p_susy = sqrt(err_p_nlo**2 + pdf_err[8]**2)

	combined_m_nlo = sqrt(err_m_nlo**2 + pdf_err[4]**2)
	combined_p_nlo = sqrt(err_p_nlo**2 + pdf_err[5]**2)

	global as_mstwwarning
	if not as_mstwwarning:
		print "WARNING: No LO alphas+pdf-error for MSTW2008."
		as_mstwwarning = True

	return (pdf_err[0], 0.0, 0.0,
	        pdf_err[3], combined_m_nlo, combined_p_nlo,
	        pdf_err[6], combined_m_susy, combined_p_susy,
		-1*err_m_nlo, err_p_nlo)


alphas_pdf_error["MSTW2008"] = alphas_pdf_error3


	
##################################################################
#
# Actual analysis and plotting 
#
##################################################################

from pdf_error import read_table

def get_alphas_pdf_error(pdf, m_H):
	if not pdf in alphas_pdf_error:
		raise ValueError("Don't have an alphas-pdf-error-function for %s" % pdf)

	err_fun = alphas_pdf_error[pdf]

#	data = read_table("%s_%dGeV" % (pdf, m_H))
	res = err_fun(m_H)

	# Hack for CT10, cteq6ll doesn't provide error sets, 
	# take CT10 errors
#	if pdf == "CT10":
#		global as_ct10warning
#		if not as_ct10warning:
#			print "WARNING: No LO alphas+pdf-error for CT10."
#			as_ct10warning = True
#		res = (res[0], res[4], res[5], res[3], res[4], res[5], res[6], res[7], res[8])

	return res

def calc_alphas_pdf_errors(pdf_data, m_Hs):
	for pdf in pdf_data:
		if pdf == "combined":
			continue

		data_set = pdf_data[pdf]

		for i in range(0, len(m_Hs)):
			data_point = data_set[i]

			res = get_alphas_pdf_error(pdf, m_Hs[i][0])

			# Try to find problems
			if "central_lo" in data_point and data_point["central_lo"] != res[0]:
				print "WARNING for PDF %s with m_H = %d: Previously calculated value for central_lo %10e differs from the value %10e calculated now." % (pdf, m_Hs[i][0], data_point["central_lo"], res[0]) 
			if "central_nlo" in data_point and data_point["central_nlo"] != res[3]:
				print "WARNING for PDF %s with m_H = %d: Previously calculated value for central_nlo %10e differs from the value %10e calculated now." % (pdf, m_Hs[i][0], data_point["central_nlo"], res[3]) 

			data_point["central_lo"] = res[0]
			data_point["alphas_central_lo"] = res[0]
			data_point["alphaspdflo_lo"] = res[1]
			data_point["alphaspdfup_lo"] = res[2]
			data_point["central_nlo"] = res[3]
			data_point["alphas_central_nlo"] = res[3]
			data_point["alphaspdflo_nlo"] = res[4]
			data_point["alphaspdfup_nlo"] = res[5]
			data_point["alphaslo_nlo"] = res[9]
			data_point["alphasup_nlo"] = res[10]


	if not "combined" in pdf_data:
		return

	data_set = pdf_data["combined"]
	for i in range(0, len(m_Hs)):
		#mean_lo = 0.0
		lo_sigma_lo = None
		up_sigma_lo = None
		#mean_nlo = 0.0
		lo_sigma_nlo = None
		up_sigma_nlo = None

		count = 0
		for pdf in pdf_data:
			if pdf == "combined":
				continue

			res = pdf_data[pdf][i]

			count += 1

		#	mean_lo += res["central_lo"]
		#	mean_nlo += res["central_nlo"]

			if lo_sigma_lo == None:
				lo_sigma_lo = res["central_lo"]
			if up_sigma_lo == None:
				up_sigma_lo = res["central_lo"]

			if lo_sigma_nlo == None:
				lo_sigma_nlo = res["central_nlo"]
			if up_sigma_nlo == None:
				up_sigma_nlo = res["central_nlo"]

			if res["central_lo"] - res["alphaspdflo_lo"] < lo_sigma_lo:
				lo_sigma_lo = res["central_lo"]-res["alphaspdflo_lo"]
			if res["central_lo"] + res["alphaspdfup_lo"] > up_sigma_lo:
				up_sigma_lo = res["central_lo"]+res["alphaspdfup_lo"]

			if res["central_nlo"] - res["alphaspdflo_nlo"] < lo_sigma_nlo:
				lo_sigma_nlo = res["central_nlo"]-res["alphaspdflo_nlo"]
			if res["central_nlo"] + res["alphaspdfup_nlo"] > up_sigma_nlo:
				up_sigma_nlo = res["central_nlo"] + res["alphaspdfup_nlo"]

		#mean_lo = mean_lo/count
		#mean_nlo = mean_nlo/count

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
		data_point["alphas_central_lo"] = mean_lo 
		data_point["alphaspdflo_lo"] = lo_sigma_lo
		data_point["alphaspdfup_lo"] = up_sigma_lo
		data_point["central_nlo"] = mean_nlo
		data_point["alphas_central_nlo"] = mean_nlo
		data_point["alphaspdflo_nlo"] = lo_sigma_nlo
		data_point["alphaspdfup_nlo"] = up_sigma_nlo

def print_alphas_pdf_error(pdf_data, m_Hs):	
	print ""
	print "****************************"
	print "*  ALPHAS - PDF - Errors   *"
	print "****************************"


	for i in range(0, len(m_Hs)):
		start = True
		print "        M_H            LO     pdf-error           NLO     pdf-error  pdf-as-error  "
		print "-----------------------------------------------------------------------------------"

		for pdf in pdf_data:
			if pdf == "combined":
				continue

			res = pdf_data[pdf][i]

			print " %10s  %10e +%10e  %10e +%10e +%10e    %s" % ((m_Hs[i][0] if start else ""), res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], res["alphaspdfup_nlo"], pdf)
			print " %10s  %12s -%10e  %12s -%10e -%10e" % ("", "", res["pdflo_lo"], "", res["pdflo_nlo"], res["alphaspdflo_nlo"])

			start = False	

		print ""
		print "  Combination:    LO + pdf: %10e    +%10e" % (res["central_lo"], res["pdfup_lo"])
		print "                                            -%10e" % res["pdflo_nlo"]
		print "              NLO + as_pdf: %10e    +%10e" % (res["central_nlo"], res["alphaspdfup_nlo"])
		print "                                            -%10e" % res["alphaspdflo_nlo"] 
