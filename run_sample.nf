#!/usr/bin/env nextflow
 
input_dir = Channel.fromPath(params.input_folder, type: 'dir')
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
    file params.plot_1 into plt1
    file params.plot_2 into plt2
    file params.plot_3 into plt3
 
    shell:
    """   
    Rscript ${r} -i ${f} -p $params.plot_1 -q $params.plot_2 -r $params.plot_3

    """
}