OBJ=  aao.o aao_norad.o cgln_amps.o daresbury.o dsigma.o dvmpw.o dvmpx.o fint.o helicity_amps.o interp.o legendre.o maid_lee.o multipole_amps.o read_sf_file.o splie2.o splin2.o spline.o splint.o timex.o xsection.o 
OBJC=  unixtime.o 

#CERNLIBS =  -L/apps/cernlib/x86_64_rhel6_4.7.2/2005/lib  -lmathlib  -lpacklib 
 
aao_rad : $(OBJ) $(OBJC)
	mkdir -p build
	gfortran -o build/aao_norad $(addprefix build/, $(OBJ)) build/$(OBJC) 
$(OBJ) : %.o: %.F
	mkdir -p build
	gfortran -fno-automatic -ffixed-line-length-none -fno-second-underscore -funroll-loops -fomit-frame-pointer  -c $< -o build/$@  
$(OBJC) : %.o: %.c
	mkdir -p build
	gcc -c $< -o build/$@ 
clean:
	rm -f build/aao_norad $(addprefix build/, $(OBJ)) $(addprefix build/, $(OBJC)) 



##g77  -O2 -fno-automatic -finit-local-zero -ffixed-line-length-none -fno-second-underscore \
##        -DLinux \
##        -I. -I./ -I/group/clas/builds/release-4-14/packages/include -I/group/clas/builds/release-4-14/packages/inc_derived -I/apps/tcl/include -I/usr/X11R6/include -c \
##        aac.F  -o /home/avakian/w6/tmp/obj/LinuxRHEL3/generator/aac.o

