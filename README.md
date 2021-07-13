# Commands to run:

## clone the repository
git clone https://github.com/JeffersonLab/aao_gen.git
 
## Example usage to generate 1000 events with minimum xB 0.1 and minimum W2 of 3:
python3 aao_gen.py --xBmin 0.1 --w2min 3 --trig 1000  
## output datafile is in aao_gen.dat

## To get command line options: ./aao_gen.py -h

```
optional arguments:
  -h, --help            show this help message and exit
  --rad                 Uses radiative generator instead of nonradiative one,
                        CURRENTLY NOT WORKING (default: False)
  --physics_model PHYSICS_MODEL
                        Physics model: 1=A0, 4=MAID98, 5=MAID2000 (default: 5)
  --flag_ehel FLAG_EHEL
                        0= no polarized electron, 1=polarized electron
                        (default: 1)
  --npart NPART         number of particles in BOS banks: 2=(e-,h+),
                        3=(e-,h+,h0) (default: 3)
  --epirea EPIREA       final state hadron: 1=pi0, 3=pi+ (default: 1)
  --ebeam EBEAM         incident electron beam energy in GeV (default: 10.6)
  --q2min Q2MIN         minimum Q^2 limit in GeV^2 (default: 0.2)
  --q2max Q2MAX         maximum Q^2 limit in GeV^2 (default: 10.6)
  --epmin EPMIN         minimum scattered electron energy limits in GeV
                        (default: 0.2)
  --epmax EPMAX         maximum scattered electron energy limits in GeV
                        (default: 10.6)
  --fmcall FMCALL       factor to adjust the maximum cross section, used in
                        M.C. selection (default: 1.0)
  --boso BOSO           1=bos output, 0=no bos output (default: 1)
  --seed SEED           0= use unix timestamp from machine time to generate
                        seed, otherwise use given value as seed (default: 0)
  --trig TRIG           number of generated events (default: 10000)
  --precision PRECISION
                        Enter how close, in percent, you want the number of
                        filtered events to be relative to desired events
                        (default: 5)
  --maxloops MAXLOOPS   Enter the number of generation iteration loops
                        permitted to converge to desired number of events
                        (default: 10)
  --input_filename INPUT_FILENAME
                        filename for aao_norad (default: aao_norad_input.inp)
  --generator_exe_path GENERATOR_EXE_PATH
                        Path to generator executable (default: <path>/aao_norad/build/aao_norad.exe
                        )
  --xBmin XBMIN         minimum Bjorken X value (default: -1)
  --xBmax XBMAX         maximum Bjorken X value (default: 10)
  --w2min W2MIN         minimum w2 value, in GeV^2 (default: -1)
  --w2max W2MAX         maximum w2 value, in GeV^2 (default: 100)
  --tmin TMIN           minimum t value, in GeV^2 (default: -1)
  --tmax TMAX           maximum t value, in GeV^2 (default: 100)
  --filter_infile FILTER_INFILE
                        specify input lund file name. Currently only works for
                        4-particle final state DVPiP (default: aao_norad.lund)
  --filter_outfile FILTER_OUTFILE
                        specify processed lund output file name (default:
                        aao_gen.dat)
  --outdir OUTDIR       Specify full or relative path to output directory
                        final lund file (default: <path>/aao_gen/output/)
  -r                    Removes all files from output directory, if any
                        existed (default: False)
  --docker              this arguement is ignored, but needed for inclusion in
                        clas12-mcgen (default: False)

```
# Instructions to build
##Move into the generator repository
cd aao_gen/aao_norad/

## Build the aao_norad generator executable
scons-2.7

## cd into head of repository
cd ..

## See all options for wrapper:
python3 aao_gen.py -h


#  Generator Options to Use for Deeply Virtual Neutral Pion Production at CLAS12:
## aao_norad
```
5                ! Physics model: 1=A0, 4=MAID98, 5=MAID2000  
1                ! 0= no polarized electron, 1=polarized electron  
3                ! number of particles in BOS banks: 2=(e-,h+), 3=(e-,h+,h0)  
1                ! final state hadron: 1=pi0, 3=pi+  
10.6             ! incident electron beam energy in GeV  
0.2 14           ! minimum and maximum Q^2 limits in GeV^2  
0.2 10.6         ! minimum and maximum scattered electron energy limits in GeV  
1000             ! number of output events  
1.0              ! factor to adjust the maximum cross section, used in M.C. selection  
1                ! 1=bos output, 0=no bos output  
0                ! 0= use unix timestamp from machine time to generate seed, otherwise use given value as seed
```

## aao_rad
```
11                         ! Physics model (1=AO, 4=MAID, 11=dvmp)  
1	                         !  1 for polarized electron, 0 for unpolarized electron  
.20 .12 .20 .20            ! the sizes of the integration regions  
4                          ! npart  
1                          ! 1: pi0 , 3:pi+, 5:eta  
.4                         ! a limit on the error in (mm)**2  
5                          ! target cell length (cm)  
.775                       ! radius of target cyclinder  
.000                       ! x-coord of beam position  
.000                       ! y-coord of beam position  
-66.0                      ! z-coord of beam position  
10.6                       ! beam energy  
0.9 14.0                   ! Q2_min, Q2_max  
0.2 10.6                   ! scattered electron momentum min and max  
.001                       ! minimum photon energy for integration  
1000                       ! number of events  
0.0                        ! a multiplication factor for sigr_max                  
1.0                        ! sigr_max  
1.7		                      ! minimum W (GeV) only for physics model 11
```
