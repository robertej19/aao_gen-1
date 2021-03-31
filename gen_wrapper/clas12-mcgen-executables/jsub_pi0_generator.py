  
#!/usr/bin/env python3

"""
This is a text file generator to submit pi0_generator jobs on batch farm at JLab
"""

import random 
import sys
import os, subprocess
import argparse
import shutil
import time
import datetime 

def gen_jsub(args,count):
    outfile = open(args.jsub_textdir+"jsub_lund_job_{}.txt".format(count),"w")
    header = """PROJECT: clas12
JOBNAME: pi0gen_{0}

TRACK: {1}
DISK_SPACE: 4 GB

MEMORY: 1024 MB

COMMAND:
""".format(count,args.track)

    setup = """
mkdir -p aao_norad/build
mkdir -p gen_wrapper/run
cp {0} gen_wrapper/run/
cp {1} aao_norad/build/
cp {2} gen_wrapper/run/
cp {3} gen_wrapper/run/

""".format(args.input_exe_path,
        args.generator_exe_path,
        args.filter_exe_path,
        args.pi0_gen_exe_path)

    run_command = """
./gen_wrapper/run/pi0_gen_wrapper.exe \
--input_exe_path gen_wrapper/run/input_file_maker_aao_norad.exe \
--physics_model {} \
--flag_ehel {} \
--npart {} \
--epirea {} \
--ebeam {} \
--q2min {} \
--q2max {} \
--epmin {} \
--epmax {} \
--fmcall {} \
--boso {} \
--trig {} \
--precision {} \
--maxloops {} \
--generator_exe_path aao_norad/build/aao_norad.exe \
--filter_exe_path gen_wrapper/run/lund_filter.exe \
--outdir output/ \
--xBmin {} \
--xBmax {} \
--w2min {} \
--w2max {} \
--tmin {} \
--tmax {} \
--seed {} \
--docker {}
""".format(args.physics_model,
    args.flag_ehel,args.npart,args.epirea,args.ebeam,
    args.q2min,args.q2max,args.epmin,args.epmax,args.fmcall,
    args.boso,args.trig,args.precision,args.maxloops,
    args.xBmin,args.xBmax,args.w2min,args.w2max,
    args.tmin,args.tmax,
    args.seed,args.docker)

    footer = """
SINGLE_JOB: true

OUTPUT_DATA: output/pi0_gen.dat
OUTPUT_TEMPLATE:{0}pi0_gen{1}.lund
""".format(args.return_dir,count)

    outfile.write(header+setup+run_command+footer)
    outfile.close()

#Currently not using the args.rad or args.r flags

