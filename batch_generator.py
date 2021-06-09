#This is to make large scale simulation runs

q2_divisions = [0.5,1,2,5,9,12]
xb_divisions = [0,0.2,0.5,1]
t_divisions = [0,1,2,3,6]
phi_divisions = [0,90,270,360]

args:
rad?
num events total / per area


generate appropriate mother directory
generate summary card - date, overall range and scheme
for division in space:
    generate appropriate directory
    generate summary card:
    xb q2 t range, num events, generator info
    jsub_aao_(no)rad_generator -- arguements
