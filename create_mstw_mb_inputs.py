job_count = 0

pdfsets = [
	("MSTW2008nlo_mbrange.LHgrid", 7, True, "MSTW2008nlo_mbrange.LHgrid", 7, True),
	]


from mh_detail import *
from prospino_inp import *
from bsub_inp import *

for m_H in m_Hs:
	for pdf in pdfsets:
		for i in range(0, max(pdf[1], pdf[4])):
			job_count += 1

			f = file("inputs_mstw_mb/input%d" % job_count, "w")

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
				"b_mass" : ([4.75, 4.0, 4.25, 4.5, 5.0,5.25,5.50])[i]
			}

			f.write(prospino_input % desc)
			f.close()

make_bsub_files("mstw_mb", "0:20", "2048", job_count)

print "Created %d input-files." % job_count
