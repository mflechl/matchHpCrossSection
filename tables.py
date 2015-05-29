################################################
#
# TABLE CREATION 
#
################################################

cm_energy = "8TeV"
#cm_energy = "14TeV"

import re

def search_line(stri, f):
	line = ""
	res = None
	while True:
		line = f.readline()
		res = re.match(stri, line)
		if res:
			break
		if len(line) == 0:
			print "End of file reached while searching \"%s\"" % stri
			exit()

	return line, res

def check_pdf_names(lo, nlo, pdfs):
	for pdf in pdfs:
		if pdf[0] == nlo and pdf[2] == lo:
			return pdf

	return None

import os.path as path

def create_tables(name, pdfs, m_Hs, as_name = False, mb_name = False):
	pdfsets = {}

	pdf_sets = 0
	for pdf in pdfs:
		pdf_sets += max(pdf[1], pdf[3])

	jobs = len(m_Hs)*pdf_sets

	if name == "pdf_error":
		# For central values of mstw
		jobs += len(m_Hs) 

#	print ""
	print ""
	print "Creating tables for %s from %d jobs." % (name, jobs) 
	
	for i in range(1, jobs+1):
		if not path.isfile("jobs_%s/job_%s%d" % (cm_energy, name, i)):
			print "File jobs_%s/job_%s%d missing." % (cm_energy, name, i)
			continue

#		print "Processing jobs_%s/job_%s%d" % (cm_energy, name, i)
		f = open("jobs_%s/job_%s%d" % (cm_energy, name, i), "r")

		search_line("\s*Using for lo:", f)

		line, res = search_line("\s*([^.]+)\.", f)
		pdf_name_lo = res.group(1)

		line, res = search_line("\s*set\s*(\d+)", f)
		pdf_set_lo = int(res.group(1))

		search_line("\s*and for nlo:", f)

		line, res = search_line("\s*([^.]+)\.", f)
		pdf_name_nlo = res.group(1)

		line, res = search_line("\s*set\s*(\d+)", f)
		pdf_set_nlo = int(res.group(1))
		
		# Skip central value for mstw2008nlo68cl
