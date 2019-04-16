#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s]: %(levelname)s: %(message)s')

def batchfile_generator(xml_file, input_data, ms_level, detector_noiselevel, detector_scalelevel, detector_windowsize, buider_mintimespan, builder_minheight,
                        builder_abstolerance, builder_ppm, decov_snthreshold, decov_wavscamin, decov_wavscamax, decov_peadurmin, decov_peadurmax, output_data):
    with open(xml_file, "w+") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
<batch>\n\
    <batchstep method=\"net.sf.mzmine.modules.rawdatamethods.rawdataimport.RawDataImportModule\">\n\
        <parameter name=\"Raw data file names\">\n\
            <file>{0}</file>\n\
        </parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.rawdatamethods.peakpicking.massdetection.MassDetectionModule\">\n\
        <parameter name=\"Raw data files\" type=\"BATCH_LAST_FILES\"/>\n\
        <parameter name=\"Scans\">\n\
            <ms_level>{1}</ms_level>\n\
        </parameter>\n\
        <parameter name=\"Mass detector\" selected=\"Wavelet transform\">\n\
            <module name=\"Centroid\">\n\
                <parameter name=\"Noise level\">100.0</parameter>\n\
            </module>\n\
            <module name=\"Exact mass\">\n\
                <parameter name=\"Noise level\">100.0</parameter>\n\
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
                <parameter name=\"Noise level\">{2}</parameter>\n\
                <parameter name=\"Scale level\">{3}</parameter>\n\
                <parameter name=\"Wavelet window size (%)\">{4}</parameter>\n\
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
        <parameter name=\"Min time span (min)\">{5}</parameter>\n\
        <parameter name=\"Min height\">{6}</parameter>\n\
        <parameter name=\"m/z tolerance\">\n\
            <absolutetolerance>{7}</absolutetolerance>\n\
            <ppmtolerance>{8}</ppmtolerance>\n\
        </parameter>\n\
        <parameter name=\"Suffix\">chromatograms</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.peakpicking.deconvolution.DeconvolutionModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Suffix\">deconvoluted</parameter>\n\
        <parameter name=\"Algorithm\" selected=\"Wavelets (XCMS)\">\n\
            <module name=\"Baseline cut-off\">\n\
                <parameter name=\"Min peak height\">100.0</parameter>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>0.0</min>\n\
                    <max>10.0</max>\n\
                </parameter>\n\
                <parameter name=\"Baseline level\">100.0</parameter>\n\
            </module>\n\
            <module name=\"Noise amplitude\">\n\
                <parameter name=\"Min peak height\"/>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>0.0</min>\n\
                    <max>10.0</max>\n\
                </parameter>\n\
                <parameter name=\"Amplitude of noise\"/>\n\
            </module>\n\
            <module name=\"Savitzky-Golay\">\n\
                <parameter name=\"Min peak height\"/>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>0.0</min>\n\
                    <max>10.0</max>\n\
                </parameter>\n\
                <parameter name=\"Derivative threshold level\"/>\n\
            </module>\n\
            <module name=\"Local minimum search\">\n\
                <parameter name=\"Chromatographic threshold\"/>\n\
                <parameter name=\"Search minimum in RT range (min)\"/>\n\
                <parameter name=\"Minimum relative height\"/>\n\
                <parameter name=\"Minimum absolute height\"/>\n\
                <parameter name=\"Min ratio of peak top/edge\"/>\n\
                <parameter name=\"Peak duration range (min)\">\n\
                    <min>0.0</min>\n\
                    <max>10.0</max>\n\
                </parameter>\n\
            </module>\n\
            <module name=\"Wavelets (XCMS)\">\n\
                <parameter name=\"S/N threshold\">{9}</parameter>\n\
                <parameter name=\"Wavelet scales\">\n\
                    <min>{10}</min>\n\
                    <max>{11}</max>\n\
                </parameter>\n\
                <parameter name=\"Peak duration range\">\n\
                    <min>{12}</min>\n\
                    <max>{13}</max>\n\
                </parameter>\n\
                <parameter name=\"Peak integration method\">Use smoothed data</parameter>\n\
                <parameter name=\"R engine\">RCaller</parameter>\n\
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
                    <min>0.0</min>\n\
                    <max>0.1</max>\n\
                </parameter>\n\
            </module>\n\
        </parameter>\n\
        <parameter measure=\"MEDIAN\" name=\"m/z center calculation\" weighting=\"NONE\">CenterFunction</parameter>\n\
        <parameter name=\"m/z range for MS2 scan pairing (Da)\" selected=\"false\"/>\n\
        <parameter name=\"RT range for MS2 scan pairing (min)\" selected=\"false\"/>\n\
        <parameter name=\"Remove original peak list\">false</parameter>\n\
    </batchstep>\n\
    <batchstep method=\"net.sf.mzmine.modules.peaklistmethods.io.csvexport.CSVExportModule\">\n\
        <parameter name=\"Peak lists\" type=\"BATCH_LAST_PEAKLISTS\"/>\n\
        <parameter name=\"Filename\">{14}</parameter>\n\
        <parameter name=\"Field separator\">,</parameter>\n\
        <parameter name=\"Export common elements\">\n\
            <item>Export row ID</item>\n\
            <item>Export row m/z</item>\n\
            <item>Export row retention time</item>\n\
            <item>Export row identity (main ID)</item>\n\
            <item>Export row identity (all IDs)</item>\n\
            <item>Export row identity (main ID + details)</item>\n\
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
        <parameter name=\"Export quantitation results and other information\">true</parameter>\n\
        <parameter name=\"Identification separator\">;</parameter>\n\
        <parameter name=\"Filter rows\">ALL</parameter>\n\
    </batchstep>\n\
</batch>\n".format(input_data, int(ms_level), float(detector_noiselevel), int(detector_scalelevel), float(detector_windowsize), float(buider_mintimespan), float(builder_minheight),
                float(builder_abstolerance), float(builder_ppm), float(decov_snthreshold), float(decov_wavscamin), float(decov_wavscamax), float(decov_peadurmin), float(decov_peadurmax), output_data))

