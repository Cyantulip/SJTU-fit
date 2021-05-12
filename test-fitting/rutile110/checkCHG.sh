#!/bin/bash
#by lingci 2021/03/24

a=$1
#file1=$2
#file2=$3

#awk -v b=$a '{if(NF==9 && $3==10){$4=1.524*b; print} else if(NF==9 && $3==7){$4=-0.657*b; print} else if(NF==9 && $3==9){$4=-0.867*b; print} else if(NF==9 && $3==11){$4=1.734*b; print} else print}' $file1 > $file2;
awk -v c=$a '{if(NF==9 && $3==3){$4=1.524*c; print} else if(NF==9 && $3==1){$4=-0.657*c; print} else if(NF==9 && $3==2){$4=-0.867*c; print} else if(NF==9 && $3==4){$4=1.734*c; print} else print}' rutile110.data > rut-slabC.data

#for i in `seq 1 1 14`
#do
#awk -v b=$a '{if(NF==9 && $3==10){$4=1.524*b; print} else if(NF==9 && $3==7){$4=-0.657*b; print} else if(NF==9 && $3==9){$4=-0.867*b; print} else if(NF==9 && $3==11){$4=1.734*b; print} else print}' out$i.data > paa-$i.data;
#awk -v c=$a '{if(NF==9 && $3==3){$4=1.524*c; print} else if(NF==9 && $3==1){$4=-0.657*c; print} else if(NF==9 && $3==2){$4=-0.867*c; print} else if(NF==9 && $3==4){$4=1.734*c; print} else print}' rutile.data > rut-slabC.data

awk 'NF==9{sum += $4;x +=1}END{print sum,x}' rut-slabC.data;
#awk 'NF==9{sum += $4;x +=1}END{print sum,x}' paa-$i.data;
#done
