**********************************
*    ____PDF ____________________*
**********************************
      program check
      implicit none
      
      integer idum,jdum,i,j,irep,nrep,nrep_as
      integer iplus_68,iminus_68,iaver_68
      integer nrep_0115,nrep_0116,nrep_0117,nrep_0118
      integer nrep_0119,nrep_0120,nrep_0121
      double precision lo_0,nlo_0,nlo_susy_0
      double precision nlo_down,nlo_up
      double precision dum,lo(100),nlo(100),nlo_susy(100)
      double precision lo_as(300),nlo_as(300),nlo_as_susy(300)
      double precision sum, sum2, sig2, cl68, avg, tmp,pdfERR,pdfasERR
      character*10 cdum

      write(*,*)"=================================="
      write(*,*)"= PDF uncertainty                ="
      write(*,*)"=================================="
      nrep = 100

      open(unit=17,status="old",
     $     file="tables_8TeV/NNPDF21_as0118_200GeV")
      read(17,*) cdum
      read(17,*)idum,idum,lo_0,dum,nlo_0,dum,dum
     $     ,nlo_susy_0,dum,dum,dum,dum
      do i=1,100
         read(17,*)idum,idum,lo(idum),dum,nlo(idum),dum,dum,
     $        nlo_susy(idum),dum,dum,dum,dum
      enddo
      close(17)

c     Order NLO xsec in order to compute 68% CL
      call sort_100(nlo)

      sum  = 0d0
      sum2 = 0d0
      do irep = 1,nrep
         sum  = sum  + nlo(irep)
         sum2 = sum2 + nlo(irep)*nlo(irep)
      enddo
      avg  = sum/dble(nrep)
      tmp  = sum2 - sum*sum/dble(nrep)
      sig2 = dsqrt(tmp/dble(nrep-1))
      iplus_68  = nrep - int(0.5d0 * ( nrep - nrep * 68d0 / 1d2) )
      iminus_68 = int(0.5d0 * ( nrep - nrep * 68d0 / 1d2) )
      iaver_68  = int(nrep/2d0)
      write(*,*) avg,sig2," +",nlo(iplus_68)-nlo(iaver_68), 
     $     "-",nlo(iaver_68)-nlo(iminus_68)
      pdfERR = sig2
      write(*,*) "----> ",avg," +/- ",pdfERR


