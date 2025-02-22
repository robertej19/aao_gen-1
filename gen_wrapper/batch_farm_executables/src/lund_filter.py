#!/bin/python
#cython: language_level=3

import os
import argparse

def vec_subtract(vec1,vec2):
    res = tuple(map(lambda i, j: i - j, vec1, vec2)) 
    return res

def vec_add(vec1,vec2):
    res = tuple(map(lambda i, j: i + j, vec1, vec2)) 
    return res

def calc_inv_mass_squared(four_vector):
    fv = four_vector
    inv_mass2 = fv[0]**2-fv[1]**2-fv[2]**2-fv[3]**2
    return inv_mass2

e_mass = 0.00051099895
Ebeam_4mom = (10.604,0,0,10.604)
p_mass = 0.9382721
pi_mass = 0.1349768
target_4mom = (p_mass,0,0,0)


def filter_lund(args):
    filter_infile_name = args.filter_infile
    output_filename = args.filter_outfile

    with open(filter_infile_name,"r") as lst:
        txtlst = lst.readlines()
    
    outlines = []
    for ind,line in enumerate(txtlst):
        if ind %5000 == 0:
            print("On event {}".format(ind/5))

        if ind % 5 == 0:
            a = line
            b = txtlst[ind+1]
            c = txtlst[ind+2]
            d = txtlst[ind+3]
            e = txtlst[ind+4]
            for sub_line in (a,b,c,d):
                cols = sub_line.split()
                if cols[3]=='11':
                    e_4mom = (float(cols[9]),float(cols[6]),float(cols[7]),float(cols[8]))
                
                if cols[3]=='2212':
                    pro_4mom = (float(cols[9]),float(cols[6]),float(cols[7]),float(cols[8]))

                if cols[3]=='111':
                    pi_4mom = (float(cols[9]),float(cols[6]),float(cols[7]),float(cols[8]))
                
                if cols[3]=='22':
                    gamma_4mom = (float(cols[9]),float(cols[6]),float(cols[7]),float(cols[8]))


            virtual_gamma = vec_subtract(Ebeam_4mom,e_4mom)
            Q2 = -1*calc_inv_mass_squared(virtual_gamma)
            W2 = calc_inv_mass_squared(vec_subtract(vec_add(Ebeam_4mom,target_4mom),e_4mom))
            nu = virtual_gamma[0]
            xB = Q2/(2*p_mass*nu)
            t = -1*calc_inv_mass_squared(vec_subtract(target_4mom,pro_4mom))


            if t> float(args.tmin) and t< float(args.tmax) and Q2> float(args.q2min) and Q2< float(args.q2max) and W2> float(args.w2min) and W2< float(args.w2max) and xB > float(args.xBmin) and xB < float(args.xBmax):
                outlines.append(a)
                outlines.append(b)
                outlines.append(c)
                outlines.append(d)
                outlines.append(e)
        if (len(outlines)/5 == int(args.trig)):
            break
                            
    print("Original length {}, filtered length {}".format(len(txtlst)/5,len(outlines)/5))
    print(output_filename)
    with open(output_filename, 'w') as f:
        f.write(''.join(outlines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filters pi0 generated LUND file on ",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--filter_infile",help="specify input lund file name. Currently only works for 4-particle final state DVPiP",default="aao_norad.dat")
    parser.add_argument("--filter_outfile",help='specify processed lund output file name',default="filtered_lund_file.dat")
    parser.add_argument("--q2min",type=float,help='minimum Q2 value, in GeV^2',default=-1)
    parser.add_argument("--q2max",type=float,help='maximum Q2 value, in GeV^2',default=100)
    parser.add_argument("--xBmin",type=float,help='minimum Bjorken X value',default=-1)
    parser.add_argument("--xBmax",type=float,help='maximum Bjorken X value',default=10)
    parser.add_argument("--w2min",type=float,help='minimum w2 value, in GeV^2',default=-1)
    parser.add_argument("--w2max",type=float,help='maximum w2 value, in GeV^2',default=100)
    parser.add_argument("--tmin",type=float,help='minimum t value, in GeV^2',default=-1)
    parser.add_argument("--tmax",type=float,help='maximum t value, in GeV^2',default=100)
    parser.add_argument("--trig",type=int,help="number of desired generated events",default=10000)
    args = parser.parse_args()

    
    print("trying to process file {}".format(args.filter_infile))
    filter_lund(args)
