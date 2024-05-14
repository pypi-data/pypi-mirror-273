import pandas as pd
import sys
from Bio import SeqIO
import itertools
import scipy.stats as stats
import os


def print_usage():
    print(f"Usage: python {sys.argv[0]} <peak.xlsx> <genome.fa> [output_path]")


def calc_usage_deviation(seq, count_dict=None, n=2, model='zero-order', silence_mode=True):
    if not count_dict:
        count_dict = {}

    if not silence_mode:
        print(f"Dealing with {seq} of {n}")
    if model == 'zero-order':
        nucl = ['A', 'T', 'G', 'C']
        tmp = [nucl] * n
        for i in itertools.product(*tmp):
            nn = ''.join(i)
            o_w = seq.count(nn)
            exp = 1
            for n0 in nucl:
                c = nn.count(n0)
                if c:
                    exp *= seq.count(n0) ** c
            exp /= len(seq) ** (n - 1)
            if nn in count_dict:
                count_dict[nn].append(o_w / exp)
            else:
                count_dict[nn] = [o_w / exp]
    elif model == 'chain':
        nucl = ['A', 'T', 'G', 'C']
        tmp = [nucl] * n
        for i in itertools.product(*tmp):
            nn = ''.join(i)
            o_w = seq.count(nn)
            exp = seq.count(nn[:-1])
            exp *= seq.count(nn[1:])
            exp /= seq.count(nn[1:-1])
            if not exp:
                exp = 1
            if nn in count_dict:
                count_dict[nn].append(o_w / exp)
            else:
                count_dict[nn] = [o_w / exp]
    elif model == 'no-scale':
        nucl = ['A', 'T', 'G', 'C']
        tmp = [nucl] * n
        for i in itertools.product(*tmp):
            nn = ''.join(i)
            o_w = seq.count(nn)
            exp = 1
            if nn in count_dict:
                count_dict[nn].append(o_w / exp)
            else:
                count_dict[nn] = [o_w / exp]
    return count_dict


def calc(input_path, genome_path, output_path=None, length=200, n_max=3, peak_model='no-scale',
         genome_model='zero-order'):
    l = int(length / 2)
    df = pd.read_excel(input_path, comment='#', header=1)
    for record in SeqIO.parse(genome_path, 'fasta'):
        seq = str(record.seq)

    peaks = []
    folds = []
    count_dict = {}
    for summit, peak_name, fold in zip(df['abs_summit'], df['name'], df['fold_enrichment']):
        # tmp_seq = seq[summit - 50:summit + 50]
        tmp_seq = seq[summit - l:summit + l]
        for n in range(2, n_max + 1):
            # count_dict = calc_usage_deviation(tmp_seq, count_dict, n, model='chain')
            count_dict = calc_usage_deviation(tmp_seq, count_dict, n, model=peak_model)
            # count_dict = calc_usage_deviation(tmp_seq, count_dict, n)
        peaks.append(peak_name)
        folds.append(fold)

    rho_dict = {}
    pval_dict = {}
    zeros_dict = {}
    for k, v in count_dict.items():
        res = stats.spearmanr(v, folds)
        rho_dict[k] = res[0]
        pval_dict[k] = res[1]
        zeros_dict[k] = v.count(0)
    # calculate genomic usage deviation
    genomic_count_dict = {}
    for n in range(2, n_max + 1):
        genomic_count_dict = calc_usage_deviation(seq, genomic_count_dict, n, model=genome_model)

    # nucl, genomic_deviation, rho, pval
    output = [[k, genomic_count_dict[k][0], rho_dict[k], pval_dict[k], zeros_dict[k]] for k, v in rho_dict.items()]
    df_out = pd.DataFrame(output)
    df_out.columns = ['nucleotide', 'genomic usage deviation', 'rho', 'pval', '# of zeros']
    if not output_path:
        output_path = os.path.splitext(sys.argv[1])[0] + '_output200.xlsx'
    df_out.to_excel(output_path)


def main(args):
    n_max = int(args.n)
    peak_model = args.p_model
    genome_model = args.g_model
    length = int(args.length)
    input_path = args.input_path
    genome_path = args.ref
    output_path = args.out

    calc(*[input_path, genome_path, output_path, length, n_max, peak_model, genome_model])


if __name__ == '__main__':
    if len(sys.argv) in (3, 4):
        calc(*sys.argv)
    else:
        print_usage()
