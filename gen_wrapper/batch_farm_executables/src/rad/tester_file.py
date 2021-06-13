#!/bin/python3.6m
#cython: language_level=3

import random 
import sys
import os, subprocess
import argparse
import shutil
import time
import datetime 

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



# def gen_input_file(args):
#     try:
#         if args.rad:
#             subprocess.run([args.input_exe_path,
#                 "--physics_model", str(args.physics_model),
#                 "--flag_ehel", str(args.flag_ehel),
#                 "--int_region", str(args.int_region),
#                 "--npart", str(args.npart),
#                 "--epirea", str(args.epirea), 
#                 "--err_max", str(args.err_max),
#                 "--target_len", str(args.target_len),
#                 "--target_rad", str(args.target_rad),
#                 "--cord_x", str(args.cord_x),
#                 "--cord_y", str(args.cord_y),
#                 "--cord_z", str(args.cord_z),
#                 "--ebeam", str(args.ebeam),
#                 "--q2min", str(args.q2min),
#                 "--q2max", str(args.q2max),
#                 "--epmin", str(args.epmin),
#                 "--epmax", str(args.epmax),
#                 "--rad_emin", str(args.rad_emin),
#                 "--trig", str(args.trig),
#                 "--sigr_max_mult", str(args.sigr_max_mult),
#                 "--sigr_max", str(args.sigr_max),
#                 "--seed", str(args.seed),
#                 "--input_filename", str(args.input_filename)])
#         else:
#             subprocess.run([args.input_exe_path,
#                 "--physics_model",str(args.physics_model),
#                 "--flag_ehel", str(args.flag_ehel),
#                 "--npart", str(args.npart),
#                 "--epirea", str(args.epirea),
#                 "--ebeam", str(args.ebeam),
#                 "--q2min", str(args.q2min),
#                 "--q2max", str(args.q2max),
#                 "--epmin", str(args.epmin),
#                 "--epmax", str(args.epmax),
#                 "--trig", str(args.trig),
#                 "--fmcall", str(args.fmcall),
#                 "--boso", str(args.boso),
#                 "--seed", str(args.seed),
#                 "--out", args.outdir+'aao_input.inp'])
#         return 0
#     except OSError as e:
#         print("\nError creating generator input file")
#         print("The error message was:\n %s - %s." % (e.filename, e.strerror))
#         print("Exiting\n")
#         return -1




# def run_generator(args,repo_base_dir):
#     try:
#         runstring = "{} < {}".format(args.generator_exe_path,args.input_filename)
#         process = subprocess.Popen(runstring,stdout=subprocess.PIPE,shell=True)
#         process.wait()
#         #process2 = subprocess.Popen("mv aao_norad.lund {}aao_norad.lund".format(args.outdir),shell=True)
#         #process2.wait()
#         #shutil.move(repo_base_dir+"/aao_rad.lund", args.outdir+"aao_rad.lund")
#         print("Moved lund file to new directory")
#         return 0
#     except OSError as e:
#         print("\nError using event generator")
#         print("The error message was:\n %s - %s." % (e.filename, e.strerror))
#         print("Exiting\n")  
#         return -1





# def filter_lund(args):
#     try:
#         if args.rad:
#             subprocess.run([args.filter_exe_path,
#                     "--filter_infile","aao_rad.lund",
#                     "--filter_outfile","aao_gen_filtered.dat",
#                     "--q2min", str(args.q2min),
#                     "--q2max", str(args.q2max),
#                     "--xBmin", str(args.xBmin),
#                     "--xBmax", str(args.xBmax),
#                     "--tmin", str(args.tmin),
#                     "--tmax", str(args.tmax),
#                     "--w2min", str(args.w2min),
#                     "--trig", str(args.trig),
#                     "--w2max", str(args.w2max)])
#         else:
#             subprocess.run([args.filter_exe_path,
#                     "--infile",args.outdir+"aao_norad.lund",
#                     "--outfile",args.outdir+"aao_gen.dat",
#                     "--q2min", str(args.q2min),
#                     "--q2max", str(args.q2max),
#                     "--xBmin", str(args.xBmin),
#                     "--xBmax", str(args.xBmax),
#                     "--tmin", str(args.tmin),
#                     "--tmax", str(args.tmax),
#                     "--w2min", str(args.w2min),
#                     "--trig", str(args.trig),
#                     "--w2max", str(args.w2max)])
#         return 0
#     except OSError as e:
#         print("\nError filtering generated events")
#         print("The error message was:\n %s - %s." % (e.filename, e.strerror))
#         print("Exiting\n")
#         return -1


