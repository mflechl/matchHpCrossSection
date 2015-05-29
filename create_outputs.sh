#!/bin/bash

#python2.7 analysis.py tables
#python2.7 analysis.py scale_var -l 5F_scale_var_results_$1.tex | tee 5F_scale_var_results_$1.txt
#python2.7 analysis.py CT10 -l 5F_ct10_results_$1.tex | tee 5F_ct10_results_$1.txt
#python2.7 analysis.py MSTW -l 5F_mstw_results_$1.tex | tee 5F_mstw_results_$1.txt
#python2.7 analysis.py NNPDF -l 5F_nnpdf_results_$1.tex | tee 5F_nnpdf_results_$1.txt
#python2.7 analysis.py pdf_error -l 5F_pdf_results_$1.tex | tee 5F_pdf_results_$1.txt
#python2.7 analysis.py alphas_pdf_error -l 5F_pdfas_results_$1.tex | tee 5F_pdfas_results_$1.txt
#python2.7 analysis.py mb_pdf_error -l 5F_pdfmb_results_$1.tex | tee 5F_pdfmb_results_$1.txt
python2.7 analysis.py combined -l 5F_combined_results_$1.tex | tee 5F_combined_results_$1.txt
#mf python analysis.py combined2 
#mf python analysis.py santander 
