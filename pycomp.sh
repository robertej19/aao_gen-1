
inname=$1
outname=$2

cython --embed -o cythonizedfile.c $1
g+= -I/usr/include/python3.6m cythonizedfile.c -lpython3.6m cythonizedfile.c
