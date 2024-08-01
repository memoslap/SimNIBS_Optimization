#!/usr/bin/bash

#subjs=("006" "008" "009" "012" "013" "016" "017" "018" "020" "024" "025" "027" "028" "029" "030" "032" "033" "034" "035" "062" "064")
#subjs=("066" "072" "074" "079" "080" "081" "086" "089" "091" "095" "097" "098" "105" "106" "994" "995" "996" "997" "998" "999")
subjs=("001" "003" "004")

root_dir=/media/data03/hayekd/Memoslap/Sample1/01-charm_new
echo $root_dir
for subj in "${subjs[@]}"
do
    echo "$subj"
    t1_file="$root_dir"/"$subj"/T1w.nii
    echo "$t1_file"
    t2_file="$root_dir"/"$subj"/T2w.nii
    echo "$t2_file"  
    cd "$root_dir"/"$subj"  
    charm $subj $t1_file $t2_file --forcerun --forceqform
done
