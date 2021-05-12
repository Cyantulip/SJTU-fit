program main
implicit none
integer i,j,k,n_atom,nargs,n_type
integer eleNum1,eleNum2
parameter(n_atom=144)
parameter(n_type=5)
!integer n1,n2,n3
real*8 xd(n_atom),yd(n_atom),zd(n_atom),chg(n_atom)
real*8 sf,c,Csf
real*8 a1,a2,a3,b1,b2,b3,c1,c2,c3
character*20 ele1,ele2,ele(n_atom),tmp(5,2)
character*79 filename,atomtype,contcar,charges,output,arg

        nargs=iargc()
        if(nargs==5)then
                call getarg(1,atomtype)
                call getarg(2,contcar)
                call getarg(3,charges)
                call getarg(4,output)
                call getarg(5,arg)
                read(arg,"(f10.7)") Csf
        else
                write(*,*) "Wrong Input!"
                write(*,*) "#Usage: ./xx.x atomtype contcar charges output CHGsf"
                write(*,*) "#Usage: ./xx.x atomtype-zro2.dat POSCAR sBADER9.dat output"
                write(*,*) "#Usage: ./xx.x atomtype-zro2.dat POSCAR atomcharge-zro2.dat output 0.75"
                goto 1000
        endif

open(10,file=contcar,status="old")
open(20,file=output,status="replace")
open(30,file=atomtype,status="old")
open(40,file=charges,status="old")

        read(10,*)
        read(10,*) sf
        read(10,*) a1,a2,a3
        read(10,*) b1,b2,b3
        read(10,*) c1,c2,c3
        read(10,*) ele1,ele2
        read(10,*) eleNum1,eleNum2

        do i = 1,2
                read(10,*)
        enddo

        do i=1,n_atom
                read(10,*) xd(i),yd(i),zd(i)
        enddo

        do i=1,n_atom
                read(30,*) ele(i)
        enddo

        !do i=1,n_atom
        !        read(40,*) chg(i)
        !enddo
        do i =1,n_type
                read(40,*)(tmp(i,j),j=1,2)
        enddo

!do i=1,n_type
!write(*,*) tmp(i,1),tmp(i,2)
!enddo




999 format(a4,2x,3f12.6,3x,f10.6)

        write(20,"(a9)") "Cartesian"

        do i =1,n_atom
                !!if(i<=eleNum1)then
                !!write(20,999)ele1,xd(i)*a1+yd(i)*b1+zd(i)*c1,xd(i)*a2+yd(i)*b2+zd(i)*c2,xd(i)*a3+yd(i)*b3+zd(i)*c3,1.000
                !write(20,999)ele(i),xd(i)*a1+yd(i)*b1+zd(i)*c1,xd(i)*a2+yd(i)*b2+zd(i)*c2,xd(i)*a3+yd(i)*b3+zd(i)*c3,chg(i)
                do j =1,n_type
                        if(tmp(j,1)==ele(i))then
                        read(tmp(j,2),"(f10.7)") c
                        endif
                enddo
                        write(20,999)ele(i),xd(i)*a1+yd(i)*b1+zd(i)*c1,xd(i)*a2+yd(i)*b2+zd(i)*c2,xd(i)*a3+yd(i)*b3+zd(i)*c3,Csf*c
                !!else
                !!write(20,999)ele2,xd(i)*a1+yd(i)*b1+zd(i)*c1,xd(i)*a2+yd(i)*b2+zd(i)*c2,xd(i)*a3+yd(i)*b3+zd(i)*c3,1.000
                !!endif
        enddo
close(10)
close(20)
close(30)
close(40)
1000 end program
