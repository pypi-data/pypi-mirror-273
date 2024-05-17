
from pathlib import Path
END_CODONS = ['TAA', 'TAG', 'TGA']

def is_monotonic(A):
    x, y = [], []
    x.extend(A)
    y.extend(A)
    x.sort()
    y.sort(reverse=True)
    if(x == A or y == A):
        return True
    return False


class Mutation:
    def __init__(self, mid):
        self.mut_id = mid

        gene, chrom, pos, ref, alt = mid.split(':')
        self.gene = gene
        self.chrom = chrom.strip('chr')
        self.start = int(pos)

        self.file_identifier = self.mut_id.replace(':', '_')
        self.file_identifier_short = f'{self.start}_{ref}_{alt}'

        self.ref = ref if ref != '-' else ''
        self.alt = alt if alt != '-' else ''

        if len(self.ref) == len(self.alt) == 1:
            self.vartype = 'SNP'
        elif len(self.ref) == len(self.alt) > 1:
            self.vartype = 'SUB'
        elif self.ref and not self.alt:
            self.vartype = 'DEL'
        elif self.alt and not self.ref:
            self.vartype = 'INS'
        else:
            self.vartype = 'INDEL'

    def __str__(self):
        return self.mut_id

    def __repr__(self):
        return self.mut_id

    def __lt__(self, other):
        return self.start < other.start


class Variations:
    def __init__(self, epistatic_set):
        self.variants = sorted([Mutation(m) for m in epistatic_set.split('|')])
        self.mut_id = epistatic_set
        self.start = self.variants[0].start
        self.positions = [v.start for v in self.variants]
        # self.ref = ','.join([m.ref for m in self.variants])
        # self.alt = ','.join([m.alt for m in self.variants])
        self.gene = self.variants[0].gene
        self.chrom = self.variants[0].chrom.strip('chr')
        self.file_identifier = f'{self.gene}_{self.chrom}' + '_' + '_'.join([v.file_identifier_short for v in self.variants])

    def __str__(self):
        return '|'.join([m.mut_id for m in self.variants])

    def __repr__(self):
        return '|'.join([m.mut_id for m in self.variants])

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.variants):
            x = self.variants[self.current_index]
            self.current_index += 1
            return x
        raise StopIteration

    @property
    def file_identifier_json(self):
        return Path(self.file_identifier + '.json')


def generate_mut_variant(seq: str, indices: list, mut: Mutation):
    offset = 1 if not mut.ref else 0

    check_indices = list(range(mut.start, mut.start + len(mut.ref) + offset))
    check1 = all([m in indices for m in check_indices])
    if not check1:
        print(f"Mutation {mut} not within transcript bounds: {min(indices)} - {max(indices)}.")
        return seq, indices, False, False

    rel_start, rel_end = indices.index(mut.start)+offset, indices.index(mut.start)+offset+len(mut.ref)
    acquired_seq = seq[rel_start:rel_end]
    check2 = acquired_seq == mut.ref
    if not check2:
        print(f'Reference allele does not match genome_build allele. {acquired_seq}, {mut.ref}, {mut.start}')
        consensus_allele = False
    else:
        consensus_allele = True
    if len(mut.ref) == len(mut.alt) > 0:
        temp_indices = list(range(mut.start, mut.start + len(mut.ref)))
    else:
        temp_indices = [indices[indices.index(mut.start)] + v / 1000 for v in list(range(1, len(mut.alt)+1))]


    new_indices = indices[:rel_start] + temp_indices + indices[rel_end:]
    new_seq = seq[:rel_start] + mut.alt + seq[rel_end:]

    assert len(new_seq) == len(new_indices), f'Error in variant modification: {mut}, {len(new_seq)}, {len(new_indices)}'
    assert is_monotonic(list(filter((-1).__ne__, new_indices))), f'Mut indices are not monotonic.'
    return new_seq, new_indices, True, consensus_allele


def find_new_tts(seq, indices, tis):
    seq, indices = seq[indices.index(tis):], indices[indices.index(tis):]
    pos_options = [i for i in list(range(0, len(seq), 3)) if seq[i:i + 3] in END_CODONS and i+3 <= len(seq)]
    if len(pos_options) == 0:
        return indices[0] #[len(seq) - (len(seq) % 3) - 1]
    pos_options = pos_options[0]
    assert pos_options % 3 == 0, f'{pos_options} not divisible by three.'
    pos_options -= 1
    return indices[pos_options]
