

prospino_input = 
"""
%(collider)d
%(final_state)s
%(particle1)d
%(particle2)d
%(pdf_lo)s
%(member_lo)d
%(use_pdfals_lo)s
%(pdf_nlo)s
%(member_nlo)d
%(use_pdfals_nlo)s
"""

modelline = "line.10.4_%d.out"

pdf = ("cteq6ll.LHpdf", "cteq66.LHgrid", 45)

bsub_input = 
"""
#!/usr/bin/env zsh

#BSUB -J "myArray[%(start)d-%(end)d]" ARRAYJOB

module switch intel gcc/4.6
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/rk066459/LHAPDF/lib
cp %(modelline)s prospino.in.les_houches
./prospino_2.run < inputs_prospino/input$LSB_JOBINDEX
""" 

states = [("nn", 2, 5), ("ng", 2, 1), ("ll", 3, 1)]

job_count = 0
job_count2 = 0

start = 0

for i in range(1,11):
	modline = modelline % i

	start = job_count + 1
	job_count2 += 1

	for s in state:
		for j in range(0, pdf[2]):
			job_count += 1

			f = file("inputs_prospino/input%d" % job_count, "w")

			desc = {
				"collider" : 3,
				"final_state" : s[0],
				"particle1" : s[1],
				"particle2" : s[2],
				"pdf_lo" : pdf[0],
				"member_lo" : 0,
				"use_pdfals_lo" : ".true.",
				"pdf_nlo" : pdf[1],
				"member_nlo" : j,
				"use_pdfals_nlo" : ".false."
			}

			f.write(prospino_input % desc)
			f.close()

	f = file("prospino_job%d.sh" % job_count2, "w")

	desc = {
		"start" : start,
		"end" : job_count,
		"modelline" : modline
	}

	f.write(bsub_input % desc) 

	f.close()

print "Total number of created inputs: %d" % job_count
