#!/bin/python
#cython: language_level=3

import os
import argparse
import sys
import json

"Consult aao_norad and aao_rad generator repository README for options descriptions"

def gen_input_norad(args):
    outfile = open(args.input_filename_norad,"w")
    print("generating aao_norad_input file named {}".format(args.input_filename_norad))
    string = """{}
{}
{}
{}
{}
{} {}
{} {}
{}
{}
{}
0
""".format(args.physics_model_norad,args.flag_ehel,args.npart_norad,args.epirea,
    args.ebeam,args.q2min,args.q2max,args.epmin,args.epmax,
    int(args.trig),args.fmcall,args.boso)
    #NOTE: Args.seed was removed for testing
    outfile.write(string)
    outfile.close()

def gen_input_rad(args):
    outfile = open(args.input_filename_rad,"w")
    print("generating aao_rad_input file named {}".format(args.input_filename_rad))
    string = """{}     ! physics_model
{}     ! flag_ehel
{}     ! int_region
{}     ! npart
{}     ! epirea
{}     ! err_max
{}     ! target_len
{}     ! target_rad
{}     ! cord_x
{}     ! cord_y
{}     ! cord_z
{}     ! ebeam
{}  {}     ! q2min q2max
{}  {}     ! epmin epmax
{}     ! rad_emin
{}     ! trig
{}     ! sigr_max_mult
{}     ! sigr_max
{}     ! minimum W only for physics model 5
""".format(args.physics_model_rad,
args.flag_ehel,
args.int_region,
args.npart_rad,
args.epirea,
args.err_max,
args.target_len,
args.target_rad,
args.cord_x,
args.cord_y,
args.cord_z,
args.ebeam,
args.q2min, args.q2max,
args.epmin, args.epmax,
args.rad_emin,
int(args.trig),
args.sigr_max_mult,
args.sigr_max,
args.model_5_min_W)
    outfile.write(string)
    outfile.close()

class Dict2Class(object):
      
    def __init__(self, my_dict):        
        for key in my_dict:
            setattr(self, key, my_dict[key])

if __name__ == "__main__":

    try:
        __file__
    except NameError:
        full_file_path = sys.executable #This sets the path for compiled python
    else:
        full_file_path = os.path.abspath(__file__) #This sets the path for interpreted python

    
    main_source_dir = "/".join(full_file_path.split("/")[:-3])

    # location of default generator args:
    location_of_default_generator_args = main_source_dir + "/aao_gen/gen_wrapper/batch_farm_executables/src/default_generator_args.json"


    # This should be fixed because it is a local operator! But it can't be loaded through args yet
    with open('default_generator_args.json') as fjson:
        d = json.load(fjson)

    norad = Dict2Class(d["aao_norad"][0])
    rad = Dict2Class(d["aao_rad"][0])


    parser = argparse.ArgumentParser(description="This generates an input file with specifications for the aao_norad or aao_rad pi0 generator",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

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
    parser.add_argument("--trig",type=int,help="number of output events",default=norad.trig)
    parser.add_argument("--epirea",help="1: pi0 , 3:pi+, 5:eta",default=norad.epirea)

    #aao_rad specific options
    parser.add_argument("--physics_model_rad",help="Physics model for aao_rad (1=AO, 4=MAID, 11=dvmp)",default=rad.physics_model)
    parser.add_argument("--int_region",help="the sizes of the integration regions",default =rad.int_region)
    parser.add_argument("--npart_rad",help="number of particles in BOS banks for rad generator",default=rad.npart_rad)
    parser.add_argument("--sigr_max_mult",help="a multiplication factor for sigr_max",default=rad.sigr_max_mult)
    parser.add_argument("--sigr_max",help="sigr_max",default=rad.sigr_max)
    parser.add_argument("--model_5_min_W",help="minimum W (GeV) only for physics model 5",default=rad.model_5_min_W)
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

    #Other
    parser.add_argument("--default_gen_args_loc",help="location of default generator args json file",default="default_generator_args.json")

    args = parser.parse_args()


    if args.generator_type == "rad":
        gen_input_rad(args)
    elif args.generator_type == "norad": 
        gen_input_norad(args)
    else:
        print("The selected generator type, '{}', does not exist, try again.".format(args.generator_type))
        sys.exit()



        subprocess.run([args.generator_input_exe_path,
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
                "--input_filename_rad", str(params.output_location+"/"+args.input_filename_rad),
                "--input_filename_norad", str(params.output_location+"/"+args.input_filename_norad)])