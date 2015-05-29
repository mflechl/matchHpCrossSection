from pdf_error import read_table
from pdf_error import pdf_error1
from alphas_pdf_error import alphas_pdf_error1
from math import sqrt, exp

import matplotlib.pyplot as plt

alphas = [0.115, 0.116, 0.117, 0.118, 0.119, 0.120, 0.121]

M_H = 400

N_repl = {}

for i in alphas:
	N_repl[i] = int(round(exp( (-( i - 0.118)**2) / (2.0*((0.0012)**2)) ) * 100))

als_data = []

count = 0

for a_s in alphas:
	count += 1
	print "==> a_s = %f" % a_s
	data = read_table("NNPDF21_as0%d_%dGeV" % (a_s*1000, M_H))

	nlo = [d[4] for d in data[1:]]

	als_data += nlo[:(N_repl[a_s])]

#	mean = 0.0
#
#	for n in nlo:
#		mean += n
#
#	mean = mean/len(nlo)
#
#	sigma = 0.0
#	
#	for n in nlo:
#		sigma += (mean - n)**2.0
#
#	sigma = sqrt(sigma/(len(nlo)-1))
#
#	print "Mean1:  %e" % mean
#	print "Sigma1: %e" % sigma
#
	pdf_err = pdf_error1(data)

	print "Mean:  %e" % pdf_err[3]
	print "Sigma:  %e" % pdf_err[4]

#	plt.errorbar([a_s+0.0001], [mean], yerr=[sigma])
	plt.errorbar([a_s+0.0001], [pdf_err[3]], yerr=[pdf_err[4]], marker="o")

	plt.plot([a_s-0.0001]*100, nlo , ".")

	print "Span: %f" % (max(nlo)-min(nlo))
	print ""

als_err = alphas_pdf_error1(M_H)

print "==> Calculating a_s+pdf-error"


plt.plot([0.122-0.0001]*len(als_data), als_data , ".")
plt.errorbar([0.122+0.0001], [als_err[3]], yerr=[als_err[4]], marker = "o")

mean = 0.0

for d in als_data:
	mean += d

mean = mean/len(als_data)

sigma = 0.0

for d in als_data:
	sigma += (mean - d)**2.0

sigma = sqrt(sigma/(len(als_data)-1.0))

print ""
print "With 'new' algorithm: "
print "The bins for gaussian: %s" % N_repl
print "Mean_as:  %e" % mean
print "Sigma_as: %e" % sigma

print ""
print "With original algorithm: "
print "Mean_as: %e" % als_err[3]
print "Sigma_as: %e" % als_err[4]
print ""

plt.xticks(alphas + [0.122], alphas + ["combined"])
plt.xlim(0.1145, 0.1225)
plt.show()
