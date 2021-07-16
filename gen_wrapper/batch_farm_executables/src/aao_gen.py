#!/bin/python3.6m
#cython: language_level=3

import random 
import sys
import os, subprocess
import argparse
import shutil
import time
import datetime 
import json

"""
This is a wrapper for the aao_norad (and aao_rad?) DVPi0 generators. It takes as input command line arguements which 
you can observe with the command line arguement -h, and gives as output a single .dat output file,
in lund format (https://gemc.jlab.org/gemc/html/documentation/generator/lund.html)

Requirements for inclusion on clas12-mcgen: (check requirements at https://github.com/JeffersonLab/clas12-mcgen)
--done-- C++ and Fortran: software should compile using gcc > 8.
--done-- An executable with the same name as the github repository name, installed at the top level dir
--done-- The generator output file name must be the same name as the exectuable + ".dat". For example, the output of clasdis must be clasdis.dat
--done-- If --seed is ignored, the generator is responsible for choosing unique random seeds (without preserving state between jobs), which could be done from a millisecond or better precision system clock.
--done-- The argument --seed <integer value> is added on the OSG to all executable. This option must be ignored or it can be used by the executable to set the generator random seed using <integer value>
--done-- To specify the number of events, the option "--trig" must be used
--done-- The argument --docker is added on the OSG to all executable. This option must be ignored or it can be used by the executable to set conditions to run on the OSG container

To verify all requirements are met, the executable must pass the following test:

genName --trig 10 --docker --seed 1448577483

This should produce a file genName.dat.
"""



def gen_input_file(args):
    try:
        subprocess.run([args.input_exe_path,
                "--generator_type", str(args.generator_type),
                "--physics_model_rad", str(args.physics_model_rad),
                "--physics_model_norad",str(args.physics_model_norad),
                "--npart_norad", str(args.npart_norad),
                "--npart_rad", str(args.npart_rad),
                "--flag_ehel", str(args.flag_ehel),
                "--int_region", str(args.int_region),
                "--epirea", str(args.epirea), 
                "--err_max", str(args.err_max),
                "--target_len", str(args.target_len),
                "--target_rad", str(args.target_rad),
                "--cord_x", str(args.cord_x),
                "--cord_y", str(args.cord_y),
                "--cord_z", str(args.cord_z),
                "--ebeam", str(args.ebeam),
                "--q2min", str(args.q2min),
                "--q2max", str(args.q2max),
                "--epmin", str(args.epmin),
                "--epmax", str(args.epmax),
                "--rad_emin", str(args.rad_emin),
                "--trig", str(args.trig),
                "--sigr_max_mult", str(args.sigr_max_mult),
                "--sigr_max", str(args.sigr_max),
                "--seed", str(args.seed),
                "--fmcall", str(args.fmcall),
                "--boso", str(args.boso),
                "--input_filename_rad", str(args.input_filename_rad),
                "--input_filename_norad", str(args.input_filename_norad)])
        return 0
    except OSError as e:
        print("\nError creating generator input file")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")
        return -1




def run_generator(args,repo_base_dir):
    try:
        runstring = "{} < {}".format(args.generator_exe_path,args.input_filename)
        print("Generator runstring is: {}".format(runstring))
        process = subprocess.Popen(runstring,stdout=subprocess.PIPE,shell=True)
        process.wait()
        #process2 = subprocess.Popen("mv aao_norad.lund {}aao_norad.lund".format(args.outdir),shell=True)
        #process2.wait()
        #shutil.move(repo_base_dir+"/aao_rad.lund", args.outdir+"aao_rad.lund")
        print("Generated events")
        return 0
    except OSError as e:
        print("\nError using event generator")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")  
        return -1





def filter_lund(args):
    infile_name = "aao_rad.lund" if args.generator_type == "rad" else "aao_norad.lund"
    print("trying to filter {}".format(infile_name))
    try:
        subprocess.run([args.filter_exe_path,
                "--filter_infile",infile_name,
                "--filter_outfile","aao_gen_filtered.dat",
                "--q2min", str(args.q2min),
                "--q2max", str(args.q2max),
                "--xBmin", str(args.xBmin),
                "--xBmax", str(args.xBmax),
                "--tmin", str(args.tmin),
                "--tmax", str(args.tmax),
                "--w2min", str(args.w2min),
                "--trig", str(args.trig),
                "--w2max", str(args.w2max)])
        return 0
    except OSError as e:
        print("\nError filtering generated events")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")
        return -1


