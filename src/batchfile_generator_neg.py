#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

def batchfile_generator(xml_file, input_dir, library, output_csv):

#    output = os.path.abspath(output_csv)

    input_files = [os.path.abspath(os.path.join(input_dir, f)) for f in os.listdir(input_dir)]
    input_str = ""
    for i in input_files:
        input_str += "            <file>" + i + "</file>\n"

    with open(xml_file, "w+") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
<batch>\n\
    <batchstep method=\"net.sf.mzmine.modules.rawdatamethods.rawdataimport.RawDataImportModule\">\n\
        <parameter name=\"Raw data file names\">\n" + input_str + 
"        </parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.rawdatamethods.peakpicking.massdetection.MassDetectionModule\">\n\
        <parameter name=\"Raw data files\" type=\"BATCH_LAST_FILES\"/>\n\
        <parameter name=\"Scans\">\n\
            <ms_level>1</ms_level>\n\
        </parameter>\n\
        <parameter name=\"Mass detector\" selected=\"Centroid\">\n\
            <module name=\"Centroid\">\n\
                <parameter name=\"Noise level\">1000.0</parameter>\n\
            </module>\n\
            <module name=\"Exact mass\">\n\
                <parameter name=\"Noise level\">1000.0</parameter>\n\
            </module>\n\
            <module name=\"Local maxima\">\n\
                <parameter name=\"Noise level\"/>\n\
            </module>\n\
            <module name=\"Recursive threshold\">\n\
                <parameter name=\"Noise level\"/>\n\
                <parameter name=\"Min m/z peak width\"/>\n\
                <parameter name=\"Max m/z peak width\"/>\n\
            </module>\n\
            <module name=\"Wavelet transform\">\n\
                <parameter name=\"Noise level\"/>\n\
                <parameter name=\"Scale level\"/>\n\
                <parameter name=\"Wavelet window size (%)\"/>\n\
            </module>\n\
        </parameter>\n\
        <parameter name=\"Mass list name\">masses</parameter>\n\
        <parameter name=\"CDF Filename (optional)\" selected=\"false\"/>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.masslistmethods.chromatogrambuilder.ChromatogramBuilderModule\">\n\
        <parameter name=\"Raw data files\" type=\"BATCH_LAST_FILES\"/>\n\
        <parameter name=\"Scans\">\n\
            <ms_level>1</ms_level>\n\
        </parameter>\n\
        <parameter name=\"Mass list\">masses</parameter>\n\
        <parameter name=\"Min time span (min)\">0.06</parameter>\n\
        <parameter name=\"Min height\">100000.0</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>0.005</absolutetolerance>\n\
            <ppmtolerance>10.0</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Suffix\">chromatograms-1E5</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.peakpicking.smoothing.SmoothingModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Filename suffix\">smoothed</parameter>\n\
        <parameter name=\"Filter width\">5</parameter>\n\
        <parameter name=\"Remove original peak list\">false</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.peakpicking.deconvolution.DeconvolutionModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Suffix\">deconvoluted</parameter>\n\
        <parameter name=\"Algorithm\" selected=\"Local minimum search\">\n\
            <module name=\"Baseline cut-off\">\n\
                <parameter name=\"Min peak height\">10000.0</parameter>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>0.0</min>\n\
                    <max>10.0</max>\n\
                </parameter>\n\
                <parameter name=\"Baseline level\">1000.0</parameter>\n\
            </module>\n\
            <module name=\"Noise amplitude\">\n\
                <parameter name=\"Min peak height\">10000.0</parameter>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>0.0</min>\n\
                    <max>10.0</max>\n\
                </parameter>\n\
                <parameter name=\"Amplitude of noise\">1000.0</parameter>\n\
            </module>\n\
            <module name=\"Savitzky-Golay\">\n\
                <parameter name=\"Min peak height\">10000.0</parameter>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>0.0</min>\n\
                    <max>10.0</max>\n\
                </parameter>\n\
                <parameter name=\"Derivative threshold level\">0.2</parameter>\n\
            </module>\n\
            <module name=\"Local minimum search\">\n\
                <parameter name=\"Chromatographic threshold\">0.95</parameter>\n\
                <parameter name=\"Search minimum in RT range (min)\">0.2</parameter>\n\
                <parameter name=\"Minimum relative height\">0.05</parameter>\n\
                <parameter name=\"Minimum absolute height\">30000.0</parameter>\n\
                <parameter name=\"Min ratio of peak top/edge\">3.0</parameter>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>0.06</min>\n\
                    <max>1.0</max>\n\
                </parameter>\n\
            </module>\n\
            <module name=\"Wavelets (XCMS)\">\n\
                <parameter name=\"S/N threshold\">10.0</parameter>\n\
                <parameter name=\"Wavelet scales\">\n\
                    <min>0.25</min>\n\
                    <max>5.0</max>\n\
                </parameter>\n\
                <parameter name=\"Peak duration range\">\n\
                    <min>0.0</min>\n\
                    <max>10.0</max>\n\
                </parameter>\n\
                <parameter name=\"Peak integration method\">Use smoothed data</parameter>\n\
            </module>\n\
            <module name=\"Wavelets (ADAP)\">\n\
                <parameter name=\"S/N threshold\">10.0</parameter>\n\
                <parameter name=\"S/N estimator\" selected=\"Intensity window SN\">\n\
                    <module name=\"Intensity window SN\"/>\n\
                    <module name=\"Wavelet Coeff. SN\">\n\
                        <parameter name=\"Peak width mult.\">3.0</parameter>\n\
                        <parameter name=\"abs(wavelet coeffs.)\">true</parameter>\n\
                    </module>\n\
                </parameter>\n\
                <parameter name=\"min feature height\">10.0</parameter>\n\
                <parameter name=\"coefficient/area threshold\">110.0</parameter>\n\
                <parameter name=\"Peak duration range\">\n\
                    <min>0.0</min>\n\
                    <max>10.0</max>\n\
                </parameter>\n\
                <parameter name=\"RT wavelet range\">\n\
                    <min>0.001</min>\n\
                    <max>0.1</max>\n\
                </parameter>\n\
            </module>\n\
        </parameter>\n\
        <parameter name=\"m/z range for MS2 scan pairing (Da)\" selected=\"false\">2.0</parameter>\n\
        <parameter name=\"RT range for MS2 scan pairing (min)\" selected=\"false\">0.1</parameter>\n\
        <parameter name=\"Remove original peak list\">true</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.isotopes.deisotoper.IsotopeGrouperModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Name suffix\">deisotoped</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>0.005</absolutetolerance>\n\
            <ppmtolerance>10.0</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Retention time tolerance\" type=\"absolute\">0.05</parameter>\n\
        <parameter name=\"Monotonic shape\">false</parameter>\n\
        <parameter name=\"Maximum charge\">2</parameter>\n\
        <parameter name=\"Representative isotope\">Most intense</parameter>\n\
        <parameter name=\"Remove original peaklist\">true</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.alignment.join.JoinAlignerModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Peak list name\">Aligned peak list</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>0.005</absolutetolerance>\n\
            <ppmtolerance>10.0</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Weight for m/z\">20.0</parameter>\n\
        <parameter name=\"Retention time tolerance\" type=\"absolute\">0.2</parameter>\n\
        <parameter name=\"Weight for RT\">15.0</parameter>\n\
        <parameter name=\"Require same charge state\">false</parameter>\n\
        <parameter name=\"Require same ID\">false</parameter>\n\
        <parameter name=\"Compare isotope pattern\" selected=\"false\">\n\
            <parameter name=\"Isotope m/z tolerance\">\n\
                <absolutetolerance>0.001</absolutetolerance>\n\
                <ppmtolerance>5.0</ppmtolerance>\n\
            </parameter>\n\
            <parameter name=\"Minimum absolute intensity\">10000.0</parameter>\n\
            <parameter name=\"Minimum score\">0.1</parameter>\n\
        </parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.gapfilling.peakfinder.PeakFinderModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Name suffix\">gap-filled</parameter>\n\
        <parameter name=\"Intensity tolerance\">0.25</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>0.005</absolutetolerance>\n\
            <ppmtolerance>10.0</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Retention time tolerance\" type=\"absolute\">0.3</parameter>\n\
        <parameter name=\"RT correction\">false</parameter>\n\
        <parameter name=\"Remove original peak list\">false</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.filtering.duplicatefilter.DuplicateFilterModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Name suffix\">filtered</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>0.003</absolutetolerance>\n\
            <ppmtolerance>10.0</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"RT tolerance\" type=\"absolute\">0.05</parameter>\n\
        <parameter name=\"Require same identification\">false</parameter>\n\
        <parameter name=\"Remove original peaklist\">false</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.identification.customdbsearch.CustomDBSearchModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Database file\">{0}</parameter>\n\
        <parameter name=\"Field separator\">,</parameter>\n\
        <parameter name=\"Field order\">\n\
            <item>ID</item>\n\
            <item>m/z</item>\n\
            <item>Retention time (min)</item>\n\
            <item>Identity</item>\n\
            <item>Formula</item>\n\
        </parameter>\n\
        <parameter name=\"Ignore first line\">true</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>0.003</absolutetolerance>\n\
            <ppmtolerance>10.0</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Retention time tolerance\" type=\"absolute\">0.2</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.io.csvexport.CSVExportModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Filename\">{1}</parameter>\n\
        <parameter name=\"Field separator\">,</parameter>\n\
        <parameter name=\"Export common elements\">\n\
            <item>Export row ID</item>\n\
            <item>Export row m/z</item>\n\
            <item>Export row retention time</item>\n\
            <item>Export row identity</item>\n\
            <item>Export row comment</item>\n\
            <item>Export row number of detected peaks</item>\n\
        </parameter>\n\
        <parameter name=\"Export data file elements\">\n\
            <item>Peak status</item>\n\
            <item>Peak m/z</item>\n\
            <item>Peak RT</item>\n\
            <item>Peak RT start</item>\n\
            <item>Peak RT end</item>\n\
            <item>Peak duration time</item>\n\
            <item>Peak height</item>\n\
            <item>Peak area</item>\n\
            <item>Peak charge</item>\n\
            <item>Peak # data points</item>\n\
            <item>Peak FWHM</item>\n\
            <item>Peak tailing factor</item>\n\
            <item>Peak asymmetry factor</item>\n\
            <item>Peak m/z min</item>\n\
            <item>Peak m/z max</item>\n\
        </parameter>\n\
        <parameter name=\"Export all IDs for peak\">true</parameter>\n\
        <parameter name=\"Export quantitation results and other information\">true</parameter>\n\
        <parameter name=\"Identification separator\">;</parameter>\n\
    </batchstep>\n\
</batch>".format(library, output_csv))

if __name__ == '__main__':

    logger.info('generating batch file...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-x', '--x_output', help="define the location of the xml file that needs to be generated;", dest = "x_output", default="config.xml", required = False)
    parser.add_argument(
        '-l', '--library', help="define the location of the library file;", dest = "library", default="../data/Positive_Garrett_MetaboliteStd_Library_RP_edited01152019JG.csv", required = False)
    parser.add_argument(
        '-i', '--input', help="define the location of input folder;", default="../../../data/metabolomics/fraction/grp1_fat/", required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output csv file;", default="../results/test.csv", required = False)
    
    args = parser.parse_args()
    batchfile_generator(args.x_output, args.input, args.library, args.output)


