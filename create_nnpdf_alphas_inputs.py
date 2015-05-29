job_count = 0

pdfsets = [
	("NNPDF21_as_0114_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_as_0115_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_as_0116_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_as_0117_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_as_0118_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_as_0120_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_as_0121_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_as_0122_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_as_0123_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True),
	("NNPDF21_as_0124_100.LHgrid", 101, True, "NNPDF21_lo_as_0130_100.LHgrid", 101, True)
	]


from mh_detail import *
from prospino_inp import *
from bsub_inp import *

for m_H in m_Hs:
	for pdf in pdfsets:
		for i in range(0, max(pdf[1], pdf[4])):
			job_count += 1

			f = file("inputs_nnpdf_alphas/input%d" % job_count, "w")

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

make_bsub_files("nnpdf_alphas", "0:20", "2048", job_count)

print "Created %d input-files." % job_count
