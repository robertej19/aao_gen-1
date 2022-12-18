#!/usr/bin/python3

import random 
import sys
import os, subprocess
import argparse
import shutil
import time
import datetime 
import math
import json


"""
This is a text file generator to submit pi0_generator jobs on sbatch farm at JLab
This Replaces sbatch_aao_generator.py
"""


class Dict2Class(object):
      
    def __init__(self, my_dict):        
        for key in my_dict:
            setattr(self, key, my_dict[key])

def gen_sbatch(args,count):
    outfile = open(args.sbatch_textdir+"sbatch_lund_job_{}.txt".format(count),"w")
    header = """#!/bin/bash
#
#SBATCH --account=clas12
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1000
#SBATCH --job-name={2}_{0}.job
#SBATCH --time=24:00:00
#SBATCH --gres=disk:10000
#SBATCH --output={3}gen_output/{0}.out
#SBATCH --error={3}gen_error/{0}.err

cd /scratch/slurm/$SLURM_JOB_ID

echo "currently located in:"
echo $PWD

# Sleep a random amount of time from 0-180s
# This avoids conflicts when lots of jobs start simultaneously.
TSLEEP=$[ ( $RANDOM % (180+1) ) ]s
echo "Sleeping for ${{TSLEEP}} ..."
sleep $TSLEEP""".format(count,args.track,args.slurm_job_name,args.return_dir)


    setup = """
mkdir -p aao_gen/build
mkdir -p gen_wrapper/src
cp {0} gen_wrapper/src/
cp {1} aao_gen/build/aao_generator.exe
cp {2} gen_wrapper/src/lund_filter.py
cp {3} gen_wrapper/src/
cp {4} .
chmod +x gen_wrapper/src/*
chmod +x aao_gen/build/*

""".format(args.input_exe_path,
        args.generator_exe_path,
        args.filter_exe_path,
        args.aao_gen_path_exe,
        args.json_args_path)


    run_command = """
./gen_wrapper/src/aao_gen.py \
--generator_type {} \
--input_filename_rad {} \
--input_filename_norad {} \
--flag_ehel {} \
--ebeam {} \
--q2min {} \
--q2max {} \
--epmin {} \
--epmax {} \
--fmcall {} \
--boso {} \
--seed {} \
--trig {} \
--epirea {} \
--physics_model_rad {} \
--int_region "{}" \
--npart_rad {} \
--sigr_max_mult {} \
--sigr_max {} \
--model_5_min_W {} \
--rad_emin {} \
--err_max {} \
--target_len {} \
--target_rad {} \
--cord_x {} \
--cord_y {} \
--cord_z {} \
--physics_model_norad {} \
--npart_norad {} \
--input_exe_path gen_wrapper/src/aao_input_file_maker.py \
--precision {} \
--maxloops {} \
--generator_exe_path aao_gen/build/aao_generator.exe \
--xBmin {} \
--xBmax {} \
--w2min {} \
--w2max {} \
--tmin {} \
--tmax {} \
--filter_infile {} \
--filter_outfile {} \
--filter_exe_path gen_wrapper/src/lund_filter.py \
--outdir {} \
""".format(args.generator_type,
args.input_filename_rad,
args.input_filename_norad,
args.flag_ehel,
args.ebeam,
args.q2min,
args.q2max,
args.epmin,
args.epmax,
args.fmcall,
args.boso,
args.seed,
args.trig,
args.epirea,
args.physics_model_rad,
args.int_region,
args.npart_rad,
args.sigr_max_mult,
args.sigr_max,
args.model_5_min_W,
args.rad_emin,
args.err_max,
args.target_len,
args.target_rad,
args.cord_x,
args.cord_y,
args.cord_z,
args.physics_model_norad,
args.npart_norad,
args.precision,
args.maxloops,
args.xBmin,
args.xBmax,
args.w2min,
args.w2max,
args.tmin,
args.tmax,
args.filter_infile,
args.filter_outfile,
args.outdir) ########## NOTE: args.r and args.docker are not currently included

    footer = """

mv aao_gen_filtered.dat {0}pi0_gen{1}.lund
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
    #repo_base_dir = slash.join(full_file_path.split(slash)[:-1])
    repo_base_dir = slash.join(full_file_path.split(slash)[:-4])
    output_file_path = repo_base_dir + "/output/"



    input_file_maker_path = repo_base_dir + "/gen_wrapper/batch_farm_executables/src/aao_input_file_maker.py"
    lund_filter_path = repo_base_dir + "/gen_wrapper/batch_farm_executables/src/lund_filter.py"
    aao_norad_path = repo_base_dir + "/aao_norad/build/aao_norad.exe"
    aao_rad_path = repo_base_dir + "/aao_rad/build/aao_rad.exe"
    json_args_path = repo_base_dir + "/gen_wrapper/batch_farm_executables/src/default_generator_args.json"
    
    with open('default_generator_args.json') as fjson:
        d = json.load(fjson)

    norad = Dict2Class(d["aao_norad"][0])
    rad = Dict2Class(d["aao_rad"][0])

    #with open('utils/histo_config.json') as fjson:
    #hftm = json.load(fjson)



    sbatch_textdir_path = repo_base_dir + "/gen_wrapper/batch_farm_executables/src/submission_warehouse/"
    aao_gen_path = repo_base_dir + "/gen_wrapper/batch_farm_executables/src/aao_gen.py"


    parser = argparse.ArgumentParser(description="""Currently only works with aao_norad and aao_rad pi0 final state generators \n
                                This script: \n
                                1.) Creates an input file for aao_norad \n
                                2.) Generates specified number of events \n
                                3.) Filters generated events based off specifications \n
                                4.) Returns .dat data file""",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   

    #General options
    parser.add_argument("--generator_type",help="rad | norad, lets you build input for either aao_rad or aao_norad generators",default="norad")
    parser.add_argument("--input_filename_rad",help="filename for aao_rad",default="aao_rad_input.inp")
    parser.add_argument("--input_filename_norad",help="filename for aao_norad",default="aao_norad_input.inp")
    parser.add_argument("--slurm_job_name",help="name for identification in scicomp",default="aao_(no)rad_generator")

    # common generator options
    parser.add_argument("--flag_ehel",help="0= no polarized electron, 1=polarized electron",default=norad.flag_ehel)
    parser.add_argument("--ebeam",help="incident electron beam energy in GeV",default=norad.ebeam)
    parser.add_argument("--q2min",help="minimum Q^2 limit in GeV^2",default=norad.q2min)
    parser.add_argument("--q2max",help="maximum Q^2 limit in GeV^2",default=norad.q2max)
    parser.add_argument("--epmin",help="minimum scattered electron energy limits in GeV",default=norad.epmin)
    parser.add_argument("--epmax",help="maximum scattered electron energy limits in GeV",default=norad.epmax)
    parser.add_argument("--fmcall",help="factor to adjust the maximum cross section, used in M.C. selection",default=norad.fmcall)
    parser.add_argument("--boso",help="1=bos output, 0=no bos output",default=norad.boso)    
    parser.add_argument("--seed",help="0= use unix timestamp from machine time to generate seed, otherwise use given value as seed",default=norad.seed)
    parser.add_argument("--trig",type=int,help="number of output events",default=norad.trig)
    parser.add_argument("--epirea",help="1: pi0 , 3:pi+, 5:eta",default=norad.epirea)

    #aao_rad specific options
    parser.add_argument("--physics_model_rad",help="Physics model for aao_rad (1=AO, 4=MAID, 11=dvmp)",default=rad.physics_model)
    parser.add_argument("--int_region",help="the sizes of the integration regions",default =rad.int_region)
    parser.add_argument("--npart_rad",help="number of particles in BOS banks for rad generator",default=rad.npart_rad)
    parser.add_argument("--sigr_max_mult",help="a multiplication factor for sigr_max",default=rad.sigr_max_mult)
    parser.add_argument("--sigr_max",help="sigr_max",default=rad.sigr_max)
    parser.add_argument("--model_5_min_W",help="minimum W (GeV) only for physics model 11",default=rad.model_5_min_W)
    parser.add_argument("--rad_emin",help="minimum photon energy for integration",default=rad.rad_emin)
    parser.add_argument("--err_max",help="limit on the error in (mm)**2",default=rad.err_max)
    parser.add_argument("--target_len",help="target cell length (cm)",default=rad.target_len)
    parser.add_argument("--target_rad",help="target cell cylinder radius",default=rad.target_radius)
    parser.add_argument("--cord_x",help="x-coord of beam position",default=rad.cord_x)
    parser.add_argument("--cord_y",help="y-coord of beam position",default=rad.cord_y)
    parser.add_argument("--cord_z",help="z-coord of beam position",default=rad.cord_z)

    # aao_norad specific options
    parser.add_argument("--physics_model_norad",help="Physics model for norad : 1=A0, 4=MAID98, 5=MAID2000",default=norad.physics_model)
    parser.add_argument("--npart_norad",help="number of particles in BOS banks for norad: 2=(e-,h+), 3=(e-,h+,h0)",default=norad.npart_norad)



    parser.add_argument("--json_args_path",help="Path to default_generator_args.json file ",default=json_args_path)

    parser.add_argument("--input_exe_path",help="Path to input file maker executable",default=input_file_maker_path)
    parser.add_argument("--precision",type=float,help="Enter how close, in percent, you want the number of filtered events to be relative to desired events",default=5)
    parser.add_argument("--maxloops",type=int,help="Enter the number of generation iteration loops permitted to converge to desired number of events",default=10)


    #For step2: (optional) set path to aao_norad generator
    parser.add_argument("--generator_exe_path",help="Path to generator executable",default=aao_norad_path)



    #For step3: (optional) set path to lund filter script and get filtering arguemnets
    parser.add_argument("--xBmin",type=float,help='minimum Bjorken X value',default=-1)
    parser.add_argument("--xBmax",type=float,help='maximum Bjorken X value',default=10)
    parser.add_argument("--w2min",type=float,help='minimum w2 value, in GeV^2',default=-1)
    parser.add_argument("--w2max",type=float,help='maximum w2 value, in GeV^2',default=100)
    parser.add_argument("--tmin",type=float,help='minimum t value, in GeV^2',default=-1)
    parser.add_argument("--tmax",type=float,help='maximum t value, in GeV^2',default=100)
    parser.add_argument("--filter_infile",help="specify input lund file name. Currently only works for 4-particle final state DVPiP",default="aao_norad.lund")
    parser.add_argument("--filter_outfile",help='specify processed lund output file name',default="aao_gen.dat")
   

    #Specify output directory for lund file
    parser.add_argument("--filter_exe_path",help="Path to lund filter executable",default=lund_filter_path)
    parser.add_argument("--outdir",help="Specify full or relative path to output directory final lund file",default=output_file_path)
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')


    #For conforming with clas12-mcgen standards
    parser.add_argument("--docker",help="this arguement is ignored, but needed for inclusion in clas12-mcgen",default=False,action='store_true')


    #Specific to creating sbatch files
    parser.add_argument("--track",help="sbatch track, e.g. debug, analysis",default="analysis")
    parser.add_argument("--sbatch_textdir",help="Specify full or relative path to output directory for sbatch file",default=sbatch_textdir_path)
    parser.add_argument("-n",type=int,help="Number of batch submission text files",default=1)
    parser.add_argument("--return_dir",type=str,help="Directory you want batch farm files returned to",default="/volatile/clas12/robertej/")
    parser.add_argument("--aao_gen_path_exe",help="Path to lund filter executable",default=aao_gen_path)


    args = parser.parse_args()


    if not os.path.isdir(args.sbatch_textdir):
        print(args.sbatch_textdir+" is not present, creating now")
        subprocess.call(['mkdir','-p',args.sbatch_textdir])
    else:
        print(args.sbatch_textdir + "exists already, remove it and try again")
        sys.exit()

    if args.generator_type == "rad":
        if args.generator_exe_path==aao_norad_path:
            args.generator_exe_path = aao_rad_path #change to using radiative generator
        if args.filter_infile == "aao_norad.lund":
            args.filter_infile = "aao_rad.lund" #change to using radiative generator


    print("Generating {} submission files for {} generator".format(args.n,args.generator_type))
    for index in range(0,args.n):
        print("Creating rad submission file {} of {}".format(index+1,args.n))
        gen_sbatch(args,index)
 