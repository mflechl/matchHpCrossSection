from os import path
import re

from tables import search_line, cm_energy

from mh_detail import *

def create_tanbeta_tables(m_Hs):

	jobs = len(m_Hs)*28*3  #3 pdf sets, 28 tb values

#	print ""
	print ""
	print "Creating tables for grid from %d jobs." % (jobs) 

        pdfnames=("NNPDF23_nlo_as_0118","MSTW2008nlo_asmzrange","CT10")
        pdfnames_brief=("NNPDF23","MSTW2008","CT10")

	for ipdf in range(0, 3):
		m_Hdata = {}

		for i in range(1, jobs+1):
			if not path.isfile("jobs_%s/job_tanbeta%d" % (cm_energy, i)):
				print "File job_%s/job_tanbeta%d missing." % (cm_energy, i)
				continue

		#		print "Processing job_%s/job_tanbeta%d" % (cm_energy, i)
			f = open("jobs_%s/job_tanbeta%d" % (cm_energy, i), "r")

			search_line("\s*and for nlo:", f)
			line, res = search_line("\s*([^.]+)\.", f)
			pdf_name_nlo = res.group(1)

                        if pdf_name_nlo!=pdfnames[ipdf]: continue
#			if  pdf_name_nlo=="NNPDF23_nlo_as_0118": pdfname="NNPDF23"
#			if  pdf_name_nlo=="MSTW2008nlo_asmzrange": pdfname="MSTW08"
#			if  pdf_name_nlo=="CT10": pdfname="CT10"

			M_H = 0.0
			M_t = 0.0

			line, res = search_line(".*M_t\s*=\s*([0-9.]+)", f)
			M_t = float(res.group(1))
			line, res = search_line("\s*M_H\s*=\s*([0-9.]+)", f)
			M_H = float(res.group(1))

			if not M_H in m_Hdata.viewkeys():
				m_Hdata[M_H] = []

			data = m_Hdata[M_H]

		       	f.close()
		       	f = open("jobs_%s/job_tanbeta%d" % (cm_energy, i), "r")

		       	tanbeta = 0.0
		       	#		line, res = search_line(".*tan_b\s*=\s*([0-9.]+)", f)
		       	#		line, res = search_line("\s*M_H\s*=\s*([0-9.]+)", f)
		       	line, res = search_line("\s*tan_b\s*=\s*([0-9.]+)", f)
		       	tanbeta = float(res.group(1))


		       	search_line("\s*RESULTS:", f)

			line = f.readline()
		       	line = line.split()

		       	# format: 0: tan beta, 1: cs lo, 2: integ err lo, 3: cs nlo, 4: integ err nlo, 5:k factor, 6:nlo susy
#		       	data.append((tanbeta, float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]), float(line[14])))

		       	data.append((M_H, tanbeta, float(line[11])))

		       	f.close()

		       	#                if M_H == 200 and i==71: 
		       	#			break



		for mass_name in m_Hdata:
			mass = m_Hdata[mass_name]
			mass = sorted(mass, key = lambda x: x[0])

			f = open("tables_%s/tanbeta_%s_%dGeV" % (cm_energy, pdfnames_brief[ipdf], mass_name), "w")
		
#			f.write("# tan_beta   LO            relative_err  NLO           relative_err  K-Factor      NLO(SUSY)\n")
			f.write("# mhp       tanbeta      NLO_xsec\n")

			for d in mass:
#				f.write(" %10e  %10e  %10e  %10e  %10e  %10e  %10e\n" % d)
				f.write(" %.3e  %.3e  %.3e\n" % d)

			f.close()

def read_tanbeta_table(name):
	f = open("tables_%s/%s" % (cm_energy, name), "r")

	# drop first line
	for line in f:
		break

	data = []

	for line in f:
		l = line.split()
		data.append((float(l[0]), float(l[1]), float(l[2]), float(l[3]), float(l[4]), float(l[5]), float(l[6])))

	return data

#import matplotlib.pyplot as plt
from plotting import *

m_t = 172.5

def get_sigma_bounds(data):
	upper_lo = max(data, key = lambda x: x[1])[1]
	lower_lo = min(data, key = lambda x: x[1])[1]
	upper_nlo = max(data, key = lambda x: x[3])[3]
	lower_nlo = min(data, key = lambda x: x[3])[3]

	return ((upper_lo, lower_lo), (upper_nlo, lower_nlo))

from math import floor

def get_tanbeta(m_H):
	data = read_tanbeta_table("tanbeta_%dGeV" % m_H)

import sys

if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.argv[1] == "tables":
			create_tanbeta_tables(m_Hs)
			exit()
		else:
			print "Unknown param: %s" % sys.argv[1]
			exit()

#	tanbeta_analysis()
		