if __name__ == '__main__':

    logger.info('generating batch file...')

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--mzmine', help="define the location of the mzmine execution file;", dest = "mzmine", default="./docker/main/MZmine-2.38/startMZmine_MacOSX.command", required = False)
    parser.add_argument(
        '-x', '--x_output', help="define the location of the xml file that needs to be generated;", dest = "x_output", default="config.xml", required = False)
    parser.add_argument(
        '-i', '--input', help="define the location of input file (.xzXML format);", default="/app/data/DCSM/DCSM.mzXML", required = False)
    parser.add_argument(
        '-ml', '--ms_level', help="define ms level of mass detector;", dest = 'ms_level', default=1, required = False)
    parser.add_argument(
        '-dn', '--detector_noiselevel', help="define the noise level of Wavelet transform in mass detector;", dest = 'detector_noiselevel', default=100, required = False)
    parser.add_argument(
        '-ds', '--detector_scalelevel', help="define the scale level of Wavelet transform in mass detector;", dest = 'detector_scalelevel', default=20, required = False)
    parser.add_argument(
        '-dw', '--detector_windowsize', help="define the window size of mass detector;", dest = 'detector_windowsize', default=0.3, required = False)
    parser.add_argument(
        '-bt', '--buider_mintimespan', help="define the Min time span (min) for chromatogram builder;", dest = 'buider_mintimespan', default=0.04, required = False)
    parser.add_argument(
        '-bh', '--builder_minheight', help="define the Min height for chromatogram builder;", dest = 'builder_minheight', default=5000.0, required = False)
    parser.add_argument(
        '-ba', '--builder_abstolerance', help="define the abosolute tolerance of m/z tolerance for chromatogram builder;", dest = 'builder_abstolerance', default=0.01, required = False)
    parser.add_argument(
        '-bp', '--builder_ppm', help="define the ppm of m/z tolerance for chromatogram builder;", dest = 'builder_ppm', default=5.0, required = False)
    parser.add_argument(
        '-dt', '--decov_snthreshold', help="define the S/N threshold for chromatogram deconvolution;", dest = 'decov_snthreshold', default=10.0, required = False)
    parser.add_argument(
        '-dwi', '--decov_wavscamin', help="define the min wavelet scale for chromatogram deconvolution;", dest = 'decov_wavscamin', default=0.02, required = False)
    parser.add_argument(
        '-dwa', '--decov_wavscamax', help="define the max wavelet scale for chromatogram deconvolution;", dest = 'decov_wavscamax', default=0.8, required = False)
    parser.add_argument(
        '-dpi', '--decov_peadurmin', help="define the min peak duration for chromatogram deconvolution;", dest = 'decov_peadurmin', default=0.02, required = False)
    parser.add_argument(
        '-dpa', '--decov_peadurmax', help="define the max peak duration for chromatogram deconvolution;", dest = 'decov_peadurmax', default=0.6, required = False)
    parser.add_argument(
        '-o', '--output', help="define the location of output file (.csv format);", default="/app/outputs/DCSM_peaks.csv", required = False)

    args = parser.parse_args()

    batchfile_generator(args.x_output, args.input, args.ms_level, args.detector_noiselevel, args.detector_scalelevel, args.detector_windowsize, args.buider_mintimespan, args.builder_minheight,
                        args.builder_abstolerance, args.builder_ppm, args.decov_snthreshold, args.decov_wavscamin, args.decov_wavscamax, args.decov_peadurmin, args.decov_peadurmax, args.output)

    print("start to run mzmine")
#    print(args.mzmine + " " + args.x_output)
#    os.system(args.mzmine + " " + args.x_output)



