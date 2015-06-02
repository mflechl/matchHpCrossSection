################################################
#
#  PDF + MB - ERROR
#
################################################

from pdf_error import get_pdf_error
from math import sqrt, exp

mb_pdf_error = {}

mb_nnpdfwarning = False
mb_nnpdfgaussian = False

# Calculate alphas + pdf error for nnpdf
def mb_pdf_error1(m_H):
	# Create bins for gaussian peak around 0.118

	N_cent = 100

	N_repl = [ (i, int(round(exp( - ( i - 4.75)**2 / (2.0*(0.10)**2) ) * N_cent))) for i in [4.25, 4.5, 4.75, 5.0, 5.25]] #MF
#	N_repl = [ (i, int(round(exp( - ( i - 4.75)**2 / (2.0*(0.25)**2) ) * 100))) for i in [4.25, 4.5, 4.75, 5.0, 5.25]]

	global mb_nnpdfgaussian
	if not mb_nnpdfgaussian:
		print "Gaussian-bins for mb: %s" % N_repl
		mb_nnpdfgaussian = True
#		exit()

	sum_lo = 0.0
	sum_lo2 = 0.0
	sum_nlo = 0.0
	sum_nlo2 = 0.0
	sum_susy = 0.0
	sum_susy2 = 0.0

	N = 0

	for repl in N_repl:
		data = read_table("NNPDF21_mb%d_%dGeV" % (repl[0]*100, m_H))
#		data = read_table("NNPDF21_mb%d_%dGeV" % (repl[0]*N_cent, m_H))
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

	sum_lo = sum_lo/N
	sum_lo2 = sum_lo2/N
	sum_nlo = sum_nlo/N
	sum_nlo2 = sum_nlo2/N
	sum_susy = sum_susy/N
	sum_susy2 = sum_susy2/N

	global mb_nnpdfwarning
	if not mb_nnpdfwarning:
		print "WARNING: No LO mb+pdf-error for NNPDF."
		mb_nnpdfwarning = True

	return ( sum_lo, 0.0, 0.0, 
	         sum_nlo, sqrt(N * (sum_nlo2 - sum_nlo**2.0) / ( N - 1)), sqrt(N * (sum_nlo2 - sum_nlo**2.0) / ( N - 1)),
	         sum_susy, sqrt(N * (sum_susy2 - sum_susy**2.0) / ( N - 1)), sqrt(N * (sum_susy2 - sum_susy**2.0) / ( N - 1)),
		 0.0, 0.0)

mb_pdf_error["NNPDF23"] = mb_pdf_error1

mb_ct10warning = False

# Calculate mb-error for ct10
def mb_pdf_error2(m_H):
	pdf_err = get_pdf_error("CT10", m_H)

	global mb_ct10warning
	if not mb_ct10warning:
		print "WARNING: No mb-error for CT10!!"
		mb_ct10warning = True

	return (pdf_err[0], 0.0, 0.0,
		pdf_err[3], 0.0, 0.0,
		pdf_err[6], 0.0, 0.0,
		0.0, 0.0)

mb_pdf_error["CT10"] = mb_pdf_error2

from pdf_error import get_pdf_error

mb_mstwwarning = False

# Calculate pdf-error from mstw with hepdata method
def mb_pdf_error3(m_H):
	pdf_err = get_pdf_error("MSTW2008", m_H)

	mstw_mb = read_table("MSTW2008mb_%dGeV" % m_H)
	mstw = read_table("MSTW2008_%dGeV" % m_H) 

	err_p_nlo = ( mstw_mb[4][4] - mstw[0][4] ) * 0.24   #MF
	err_m_nlo = ( mstw_mb[3][4] - mstw[0][4] ) * 0.24   #MF

        print "X %d" % err_p_nlo 

	if err_m_nlo > 0:
		if err_m_nlo > err_p_nlo:
			err_p_nlo = err_m_nlo
		err_m_nlo = 0
	if err_p_nlo < 0:
		if err_p_nlo * -1 > err_m_nlo:
			err_m_nlo = err_p_nlo * -1
		err_p_nlo = 0

	if err_m_nlo == 0.0:
		err_m_nlo = -0.0



	# Using nlo error for lo and susy
	combined_p_lo = sqrt(err_p_nlo**2 + pdf_err[2]**2)
	combined_m_lo = sqrt(err_m_nlo**2 + pdf_err[1]**2)
	combined_p_susy = sqrt(err_p_nlo**2 + pdf_err[8]**2)
	combined_m_susy = sqrt(err_m_nlo**2 + pdf_err[7]**2)

	combined_p_nlo = sqrt(err_p_nlo**2 + pdf_err[5]**2)
	combined_m_nlo = sqrt(err_m_nlo**2 + pdf_err[4]**2)

	global mb_mstwwarning
	if not mb_mstwwarning:
		print "WARNING: No LO mb+pdf-error for MSTW."
		mb_mstwwarning = True

	return (pdf_err[0], 0.0, 0.0,
	        pdf_err[3], combined_m_nlo, combined_p_nlo,
	        pdf_err[6], combined_m_susy, combined_p_susy,
		-1*err_m_nlo, err_p_nlo)


mb_pdf_error["MSTW2008"] = mb_pdf_error3


from tables import read_table as read_table

nnpdf_mb_warning = False

def get_mb_pdf_error(pdf, m_H):
	if not pdf in mb_pdf_error:
		raise ValueError("Don't have a mb-pdf-error-function for %s." % pdf)

	err_fun = mb_pdf_error[pdf]
	res = err_fun(m_H)
		

	return res


