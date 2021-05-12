program main
implicit none
  integer i,j,k,n_atom
  parameter(n_atom=65)
  integer n1, n2, n3
  real*8 x(n_atom),y(n_atom),z(n_atom),d
  real*8 a1,a2,a3,b1,b2,b3,c1,c2,c3
  character cha1*68

  open(1,file='CONTCAR')
  open(2,file='staple_60.xyz')

  read(1,*)
  read(1,*)

  read(1,*) a1,a2,a3
  read(1,*) b1,b2,b3
  read(1,*) c1,c2,c3

  do i = 1, 4

     read(1,*)

  enddo

  do i = 1, 65

     read(1,*) x(i),y(i),z(i)

  enddo

  write(2,"(i6)") n_atom

  do i = 1, 49

     if(i==40) then

       write(2,99) i,'Au',x(i)*a1,y(i)*b2,z(i)*c3,2,51

     elseif(i==49) then

       write(2,98) i,'Au',x(i)*a1,y(i)*b2,z(i)*c3,3,50,51

     elseif(i==46) then

       write(2,99) i,'Au',x(i)*a1,y(i)*b2,z(i)*c3,2,50

     else

      if(z(i)>0.99) then

         d = 1.0 - z(i)
         write(2,97) i,'Au',x(i)*a1,y(i)*b2,d*c3,1

       else

         d = z(i)
         write(2,97) i,'Au',x(i)*a1,y(i)*b2,d*c3,1

       endif

     endif
            
  enddo

99 format(i6,2x,a2,1x,3f12.6,2i6)
98 format(i6,2x,a2,1x,3f12.6,3i6)
97 format(i6,2x,a2,1x,3f12.6,i6)
  
   write(2,96) 50,'S',x(50)*a1,y(50)*b2,z(50)*c3,4,46,49,52

   write(2,96) 51,'S',x(51)*a1,y(51)*b2,z(51)*c3,4,40,49,54

96 format(i6,2x,a2,1x,3f12.6,4i6)
   
   write(2,95) 52,'C',x(52)*a1,y(52)*b2,z(52)*c3,5,50,53,56,57

   write(2,95) 53,'C',x(53)*a1,y(53)*b2,z(53)*c3,6,52,58,59,60

   write(2,95) 54,'C',x(54)*a1,y(54)*b2,z(54)*c3,5,51,55,61,62

   write(2,95) 55,'C',x(55)*a1,y(55)*b2,z(55)*c3,6,54,63,64,65

95 format(i6,2x,a2,1x,3f12.6,5i6)

  do i = 56,60

     if(i<=57) then

        write(2,99) i,'H',x(i)*a1,y(i)*b2,z(i)*c3,7,52

     else

        write(2,99) i,'H',x(i)*a1,y(i)*b2,z(i)*c3,7,53

     endif

  enddo

  do i = 61, 65

     if(i<=62) then

        write(2,99) i,'H',x(i)*a1,y(i)*b2,z(i)*c3,7,54

     else

        write(2,99) i,'H',x(i)*a1,y(i)*b2,z(i)*c3,7,55

     endif

  enddo

  end
