# Copyright (c) 2015 Boocock James <james.boocock@otago.ac.nz>
# Author: Boocock James <james.boocock@otago.ac.nz>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
import argparse
    
from fine_mapping_pipeline.prepare_input.prepare_run import prepare_runs

def main():
    """
        Creates and runs a fine mapping analysis.

    """
    logging.info('Starting the fine mapping pipeline')
    parser = argparse.ArgumentParser(description="Processes SNP based data and performs various fine mapping tasks")
    subparsers = parser.add_subparsers(help='Sub-command help')
    # Prepare parser 
    prepare_parser = subparsers.add_parser('prepare',help='Prepare for paintor run')
    prepare_parser.add_argument('-s', '--snp-list', dest='snp_list', help='SNP List file rsids or bed formatted')
    prepare_parser.add_argument('-z', '--z-score-dir', dest='z_score_dir', help='File containing Z-scores for an entire chromosome of SNPs')
    prepare_parser.add_argument('-f', '--flanking-region', dest='flanking_region', help='Flanking region')
    prepare_parser.add_argument('-n', '--number_of_snps', dest='flanking_units',action='store_true',help='Use a number of SNPs either side instead of a region', default=False)
    prepare_parser.add_argument('-b', '--build', dest='build', help='Genome build',default='hg19')
    prepare_parser.add_argument('-o', '--output', dest='output_directory', help='output directory empty or non-existent directory for dumping files to be used in a paintor run')
    prepare_parser.add_argument('-p', '--population', dest='population', help='1kg population to calculate LD from', default='EUR')
    prepare_parser.add_argument('-m', '--maf', dest='maf', help='MAF filtering for 1000 genomes VCF file', default=0.01)
    prepare_parser.set_defaults(func=prepare_runs)
    
    #Finemap parser
    paintor_parser = subparsers.add_parser('paintor', help='Run and process paintor\
                                           data following file preparation')
    paintor_parser.add_argument('-i','--input_directory', dest='input_directory', 
                                help="Directory files were prepared in after running the"
                                "prepare command", required=True)
    paintor_parser.add_argument('-a', '-auto-annotations', dest='auto_select_annotations',
                                help='If using paintor select the annotations.')
    paintor_parser.add_argument('-d','--output_directory', dest='output_directory', help="Results output dir")
    paintor_parser.set_defaults(func=run_paintor)
    
    caviarbf_parser = subparsers.add_parser('caviarbf', help='Run and process caviarbf\
                                            output following file preparation')
    caviarbf_parser.add_argument('-i','--input_directory', dest='input_directory', 
                                help="Directory files were prepared in after running the"
                                "prepare command", required=True)
    caviarbf_parser.add_argument('-d', '--output_directory', dest='output_directory', help="Results output dir")
    caviarbf_parser.set_defaults(func=run_caviarbf)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
