# Commands to get running:
## clone the repository
git clone https://github.com/robertej19/aao_gen.git
 
## Move into the generator repository
cd aao_gen/aao_norad/

## Build the aao_norad generator executable
scons-2.7

## cd into head of repository
cd ..

## See all options for wrapper:
python3 aao_gen.py -h

## Example usage to generate 1000 events with minimum xB 0.1 and minimum W2 of 3:
python3 aao_gen.py --xBmin 0.1 --w2min 3 --trig 1000  
## output datafile is in output/pi0_gen.dat