# def compare_raw_to_filt(args,num_desired_events):
#     try:
#         filtered_lund = "aao_gen_filtered.dat"
#         with open(filtered_lund,"r") as f:
#             filtered_num = len(f.readlines())/5
#         ratio = filtered_num/num_desired_events
#         print(r"Produced {}% of desired number of events in kinematic range".format(100*ratio))
#         return ratio
#     except OSError as e:
#         print("\nError extracting filtering ratio")
#         print("The error message was:\n %s - %s." % (e.filename, e.strerror))
#         print("Exiting\n")  
#         return -1






def gen_events(args,repo_base_dir):
    print('hello3')
    for i in range(0,int(args.maxloops)):
        print("ehllo")
    # num_desired_events = args.trig
    # #If the number of events is not close enough to the desired number, generate recursively.
    # #It would be computationally better to just run the generator again and again until more than enough events are created,
    # #And then just cut out the last few events to get exactly the desired number of events, but I'm not sure that 
    # #This wouldn't bias things. If someone can verify that it doesn't bias anything, then this part of code should be restructured.
    # ratio = 0

    # max_num_loops = int(args.maxloops)+1
    # gen_rate = 0.0005 #seconds per event for aao_norad, this is just emperically observed


    # #for i in range(0,6):
    # for i in range(0,3):
    #     #print(1)
    #     print("generating {} raw events".format(args.trig))


        # gen_input_file(args)
        # print("Created generator input file, now trying to run generator")

        # start_time = time.time()
        # start_time_hr = datetime.datetime.fromtimestamp(start_time).strftime('%d %B %Y %H:%M:%S')
        # end_time = start_time+gen_rate*args.trig
        # end_time_hr = datetime.datetime.fromtimestamp(end_time).strftime('%d %B %Y %H:%M:%S')
        # print("Generator starting at {} ".format(start_time_hr))
        # print("Estimated finish time at {}".format(end_time_hr))


#         run_generator(args,repo_base_dir)


#         seconds_elapsed = time.time() - start_time
#         gen_rate = seconds_elapsed/args.trig
#         print("Generator took {} seconds to run".format(seconds_elapsed))

#         print("Event generation complete, now trying to filter")
        

#         filter_lund(args)
#         print("Lund file filtered, now comparing event sizes")

#         print("Now counting the effect of filtering")
#         ratio = compare_raw_to_filt(args,num_desired_events)
        
#         #if abs(ratio-1) < args.precision/100:
#         #if (ratio > 1):# and (abs(ratio-1) < args.precision/100): #This should be replaced to just truncate once the desired number of events are made
#         if abs(ratio-1) < args.precision/100:
#         #if (ratio ==1):
#             break
#         elif loop_counter == max_num_loops:
#             print("WARNING: Could not produce desired number of events after {} iterations".format(loop_counter))
#             print("Produced {} events".format(round(ratio*num_desired_events)))
#         else:
#             if ratio == 0:
#                 #This means no events made it past filtering, and we need to increase our stastics by a large factor
#                 args.trig = round(100* args.trig)
#             else:
#                 args.trig = round(args.trig/ratio)
#             print("Due to filtering, need to rerun and produce {} raw events, to end up with {} filtered events".format(args.trig,num_desired_events))


