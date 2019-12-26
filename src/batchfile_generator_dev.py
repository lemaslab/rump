#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

def batchfile_generator(xml_file, input_dir, mass_detector, noise_level):

    input_files = [os.path.abspath(f) for f in os.listdir(input_dir)]
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
        <parameter name=\"Raw data files\"/>\n\
        <parameter name=\"Mass detector\" selected=\"{0}\">\n\
            <module name=\"Centroid\">\n\
                <parameter name=\"Noise level\">{1}</parameter>\n\
            </module>\n\
            <module name=\"Exact mass\">\n\
                <parameter name=\"Noise level\">{1}</parameter>\n\
            </module>\n\
            <module name=\"Local maxima\">\n\
                <parameter name=\"Noise level\">{1}</parameter>\n\
            </module>\n\
            <module name=\"Recursive threshold\">\n\
                <parameter name=\"Noise level\">{1}</parameter>\n\
                <parameter name=\"Min m/z peak width\">{2}</parameter>\n\
                <parameter name=\"Max m/z peak width\">{3}</parameter>\n\
            </module>\n\
            <module name=\"Wavelet transform\">\n\
                <parameter name=\"Noise level\">{1}</parameter>\n\
                <parameter name=\"Scale level\">{4}</parameter>\n\
                <parameter name=\"Wavelet window size (%)\">{5}</parameter>\n\
            </module>\n\
        </parameter>\n\
        <parameter name=\"MS level\">{6}</parameter>\n\
        <parameter name=\"Mass list name\">masses</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.masslistmethods.chromatogrambuilder.ChromatogramBuilderModule\">\n\
        <parameter name=\"Raw data files\"/>\n\
        <parameter name=\"Mass list\">masses</parameter>\n\
        <parameter name=\"Min time span (min)\">{7}</parameter>\n\
        <parameter name=\"Min height\">{8}</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>{9}</absolutetolerance>\n\
            <ppmtolerance>{10}</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Suffix\">chromatograms-1E5</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.peakpicking.smoothing.SmoothingModule\">\n\
        <parameter name=\"Peak lists\"/>\n\
        <parameter name=\"Filename suffix\">smoothed</parameter>\n\
        <parameter name=\"Filter width\">{11}</parameter>\n\
        <parameter name=\"Remove original peak list\">false</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.peakpicking.deconvolution.DeconvolutionModule\">\n\
        <parameter name=\"Peak lists\"/>\n\
        <parameter name=\"Suffix\">deconvoluted</parameter>\n\
        <parameter name=\"Algorithm\" selected=\"{12}\">\n\
            <module name=\"Baseline cut-off\">\n\
                <parameter name=\"Min peak height\">{13}</parameter>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>{14}</min>\n\
                    <max>{15}</max>\n\
                </parameter>\n\
                <parameter name=\"Baseline level\">{16}</parameter>\n\
            </module>\n\
            <module name=\"Noise amplitude\">\n\
                <parameter name=\"Min peak height\">{13}</parameter>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>{14}</min>\n\
                    <max>{15}</max>\n\
                </parameter>\n\
                <parameter name=\"Amplitude of noise\">{17}</parameter>\n\
            </module>\n\
            <module name=\"Savitzky-Golay\">\n\
                <parameter name=\"Min peak height\">{13}</parameter>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>{14}</min>\n\
                    <max>{15}</max>\n\
                </parameter>\n\
                <parameter name=\"Derivative threshold level\">{18}</parameter>\n\
            </module>\n\
            <module name=\"Local minimum search\">\n\
                <parameter name=\"Chromatographic threshold\">{19}</parameter>\n\
                <parameter name=\"Search minimum in RT range (min)\">{20}</parameter>\n\
                <parameter name=\"Minimum relative height\">{21}</parameter>\n\
                <parameter name=\"Minimum absolute height\">{22}</parameter>\n\
                <parameter name=\"Min ratio of peak top/edge\">{23}</parameter>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>{14}</min>\n\
                    <max>{15}</max>\n\
                </parameter>\n\
            </module>\n\
            <module name=\"Wavelets (XCMS)\">\n\
                <parameter name=\"S/N threshold\">{24}</parameter>\n\
                <parameter name=\"Wavelet scales\">\n\
                    <min>{25}</min>\n\
                    <max>{26}</max>\n\
                </parameter>\n\
                <parameter name=\"Peak duration range\">\n\
                    <min>{14}</min>\n\
                    <max>{15}</max>\n\
                </parameter>\n\
                <parameter name=\"Peak integration method\">Use smoothed data</parameter>\n\
            </module>\n\
        </parameter>\n\
        <parameter name=\"Remove original peak list\">true</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.isotopes.deisotoper.IsotopeGrouperModule\">\n\
        <parameter name=\"Peak lists\"/>\n\
        <parameter name=\"Name suffix\">deisotoped</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>{27}</absolutetolerance>\n\
            <ppmtolerance>{28}</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Retention time tolerance\" type=\"absolute\">{29}</parameter>\n\
        <parameter name=\"Monotonic shape\">{30}</parameter>\n\
        <parameter name=\"Maximum charge\">{31}</parameter>\n\
        <parameter name=\"Representative isotope\">Most intense</parameter>\n\
        <parameter name=\"Remove original peaklist\">true</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.alignment.join.JoinAlignerModule\">\n\
        <parameter name=\"Peak lists\"/>\n\
        <parameter name=\"Peak list name\">Aligned peak list</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>{32}</absolutetolerance>\n\
            <ppmtolerance>{33}</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Weight for m/z\">{34}</parameter>\n\
        <parameter name=\"Retention time tolerance\" type=\"absolute\">{35}</parameter>\n\
        <parameter name=\"Weight for RT\">{36}</parameter>\n\
        <parameter name=\"Require same charge state\">{37}</parameter>\n\
        <parameter name=\"Require same ID\">{38}</parameter>\n\
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
        <parameter name=\"Peak lists\"/>\n\
        <parameter name=\"Name suffix\">gap-filled</parameter>\n\
        <parameter name=\"Intensity tolerance\">0.25</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>0.003</absolutetolerance>\n\
            <ppmtolerance>5.0</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Retention time tolerance\" type=\"absolute\">0.05</parameter>\n\
        <parameter name=\"RT correction\">false</parameter>\n\
        <parameter name=\"Remove original peak list\">false</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.filtering.duplicatefilter.DuplicateFilterModule\">\n\
        <parameter name=\"Peak lists\"/>\n\
        <parameter name=\"Name suffix\">filtered</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>0.002</absolutetolerance>\n\
            <ppmtolerance>5.0</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"RT tolerance\" type=\"absolute\">0.05</parameter>\n\
        <parameter name=\"Require same identification\">false</parameter>\n\
        <parameter name=\"Remove original peaklist\">false</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.io.csvexport.CSVExportModule\">\n\
        <parameter name=\"Peak lists\"/>\n\
        <parameter name=\"Filename\">{39}</parameter>\n\
        <parameter name=\"Field separator\">,</parameter>\n\
        <parameter name=\"Export common elements\">\n\
            <item>Export row ID</item>\n\
            <item>Export row m/z</item>\n\
            <item>Export row retention time</item>\n\
            <item>Export row comment</item>\n\
            <item>Export row number of detected peaks</item>\n\
        </parameter>\n\
        <parameter name=\"Export identity elements\">\n\
            <item>All identity elements</item>\n\
        </parameter>\n\
        <parameter name=\"Export data file elements\">\n\
            <item>Export peak status</item>\n\
            <item>Export peak m/z</item>\n\
            <item>Export peak retention time</item>\n\
            <item>Export peak height</item>\n\
            <item>Export peak area</item>\n\
            <item>Export peak charge</item>\n\
            <item>Export peak duration time</item>\n\
        </parameter>\n\
    </batchstep>\n\
</batch>".format(mass_detector, noise_level, minmz_peakwidth, maxmz_peakwidth, scale_level, wavwlet_windowsize, ms_level, min_timespan, 
                 min_height, abs_tol, ppm, filter_width, decov_method, min_peakheight, min_peakdur, max_peakdur, baseline_level, amp_noise,
                 dtl, chrom_threshold, rt_min, min_rheight, min_aheight, min_peaktop, sn_threshold, min_wavelet, max_wavelet, grouper_abstol, 
                 grouper_ppm, rt_tol, monotonic_shape, max_charge, align_abstol, align_ppm, mz_weight, align_rt_tol, align_rt_weight, 
                 same_chargestate, same_id, output))

