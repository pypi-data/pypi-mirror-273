import pickle
import json
import re
from pathlib import Path
from bisect import bisect_left


def available_genes():
    from geney import config_setup
    annotation_path = config_setup['MRNA_PATH'] / 'protein_coding'
    return sorted(list(set([m.stem.split('_')[-1] for m in annotation_path.glob('*')])))

def contains(a, x):
    """returns true if sorted sequence `a` contains `x`"""
    i = bisect_left(a, x)
    return i != len(a) and a[i] == x


def unload_json(file_path):
    """Opens a specified json file.

    Parameters
    ----------
    input_file : str
        Path to a json file.

    Returns
    -------
    dict
        data stored in specified json file.

    Examples
    --------
    >>> unload_json('/Users/abc/Desktop/semester_grades.json')
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def dump_json(file_path, payload):
    with open(file_path, 'w') as f:
        json.dump(payload, f)
    return None


def unload_pickle(file_path):

    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    return data


def dump_pickle(file_path, payload):
    with open(file_path, 'wb') as f:
        pickle.dump(payload, f)
    return None


def find_files_by_gene_name(gene_name):
    from geney import config_setup
    mrna_path = config_setup['MRNA_PATH'] / 'protein_coding'
    matching_files = [f for f in mrna_path.glob(f'*_{gene_name}.pkl')]
    if len(matching_files) > 1:
        print(f"Multiple files available ({[f.name for f in matching_files]}).")
    elif len(matching_files) == 0:
        raise FileNotFoundError(f"No files available for gene {gene_name}.")

    return matching_files[0]


def reverse_complement(s: str, complement: dict = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'} ) -> str:
    '''Performs reverse-complement of a sequence. Default is a DNA sequence.'''
    s_rev = s[::-1]
    lower = [b.islower() for b in list(s_rev)]
    bases = [complement.get(base, base) for base in list(s_rev.upper())]
    rev_compl = ''.join([b.lower() if l else b for l, b in zip(lower, bases)])
    return rev_compl