def compare_raw_to_filt(args,num_desired_events):
    try:
        filtered_lund = "aao_gen_filtered.dat"
        with open(filtered_lund,"r") as f:
            filtered_num = len(f.readlines())/5
        ratio = filtered_num/num_desired_events
        print(r"Produced {}% of desired number of events in kinematic range".format(100*ratio))
        return ratio
    except OSError as e:
        print("\nError extracting filtering ratio")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")  
        return -1






def gen_events(args,repo_base_dir):

    num_desired_events = args.trig
    #If the number of events is not close enough to the desired number, generate recursively.
    #It would be computationally better to just run the generator again and again until more than enough events are created,
    #And then just cut out the last few events to get exactly the desired number of events, but I'm not sure that 
    #This wouldn't bias things. If someone can verify that it doesn't bias anything, then this part of code should be restructured.
    ratio = 0

    max_num_loops = args.maxloops
    gen_rate = 0.0005 #seconds per event for aao_norad, this is just emperically observed
    for loop_counter in range(0,max_num_loops+1):


        gen_input_file(args)
        print("Created generator input file, now trying to run generator")

        start_time = time.time()
        start_time_hr = datetime.datetime.fromtimestamp(start_time).strftime('%d %B %Y %H:%M:%S')
        end_time = start_time+gen_rate*args.trig
        end_time_hr = datetime.datetime.fromtimestamp(end_time).strftime('%d %B %Y %H:%M:%S')
        print("Generator starting at {} ".format(start_time_hr))
        print("Estimated finish time at {}".format(end_time_hr))


        run_generator(args,repo_base_dir)


        seconds_elapsed = time.time() - start_time
        gen_rate = seconds_elapsed/args.trig
        print("Generator took {} seconds to run".format(seconds_elapsed))

        print("Event generation complete, now trying to filter")
        

        filter_lund(args)
        print("Lund file filtered, now comparing event sizes")

        print("Now counting the effect of filtering")
        ratio = compare_raw_to_filt(args,num_desired_events)
        
        #if abs(ratio-1) < args.precision/100:
        #if (ratio > 1):# and (abs(ratio-1) < args.precision/100): #This should be replaced to just truncate once the desired number of events are made
        if abs(ratio-1) < args.precision/100:
        #if (ratio ==1):
            break
        elif loop_counter == max_num_loops:
            print("WARNING: Could not produce desired number of events after {} iterations".format(loop_counter))
            print("Produced {} events".format(round(ratio*num_desired_events)))
        else:
            if ratio == 0:
                #This means no events made it past filtering, and we need to increase our stastics by a large factor
                args.trig = round(100* args.trig)
            else:
                args.trig = round(args.trig/ratio)
            print("Due to filtering, need to rerun and produce {} raw events, to end up with {} filtered events".format(args.trig,num_desired_events))


#should consider changing filtering method so if we generate more than enough valid events, we can just delete some at random       
#Should add logic checks that all the executables exist where they should exist
#Make filtering more general for other processes, and include e.g. basic kinematics
#Include aao_rad functionality

class Dict2Class(object):
      
    def __init__(self, my_dict):        
        for key in my_dict:
            setattr(self, key, my_dict[key])

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

    
    with open('default_generator_args.json') as fjson:
        d = json.load(fjson)

    norad = Dict2Class(d["aao_norad"][0])
    rad = Dict2Class(d["aao_rad"][0])

    #with open('utils/histo_config.json') as fjson:
    #hftm = json.load(fjson)


    parser = argparse.ArgumentParser(description="""CURRENTLY ONLY WORKS WITH AAO_NORAD 4 PARTICLE FINAL STATE \n
                                This script: \n
                                1.) Creates an input file for aao_norad \n
                                2.) Generates specified number of events \n
                                3.) Filters generated events based off specifications \n
                                4.) Returns .dat data file""",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   
    #general options
    parser.add_argument("--generator_type",help="rad | norad, lets you build input for either aao_rad or aao_norad generators",default="norad")
    parser.add_argument("--input_filename_rad",help="filename for aao_rad",default="aao_rad_input.inp")
    parser.add_argument("--input_filename_norad",help="filename for aao_norad",default="aao_norad_input.inp")

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
    parser.add_argument("--trig",help="number of output events",default=norad.trig)
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


    #This one needs to be fixed!
    parser.add_argument("--input_filename",help="filename for aao_norad",default="aao_norad_input.inp")
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

    args = parser.parse_args()

    if args.generator_type == "rad":
        if args.generator_exe_path==aao_norad_path:
            args.generator_exe_path = aao_rad_path #change to using radiative generator
        if args.filter_infile == "aao_norad.lund":
            args.filter_infile = "aao_rad.lund" #change to using radiative generator



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
    gen_events(args,repo_base_dir)
