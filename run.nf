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
timestamp='20190421'

// input_dir = Channel.fromPath(params.input_folder, type: 'dir')
input_file_xcms = Channel.fromPath(params.input_file)
input_file_mzmine = Channel.fromPath(params.input_file)
mzmine = Channel.fromPath(params.mzmine_dir, type: 'dir')
// mzmine_peak_file = Channel.fromPath("MZmine-2.38/$params.mzmine_peak_output")
python_file = Channel.fromPath('./src/batchfile_generator.py')
R_file = Channel.fromPath('./xcms_R/peak_detection_xcms.R')
output_dir = Channel.fromPath(params.output_dir, type: 'dir')

/**
    Prints version when asked for
*/

if (params.version) {
    System.out.println("")
    System.out.println("METAGENOMIC PIPELINE FOR SUPERCOMPUTERS (MPS) - Version: $version ($timestamp)")
    exit 1
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
    System.out.println("   nextflow run.nf [options] -with-docker galaxydream/bioconductor_metabolomics")
    System.out.println("")
    System.out.println("Arguments:")
    System.out.println("----------------------------- common parameters ----------------------------------")
    System.out.println("    --version                   whether to show version information or not, default is null")
    System.out.println("    --help                      whether to show help information or not, default is null")
    System.out.println("    --input_file                location of your input metabolomics data file")
    System.out.println("    --noise                     noise value used by both mzmine and xcms, default is 100")
    System.out.println("    --ppm                       relative m/z tolerance used by both mzmine and xcms, default is 25")
    System.out.println("------------------------------- xcms parameters ----------------------------------")
    System.out.println("    --peakwidth_low             lower bound of peak width, default is 0.6")
    System.out.println("    --peakwidth_high            higher bound of peak width, default is 30")
    System.out.println("    --prefilter_low             lower bound of prefilter, default is 1")
    System.out.println("    --prefilter_high            higher bound of prefilter, default is 1000")
    System.out.println("    --integrate                 value of integrate in xcms, default is 2")
    System.out.println("    --xcms_peak_output          csv file name of the peak table output by xcms; note: this is not path, just a file name")
    System.out.println("------------------------------ mzmine parameters ---------------------------------")
    System.out.println("    --mzmine_dir                path of the mzmine directory on your machine")
    System.out.println("    --ms_level                  MS level for mass detection in mzmine, default is 1")
    System.out.println("    --detector_scalelevel       scale level for mass detector in mzmine, default is 20")
    System.out.println("    --detector_windowsize       window size for mass detector in mzmine, default is 0.3")
    System.out.println("    --buider_mintimespan        minimum time span for chromatogram builder in mzmine, default is 0.04")
    System.out.println("    --buider_minheight          minimum height for chromatogram builder in mzmine, default is 5000")
    System.out.println("    --decov_snthreshold         S/N threshold for chromatogram builder in mzmine, default is 10")
    System.out.println("    --decov_wavscamin           minimum wavelet scales for chromatogram deconvolution in mzmine, default is 0.02")
    System.out.println("    --decov_wavscamax           maximum wavelet scales for chromatogram deconvolution in mzmine, default is 0.8")
    System.out.println("    --decov_peadurmin           minimum peak duration for chromatogram deconvolution in mzmine, default is 0.02")
    System.out.println("    --decov_peadurma            maximum peak duration for chromatogram deconvolution in mzmine, default is 0.6")
    System.out.println("    --mzmine_peak_output        output file name of peak detection result using mzmine, default is ./mzmine_dcsm_peaks.csv; note: the value must start with ./, followed by the file name")
    System.out.println("Please refer to nextflow.config for more options.")
    System.out.println("")
    System.out.println("Container:")
    System.out.println("    Docker image to use with -with-docker|-with-singularity options is")
    System.out.println("    'docker://galaxydream/bioconductor_metabolomics'")
    System.out.println("")
    System.out.println("MPS supports mzData files.")
    System.out.println("")
    exit 1
}

process peakDetection_xcms {

//    echo true

    publishDir './results/', mode: 'move'

    input:
    file f from input_file_xcms
    file r from R_file

    output:
    file params.xcms_peak_output into xcms_peak_output

    shell:
    """   
    Rscript ${r} -i ${f} -a $params.mzTolerance -b $params.peakwidth_low -c $params.peakwidth_high -d $params.noise -e $params.prefilter_low -f $params.prefilter_high -g $params.integrate -j $params.xcms_peak_output -k $params.ppm -o $params.output_dir

    """
}

process batchfile_generation_mzmine {

//    echo true

    input:
    file p from python_file
//    file g from input_file_mzmine

    output:
    file params.x_output into batchfile

    shell:
    """   
    python ${p} -x ${params.x_output} -i $params.input_file -ml $params.ms_level -dn $params.noise -ds $params.detector_scalelevel -dw $params.detector_windowsize -bt $params.buider_mintimespan -bh $params.builder_minheight -ba $params.mzTolerance -bp $params.ppm -dt $params.decov_snthreshold -dwi $params.decov_wavscamin -dwa $params.decov_wavscamax -dpi $params.decov_peadurmin -dpa $params.decov_peadurmax -o $params.mzmine_peak_output

    """
}
// batchfile.subscribe{File file = new File("${it}")
//                     println "The file ${file.absolutePath} has ${file.length()} bytes"}

process peakDetection_mzmine {

    publishDir './results/', mode: 'move'

    echo true

    input:
    file b from batchfile
    file m from mzmine

    output:
    file "MZmine-2.38/${params.mzmine_peak_output}" into mzmine_peaks
    stdout result

// Change "startMZmine_Linux.sh" to "startMZmine_MacOSX.command" in the following code if running locally with Mac

    shell:
    """   
    mv ${b} ${m} && ${m}/startMZmine_Linux.sh ${b}

    """
}

// result.subscribe{println it}


