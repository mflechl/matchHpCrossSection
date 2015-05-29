job_count = 0

pdfsets = [("CT10.LHgrid", 53, True),
	   ("LHECNLO_EIG.LHgrid", 35, True),
           ("MSTW2008nlo68cl.LHgrid", 41, True),
           ("NNPDF21_100.LHgrid", 101, True),
           ("HERAPDF10_EIG.LHgrid", 21, True),
           ("abkm09_5_nlo.LHgrid", 26, True)]

for pdf in pdfsets:
	for i in range(0, 46):

		m_g = 500.0 + i * (4500.0/45)

		for mem in range(0, pdf[1]): 
			job_count += 1

			f = file("inputs_propaganda2/input%d" % job_count, "w")

			f.write("%s\n" % pdf[0])
			f.write("%d\n" % mem)
	        	f.write(".true.\n")
			f.write("%s\n" % pdf[0])
			f.write("%d\n" % mem)
        		f.write(".true.\n")
			f.write("1.0\n")
        		f.write("4.75\n")
	        	f.write("172.5\n")
			f.write("%d\n" % 300)
			f.write("%d\n" % m_g) 

			f.close()

print "Created inputs for %d jobs." % job_count	
