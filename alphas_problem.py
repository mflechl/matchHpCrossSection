from pdf_error import read_table
from pdf_error import pdf_error1
from alphas_pdf_error import alphas_pdf_error1
from math import sqrt, exp

from math import floor
from math import ceil 
from math import pi

def histogram(values, r, bin_num, fun = lambda x: 1):
	bins = bin_num * [0.0]
	width = (r[1] - r[0]) / bin_num
	edges = [ i * width + r[0] for i in range(0, bin_num + 1) ]
	for v in values:
		if v < r[0] or v > r[1]:
			continue
		index = int(floor((v-r[0])/width))
		bins[index] += fun(v) 

	return bins, edges

def plot_histogram(plot, bins, edges):
	points_x = [] 
	points_y = []
	for i in range(0,len(bins)):
		points_x.append(edges[i])
		points_y.append(bins[i])
		points_x.append(edges[i+1])
		points_y.append(bins[i])

	plot.plot(points_x, points_y, "g-", marker=None)



import matplotlib.pyplot as plt

alphas = [0.115, 0.116, 0.117, 0.118, 0.119, 0.120, 0.121]

M_H = 400

bin_num = 20

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

#	print "Mean:  %e" % pdf_err[3]
#	print "Sigma:  %e" % pdf_err[4]

#	plt.errorbar([a_s+0.0001], [mean], yerr=[sigma])
#	plt.errorbar([a_s+0.0001], [pdf_err[3]], yerr=[pdf_err[4]], marker="o")

#	plt.plot([a_s-0.0001]*100, nlo , ".")

	plt.subplot("42%d" % count)
	plt.title("a_s = %f" % a_s)

	#bins, edges = histogram(nlo, (0.17,0.24), bin_num) 
	bins, edges = histogram(nlo, (0.022,0.040), bin_num) 
        
	max_bins = max(bins)

        plot_histogram(plt, [b/max_bins for b in bins], edges)

	plt.errorbar([pdf_err[3]], [0.5], xerr=[pdf_err[4]], marker="o")
	plt.axvline([pdf_err[3]])
	plt.axvline([pdf_err[3]-pdf_err[4]], linestyle="--")
	plt.axvline([pdf_err[3]+pdf_err[4]], linestyle="--")

	def gaussian(mu, sigma, x, scale):
		return exp( ( -0.5*(mu - x)**2/(sigma**2) ) ) * scale

	#xs = [0.17 + 0.001*i for i in range(0, 70)]
	xs = [0.022 + 0.0001*i for i in range(0, 180)]

	plt.plot(xs, [gaussian(pdf_err[3], pdf_err[4], x, 1.0) for x in xs], "b-")

#	print "Span: %f" % (max(nlo)-min(nlo))
#	print ""

als_err = alphas_pdf_error1(M_H)

plt.subplot("428")
plt.title("combined")

#bins, edges = histogram(als_data, (0.17,0.24), bin_num) 
bins, edges = histogram(als_data, (0.022,0.040), bin_num) 

max_bins = max(bins)

plot_histogram(plt, [b/max_bins for b in bins], edges)

plt.errorbar([als_err[3]], [0.5], xerr=[als_err[4]], marker="o")
plt.axvline([als_err[3]])
plt.axvline([als_err[3]-als_err[4]], linestyle="--")
plt.axvline([als_err[3]+als_err[4]], linestyle="--")

def gaussian(mu, sigma, x, scale):
	return exp( ( -0.5*(mu - x)**2/(sigma**2) ) ) * scale

#xs = [0.17 + 0.001*i for i in range(0, 70)]
xs = [0.022 + 0.0001*i for i in range(0, 180)]
max_bins = max(bins)

plt.plot(xs, [gaussian(pdf_err[3], pdf_err[4], x, 1.0) for x in xs], "b-")


#plt.xticks(alphas + [0.122], alphas + ["combined"])
#plt.xlim(0.1145, 0.1225)
plt.show()
