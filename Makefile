build:
	$(MAKE) -C aao_rad
	$(MAKE) -C aao_norad
clean:
	$(MAKE) -C aao_rad clean
	$(MAKE) -C aao_norad clean

