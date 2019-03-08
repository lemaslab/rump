#!/usr/bin/env nextflow
 
input_dir = Channel.fromPath('/Users/xinsongdu/Library/R/3.5/library/faahKO/cdf', type: 'dir')
R_file = Channel.fromPath('./xcms_R/xcms-faahKO.R')
// plot_1 = file('chromatograms_1.pdf')
// plot_2 = file('ion_current.pdf')
// plot_3 = file('chromatograms_2.pdf')

process run_sample {

    publishDir './results/', mode: 'move'

    input:
    file f from input_dir
    file r from R_file

    output:
    file "plot_1.pdf" into plt1
    file "plot_2.pdf" into plt2
    file "plot_3.pdf" into plt3
 
    shell:
    """   
    Rscript ${r} -i ${f} -p "plot_1.pdf" -q "plot_2.pdf" -r "plot_3.pdf"

    """
}