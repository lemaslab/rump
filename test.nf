#!/usr/bin/env nextflow

/**
    Metabolomics Pipeline for Suptercomputers (MPS)
    Copyright (C) lemas-research-group          
          
    This script is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This script is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this script.  If not, see <http://www.gnu.org/licenses/>.
    
    For any bugs or problems found, please contact us at
    - [email placeholder]; 
    - [github placeholder]
*/

version='0.0.0'
timestamp='20190416'

// input_dir = Channel.fromPath(params.input_folder, type: 'dir')
input_file_xcms = Channel.fromPath(params.input_file)
input_file_mzmine = Channel.fromPath(params.input_file)
mzmine = Channel.fromPath(params.mzmine_dir, type: 'dir')
mzmine_peak_file = Channel.from("MZmine-2.38/$params.mzmine_peak_output")
python_file = Channel.fromPath('./src/batchfile_generator.py')
R_file = Channel.fromPath('./xcms_R/peak_detection_xcms.R')
output_dir = Channel.fromPath(params.output_dir, type: 'dir')

/**
    Prints version when asked for
*/

if (params.version) {
    System.out.println("")
    System.out.println("METAGENOMIC PIPELINE FOR SUPERCOMPUTERS (MPS) - Version: $version ($timestamp)")
//    exit 1
}

/**
    Prints help when asked for
*/

if (params.help) {
    System.out.println("")
    System.out.println("Metabolomics Pipeline for Suptercomputers (MPS) - Version: $version ($timestamp)")
    System.out.println("This pipeline is distributed in the hope that it will be useful")
    System.out.println("but WITHOUT ANY WARRANTY. See the GNU GPL v3.0 for more details.")
    System.out.println("")
    System.out.println("Please report comments and bugs to alessia.visconti@kcl.ac.uk")
    System.out.println("or at https://github.com/GalaxyDream/metabolomics_data_processing/issues.")
    System.out.println("Check https://github.com/GalaxyDream/metabolomics_data_processing for updates, and refer to")
    System.out.println("[wiki placeholder]")
    System.out.println("")
    System.out.println("Usage: ")
    System.out.println("   nextflow run YAMP.nf --reads1 R1 --reads2 R2 --prefix mysample --outdir path --mode MODE  ")
    System.out.println("                [options] [-with-docker|-with-singularity]")
    System.out.println("")
    System.out.println("Mandatory arguments:")
    System.out.println("    --plot_1   p1      Name of the first plot, please ends with '_mqc.jepg'")
    System.out.println("    --plot_2   p2      Name of the second plot, please ends with '_mqc.jepg'")
    System.out.println("    --plot_3   p3      Name of the third plot, please ends with '_mqc.jepg'")
    System.out.println("    --plot_4   p4      Name of the first plot, please ends with '_mqc.jepg'")
    System.out.println("Please refer to nextflow.config for more options.")
    System.out.println("")
    System.out.println("Container:")
    System.out.println("    Docker image to use with -with-docker|-with-singularity options is")
    System.out.println("    'docker://galaxydream/bioconductor_metabolomics'")
    System.out.println("")
    System.out.println("MPS supports mzData files.")
    System.out.println("")
//    exit 1
}

process peakDetection_mzmine {

    echo true

    script:
    """   
    echo $(pwd)/MZmine-2.38/mzmine_dcsm_peaks.csv

    """
}