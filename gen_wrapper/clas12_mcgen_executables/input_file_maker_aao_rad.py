  
#!/usr/bin/env python3

import os
import argparse
import sys

"Consult aao_norad generator repository README for options descriptions"

def gen_input(args):
    outfile = open(args.input_filename,"w")
    print("generating aao_norad_input file named {}".format(args.input_filename))
    string = """{} physics_model
{} flag_ehel
{} int_region
{} npart
{} epirea
{} err_max
{} target_len
{} target_rad
{} cord_x
{} cord_y
{} cord_z
{} ebeam
{} {} q2min q2max
{} {} epmin epmax
{} rad_emin
{} trig
{} sigr_max_mult
{} sigr_max
""".format(args.physics_model,
args.flag_ehel,
args.int_region,
args.npart,
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
args.trig,
args.sigr_max_mult,
args.sigr_max)
    outfile.write(string)
    outfile.close()

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="This generates an input file with specifications for the aao_norad pi0 generator",formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--physics_model",help="Physics model: 1=AO,4=MAID98,5=MAID2007",default=5)
    parser.add_argument("--flag_ehel",help="0= no polarized electron, 1=polarized electron",default=1)
    parser.add_argument("--int_region",help="the sizes of the integration regions",default =".20 .12 .20 .20")
    parser.add_argument("--npart",help="number of particles in BOS banks",default=4)
    parser.add_argument("--epirea",help="final state hadron: 1=pi0, 3=pi+",default=1)
    parser.add_argument("--err_max",help="limit on the error in (mm)**2",default=0.2)
    parser.add_argument("--target_len",help="target cell length (cm)",default=5)
    parser.add_argument("--target_rad",help="target cell cylinder radius",default=0.43)
    parser.add_argument("--cord_x",help="x-coord of beam position",default=0.0)
    parser.add_argument("--cord_y",help="y-coord of beam position",default=0.0)
    parser.add_argument("--cord_z",help="z-coord of beam position",default=0.0)
    parser.add_argument("--ebeam",help="incident electron beam energy in GeV",default=10.6)
    parser.add_argument("--q2min",help="minimum Q^2 limit in GeV^2",default=0.2)
    parser.add_argument("--q2max",help="maximum Q^2 limit in GeV^2",default=10.0)
    parser.add_argument("--epmin",help="minimum scattered electron energy limits in GeV",default=0.2)
    parser.add_argument("--epmax",help="maximum scattered electron energy limits in GeV",default=10.6)
    parser.add_argument("--rad_emin",help="minimum photon energy for integration",default=0.005)
    parser.add_argument("--trig",help="number of output events",default=10000)
    parser.add_argument("--sigr_max_mult",help="a multiplication factor for sigr_max",default=0.0)
    parser.add_argument("--sigr_max",help="sigr_max",default=0.005)

    parser.add_argument("--seed",help="0= use unix timestamp from machine time to generate seed, otherwise use given value as seed",default=0)
    parser.add_argument("--input_filename",help="filename for aao_norad",default="aao_rad_input.inp")



    args = parser.parse_args()

    gen_input(args)
