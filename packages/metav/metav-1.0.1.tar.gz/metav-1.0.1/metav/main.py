# -*- coding: utf-8 -*-

"""
Metagenomics virus detection (MetaV)
Author: Zhou Zhi-Jian
Time: 2023/12/16 ‏‎13:05

"""
import sys

import time
import argparse

from datetime import datetime

from my_func import parse_xml,my_mkdir

import pecorec

import secorec




example_use = r'''
----------------☆ Example of use ☆-----------------
 
  (i) if paired-end sequencing:
  metav -pe -i1 reads_R1.fq -i2 reads_R2.fq -xml profiles.xml -r1 -r2 -t 8 -o outdir
  
  
  (ii) if single-end sequencing:
  metav -se -u reads.fq -xml profiles.xml -r1 -r2 -t 8 -o outdir
  
----------------------☆  End  ☆---------------------

'''



def parameter():
      parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog="metav",
            description="",
            epilog=example_use)

      parser.add_argument(
            "-pe",dest="pair_end",
            action="store_true",
            help="paired-end sequencing.")

      parser.add_argument(
            "-se",dest="single_end",
            action="store_true",
            help="single-end sequencing.")

      parser.add_argument(
            "-i1", dest="forward",
            help="forward reads (*.fq) using paired-end sequencing.",
            type=str,
            default="None")

      parser.add_argument(
            "-i2", dest="reverse",
            help="reverse reads (*.fq) using paired-end sequencing.",
            type=str,
            default="None")

      parser.add_argument(
            "-u", dest="unpaired",
            help="reads file using single-end sequencing (unpaired reads).",
            type=str,
            default="None")

      parser.add_argument(
            "-q", dest="qualities",
            help="the qualities (phred33 or phred64) of sequenced reads, default: phred33.",
            type=str,
            default="phred33")


      parser.add_argument(
            "-xml", dest="profiles",
            help="the *.xml file with parameters of dependent software and databases.",
            default="")

      parser.add_argument(
            "-len", dest="length",
            help="threshold of length of aa alignment in diamond, default: 10.",
            type=float,
            default=10)

      parser.add_argument(
            "-s", dest="identity",
            help="threshold of identity(%%) of alignment aa in diamond, default: 20.",
            type=float,
            default=20)

      parser.add_argument(
            "-e",dest="e_value",
            help="specify three e-values threshold used to filter the reads (or contigs) hit viral nr database, default: 1e-6,1e-3,1e-1.",
            type=str,
            default="1e-6,1e-3,1e-1")


      parser.add_argument(
            "-r1",
            dest="run1",
            action="store_true",
            help="run the sub-pipeline 1 (reads → viral nr).")

      parser.add_argument(
            "-r2",
            action="store_true",
            dest="run2",
            help="run the sub-pipeline 2 (reads → contigs → viral nr).")


      parser.add_argument(
            "-t", dest="thread",
            help="number of used threads, default: 1.",
            type=int,
            default=1)

      parser.add_argument(
            "-o", dest="outdir",
            help="output directory to store all results.",
            type=str,
            default="")

      myargs = parser.parse_args(sys.argv[1:])


      return myargs




def starts():

      print("\n" + "-------------------------------------------------")


      print("  Name: Metagenomics virus detection (MetaV)")


      print(
            "  Description: rapid detection and classification of viruses in metagenomics sequencing.")

      print("  Version: 1.0.1 (2023-12-20)")

      print("  Author: Zhi-Jian Zhou")


      print("-------------------------------------------------" + "\n")


      myargs = parameter()

      print(myargs)

      print("\n")

      print(">>> " + "start time： ",
            time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime(time.time())))

      print("\n")

      start = datetime.today().now()


      parameter_dic = {}

      parameter_dic["pair_end"] = myargs.pair_end

      parameter_dic["single_end"] = myargs.single_end

      parameter_dic["sub-pipeline 1"] = myargs.run1

      parameter_dic["sub-pipeline 2"] = myargs.run2

      parameter_dic["forward_reads"] = myargs.forward.replace("\\", "/")

      parameter_dic["reverse_reads"] = myargs.reverse.replace("\\", "/")

      parameter_dic["unpaired"] = myargs.unpaired

      parameter_dic["qualities"] = myargs.qualities

      parameter_dic["set_file"] = myargs.profiles.replace("\\", "/")

      parameter_dic["length_threshold"] = float(myargs.length)

      parameter_dic["identity_threshold"] = float(myargs.identity)

      parameter_dic["e-value"] = myargs.e_value.split(",")

      parameter_dic["thread"] = str(myargs.thread)

      parameter_dic["outdir"] = myargs.outdir.replace("\\", "/")

      my_mkdir(parameter_dic["outdir"])


      # Save the input parameters locally

      with open(parameter_dic["outdir"] + "/input-parameter.txt",
                "w",encoding="utf-8") as input_para:

            input_para.write("the used parameters of metav in command-line interface."
                             + "\n" *2)


            for key in list(parameter_dic.keys()):
                  input_para.write(key + ":" + "\t" + str(parameter_dic[key]) + "\n")

      # parsing the XML file
      xml_dic = parse_xml(parameter_dic["set_file"])

      # print(xml_dic)


      if parameter_dic["pair_end"]:

            clean_data1_path, clean_data2_path = pecorec.clean_reads(parameter_dic,
                                                           xml_dic,
                                                           parameter_dic["outdir"])

            if parameter_dic["sub-pipeline 1"]:

                  pecorec.sub_run1(parameter_dic,xml_dic,
                                   clean_data1_path, clean_data2_path)


            if parameter_dic["sub-pipeline 2"]:
                  pecorec.sub_run2(parameter_dic, xml_dic,
                                   clean_data1_path, clean_data2_path)

      elif parameter_dic["single_end"]:

            clean_data_fas = secorec.clean_reads(parameter_dic,
                                         xml_dic,
                                         parameter_dic["outdir"])

            if parameter_dic["sub-pipeline 1"]:
                  secorec.sub_run1(parameter_dic,xml_dic,clean_data_fas)


            if parameter_dic["sub-pipeline 2"]:
                  secorec.sub_run2(parameter_dic, xml_dic,clean_data_fas)

      else:
            print("Error!")


      duration = datetime.today().now() - start

      print(">>> " + "Finished, take " + str(duration) + " seconds in total." + "\n")

      sys.exit()



if __name__ == "__main__":
    starts()