program main
implicit none
  integer i,j,k,n_au,n_s,n_c,n_h
  parameter(n_au=49,n_s=2,n_c=4,n_h=10)
  integer n1, n2, n3
  real*8 x,y,z,lenx,leny,lenz
  parameter(lenx=8.6974000000,leny=10.0429000000,lenz=25.0000000)
  character cha*14
  character*8 c1,c2,c3

  write(*,11)
11 format(/,'Enter the PDB file:',$)
  read(*,*) cha
  open(1,file=cha)
 
  open(2,file='POSCAR')

  read(1,*)
  
  write(2,"(a7)") 'Comment'
  write(2,"(f18.14)") 1.000000
  write(2,"(f20.16,2f20.16)") lenx,0.00,0.00
  write(2,"(f20.16,2f20.16)") 0.00,leny,0.00
  write(2,"(f20.16,2f20.16)") 0.00,0.00,lenz
  write(2,"(4a4)") 'Au','S','C','H'
  write(2,"(4i4)") 49,2,4,10
  write(2,"(2a18)") 'Selective dynamics'
  write(2,"(a6)") 'Direct'

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!! For Au atoms !!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  do i = 1, n_au

     read(1,*) c1,n1,c2,n2,x,y,z

     write(2,99) x/lenx,y/leny,z/lenz,'F','F','F'

  enddo

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!! For S atoms !!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  read(1,*) c1,n1,c2,n2,x,y,z 
  write(2,99) x/lenx,y/leny,z/lenz,'T','T','T'
  read(1,*) c1,n1,c2,n2,x,y,z
  write(2,99) x/lenx,y/leny,z/lenz,'F','F','F'
  
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!! For Four C atoms !!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 
  read(1,*) c1,n1,c2,n2,x,y,z
  write(2,99) x/lenx,y/leny,z/lenz,'T','T','T'
  read(1,*) c1,n1,c2,n2,x,y,z
  write(2,99) x/lenx,y/leny,z/lenz,'T','T','T'

  read(1,*) c1,n1,c2,n2,x,y,z
  write(2,99) x/lenx,y/leny,z/lenz,'F','F','F'
  read(1,*) c1,n1,c2,n2,x,y,z
  write(2,99) x/lenx,y/leny,z/lenz,'F','F','F'

  do i = 1, n_h

     read(1,*) c1,n1,c2,n2,x,y,z
     write(2,99) x/lenx,y/leny,z/lenz,'T','T','T'
 
  enddo

99 format(3f20.16,4a4)

end
