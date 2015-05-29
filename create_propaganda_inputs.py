job_count = 0

#pdfsets = [("CT10.LHgrid", 53),
#           ("cteq6ll.LHpdf", 44),
#           ("MSTW2008nlo68cl.LHgrid", 41),
#           ("MSTW2008lo68cl.LHgrid", 41),
#           ("NNPDF21_as_0118_100.LHgrid", 100),
#           ("NNPDF21_lo_as_0130_100.LHgrid", 100)]

for i in range(0, 76):

	m_g = 500.0 + i * (4500.0/75)

	for mem in range(0,41): 
		job_count += 1

		f = file("inputs_propaganda/input%d" % job_count, "w")

		f.write("cteq6.LHpdf\n")
		f.write("%d\n" % mem)
	        f.write(".false.\n")
		f.write("cteq6.LHpdf\n")
		f.write("%d\n" % mem)
        	f.write(".false.\n")
		f.write("1.0\n")
        	f.write("4.75\n")
	        f.write("172.5\n")
		f.write("%d\n" % 400)
		f.write("%d\n" % m_g) 

		f.close()

	for mem in range(0,35): 
		job_count += 1

		f = file("inputs_propaganda/input%d" % job_count, "w")

		f.write("LHECNLO_EIG.LHgrid\n")
		f.write("%d\n" % mem)
	        f.write(".false.\n")
		f.write("LHECNLO_EIG.LHgrid\n")
		f.write("%d\n" % mem)
        	f.write(".false.\n")
		f.write("1.0\n")
        	f.write("4.75\n")
	        f.write("172.5\n")
		f.write("%d\n" % 400)
		f.write("%d\n" % m_g) 

		f.close()

print "Created inputs for %d jobs." % job_count	