if __name__ == "__main__":
    # The following is needed since an executable does not have __file__ defined, but when working in interpreted mode,
    # __file__ is needed to specify the relative file path of other packages. In principle strict relative 
    # path usage should be sufficient, but it is easier to debug / more robust if absolute.
    try:
        __file__
    except NameError:
        full_file_path = sys.executable #This sets the path for compiled python
    else:
        full_file_path = os.path.abspath(__file__) #This sets the path for interpreted python

    #File structure:
    # repository head
    # ├── aao_norad
    # │   ├── build
    # │   │   └── aao_norad.exe
    # ├── aao_rad
    # ├── gen_wrapper
    # │   ├── run
    # │   │   ├── input_file_maker_aao_norad.exe
    # │   │   └── lund_filter.exe
    # │   └── src
    # │       ├── aao_norad_text.py
    # │       ├── input_file_maker_aao_norad.py
    # │       ├── lund_filter.py
    # │       └── pi0_gen_wrapper.py

    slash = "/"
    repo_base_dir = slash.join(full_file_path.split(slash)[:-3])
    input_file_maker_path = repo_base_dir + "/gen_wrapper/run/input_file_maker_aao_norad.exe"
    aao_norad_path = repo_base_dir + "/aao_norad/build/aao_norad.exe"
    lund_filter_path = repo_base_dir + "/gen_wrapper/run/lund_filter.exe"
    output_file_path = repo_base_dir + "/output/"
    jsub_textdir_path = repo_base_dir + "/submission_warehouse/"
    pi0_gen_path = repo_base_dir + "/gen_wrapper/run/pi0_gen_wrapper.exe"


    parser = argparse.ArgumentParser(description="""CURRENTLY ONLY WORKS WITH AAO_NORAD 4 PARTICLE FINAL STATE \n
                                This script: \n
                                1.) Creates an input file for aao_norad \n
                                2.) Generates specified number of events \n
                                3.) Filters generated events based off specifications \n
                                4.) Returns .dat data file""",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   
    #General options
    parser.add_argument("--rad",help="Uses radiative generator instead of nonradiative one, CURRENTLY NOT WORKING",default=False,action='store_true')

    #For step 1: input_file_maker_aao_norad
    parser.add_argument("--input_exe_path",help="Path to input file maker executable",default=input_file_maker_path)
    parser.add_argument("--physics_model",help="Physics model: 1=A0, 4=MAID98, 5=MAID2000",default=5)
    parser.add_argument("--flag_ehel",help="0= no polarized electron, 1=polarized electron",default=1)
    parser.add_argument("--npart",help="number of particles in BOS banks: 2=(e-,h+), 3=(e-,h+,h0)",default=3)
    parser.add_argument("--epirea",help="final state hadron: 1=pi0, 3=pi+",default=1)
    parser.add_argument("--ebeam",help="incident electron beam energy in GeV",default=10.6)
    parser.add_argument("--q2min",help="minimum Q^2 limit in GeV^2",default=0.2)
    parser.add_argument("--q2max",help="maximum Q^2 limit in GeV^2",default=10.6)
    parser.add_argument("--epmin",help="minimum scattered electron energy limits in GeV",default=0.2)
    parser.add_argument("--epmax",help="maximum scattered electron energy limits in GeV",default=10.6)
    parser.add_argument("--fmcall",help="factor to adjust the maximum cross section, used in M.C. selection",default=1.0)
    parser.add_argument("--boso",help="1=bos output, 0=no bos output",default=1)
    parser.add_argument("--trig",type=int,help="number of generated events",default=10000)
    parser.add_argument("--precision",type=float,help="Enter how close, in percent, you want the number of filtered events to be relative to desired events",default=10)
    parser.add_argument("--maxloops",type=int,help="Enter the number of generation iteration loops permitted to converge to desired number of events",default=10)

    #For step2: (optional) set path to aao_norad generator
    parser.add_argument("--generator_exe_path",help="Path to generator executable",default=aao_norad_path)

    #For step3: (optional) set path to lund filter script and get filtering arguemnets
    parser.add_argument("--filter_exe_path",help="Path to lund filter executable",default=lund_filter_path)
    parser.add_argument("--xBmin",type=float,help='minimum Bjorken X value',default=-1)
    parser.add_argument("--xBmax",type=float,help='maximum Bjorken X value',default=10)
    parser.add_argument("--w2min",type=float,help='minimum w2 value, in GeV^2',default=-1)
    parser.add_argument("--w2max",type=float,help='maximum w2 value, in GeV^2',default=100)
    parser.add_argument("--tmin",type=float,help='minimum t value, in GeV^2',default=-1)
    parser.add_argument("--tmax",type=float,help='maximum t value, in GeV^2',default=100)

    #Specify output directory for lund file
    parser.add_argument("--outdir",help="Specify full or relative path to output directory final lund file",default=output_file_path)
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')

    #For conforming with clas12-mcgen standards
    parser.add_argument("--seed",help="this arguement is ignored, but needed for inclusion in clas12-mcgen",default="none")
    parser.add_argument("--docker",help="this arguement is ignored, but needed for inclusion in clas12-mcgen",default="none")


    #Specific to creating jsub files
    parser.add_argument("--track",help="jsub track, e.g. debug, analysis",default="analysis")
    parser.add_argument("--jsub_textdir",help="Specify full or relative path to output directory for jsub file",default=jsub_textdir_path)
    parser.add_argument("-n",type=int,help="Number of batch submission text files",default=1)
    parser.add_argument("--return_dir",type=str,help="Directory you want batch farm files returned to",default="/volatile/clas12/robertej/")
    parser.add_argument("--pi0_gen_exe_path",help="Path to lund filter executable",default=pi0_gen_path)



    args = parser.parse_args()


    if not os.path.isdir(args.jsub_textdir):
        print(args.jsub_textdir+" is not present, creating now")
        subprocess.call(['mkdir','-p',args.jsub_textdir])
    else:
        print(args.jsub_textdir + "exists already")
        if args.r:
            print("trying to remove output dir")
            try:
                shutil.rmtree(args.jsub_textdir)
            except OSError as e:
                print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                print("trying to remove dir again")
                try:
                    shutil.rmtree(args.jsub_textdir)
                except OSError as e:
                    print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                    print("WARNING COULD NOT CLEAR OUTPUT DIRECTORY")
            subprocess.call(['mkdir','-p',args.jsub_textdir])
    
    print("Generating {} submission files".format(args.n))
    for index in range(0,args.n):
        print("Creating submission file {} of {}".format(index+1,args.n))
        gen_jsub(args,index)