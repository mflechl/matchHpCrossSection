job_count = 0

pdfsets = [
	("CT10as.LHgrid", 11, True, "CT10as.LHgrid", 11, True),
	]

from mh_detail import *
from prospino_inp import *
from bsub_inp import *

#m_Hs = [(200, 5.42), (300, 5.77), (400, 6.10), (500, 6.41)]
#
for m_H in m_Hs:
	for pdf in pdfsets:
		for i in range(0, max(pdf[1], pdf[4])):
			job_count += 1

			f = file("inputs_ct10_alphas/input%d" % job_count, "w")

			desc = {
				"collider" : 1,
				"final_state" : "ht",
				"particle1" : 1,
				"particle2" : 1,
				"pdf_lo" : pdf[3],
				"member_lo" : i,
				"use_pdfals_lo" : ".true." if pdf[5] else ".false.",
				"pdf_nlo" : pdf[0],
				"member_nlo" : i,
				"use_pdfals_nlo" : ".true." if pdf[2] else ".false.",
				"inverse_scafac" : m_H[1],
				"cH_mass" : m_H[0],
				"b_mass" : 4.75
			}

			f.write(prospino_input % desc)
			f.close()

make_bsub_files("ct10_alphas", "0:20", "2048", job_count)

print "Created %d input-files." % job_count
