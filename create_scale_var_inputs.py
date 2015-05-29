job_count = 0

#pdfsets = [("CT10.LHgrid", 53),
#           ("cteq6ll.LHpdf", 44),
#           ("MSTW2008nlo68cl.LHgrid", 41),
#           ("MSTW2008lo68cl.LHgrid", 41),
#           ("NNPDF21_as_0118_100.LHgrid", 100),
#           ("NNPDF21_lo_as_0130_100.LHgrid", 100)]


from mh_detail import *
from prospino_inp import *
from bsub_inp import *

for m_H in m_Hs:

#	span = 2.0/m_H[1] - 1.0/(m_H[1]*2.0)
#	step = span/100.0
#	scale = 1.0/(m_H[1]*2.0)	

	for i in range(10, 91):
		job_count += 1

		scale = (1.0/m_H[1])*i/30.0

		f = file("inputs_scale_var/input%d" % job_count, "w")

		desc = {
			"collider" : 1,
			"final_state" : "ht",
			"particle1" : 1,
			"particle2" : 1,
			"pdf_lo" : "MSTW2008lo68cl.LHgrid",
			"member_lo" : 0,
			"use_pdfals_lo" : ".false.",
			"pdf_nlo" : "MSTW2008nlo_asmzrange.LHgrid\n",
			"member_nlo" : 9,
			"use_pdfals_nlo" : ".true.",
			"inverse_scafac" : 1.0/scale,
			"cH_mass" : m_H[0],
			"b_mass" : 4.75 
		}

		f.write(prospino_input % desc)
		f.close()

make_bsub_files("scale_var", "0:20", "2048", job_count)

print "Created %d input-files." % job_count
