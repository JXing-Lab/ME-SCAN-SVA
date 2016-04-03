#!/bin/sh

MEI=$1
option_tag=$2
bottom_sensitivity=$3
window_size=$4
primer_position=$5
interval=$6

path_current=$(pwd)"/"
path_ref_mescan_customized=$path_current"ref_mescan_customized"$option_tag"/" 
path_Results=$path_current"Results"$option_tag"/"
path_output=$path_current"output_bwa-blast"$option_tag"/"

libraries=$(ls|grep Sample|awk -F _ '{ print $2 }')
arr_lib=($libraries)
set $libraries
number_lib=$(echo $#)   

file_Sensitivity=$path_Results"sensitivity_stuff/"$MEI$option_tag"BB.sensi_all"
file_Depth=$path_Results"sensitivity_stuff/"$MEI$option_tag"BB.depth_all"
file_TPM=$path_Results"sensitivity_stuff/"$MEI$option_tag"BB.tpm_all"

max_depth=$(cat $path_output$MEI"_all"$option_tag"BB.bed"|awk '{print $4}'|awk '{for(x=1;x<=NF;x++)a[++y]=$x}END{c=asort(a);print a[c]}')
mapped_reads=0
for i in $(seq $number_lib)
    do

    each_lib=${arr_lib[$i-1]}
    read2=$(ls $path_current"Sample_"$each_lib"/"*.fastq|grep -E "$each_lib.*fastq"|grep R2|awk -F"." '{print $1}')
    cmd_mapped_reads=$path_samtools"samtools idxstats "$read2"_BB_sorted.bam|awk ' {sum+=\$3} END {print sum}'"

    mapped_reads=$(echo $mapped_reads+$(eval $cmd_mapped_reads)|bc)
    done

    if [[ $primer_position == 5 ]] ; then
        echo "primer binding position is at the 5'end of "$MEI".."

    elif [[ $primer_position == 3 ]] ; then
        echo "primer binding position is at the 3'end of "$MEI".."
    fi

for depth_cutoff in $(seq 1 $interval $max_depth)

    do

    if [[ $primer_position == 5 ]] ; then
        cmd_TP="windowBed -a "$path_output$MEI"_all"$option_tag"BB.bed -b "$path_ref_mescan_customized"Fixed_Reference."$MEI$option_tag"bed -w "$window_size"|awk '\$4>="$depth_cutoff"'|awk '\$7~\"plus\" && \$16==\"+\" || \$7~\"minus\" && \$16==\"C\" {print \$8,\$9,\$10}'|uniq|wc -l"
        cmd_FNp="awk '\$4 >="$depth_cutoff"' "$path_output$MEI"_all"$option_tag"BB.bed|awk '\$7~\"plus\"'|windowBed -a "$path_ref_mescan_customized"Fixed_Reference."$MEI$option_tag"bed -b stdin -w "$window_size" -v|awk '\$9==\"+\"'|wc -l"
        cmd_FNm="awk '\$4 >="$depth_cutoff"' "$path_output$MEI"_all"$option_tag"BB.bed|awk '\$7~\"minus\"'|windowBed -a "$path_ref_mescan_customized"Fixed_Reference."$MEI$option_tag"bed -b stdin -w "$window_size" -v|awk '\$9==\"C\"'|wc -l"
        cmd_FN=$(echo $(eval $cmd_FNp)+$(eval $cmd_FNm)|bc -l)        


    elif [[ $primer_position == 3 ]] ; then
        cmd_TP="windowBed -a "$path_output$MEI"_all"$option_tag"BB.bed -b "$path_ref_mescan_customized"Fixed_Reference."$MEI$option_tag"bed -w "$window_size"|awk '\$4>="$depth_cutoff"'|awk '\$7~\"plus\" && \$16==\"C\" || \$7~\"minus\" && \$16==\"+\"' {print \$8,\$9,\$10}'|uniq|wc -l"
        cmd_FNp="awk '\$4 >="$depth_cutoff"' "$path_output$MEI"_all"$option_tag"BB.bed|awk '\$7~\"plus\"'|windowBed -a "$path_ref_mescan_customized"Fixed_Reference."$MEI$option_tag"bed -b stdin -w "$window_size" -v|awk '\$9==\"C\"'|wc -l"
        cmd_FNm="awk '\$4 >="$depth_cutoff"' "$path_output$MEI"_all"$option_tag"BB.bed|awk '\$7~\"minus\"'|windowBed -a "$path_ref_mescan_customized"Fixed_Reference."$MEI$option_tag"bed -b stdin -w "$window_size" -v|awk '\$9==\"+\"'|wc -l"
        cmd_FN=$(echo $(eval $cmd_FNp)+$(eval $cmd_FNm)|bc -l) 

    fi

    pre_condition=$(echo $(eval $cmd_TP)/$(echo $(eval $cmd_TP)+$cmd_FN|bc -l)|bc -l)*100
    condition=$(echo $pre_condition/1|bc)

    ## Sensitivity
    echo $(eval $cmd_TP)/$(echo $(eval $cmd_TP)+$cmd_FN|bc -l)|bc -l >> $file_Sensitivity
    echo $depth_cutoff >> $file_Depth
    echo $depth_cutoff*1000000/$mapped_reads|bc -l >> $file_TPM

    if [[ $condition -le $bottom_sensitivity ]] ;then
    break
    fi
    done
