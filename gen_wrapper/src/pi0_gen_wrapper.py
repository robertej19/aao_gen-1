#!/bin/python
#cython: language_level=3

"""
This is a wrapper for the aao_norad (and aao_rad?) DVPi0 generators. It takes as input command line arguements which 
you can observe with the command line arguement -h, and gives as output a single .dat output file,
in lund format (https://gemc.jlab.org/gemc/html/documentation/generator/lund.html)

Requirements for inclusion on clas12-mcgen: (check requirements at https://github.com/JeffersonLab/clas12-mcgen)
--NEED-- C++ and Fortran: software should compile using gcc > 8.
--NEED-- An executable with the same name as the github repository name, installed at the top level dir
--NEED-- The generator output file name must be the same name as the exectuable + ".dat". For example, the output of clasdis must be clasdis.dat
--done-- If --seed is ignored, the generator is responsible for choosing unique random seeds (without preserving state between jobs), which could be done from a millisecond or better precision system clock.
--done-- The argument --seed <integer value> is added on the OSG to all executable. This option must be ignored or it can be used by the executable to set the generator random seed using <integer value>
--done-- To specify the number of events, the option "--trig" must be used
--done-- The argument --docker is added on the OSG to all executable. This option must be ignored or it can be used by the executable to set conditions to run on the OSG container

To verify all requirements are met, the executable must pass the following test:

genName --trig 10 --docker --seed 1448577483

This should produce a file genName.dat.
"""

import random 
import sys
import os, subprocess
import argparse
import shutil


def gen_input_file(args):
    try:
        subprocess.call([args.input_exe_path,
            "--physics_model",str(args.physics_model),
            "--flag_ehel", str(args.flag_ehel),
            "--npart", str(args.npart),
            "--epirea", str(args.epirea),
            "--ebeam", str(args.ebeam),
            "--q2min", str(args.q2min),
            "--q2max", str(args.q2max),
            "--epmin", str(args.epmin),
            "--epmax", str(args.epmax),
            "--trig", str(args.trig),
            "--fmcall", str(args.fmcall),
            "--boso", str(args.boso),
            "--out", args.outdir+'aao_input.inp'])
        return 0
    except OSError as e:
        print("\nError creating generator input file")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")
        return -1

def run_generator(args):
    try:
        subprocess.call([args.generator_exe_path,"<",args.outdir+"aao_input.inp"])
        shutil.move("aao_norad.lund", args.outdir+"aao_norad.lund")
        return 0
    except OSError as e:
        print("\nError using event generator")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")  
        return -1

def filter_lund(args):
    try:
        subprocess.call([args.filter_exe_path,"--infile",args.outdir+"aao_norad.lund","--outfile",args.outdir+"pi0_gen.dat"])
        return 0
    except OSError as e:
        print("\nError filtering generated events")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")
        return -1

def compare_raw_to_filt(args):
    try:
        raw_lund = args.outdir+"aao_norad.lund"
        filtered_lund = args.outdir+"pi0_gen.dat"
        with open(raw_lund,"r") as f:
            raw_num = len(f.readlines())/5
        with open(filtered_lund,"r") as f:
            filtered_num = len(f.readlines())/5
        ratio = filtered_num/raw_num
        print(ratio)
        return ratio
    except OSError as e:
        print("\nError extracting filtering ratio")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")  
        return -1

def gen_events(args):


    #If the number of events is not close enough to the desired number, generate recursively.
    #It would be computationally better to just run the generator again and again until more than enough events are created,
    #And then just cut out the last few events to get exactly the desired number of events, but I'm not sure that 
    #This wouldn't bias things. If someone can verify that it doesn't bias anything, then this part of code should be restructured.
    ratio = 0
    while ratio 
            

        gen_input_file(args)
        print("Created generator input file, now trying to run generator")

        run_generator(args)
        print("Event generation complete, now trying to filter")
        print("Note: currently, filtering only works for aao_norad with 4 generated particles (e,p,g,g)")
        
        filter_lund(args)
        print("Lund file filtered, now comparing event sizes")

        print("Now count the effect of filtering")
        ratio = compare_raw_to_filt(args)

   
    

        

#Make extrapolation function for multiplaction factor for a given W2, Q2 (and also xB?) range
#Make filtering more general for other processes, and include e.g. basic kinematics
#Include aao_rad functionality


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


    parser = argparse.ArgumentParser(description="""CURRENTLY ONLY WORKS WITH AAO_NORAD 4 PARTICLE FINAL STATE \n
                                This script: \n
                                1.) Creates an input file for aao_norad \n
                                2.) Generates specified number of events \n
                                3.) Filters generated events based off specifications \n
                                4.) Returns .dat data file""",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   
    #General options
    parser.add_argument("--rad",help="Uses radiative generator instead of nonradiative one",default=False,action='store_true')

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
    parser.add_argument("--trig",help="number of generated events",default=10000)

    #For step2: (optional) set path to aao_norad generator
    parser.add_argument("--generator_exe_path",help="Path to generator executable",default=aao_norad_path)

    #For step3: (optional) set path to lund filter script
    parser.add_argument("--filter_exe_path",help="Path to lund filter executable",default=lund_filter_path)

    #Specify output directory for lund file
    parser.add_argument("--outdir",help="Specify full or relative path to output directory final lund file",default=output_file_path)
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')

    #For conforming with clas12-mcgen standards
    parser.add_argument("--seed",help="this arguement is ignored, but needed for inclusion in clas12-mcgen",default="none")
    parser.add_argument("--docker",help="this arguement is ignored, but needed for inclusion in clas12-mcgen",default="none")

    args = parser.parse_args()


    if not os.path.isdir(args.outdir):
        print(args.outdir+" is not present, creating now")
        subprocess.call(['mkdir','-p',args.outdir])
    else:
        print(args.outdir + "exists already")
        if args.r:
            print("trying to remove output dir")
            try:
                shutil.rmtree(args.outdir)
            except OSError as e:
                print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                print("trying to remove dir again")
                try:
                    shutil.rmtree(args.outdir)
                except OSError as e:
                    print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                    print("WARNING COULD NOT CLEAR OUTPUT DIRECTORY")
            subprocess.call(['mkdir','-p',args.outdir])
    
    print("Generating {} DVPiP Events".format(args.trig))
    gen_events(args)