********     read as sets *************************************

      write(*,*)"=================================="
      write(*,*)"= PDF + as uncertainty           ="
      write(*,*)"=================================="

      nrep_as = 0
      nrep_0115 = 4
      open(unit=17,status="old",
     $     file="tables_8TeV/NNPDF21_as0115_200GeV")
      read(17,*) cdum
      read(17,*)idum,idum,lo_0,dum,nlo_0,dum,dum
     $     ,nlo_susy_0,dum,dum,dum,dum
      do i=1,nrep_0115
         read(17,*)idum,idum,lo_as(i),dum,nlo_as(i),dum,dum,
     $        nlo_as_susy(i),dum,dum,dum,dum
      enddo
      close(17)
      nrep_as = nrep_as + nrep_0115

      nrep_0116 = 25
      open(unit=17,status="old",
     $     file="tables_8TeV/NNPDF21_as0116_200GeV")
      read(17,*) cdum
      read(17,*)idum,idum,lo_0,dum,nlo_0,dum,dum
     $     ,nlo_susy_0,dum,dum,dum,dum
      do i=nrep_as+1,nrep_as+nrep_0116
         read(17,*)idum,idum,lo_as(i),dum,nlo_as(i),dum,dum,
     $        nlo_as_susy(i),dum,dum,dum,dum
      enddo
      close(17)
      nrep_as = nrep_as + nrep_0116

      nrep_0117 = 71
      open(unit=17,status="old",
     $     file="tables_8TeV/NNPDF21_as0117_200GeV")
      read(17,*) cdum
      read(17,*)idum,idum,lo_0,dum,nlo_0,dum,dum
     $     ,nlo_susy_0,dum,dum,dum,dum
      do i=nrep_as+1,nrep_as+nrep_0117
         read(17,*)idum,idum,lo_as(i),dum,nlo_as(i),dum,dum,
     $        nlo_as_susy(i),dum,dum,dum,dum
      enddo
      close(17)
      nrep_as = nrep_as + nrep_0117
      nlo_down = nlo_0

      nrep_0118 = 100
      open(unit=17,status="old",
     $     file="tables_8TeV/NNPDF21_as0116_200GeV")
      read(17,*) cdum
      read(17,*)idum,idum,lo_0,dum,nlo_0,dum,dum
     $     ,nlo_susy_0,dum,dum,dum,dum
      do i=nrep_as+1,nrep_as+nrep_0118
         read(17,*)idum,idum,lo_as(i),dum,nlo_as(i),dum,dum,
     $        nlo_as_susy(i),dum,dum,dum,dum
      enddo
      close(17)
      nrep_as = nrep_as + nrep_0118
      
      nrep_0119 = 71
      open(unit=17,status="old",
     $     file="tables_8TeV/NNPDF21_as0119_200GeV")
      read(17,*) cdum
      read(17,*)idum,idum,lo_0,dum,nlo_0,dum,dum
     $     ,nlo_susy_0,dum,dum,dum,dum
      do i=nrep_as+1,nrep_as+nrep_0119
         read(17,*)idum,idum,lo_as(i),dum,nlo_as(i),dum,dum,
     $        nlo_as_susy(i),dum,dum,dum,dum
      enddo
      close(17)
      nrep_as = nrep_as + nrep_0119
      nlo_up  = nlo_0

      nrep_0120 = 25
      open(unit=17,status="old",
     $     file="tables_8TeV/NNPDF21_as0120_200GeV")
      read(17,*) cdum
      read(17,*)idum,idum,lo_0,dum,nlo_0,dum,dum
     $     ,nlo_susy_0,dum,dum,dum,dum
      do i=nrep_as+1,nrep_as+nrep_0120
         read(17,*)idum,idum,lo_as(i),dum,nlo_as(i),dum,dum,
     $        nlo_as_susy(i),dum,dum,dum,dum
      enddo
      close(17)
      nrep_as = nrep_as + nrep_0120

      nrep_0121 = 4
      open(unit=17,status="old",
     $     file="tables_8TeV/NNPDF21_as0121_200GeV")
      read(17,*) cdum
      read(17,*)idum,idum,lo_0,dum,nlo_0,dum,dum
     $     ,nlo_susy_0,dum,dum,dum,dum
      do i=nrep_as+1,nrep_as+nrep_0121
         read(17,*)idum,idum,lo_as(i),dum,nlo_as(i),dum,dum,
     $        nlo_as_susy(i),dum,dum,dum,dum
      enddo
      close(17)
      nrep_as = nrep_as + nrep_0121

********************
      call sort_300(nlo_as)
      sum  = 0d0
      sum2 = 0d0
      do irep = 1,nrep_as
         sum  = sum  + nlo_as(irep)
         sum2 = sum2 + nlo_as(irep)*nlo_as(irep)
      enddo
      avg  = sum/dble(nrep_as)
      tmp  = sum2 - sum*sum/dble(nrep_as)
      sig2 = dsqrt(tmp/dble(nrep_as-1)) 
      iplus_68  = nrep_as 
     $     - int(0.5d0 * ( nrep_as - nrep_as * 68d0 / 1d2) )
      iminus_68 = int(0.5d0 * ( nrep_as - nrep_as * 68d0 / 1d2) )
      iaver_68  = int(nrep_as/2d0)
      write(*,*) avg,sig2," +",nlo_as(iplus_68)-nlo_as(iaver_68), 
     $     "-",nlo_as(iaver_68)-nlo_as(iminus_68)
      write(*,*) avg," +",nlo_up-avg," -",avg-nlo_down
      PDFasERR = dsqrt((nlo_up-avg)**2+pdfERR**2)
      write(*,*) "----> ",avg," +/- ",pdfasERR
      stop
      end
 
ccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE sort_100(A)
      IMPLICIT none

      integer N
      parameter (N=100)
      integer I,J
      double precision A(N),X
      
      do 30 I = 2,N
         X=A(I)
         J=I
 10      J=J-1
         IF(J.EQ.0 .OR.A(J).LE.X) GO TO 20
         A(J+1)=A(J)
         GO TO 10
 20      A(J+1)=X
 30   CONTINUE
      END
ccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE sort_300(A)
      IMPLICIT none

      integer N
      parameter (N=300)
      integer I,J
      double precision A(N),X
      
      do 30 I = 2,N
         X=A(I)
         J=I
 10      J=J-1
         IF(J.EQ.0 .OR.A(J).LE.X) GO TO 20
         A(J+1)=A(J)
         GO TO 10
 20      A(J+1)=X
 30   CONTINUE
      END
