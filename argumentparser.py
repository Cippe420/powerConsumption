import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v' , '--visual',action='store_true',help='Visualize the data')

args= parser.parse_args()
opts = args.visual
