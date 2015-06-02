################################################
#
# COMBINED ERRORS
#
################################################

combined_error = {}

from math import sqrt
#from scale_var import get_scale_var
from scale_var_new import get_scale_var_new

def calc_combined_errors(pdf_data, m_Hs):
	for pdf in pdf_data:
		if not pdf in ["combined", "NNPDF23", "MSTW2008", "CT10"]:
			print "WARNING: Can't calculate combined error for unknown pdf %s" % pdf

#	scale_var = [get_scale_var(m[0]) for m in m_Hs]
	scale_var = [get_scale_var_new(m[0]) for m in m_Hs]  #mf!                                                                                                                                                

	lo_sigma_lo = [None]*len(m_Hs)
	up_sigma_lo = [None]*len(m_Hs)
	lo_sigma_nlo = [None]*len(m_Hs)
	up_sigma_nlo = [None]*len(m_Hs)

	if "NNPDF23" in pdf_data:
		data_set = pdf_data["NNPDF23"]

		print "ATTENTION: Combined errors for NNPDF23"
		print "    Using mb+pdf-error as combined error for NNPDF23, since "
		print "    alphas+pdf-error is smaller then pdf-error."
		print "    Using mb+pdf-error for a_s = 0.119 for central value from"
		print "    pdf-error with a_s = 0.118."
		print ""

		for i in range(0, len(m_Hs)):
			data_point = data_set[i]

			# a_s = 0.119 instead of 0.118 for m_b-variation
			# reset central value
			data_point["central_lo"] = data_point["pdf_central_lo"]
			data_point["central_nlo"] = data_point["pdf_central_nlo"]
	
#			data_point["combinedlo_nlo"] = data_point["mbpdflo_nlo"] + scale_var[i][1]
#			data_point["combinedup_nlo"] = data_point["mbpdfup_nlo"] + scale_var[i][2]
			data_point["combinedlo_nlo"] = data_point["mbpdflo_nlo"] #mf
			data_point["combinedup_nlo"] = data_point["mbpdfup_nlo"] #mf

			data_point["combinedlo_lo"] = data_point["pdflo_lo"] + scale_var[i][4]
			data_point["combinedup_lo"] = data_point["pdfup_lo"] + scale_var[i][5]

			lo_sigma_nlo[i] = data_point["central_nlo"] - data_point["combinedlo_nlo"]
			up_sigma_nlo[i] = data_point["central_nlo"] + data_point["combinedup_nlo"] 
			lo_sigma_lo[i] = data_point["central_lo"] - data_point["combinedlo_lo"]
			up_sigma_lo[i] = data_point["central_lo"] + data_point["combinedup_lo"] 

	if "MSTW2008" in pdf_data:
		data_set = pdf_data["MSTW2008"]

		print "ATTENTION: Combined errors for MSTW2008"
		print "    Using mb + pdf + alphas-error added in quadrature."
		print ""
	
		for i in range(0, len(m_Hs)):
			data_point = data_set[i]