if __name__ == '__main__':

    logger.info('generating batch file...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-x', '--x_output', help="define the location of the xml file that needs to be generated;", dest = "x_output", default="config.xml", required = False)
    parser.add_argument(
        '-i', '--input', help="define the location of input file (.xzXML format);", default="/app/data/DCSM/DCSM.mzXML", required = False)
    parser.add_argument(
        '-md', '--mass_detector', help="under development", dest = "mass_detector", default="Centroid", required = False)
    parser.add_argument(
        '-nl', '--noise_level', help="under development", dest = "noise_level", default=1000.0, required = False)
    parser.add_argument(
        '-minpw', '--minmz_peakwidth', help="under development", dest = "minmz_peakwidth", default=10.0, required = False)
    parser.add_argument(
        '-maxpw', '--maxmz_peakwidth', help="under development", dest = "maxmz_peakwidth", default=10.0, required = False)
    parser.add_argument(
        '-sl', '--scale_level', help="under development", dest = "scale_level", default=20.0, required = False)
    parser.add_argument(
        '-ww', '--wavwlet_windowsize', help="under development", dest = "wavwlet_windowsize", default=0.3, required = False)
    parser.add_argument(
        '-ml', '--ms_level', help="under development", dest = "ms_level", default=1, required = False)
    parser.add_argument(
        '-mt', '--min_timespan', help="under development", dest = "min_timespan", default=0.06, required = False)
    parser.add_argument(
        '-mh', '--min_height', help="under development", dest = "min_height", default=100000.0, required = False)
    parser.add_argument(
        '-at', '--abs_tol', help="under development", dest = "abs_tol", default=0.002, required = False)
    parser.add_argument(
        '-p', '--ppm', help="under development", dest = "ppm", default=5.0, required = False)
    parser.add_argument(
        '-fw', '--filter_width', help="under development", dest = "filter_width", default=5, required = False)
    


    args = parser.parse_args()
    batchfile_generator(args.x_output, args.input)


