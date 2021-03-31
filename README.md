# Commands to get running:
## clone the repository
git clone https://github.com/robertej19/aao_gen.git
 
## Move into the generator repository
cd aao_gen/aao_norad/

## Build the aao_norad generator executable
scons-2.7

## cd into head of repository
cd ..

## make all executables have correct permissions
chmod +x gen_wrapper/run/*

## See all options for wrapper:
./gen_wrapper/run/pi0_gen_wrapper.exe -h

## Example usage to generate 1000 events with minimum xB 0.1 and minimum W2 of 3:
./gen_wrapper/run/pi0_gen_wrapper.exe --xBmin 0.1 --w2min 3 --trig 1000  
## output datafile is in output/pi0_gen.dat


# How to create a bunch of lund files on the batch farm (won't need to do this once generator package is in clas12-mcgen
./gen_wrapper/run/jsub_pi0_generator.exe -n 1000 --track analysis --return_dir /volatile/clas12/robertej/some_output_lund_dir/ --q2min 2 --q2max 5 --xBmin 0.2 --xBmax 0.5 --w2min 3.8 --trig 8000
## The above command would generate 1000 lund files, each with 8000 events, in the specified kinematic range
## To see all options, write:
./gen_wrapper/run/jsub_pi0_generator.exe -h
