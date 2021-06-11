*
* $Id: timex.F,v 1.1.1.1 1996/02/15 17:50:38 mclareni Exp $
*
* $Log: timex.F,v $
* Revision 1.1.1.1  1996/02/15 17:50:38  mclareni
* Kernlib
*
*
Clcs #include "kerngen/pilot.h"
Clcs #if defined(CERNLIB_QMVAX)
Clcs #include "vaxsys/timex.F"
Clcs #else
      SUBROUTINE TIMEX (T)
C
C CERN PROGLIB# Z007    TIMEX   DUMMY   .VERSION KERNFOR  4.05  821202
C
C-    DUMMY FOR NON-ESSENTIAL ROUTINE STILL MISSING ON YOUR MACHINE

      T = 9.
      RETURN
      END
Clcs #endif
