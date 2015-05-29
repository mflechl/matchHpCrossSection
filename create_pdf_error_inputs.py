job_count = 0

pdfset = [("CT10.LHgrid", 53, "cteq6ll.LHpdf", 1, True),
         ("MSTW2008nlo68cl.LHgrid", 41, "MSTW2008lo68cl.LHgrid", 41, False),
           ("NNPDF21_as_0118_100.LHgrid", 101,"NNPDF21_lo_as_0130_100.LHgrid", 101, True)]


from mh_detail import *
from prospino_inp import *
from bsub_inp import *

for m_H in m_Hs:
	for pdf in pdfsets:
		for i in range(0, max(pdf[1], pdf[3])):
			job_count += 1

			f = file("inputs_pdf_error/input%d" % job_count, "w")

			desc = {
				"collider" : 1,
				"final_state" : "ht",
				"particle1" : 1,
				"particle2" : 1,
				"pdf_lo" : pdf[2],
				"member_lo" : (i if i < pdf[3] else 0),
				"use_pdfals_lo" : ".true." if pdf[4] else ".false.",
				"pdf_nlo" : pdf[0],
				"member_nlo" : (i if i < pdf[1] else 0),
				"use_pdfals_nlo" : ".true." if pdf[4] else ".false.",
				"inverse_scafac" : m_H[1],
				"cH_mass" : m_H[0],
				"b_mass" : 4.75 
			}

			f.write(prospino_input % desc)
			f.close()

make_bsub_files("pdf_error", "0:20", "2048", job_count)

print "Created %d input-files." % job_count