def calc_mb_pdf_errors(pdf_data, m_Hs):
	for pdf in pdf_data:
		if pdf == "combined":
			continue

		data_set = pdf_data[pdf]

		for i in range(0, len(m_Hs)):
			data_point = data_set[i]

			res = get_mb_pdf_error(pdf, m_Hs[i][0])

			if "central_lo" in data_point and data_point["central_lo"] != res[0]:
				print "WARNING for PDF %s with m_H = %d: Previously calculated value for central_lo %10e differs from the value %10e calculated now." % (pdf, m_Hs[i][0], data_point["central_lo"], res[0]) 
			if "central_nlo" in data_point and data_point["central_nlo"] != res[3]:
				print "WARNING for PDF %s with m_H = %d: Previously calculated value for central_nlo %10e differs from the value %10e calculated now." % (pdf, m_Hs[i][0], data_point["central_nlo"], res[3]) 

			data_point["central_lo"] = res[0]
			data_point["mb_central_lo"] = res[0]
			data_point["mbpdflo_lo"] = res[1]
			data_point["mbpdfup_lo"] = res[2]
			data_point["central_nlo"] = res[3]
			data_point["mb_central_nlo"] = res[3]
			data_point["mbpdflo_nlo"] = res[4]
			data_point["mbpdfup_nlo"] = res[5]
			data_point["mblo_nlo"] = res[9]
			data_point["mbup_nlo"] = res[10]

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

			if res["central_lo"] - res["mbpdflo_lo"] < lo_sigma_lo:
				lo_sigma_lo = res["central_lo"]-res["mbpdflo_lo"]
			if res["central_lo"] + res["mbpdfup_lo"] > up_sigma_lo:
				up_sigma_lo = res["central_lo"]+res["mbpdfup_lo"]

			if res["central_nlo"] - res["mbpdflo_nlo"] < lo_sigma_nlo:
				lo_sigma_nlo = res["central_nlo"]-res["mbpdflo_nlo"]
			if res["central_nlo"] + res["mbpdfup_nlo"] > up_sigma_nlo:
				up_sigma_nlo = res["central_nlo"] + res["mbpdfup_nlo"]

		#mean_lo = mean_lo/count
		#mean_nlo = mean_nlo/count

		mean_lo = (up_sigma_lo + lo_sigma_lo)/2.0
		mean_nlo = (up_sigma_nlo + lo_sigma_nlo)/2.0

		lo_sigma_lo = mean_lo - lo_sigma_lo
		up_sigma_lo = up_sigma_lo - mean_lo
		lo_sigma_nlo = mean_nlo - lo_sigma_nlo
		up_sigma_nlo = up_sigma_nlo - mean_nlo

#		if lo_sigma_lo != up_sigma_lo or lo_sigma_nlo != up_sigma_nlo:
#			print lo_sigma_lo != up_sigma_lo
#			print lo_sigma_nlo != up_sigma_nlo
#			print lo_sigma_lo
#			print up_sigma_lo
#			print lo_sigma_nlo
#			print up_sigma_nlo
#			exit()

		data_point = data_set[i]

		# Try to find problems
		if "central_lo" in data_point and data_point["central_lo"] != mean_lo:
			print "WARNING for combined with m_H = %d: Previously calculated value for central_lo %10e differs from the value %10e calculated now." % (m_Hs[i][0], data_point["central_lo"], mean_lo) 
		if "central_nlo" in data_point and data_point["central_nlo"] != mean_nlo:
			print "WARNING for combined with m_H = %d: Previously calculated value for central_nlo %10e differs from the value %10e calculated now." % (m_Hs[i][0], data_point["central_nlo"], mean_nlo) 


		data_point["central_lo"] = mean_lo
		data_point["central_nlo"] = mean_nlo
		data_point["mb_central_lo"] = mean_lo
		data_point["mb_central_nlo"] = mean_nlo
		data_point["mbpdflo_lo"] = lo_sigma_lo
		data_point["mbpdfup_lo"] = up_sigma_lo
		data_point["mbpdflo_nlo"] = lo_sigma_nlo
		data_point["mbpdfup_nlo"] = up_sigma_nlo

def print_mb_pdf_error(pdf_data, m_Hs):	
	print ""
	print "****************************"
	print "*  MB - PDF - Errors       *"
	print "****************************"


	for i in range(0, len(m_Hs)):
		start = True
		print "        M_H            LO     pdf-error           NLO     pdf-error  pdf-mb-error  "
		print "-----------------------------------------------------------------------------------"

		for pdf in pdf_data:
			if pdf == "combined":
				continue

			res = pdf_data[pdf][i]

			print " %10s  %10e +%10e  %10e +%10e +%10e    %s" % ((m_Hs[i][0] if start else ""), res["central_lo"], res["pdfup_lo"], res["central_nlo"], res["pdfup_nlo"], res["mbpdfup_nlo"], pdf)
			print " %10s  %12s -%10e  %12s -%10e -%10e" % ("", "", res["pdflo_lo"], "", res["pdflo_nlo"], res["mbpdflo_nlo"])

			start = False	

		print ""
		print "  Combination:    LO + pdf: %10e    +%10e" % (res["central_lo"], res["pdfup_lo"])
		print "                                            -%10e" % res["pdflo_nlo"]
		print "              NLO + as_pdf: %10e    +%10e" % (res["central_nlo"], res["mbpdfup_nlo"])
		print "                                            -%10e" % res["mbpdflo_nlo"] 