#		if pdf_name_nlo == "MSTW2008nlo68cl" and pdf_set_nlo == 0:
#			f.close()
#			continue

		# Correct the central value for MSTW to get it for the correct
		# alpha_s
		if pdf_name_nlo == "MSTW2008nlo_asmzrange" and pdf_set_nlo == 9:
			print "-----------> Overriding MSTWnlo68cl set 0 with MSTW2008nlo_asmzrange"
			pdf_name_nlo = "MSTW2008nlo68cl"
			pdf_set_nlo = int(41)

		pdf = check_pdf_names(pdf_name_lo, pdf_name_nlo, pdfs)

		if not pdf:
			print "Found unknown combination of pdfs in file job_pdf_error%d: %s, %s" % (i, pdf_name_lo, pdf_name_nlo)
			f.close()
			continue

		# I think that mod isn't necessary anymore.
		if pdf_set_lo >= pdf[3]:
			pdf_set_lo = -1
			print "-----------> Used mod1."

		if pdf_set_nlo >= pdf[1] and pdf_name_nlo != "MSTW2008nlo68cl":
			pdf_set_nlo = -1
		
		pdf_name = pdf[4]

		if not pdf_name in pdfsets.viewkeys():
			pdfsets[pdf_name] = {}

		pdf_data = pdfsets[pdf_name]

		line, res = search_line(".*M_b\s*=\s*([0-9.]+)", f)
		M_b = float(res.group(1))

		line, res = search_line("\s*M_H\s*=\s*([0-9.]+)", f)
		M_H = float(res.group(1))

		line, res = search_line("\s*inverse\s+factor\s+for\s+scale:\s*([0-9.]+)", f)
		inv_scafac = float(res.group(1))

		line, res = search_line("\s*a_s\(M_Z\)\s*=\s*([0-9.]+)\s*at LO", f)
		als_lo = float(res.group(1))

		line, res = search_line("\s*a_s\(M_Z\)\s*=\s*([0-9.]+)\s*at NLO", f)
		als_nlo = float(res.group(1))

		# Need more tables for NNPDF
		if as_name and pdf_name == "NNPDF23":
			if not M_H in pdf_data.viewkeys():
				pdf_data[M_H] = {}
			data = pdf_data[M_H]
			if not als_nlo in data.viewkeys():
				data[als_nlo] = []
			data = data[als_nlo]
		elif mb_name and pdf_name == "NNPDF21": ##???
			if not M_H in pdf_data.viewkeys():
				pdf_data[M_H] = {}
			data = pdf_data[M_H]
			if not M_b in data.viewkeys():
				data[M_b] = []
			data = data[M_b]
		else:
			if not M_H in pdf_data.viewkeys():
				pdf_data[M_H] = []

			data = pdf_data[M_H]

		search_line("\s*RESULTS:", f)

		line = f.readline()

                if pdf_set_nlo == 41 and pdf_name == "MSTW2008" and M_H < 502:
			print "pdf set %d" %pdf_set_nlo
			print "line: %s" %line
			print "file: jobs_%s/job_%s%d" % (cm_energy, name, i)

		line = line.split()

		# format: 0:set_lo, 1:set_nlo, 2:cs lo, 3:integ err lo, 4:cs nlo, 5:integ err nlo, 6:k factor, 7:nlo susy, 8:alphas lo, 9:alphas nlo, 10:m_b, 11:inverse factorisation scale factor.
		date =	(pdf_set_lo, pdf_set_nlo, float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]), float(line[14]), als_lo, als_nlo, M_b, inv_scafac)

		data.append(date)

                if pdf_set_nlo == 41 and pdf_name == "MSTW2008" and M_H < 502:
			print "pdf set %d" %pdf_set_nlo
			print "NLO xsec: %f" %date[4]

		f.close()
		
	def write_data(mass, filename):
		mass = sorted(mass, key = lambda x: x[1])

		f = open("tables_%s/%s" % (cm_energy, filename), "w")
		
		f.write("# set lo     set nlo    LO            relative_err  NLO           relative_err  K-Factor      NLO(SUSY)     a_s(MZ) LO    a_s(MZ) NLO   m_b           inverse factorisation scale factor\n")

		for d in mass:
			f.write("%10d  %10d  %10e  %10e  %10e  %10e  %10e  %10e  %10e  %10e  %10e  %10e\n" % d)

		f.close()

	for pdf_name in pdfsets:
		pdf_data = pdfsets[pdf_name]
		for mass_name in pdf_data:

			if as_name and pdf_name == "NNPDF23":
				for als in pdf_data[mass_name]:
					mass = pdf_data[mass_name][als]
					alphas_name = "0%d" % round(als*1000)
					filename = "%s_as%s_%dGeV" % (pdf_name, alphas_name, mass_name)
					write_data(mass, filename)
			elif mb_name and pdf_name == "NNPDF21":
				for m_b in pdf_data[mass_name]:
					mass = pdf_data[mass_name][m_b]
					massb_name = "%d" % (m_b*100)
					filename = "%s_mb%s_%dGeV" % (pdf_name, massb_name, mass_name)
					write_data(mass, filename)
			else:
				mass = pdf_data[mass_name]
				filename = "%s_%dGeV" % (pdf_name, mass_name)

				write_data(mass, filename)

################################################
#
#  Reading of tables
#
################################################

def read_table(name):
	f = open("tables_%s/%s" % (cm_energy, name), "r")

	# drop first line
	for line in f:
		break

	data = []

	for line in f:
		l = line.split()
		data.append((int(l[0]), int(l[1]), float(l[2]), float(l[3]), float(l[4]), float(l[5]), float(l[6]), float(l[7]), float(l[8]), float(l[9]), float(l[10])))

	return data


