import pandas as pd
import numpy as np
import argparse

def main(args):
    first_line = 'file,position,from,to,logodds,predH,predE,predD,predR,predK,predS,predT,predN,predQ,predA,predV,predL,predI,predM,predF,predY,predW,predP,predG,predC'
    
    # make first_line header of dataframe
    df = pd.DataFrame(columns=first_line.split(','))

    # read text file ../test_mc2/HUW04_protease.mutcompute.txt
    filename = f"{args.output}/{args.name}.mutcompute.txt"
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        # if line starts with HUW04
        if line.startswith(args.name):
            # split line by comma
            data = line.split(',')
            # append line to dataframe
            df.loc[len(df)] = data
            
    # remove pred from column names
    df.columns = [col.replace('pred', '') for col in df.columns]

    # remove first 5 items of first_line
    df = df.drop(first_line.split(',')[:5], axis=1)
    amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

    # reorder df by amino acids
    df = df[amino_acids]
    # save to npy file
    df = df.astype(float)
    
    np.save(f'{args.output}/{args.name}.Mutcompute.npy', df.to_numpy())
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, help="Path to the output directory.")
    parser.add_argument("--name", type=str, help="Name of the protein.")
    args = parser.parse_args()
    
    main(args)
