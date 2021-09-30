for EXP in all sk sm km
do
    for TYPE in source hard soft75 soft5 soft25 soft1 soft0
    do
        rosrun extended_object_detection offline_image ../share/PC.jpg ../config/$EXP-$TYPE.xml ../share/$EXP-$TYPE.png 
    done
done