#			data_point["combinedlo_nlo"] = sqrt(data_point["alphaspdflo_nlo"]**2 + data_point["mbpdflo_nlo"]**2 - data_point["pdflo_nlo"]**2) + scale_var[i][1]
#			data_point["combinedup_nlo"] = sqrt(data_point["alphaspdfup_nlo"]**2 + data_point["mbpdfup_nlo"]**2 - data_point["pdfup_nlo"]**2) + scale_var[i][2]
			data_point["combinedlo_nlo"] = sqrt(data_point["alphaspdflo_nlo"]**2 + data_point["mbpdflo_nlo"]**2 - data_point["pdflo_nlo"]**2)
			data_point["combinedup_nlo"] = sqrt(data_point["alphaspdfup_nlo"]**2 + data_point["mbpdfup_nlo"]**2 - data_point["pdfup_nlo"]**2)
			data_point["combinedlo_lo"] = data_point["pdflo_lo"] + scale_var[i][4]
			data_point["combinedup_lo"] = data_point["pdfup_lo"] + scale_var[i][5]

			if data_point["central_nlo"] - data_point["combinedlo_nlo"] < lo_sigma_nlo[i]:
				lo_sigma_nlo[i] = data_point["central_nlo"] - data_point["combinedlo_nlo"]
			if data_point["central_nlo"] + data_point["combinedup_nlo"] > up_sigma_nlo[i]:
				up_sigma_nlo[i] = data_point["central_nlo"] + data_point["combinedup_nlo"]
			if data_point["central_lo"] - data_point["combinedlo_lo"] < lo_sigma_lo[i]:
				lo_sigma_lo[i] = data_point["central_lo"] - data_point["combinedlo_lo"]
			if data_point["central_lo"] + data_point["combinedup_lo"] > up_sigma_lo[i]:
				up_sigma_lo[i] = data_point["central_lo"] + data_point["combinedup_lo"]

	if "CT10" in pdf_data:
		data_set = pdf_data["CT10"]

		print "ATTENTION: Combined errors for CT10"
		print "    Using alphas + pdf-error as combined error for CT10, since no"
		print "    mb-error is available for CT10."
		print ""

		for i in range(0, len(m_Hs)):
			data_point = data_set[i]
	
#			data_point["combinedlo_nlo"] = data_point["alphaspdflo_nlo"] + scale_var[i][1]
#			data_point["combinedup_nlo"] = data_point["alphaspdfup_nlo"] + scale_var[i][2]
			data_point["combinedlo_nlo"] = data_point["alphaspdflo_nlo"]
			data_point["combinedup_nlo"] = data_point["alphaspdfup_nlo"]
			data_point["combinedlo_lo"] = scale_var[i][4]
			data_point["combinedup_lo"] = scale_var[i][5]

			if data_point["central_nlo"] - data_point["combinedlo_nlo"] < lo_sigma_nlo[i]:
				lo_sigma_nlo[i] = data_point["central_nlo"] - data_point["combinedlo_nlo"]
			if data_point["central_nlo"] + data_point["combinedup_nlo"] > up_sigma_nlo[i]:
				up_sigma_nlo[i] = data_point["central_nlo"] + data_point["combinedup_nlo"]
			if data_point["central_lo"] - data_point["combinedlo_lo"] < lo_sigma_lo[i]:
				lo_sigma_lo[i] = data_point["central_lo"] - data_point["combinedlo_lo"]
			if data_point["central_lo"] + data_point["combinedup_lo"] > up_sigma_lo[i]:
				up_sigma_lo[i] = data_point["central_lo"] + data_point["combinedup_lo"]

	if "combined" in pdf_data:
		data_set = pdf_data["combined"]

		for i in range(0, len(m_Hs)):
			data_point = data_set[i]

			# a_s = 0.119 instead of 0.118 for m_b-variation of NNPDF
			# reset central value
			#data_point["central_lo"] = data_point["pdf_central_lo"]
			#data_point["central_nlo"] = data_point["pdf_central_nlo"]
			data_point["central_nlo"] = (up_sigma_nlo[i] + lo_sigma_nlo[i])/2.0     #mf??
			data_point["central_lo"] = (up_sigma_lo[i] + lo_sigma_lo[i])/2.0        #mf??

#			data_point["combinedlo_nlo"] = data_point["central_nlo"] - lo_sigma_nlo[i] 
#			data_point["combinedup_nlo"] = up_sigma_nlo[i] - data_point["central_nlo"]
			data_point["combinedlo_nlo"] = data_point["central_nlo"] - lo_sigma_nlo[i] + scale_var[i][1] 
			data_point["combinedup_nlo"] = up_sigma_nlo[i] - data_point["central_nlo"] + scale_var[i][2]
			data_point["combinedlo_lo"] = data_point["central_lo"] - lo_sigma_lo[i] 
			data_point["combinedup_lo"] = up_sigma_lo[i] - data_point["central_lo"]
