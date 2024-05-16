# -*- coding: utf-8 -*-

"""
Author: Zhou Zhi-Jian
Time: 2023/12/16 12:54

"""
import os
import subprocess
import time

from my_func import (my_mkdir,seq_filter,fq_to_fas,fq_to_fas_re,
                     reads_diamond_class,get_name,
                     contig_diamond_class)



def runprocess(input_command):

    process = subprocess.Popen(input_command, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True, shell=True)

    while True:

        output = process.stdout.readline()
        if process.poll() is not None:
            break

        elif output:
            print(output)

    process.terminate()




def clean_reads (parameter_dic,xml_dic,out_dir):
    """
    clean the input reads
    :param parameter_dic:
    :param xml_dic:
    :param out_dir:
    :return:
    """

    clean_data1_path = ""

    clean_data2_path = ""

    run_thread = parameter_dic["thread"]

    host_index_path = " ".join(xml_dic["hostdb"]).strip()


    # Step 1. remove contamination from adapter primer

    print(">>> " + "remove contamination from adapter primer..." + "\n")

    trimmed_outdir = out_dir + "/1_trimmed"

    my_mkdir(trimmed_outdir)

    trimmed_command_list = []


    trimmed_command_list.append("trimmomatic")  # trimmomatic exe

    trimmed_command_list.append("PE "
                                + "-" + parameter_dic["qualities"] + " "
                                + "-threads " + run_thread + " "
                                + parameter_dic["forward_reads"] + " "
                                + parameter_dic["reverse_reads"])

    trimmed_command_list.append(trimmed_outdir + "/trimmed-1P.fq" + " "
                                + trimmed_outdir + "/trimmed-1U.fq" + " "
                                + trimmed_outdir + "/trimmed-2P.fq" + " "
                                + trimmed_outdir + "/trimmed-2U.fq")

    trimmed_command_list.append(" ".join(xml_dic["trimmomatic"]))


    trimmed_command = " ".join(trimmed_command_list)

    print(trimmed_command)

    runprocess(trimmed_command)


    # Step 2. remove contamination of host (by bowtie2)

    print(">>> " + "remove contamination from host genome..." + "\n")

    bowtie_outdir = out_dir + "/2_bowtie"

    my_mkdir(bowtie_outdir)


    print("all host database: ", host_index_path)


    if host_index_path.find(",") == -1:  # only one host database

        print("find only one host database." + "\n")

        bowtie_command_list = []


        bowtie_command_list.append("bowtie2")


        bowtie_command_list.append(" ".join(xml_dic["bowtie2"]).strip())

        bowtie_command_list.append("-p " + run_thread + " "
                                   + "-x " + host_index_path + " "
                                   + "-1 " + trimmed_outdir + "/trimmed-1P.fq" + " "
                                   + "-2 " + trimmed_outdir + "/trimmed-2P.fq" + " "
                                   + "--" + parameter_dic["qualities"] + " "
                                   + "-S " +  bowtie_outdir + "/out.sam" + " "
                                   + "--un-conc " + bowtie_outdir + "/unmatch.fq")

        bowtie_command = " ".join(bowtie_command_list)

        print("remove contamination from the host: ",
              host_index_path + "\n")

        print(bowtie_command)

        runprocess(bowtie_command)


        clean_data1_path = bowtie_outdir + "/unmatch.1.fq"
        clean_data2_path = bowtie_outdir + "/unmatch.2.fq"


    else: # over one host database

        host_path_list = host_index_path.split(",")

        print("find multiple host databases." + "\n")


        for i in range(0,len(host_path_list)):

            host_path = host_path_list[i].strip()

            print("remove contamination from the host " + str(i + 1) + ": ",
                  host_path + "\n")

            bowtie_command_list = []

            bowtie_command_list.append("bowtie2")


            bowtie_command_list.append(" ".join(xml_dic["bowtie2"]).strip())

            sub_outdir = bowtie_outdir + "/host_" + str(i + 1) + "_out"

            my_mkdir(sub_outdir)

            if i == 0:

                input_data_dir = trimmed_outdir


                bowtie_command_list.append("-p " + run_thread + " "
                                           + "-x " + host_path + " "
                                           + "-1 " + input_data_dir + "/trimmed-1P.fq" + " "
                                           + "-2 " + input_data_dir + "/trimmed-2P.fq" + " "
                                           + "--" + parameter_dic["qualities"] + " "
                                           + "-S " + sub_outdir + "/out.sam" + " "
                                           + "--un-conc " + sub_outdir + "/unmatch.fq")

            else:

                input_data_dir = bowtie_outdir + "/host_" + str(i) + "_out"

                bowtie_command_list.append("-p " + run_thread + " "
                                           + "-x " + host_path + " "
                                           + "-1 " + input_data_dir + "/unmatch.1.fq" + " "
                                           + "-2 " + input_data_dir + "/unmatch.2.fq" + " "
                                           + "--" + parameter_dic["qualities"] + " "
                                           + "-S " + sub_outdir + "/out.sam" + " "
                                           + "--un-conc " + sub_outdir + "/unmatch.fq")


            bowtie_command = " ".join(bowtie_command_list)

            print(bowtie_command)

            runprocess(bowtie_command)

            clean_data1_path = sub_outdir + "/unmatch.1.fq"
            clean_data2_path = sub_outdir + "/unmatch.2.fq"



    print(">>> " + "clean contamination of adapter primer and host: completed!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))




    return clean_data1_path,clean_data2_path



def sub_run1(parameter_dic,xml_dic,clean_data1_path,clean_data2_path):

    """
    the sub-pipeline of nextvirus, reads → viral nr
    :param parameter_dic:
    :param xml_dic:
    :param clean_data1_path: fq format of cleaned forward reads
    :param clean_data2_path: fq format of cleaned reverse reads
    :return:
    """
    out_dir = parameter_dic["outdir"] + "/pipeline1"

    # Step 3. fastq to fasta

    fq1_file_name = get_name(parameter_dic["forward_reads"])
    fq2_file_name = get_name(parameter_dic["reverse_reads"])


    fas_path = out_dir + "/3_fastq_to_fasta"

    my_mkdir(fas_path)

    clean_data1_fas = fas_path + "/" + fq1_file_name + "_cleaned.fasta"
    clean_data2_fas = fas_path + "/" + fq2_file_name + "_cleaned.fasta"



    fq_to_fas_re(clean_data1_path,
                 clean_data1_fas)   # unmatch.1.fq to clean_data1_fas

    fq_to_fas_re(clean_data2_path,
                 clean_data2_fas)   # unmatch.2.fq to clean_data2_fas



    print(">>> " + "the sequence format conversion: completed!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

    print("\n")


    print(">>> " + "running the sub-pipeline 1..." + "\n")



    refer_spiece_path = " ".join(xml_dic["viral_taxonomy"]).strip()

    viral_nr_path = " ".join(xml_dic["viral_nr"]).strip()

    run_thread = parameter_dic["thread"]

    fq1_file_name = get_name(parameter_dic["forward_reads"])
    fq2_file_name = get_name(parameter_dic["reverse_reads"])


    # Step 4. run diamond

    print(">>> " + "running diamond..." + "\n")

    diamond_outdir = out_dir + "/4_diamond"
    my_mkdir(diamond_outdir)


    diamond_result1 = diamond_outdir + "/" + fq1_file_name + "_result.txt"
    diamond_result2 = diamond_outdir + "/" + fq2_file_name + "_result.txt"

    diamond_commond_list1 = []
    diamond_commond_list1.append("diamond blastx "
                                + " ".join(xml_dic["diamond"]))

    diamond_commond_list1.append("-q " + clean_data1_fas)
    diamond_commond_list1.append("--db " + viral_nr_path)
    diamond_commond_list1.append("-e 1 " + "-p " + run_thread)
    diamond_commond_list1.append("-o " + diamond_result1)

    diamond_commond_list1.append(
        "--outfmt 6 qseqid sseqid stitle bitscore pident nident evalue gaps length qstart qend sstart send") # don't change --outfmt

    diamond_commond_list2 = []

    diamond_commond_list2.append("diamond blastx "
                                + " ".join(xml_dic["diamond"]))

    diamond_commond_list2.append("-q " + clean_data2_fas)

    diamond_commond_list2.append("--db " + viral_nr_path)

    diamond_commond_list2.append("-e 1 " + "-p " + run_thread)

    diamond_commond_list2.append("-o " + diamond_result2)

    diamond_commond_list2.append(
        "--outfmt 6 qseqid sseqid stitle bitscore pident nident evalue gaps length qstart qend sstart send")  # don't change --outfmt

    diamond_commond1 = " ".join(diamond_commond_list1)
    diamond_commond2 = " ".join(diamond_commond_list2)


    diamond_commond = diamond_commond1 + ";" + diamond_commond2

    print(diamond_commond)

    runprocess(diamond_commond)


    print(">>> " + "reads map to viral nr: completed!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

    print("\n")


    # Step 5. filter the results from dimond

    reads_filter_dir = out_dir + r"/5_finally_result"
    my_mkdir(reads_filter_dir)


    # 1st e-Value filtering of reads

    with open(diamond_result1, "r", encoding="utf-8") as inputs:
        diamond_result_list1 = inputs.readlines()

    with open(diamond_result2, "r", encoding="utf-8") as inputs:
        diamond_result_list2 = inputs.readlines()

    e_value_list = [float(i) for i in parameter_dic["e-value"]]

    e_value_list.sort()  # sort

    diamond_result_lists_1 = diamond_result_list1 + diamond_result_list2

    reads_filter_dir1 = reads_filter_dir + "/lower_" + str(e_value_list[0])
    my_mkdir(reads_filter_dir1)

    selected_file1 = reads_filter_dir1 + "/meets_the_conditions_"+ str(e_value_list[0]) +".txt"

    unselected_file1 = reads_filter_dir1 + "/not_meets_conditions.txt"




    seq_filter(diamond_result_lists_1, selected_file1, unselected_file1,
               parameter_dic["length_threshold"], parameter_dic["identity_threshold"],
               e_value_list[0])

    print(">>> " + "1st e-value(" + str(e_value_list[0]) + ") filtering of reads: completed!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))



    reads_diamond_class(clean_data1_fas,
                        clean_data2_fas,
                        selected_file1,
                        refer_spiece_path,
                        reads_filter_dir1)

    print(">>> " + "1st classification of reads: done!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

    print("\n")

    # 2nd e-value filtering of reads
    with open(unselected_file1, "r", encoding="utf-8") as inputs:
        diamond_result_lists_2 = inputs.readlines()

    reads_filter_dir2 = reads_filter_dir + "/lower_" + str(e_value_list[1])
    my_mkdir(reads_filter_dir2)

    selected_file2 = reads_filter_dir2 + "/meets_the_conditions_"+ str(e_value_list[1]) +".txt"

    unselected_file2 = reads_filter_dir2 + "/not_meets_conditions.txt"

    seq_filter(diamond_result_lists_2, selected_file2, unselected_file2,
               parameter_dic["length_threshold"], parameter_dic["identity_threshold"],
               e_value_list[1])

    print(">>> " + "2nd e-value(" + str(e_value_list[1]) + ") filtering of reads: completed!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))


    reads_diamond_class(clean_data1_fas,
                        clean_data2_fas,
                        selected_file2,
                        refer_spiece_path,
                        reads_filter_dir2)

    print(">>> " + "2nd classification of reads: done!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

    print("\n")

    ## 3rd e-value filtering of reads

    with open(unselected_file2, "r", encoding="utf-8") as inputs:
        diamond_result_lists_3 = inputs.readlines()

    reads_filter_dir3 = reads_filter_dir + "/lower_" + str(e_value_list[2])
    my_mkdir(reads_filter_dir3)

    selected_file3 = reads_filter_dir3 + "/meets_the_conditions_"+ str(e_value_list[2]) +".txt"

    unselected_file3 = reads_filter_dir3 + "/not_meets_conditions.txt"

    seq_filter(diamond_result_lists_3, selected_file3, unselected_file3,
               parameter_dic["length_threshold"], parameter_dic["identity_threshold"],
               e_value_list[2])

    print(">>> " + "3rd e-value(" + str(e_value_list[2]) + ") filtering of reads: completed",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))


    reads_diamond_class(clean_data1_fas,
                        clean_data2_fas,
                        selected_file3,
                        refer_spiece_path,
                        reads_filter_dir3)

    print(">>> " + "3rd classification of reads: done!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

    print("\n")


    return




def sub_run2(parameter_dic,xml_dic,clean_data1_path,clean_data2_path):
    """
    the sub-pipeline of nextvirus, reads → contigs → viral nr
    :param parameter_dic:
    :param xml_dic:
    :param clean_data1_path: fq format of cleaned forward reads
    :param clean_data2_path: fq format of cleaned reverse reads
    :return:
    """

    out_dir = parameter_dic["outdir"] + "/pipeline2"

    fas_path = out_dir + "/3_fastq_to_fasta"

    # Step 3. fastq to fasta

    fq1_file_name = get_name(parameter_dic["forward_reads"])
    fq2_file_name = get_name(parameter_dic["reverse_reads"])


    my_mkdir(fas_path)

    clean_data1_fas = fas_path + "/" + fq1_file_name + "_cleaned.fasta"
    clean_data2_fas = fas_path + "/" + fq2_file_name + "_cleaned.fasta"

    fq_to_fas(clean_data1_path,
                 clean_data1_fas)  # unmatch.1.fq to clean_data1_fas

    fq_to_fas(clean_data2_path,
                 clean_data2_fas)  # unmatch.2.fq to clean_data2_fas


    print(">>> " + "running the sub-pipeline 2..." + "\n")



    refer_spiece_path = " ".join(xml_dic["viral_taxonomy"]).strip()

    viral_nr_path = " ".join(xml_dic["viral_nr"]).strip()

    run_thread = parameter_dic["thread"]


    # Step 4. splice reads as contigs

    trinity_out_dir = out_dir + "/4_trinity_out"
    my_mkdir(trinity_out_dir)

    os.chdir(trinity_out_dir)


    trinity_command = ("Trinity" + " "
                       + "--seqType fa" + " "
                       + " ".join(xml_dic["Trinity"]) + " "
                       + "--left " + clean_data1_fas + " "
                       + "--right " + clean_data2_fas + " "
                       + "--CPU " + run_thread + " "
                       + "--output trinity_out")


    # tip：the outfile of Trinity is trinity_out.Trinity.fasta, saved in trinity_out_dir

    # out_dir + "/3_trinity_out/trinity_out.Trinity.fasta"

    print(trinity_command)
    runprocess(trinity_command)


    # Step 5. run diamond

    print(">>> " + "running diamond..." + "\n")

    trinity_out_seq = out_dir + "/4_trinity_out/trinity_out.Trinity.fasta"

    diamond_outdir = out_dir + "/5_diamond"
    my_mkdir(diamond_outdir)

    diamond_result = diamond_outdir + "/trinity_out_diamond_result.txt"

    diamond_commond_list = []

    diamond_commond_list.append("diamond blastx "
                                 + " ".join(xml_dic["diamond"]))

    diamond_commond_list.append("-q " + trinity_out_seq)
    diamond_commond_list.append("--db " + viral_nr_path)
    diamond_commond_list.append("-o " + diamond_result)
    diamond_commond_list.append("-e 1 " + "-p " + run_thread)

    diamond_commond_list.append("--outfmt 6 qseqid sseqid stitle bitscore pident nident evalue gaps length qstart qend sstart send") # don't change --outfmt


    diamond_commond = " ".join(diamond_commond_list)

    print(diamond_commond)
    runprocess(diamond_commond)


    print(">>> " + "contigs map to viral nr: completed!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

    print("\n")


    # Step 6. filter the results from dimond

    contig_filter_dir = out_dir + r"/6_finally_result"

    my_mkdir(contig_filter_dir)


    # 1st e-value filtering of contigs

    with open(diamond_result, "r", encoding="utf-8") as inputs:
        diamond_result_lists_1 = inputs.readlines()

    e_value_list = [float(i) for i in parameter_dic["e-value"]]

    e_value_list.sort()  # sort

    contig_filter_dir1 = contig_filter_dir + "/lower_" + str(e_value_list[0])

    my_mkdir(contig_filter_dir1)

    selected_file1 = contig_filter_dir1 + "/meets_the_conditions_"+ str(e_value_list[0]) +".txt"

    unselected_file1 = contig_filter_dir1 + "/not_meets_conditions.txt"


    # print(e_value_list[0])
    #
    # print(e_value_list[1])
    #
    # print(e_value_list[2])


    seq_filter(diamond_result_lists_1,
               selected_file1,
               unselected_file1,
               parameter_dic["length_threshold"], parameter_dic["identity_threshold"], e_value_list[0])

    print(">>> " + "1st e-value(" + str(e_value_list[0]) + ") filtering of contigs: completed!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))



    contig_diamond_class(trinity_out_seq,
                         selected_file1,
                         refer_spiece_path,
                         contig_filter_dir1)

    print(">>> " + "1st classification of contigs: done!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

    print("\n")


    # 2nd e-value filtering of contigs
    with open(unselected_file1, "r", encoding="utf-8") as inputs:
        diamond_result_lists_2 = inputs.readlines()

    contig_filter_dir2 = contig_filter_dir + "/lower_" + str(e_value_list[1])

    my_mkdir(contig_filter_dir2)

    selected_file2 = contig_filter_dir2 + "/meets_the_conditions_"+ str(e_value_list[1]) +".txt"

    unselected_file2 = contig_filter_dir2 + "/not_meets_conditions.txt"

    seq_filter(diamond_result_lists_2,
               selected_file2,
               unselected_file2,
               parameter_dic["length_threshold"], parameter_dic["identity_threshold"],
               e_value_list[1])

    print(">>> " + "2nd e-value(" + str(e_value_list[1]) + ") filtering of contigs: completed!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))


    contig_diamond_class(trinity_out_seq,
                         selected_file2,
                         refer_spiece_path,
                         contig_filter_dir2)

    print(">>> " + "2nd classification of contigs: done!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

    print("\n")


    # 3rd e-value filtering of contigs

    with open(unselected_file2, "r", encoding="utf-8") as inputs:
        diamond_result_lists_3 = inputs.readlines()

    contig_filter_dir3 = contig_filter_dir + "/lower_" + str(e_value_list[2])

    my_mkdir(contig_filter_dir3)

    selected_file3 = contig_filter_dir3 + "/meets_the_conditions_"+ str(e_value_list[2]) +".txt"

    unselected_file3 = contig_filter_dir3 + "/not_meets_conditions.txt"

    seq_filter(diamond_result_lists_3, selected_file3, unselected_file3,
               parameter_dic["length_threshold"], parameter_dic["identity_threshold"],
               e_value_list[2])

    print(">>> " + "3rd e-value(" + str(e_value_list[2]) + ") filtering of contigs: completed!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))


    contig_diamond_class(trinity_out_seq,
                         selected_file3,
                         refer_spiece_path,
                         contig_filter_dir3)

    print(">>> " + "3rd classification of contigs: done!",
          time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

    print("\n")


    return

