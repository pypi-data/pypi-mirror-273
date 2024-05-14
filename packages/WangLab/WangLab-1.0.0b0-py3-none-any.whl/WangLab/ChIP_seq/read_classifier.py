"""
This script classify reads into 5 classes:
1. Inside
2. Overlap start
3. Overlap end
4. Upstream
5. Downstream

The numbers are also the order of determining classes.

Usage: python read_classifier.py -a annot.xlsx -i peak.xlsx -o out.xlsx
"""
import pandas as pd
import argparse


def prepare_args(args):
    args.add_argument('-a', '--annot', dest='annot', nargs='?', type=str, required=True,
                      help='Annotation file, should consist at least 4 columns, each represent gene name, start, end, and strain')
    args.add_argument('-i', '--input', dest='input', nargs='?', type=str, required=True,
                      help='Peak informations, should be in same format with what MACS3 generates')
    args.add_argument('-o', '--output', dest='output', nargs='?', type=str, required=False, default=None,
                      help='Output file, will output to the working directory if not assigned.')

    return args


def assign_status(classes, cls, genes, f_name):
    classes.append(cls)
    genes.append(f_name)
    return 1


def main(args):
    df_annot = pd.read_excel(args.annot, comment='#')
    df_peak = pd.read_excel(args.input, comment='#', header=1)

    df_annot = df_annot.sort_values(by=df_annot.columns[1])
    df_peak = df_peak.sort_values(by=['start', 'end'])

    classes = []
    genes = []
    feature_id = 0
    # deal with every peak
    for start, end in zip(df_peak['start'], df_peak['end']):
        flag = 0
        feature_id = 0
        for f_id, (f_name, f_start, f_end, f_strain) in enumerate(
                zip(df_annot.iloc[feature_id:, 0], df_annot.iloc[feature_id:, 1], df_annot.iloc[feature_id:, 2],
                    df_annot.iloc[feature_id:, 3])):
            if f_end >= end:  # the first feature that near the read
                if end >= f_start:
                    if f_start <= start:  # condition 1
                        flag = assign_status(classes, 'Inside', genes, f_name)
                    elif f_strain == '+':  # condition 2
                        flag = assign_status(classes, 'Overlap start', genes, f_name)
                    else:
                        f_name0, f_start0, f_end0, f_strain0 = df_annot.iloc[feature_id + f_id - 1, 0:4]
                        if start > f_end0:  # condition 3
                            flag = assign_status(classes, 'Overlap end', genes, f_name)
                        elif start >= f_start0:
                            if f_strain0 == '-':  # condition 4
                                flag = assign_status(classes, 'Overlap start', genes, f_name0)
                            else:  # condition 5
                                flag = assign_status(classes, 'Overlap end', genes, ','.join([f_name0, f_name]))
                        else:  # condition 6
                            flag = assign_status(classes, 'Cover', genes, f_name0)
                else:
                    f_name0, f_start0, f_end0, f_strain0 = df_annot.iloc[feature_id + f_id - 1, 0:4]
                    if start > f_end0:  # condition 7
                        if f_strain == '+':
                            if f_strain0 == '-':
                                flag = assign_status(classes, 'Upstream', genes, ','.join([f_name0, f_name]))
                            else:
                                flag = assign_status(classes, 'Up/Downstream', genes, ','.join([f_name0, f_name]))
                        elif f_strain0 == '+':
                            flag = assign_status(classes, 'Downstream', genes, ','.join([f_name0, f_name]))
                        else:
                            flag = assign_status(classes, 'Up/Downstream', genes, ','.join([f_name0, f_name]))
                    elif start >= f_start0:  # condition 8
                        if f_strain0 == '+':
                            flag = assign_status(classes, 'Overlap end', genes, f_name0)
                        else:
                            flag = assign_status(classes, 'Overlap start', genes, f_name0)
                    else:  # condition 9
                        flag = assign_status(classes, 'Cover', genes, f_name0,)
                feature_id += f_id - 1
                break
        if not flag:
            assign_status(classes, 'Not matched', genes, 'None')

    df_peak['class'] = classes
    df_peak['related genes'] = genes
    if not args.output:
        args.output = args.input.split('.')[0] + '_output.xlsx'
    df_peak.to_excel(args.output, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser = prepare_args(parser)
    args = parser.parse_args()
    main(args)