#should consider changing filtering method so if we generate more than enough valid events, we can just delete some at random       
#Should add logic checks that all the executables exist where they should exist
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
    repo_base_dir = slash.join(full_file_path.split(slash)[:-1])
    #repo_base_dir = slash.join(full_file_path.split(slash)[:-3])
    output_file_path = repo_base_dir + "/output/"

    norad_input_file_maker_path = repo_base_dir + "/gen_wrapper/batch-farm-executables/run/norad/input_file_maker_aao_norad.exe"
    rad_input_file_maker_path = repo_base_dir + "/gen_wrapper/batch-farm-executables/run/rad/input_file_maker_aao_rad.exe"

    norad_lund_filter_path = repo_base_dir + "/gen_wrapper/batch-farm-executables/run/norad/lund_filter_norad.exe"
    rad_lund_filter_path = repo_base_dir + "/gen_wrapper/batch-farm-executables/run/rad/lund_filter_rad.exe"


    aao_norad_path = repo_base_dir + "/aao_norad/build/aao_norad.exe"
    aao_rad_path = repo_base_dir + "/aao_rad/build/aao_rad.exe"





    parser = argparse.ArgumentParser(description="""CURRENTLY ONLY WORKS WITH AAO_NORAD 4 PARTICLE FINAL STATE \n
                                This script: \n
                                1.) Creates an input file for aao_norad \n
                                2.) Generates specified number of events \n
                                3.) Filters generated events based off specifications \n
                                4.) Returns .dat data file""",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #General options
    parser.add_argument("--rad",help="Uses radiative generator instead of nonradiative one, CURRENTLY NOT WORKING",default=False,action='store_true')

    #For step 1: input_file_maker_aao_norad
    parser.add_argument("--input_exe_path",help="Path to input file maker executable",default=norad_input_file_maker_path)
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
    parser.add_argument("--seed",help="0= use unix timestamp from machine time to generate seed, otherwise use given value as seed",default=0)
    parser.add_argument("--trig",type=int,help="number of generated events",default=10000)
    parser.add_argument("--precision",type=float,help="Enter how close, in percent, you want the number of filtered events to be relative to desired events",default=5)
    parser.add_argument("--maxloops",type=int,help="Enter the number of generation iteration loops permitted to converge to desired number of events",default=10)
    parser.add_argument("--input_filename",help="filename for aao_norad",default="aao_norad_input.inp")


    #Arguements specific to aao_rad
    parser.add_argument("--int_region",help="the sizes of the integration regions",default =".20 .12 .20 .20")
    parser.add_argument("--err_max",help="limit on the error in (mm)**2",default=0.2)
    parser.add_argument("--target_len",help="target cell length (cm)",default=5)
    parser.add_argument("--target_rad",help="target cell cylinder radius",default=0.43)
    parser.add_argument("--cord_x",help="x-coord of beam position",default=0.0)
    parser.add_argument("--cord_y",help="y-coord of beam position",default=0.0)
    parser.add_argument("--cord_z",help="z-coord of beam position",default=0.0)
    parser.add_argument("--rad_emin",help="minimum photon energy for integration",default=0.005)
    parser.add_argument("--sigr_max_mult",help="a multiplication factor for sigr_max",default=0.0)
    parser.add_argument("--sigr_max",help="sigr_max",default=0.005)




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
    parser.add_argument("--filter_exe_path",help="Path to lund filter executable",default=norad_lund_filter_path)
    parser.add_argument("--outdir",help="Specify full or relative path to output directory final lund file",default=output_file_path)
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')

    #For conforming with clas12-mcgen standards
    parser.add_argument("--docker",help="this arguement is ignored, but needed for inclusion in clas12-mcgen",default=False,action='store_true')

    args = parser.parse_args()


    if args.rad:
        if args.generator_exe_path==aao_norad_path:
            args.generator_exe_path = aao_rad_path #change to using radiative generator
        if args.filter_infile == "aao_norad.lund":
            args.filter_infile = "aao_rad.lund" #change to using radiative generator
        if args.input_exe_path == norad_input_file_maker_path:
            args.input_exe_path = rad_input_file_maker_path
        if args.input_filename == "aao_norad_input.inp":
            args.input_filename = "aao_rad_input.inp" #change to using radiative generator
        if args.filter_exe_path == norad_lund_filter_path:
            args.filter_exe_path = rad_lund_filter_path


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

    print("hellow2")
    gen_events(args,repo_base_dir)

