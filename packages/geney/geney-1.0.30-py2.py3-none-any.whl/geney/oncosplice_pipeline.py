import networkx as nx
import random
from Bio.Seq import Seq
from Bio import pairwise2
from dataclasses import dataclass
from copy import deepcopy
import re
import pandas as pd
from pathlib import Path

from geney import config_setup
from geney.splicing.splicing_utils import *
from geney.utils import find_files_by_gene_name, reverse_complement, unload_pickle
from geney.Fasta_segment import Fasta_segment


def sai_predict_probs(seq: str, models: list) -> list:
    '''
    Predicts the donor and acceptor junction probability of each
    NT in seq using SpliceAI.

    Let m:=2*sai_mrg_context + L be the input seq length. It is assumed
    that the input seq has the following structure:

          seq = |<sai_mrg_context NTs><L NTs><sai_mrg_context NTs>|

    The returned probability matrix is of size 2XL, where
    the first row is the acceptor probability and the second row
    is the donor probability. These probabilities corresponds to the
    middel <L NTs> NTs of the input seq.
    '''
    x = one_hot_encode(seq)[None, :]
    y = np.mean([models[m].predict(x, verbose=0) for m in range(5)], axis=0)
    return y[0, :, 1:].T


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
        return f"Mutation({self.mut_id})"

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
        self.file_identifier = f'{self.gene}_{self.chrom}' + '_' + '_'.join(
            [v.file_identifier_short for v in self.variants])

    def __str__(self):
        return '|'.join([m.mut_id for m in self.variants])

    def __repr__(self):
        return f"Variation({', '.join([m.mut_id for m in self.variants])})"

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
        print(
            f"Mutation {mut} not within transcript bounds: {min(list(filter((-1).__ne__, indices)))} - {max(indices)}.")
        return seq, indices, False, False

    rel_start, rel_end = indices.index(mut.start) + offset, indices.index(mut.start) + offset + len(mut.ref)
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
        temp_indices = [indices[indices.index(mut.start)] + v / 1000 for v in list(range(1, len(mut.alt) + 1))]

    new_indices = indices[:rel_start] + temp_indices + indices[rel_end:]
    new_seq = seq[:rel_start] + mut.alt + seq[rel_end:]

    assert len(new_seq) == len(new_indices), f'Error in variant modification: {mut}, {len(new_seq)}, {len(new_indices)}'
    assert is_monotonic(list(filter((-1).__ne__, new_indices))), f'Mut indices are not monotonic.'
    return new_seq, new_indices, True, consensus_allele


def is_monotonic(A):
    x, y = [], []
    x.extend(A)
    y.extend(A)
    x.sort()
    y.sort(reverse=True)
    if (x == A or y == A):
        return True
    return False


class Gene:
    def __init__(self, gene_name, variation=None):
        self.gene_name = gene_name
        self.gene_id = ''
        self.rev = None
        self.chrm = ''
        self.gene_start = 0
        self.gene_end = 0
        self.transcripts = {}
        self.load_from_file(find_files_by_gene_name(gene_name))
        self.variations = variation

    def __repr__(self):
        return f'Gene(gene_name={self.gene_name})'

    def __len__(self):
        return len(self.transcripts)

    def __str__(self):
        return '{gname}, {ntranscripts} transcripts'.format(gname=self.gene_name, ntranscripts=self.__len__())

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __getitem__(self, index):
        return Transcript(list(self.transcripts.values())[index])

    def load_from_file(self, file_name):
        if not file_name.exists():
            raise FileNotFoundError(f"File '{file_name}' not found.")
        self.load_from_dict(dict_data=unload_pickle(file_name))
        return self

    def load_from_dict(self, dict_data=None):
        for k, v in dict_data.items():
            setattr(self, k, v)
        return self

    def transcript(self, tid):
        if tid not in self.transcripts:
            raise AttributeError(f"Transcript '{tid}' not found in gene '{self.gene_name}'.")
        return Transcript(self.transcripts[tid])

    def run_transcripts(self, primary_transcript=False, protein_coding=False):
        for tid, annotations in self.transcripts.items():
            if primary_transcript and not annotations['primary_transcript']:
                continue
            if protein_coding and annotations['transcript_biotype'] != 'protein_coding':
                continue

            yield Transcript(self.transcripts[tid], variations=self.variations)


class Transcript:
    def __init__(self, d=None, variations=None):
        self.transcript_id = None
        self.transcript_start = None  # transcription
        self.transcript_end = None  # transcription
        self.transcript_biotype = None  # metadata
        self.acceptors, self.donors = [], []  # splicing
        self.TIS, self.TTS = None, None  # translation
        self.transcript_seq, self.transcript_indices = '', []  # sequence data
        self.rev = None  # sequence data
        self.chrm = ''  # sequence data
        self.pre_mrna = ''  # sequence data
        self.orf = ''  # sequence data
        self.protein = ''  # sequence data
        self.log = ''  # sequence data
        self.primary_transcript = None  # sequence data
        self.cons_available = False  # metadata
        self.cons_seq = ''
        self.cons_vector = ''
        self.variations = None
        if variations:
            self.variations = Variations(variations)

        if d:
            self.load_from_dict(d)

        if self.cons_available:
            if '*' in self.cons_seq and len(self.cons_seq) == len(self.cons_vector):
                self.cons_seq = self.cons_seq.replace('*', '')
                self.cons_vector = self.cons_vector[:-1]

            elif '*' in self.cons_seq and len(self.cons_seq) == len(self.cons_vector) + 1:
                self.cons_seq = self.cons_seq.replace('*', '')

            else:
                self.cons_available = False

        if self.transcript_biotype == 'protein_coding':
            self.generate_protein()

    def __repr__(self):
        return 'Transcript(transcript_id={tid})'.format(tid=self.transcript_id)

    def __len__(self):
        return len(self.transcript_seq)

    def __str__(self):
        return 'Transcript {tid}, Transcript Type: ' \
               '{protein_coding}, Primary: {primary}'.format(
            tid=self.transcript_id, protein_coding=self.transcript_biotype.replace('_', ' ').title(),
            primary=self.primary_transcript)

    def __eq__(self, other):
        return self.transcript_seq == other.transcript_seq

    def __contains__(self, subvalue):
        if isinstance(subvalue, str):
            return subvalue in self.transcript_seq
        elif isinstance(subvalue, int):
            return subvalue in self.transcript_indices
        else:
            print(
                "Pass an integer to check against the span of the gene's coordinates or a string to check against the "
                "pre-mRNA sequence.")
            return False

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def load_from_dict(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        self.__arrange_boundaries()
        self.generate_mature_mrna(inplace=True)
        return self

    @property
    def exons(self):
        return list(zip(self.acceptors, self.donors))

    @property
    def introns(self):
        return list(zip([v for v in self.donors if v != self.transcript_end],
                        [v for v in self.acceptors if v != self.transcript_start]))

    def set_intron_boundaries(self, acceptors=None, donors=None):
        if acceptors:
            self.acceptors = acceptors
        if donors:
            self.donors = donors
        self.__arrange_boundaries()
        return self

    @property
    def introns(self):
        return list(zip([v for v in self.donors if v != self.transcript_end],
                        [v for v in self.acceptors if v != self.transcript_start]))

    def __exon_coverage_check(self):
        if sum([abs(a - b) + 1 for a, b in self.exons]) == len(self):
            return True
        else:
            return False

    @property
    def exons_pos(self):
        temp = self.exons
        if self.rev:
            temp = [(b, a) for a, b in temp[::-1]]
        return temp

    @property
    def mrna_indices(self):
        temp = [lst for lsts in [list(range(a, b + 1)) for a, b in self.exons_pos] for lst in lsts]
        return sorted(temp, reverse=self.rev)

    @property
    def exonic_indices(self):
        return [lst for lsts in [list(range(a, b + 1)) for a, b in self.exons_pos] for lst in lsts]

    def __arrange_boundaries(self):
        self.acceptors.append(self.transcript_start)
        self.donors.append(self.transcript_end)
        self.acceptors = list(set(self.acceptors))
        self.donors = list(set(self.donors))
        self.acceptors.sort(reverse=self.rev)
        self.donors.sort(reverse=self.rev)
        return self

    def positive_strand(self):
        if self.rev:
            return reverse_complement(self.transcript_seq)
        else:
            return self.transcript_seq

    def __pos2sense(self, mrna, indices):
        if self.rev:
            mrna = reverse_complement(mrna)
            indices = indices[::-1]
        return mrna, indices

    def pull_pre_mrna_pos(self):
        fasta_obj = Fasta_segment()
        if self.rev:
            return fasta_obj.read_segment_endpoints(config_setup['CHROM_SOURCE'] / f'chr{self.chrm}.fasta',
                                                    self.transcript_end,
                                                    self.transcript_start)
        else:
            return fasta_obj.read_segment_endpoints(config_setup['CHROM_SOURCE'] / f'chr{self.chrm}.fasta',
                                                    self.transcript_start,
                                                    self.transcript_end)

    def generate_pre_mrna_pos(self):
        seq, indices = self.pull_pre_mrna_pos()
        if self.variations:
            for mutation in self.variations.variants:
                seq, indices, _, _ = generate_mut_variant(seq, indices, mut=mutation)
        self.pre_mrna, _ = self.__pos2sense(seq, indices)
        return seq, indices

    def generate_pre_mrna(self, inplace=True):
        pre_mrna, pre_indices = self.__pos2sense(*self.generate_pre_mrna_pos())
        self.pre_mrna = pre_mrna
        if inplace:
            return self
        return pre_mrna, pre_indices

    def generate_mature_mrna_pos(self):
        mature_mrna, mature_indices = '', []
        pre_seq, pre_indices = self.generate_pre_mrna_pos()
        for i, j in self.exons_pos:
            rel_start, rel_end = pre_indices.index(i), pre_indices.index(j)
            mature_mrna += pre_seq[rel_start:rel_end + 1]
            mature_indices.extend(pre_indices[rel_start:rel_end + 1])
        return mature_mrna, mature_indices

    def generate_mature_mrna(self, inplace=True):
        if inplace:
            self.transcript_seq, self.transcript_indices = self.__pos2sense(*self.generate_mature_mrna_pos())
            return self
        return self.__pos2sense(*self.generate_mature_mrna_pos())

    def generate_protein(self, inplace=True, regenerate_mrna=True):
        if regenerate_mrna:
            self.generate_mature_mrna()

        if not self.TIS or self.TIS not in self.transcript_indices:
            return ''

        rel_start = self.transcript_indices.index(self.TIS)
        orf = self.transcript_seq[rel_start:]
        first_stop_index = next((i for i in range(0, len(orf) - 2, 3) if orf[i:i + 3] in {"TAG", "TAA", "TGA"}), None)
        orf = orf[:first_stop_index + 3]
        protein = str(Seq(orf).translate()).replace('*', '')
        if inplace:
            self.orf = orf
            self.protein = protein
            if self.protein != self.cons_seq:
                self.cons_available = False
            return self
        return protein


def develop_aberrant_splicing(transcript, aberrant_splicing):
    exon_starts = {v: 1 for v in transcript.acceptors}
    exon_starts.update({transcript.transcript_start: 1})
    exon_starts.update({s: v['absolute'] for s, v in aberrant_splicing['missed_acceptors'].items()})
    exon_starts.update({s: v['absolute'] for s, v in aberrant_splicing['discovered_acceptors'].items()})

    exon_ends = {v: 1 for v in transcript.donors}
    exon_ends.update({transcript.transcript_end: 1})
    exon_ends.update({s: v['absolute'] for s, v in aberrant_splicing['missed_donors'].items()})
    exon_ends.update({s: v['absolute'] for s, v in aberrant_splicing['discovered_donors'].items()})

    nodes = [SpliceSite(pos=pos, ss_type=0, prob=prob) for pos, prob in exon_ends.items()] + \
            [SpliceSite(pos=pos, ss_type=1, prob=prob) for pos, prob in exon_starts.items()]

    nodes = [s for s in nodes if s.prob > 0]
    nodes.sort(key=lambda x: x.pos, reverse=transcript.rev)

    G = nx.DiGraph()
    G.add_nodes_from([n.pos for n in nodes])

    for i in range(len(nodes)):
        trailing_prob, in_between = 0, []
        for j in range(i + 1, len(nodes)):
            curr_node, next_node = nodes[i], nodes[j]
            spread = curr_node.ss_type in in_between
            in_between.append(next_node.ss_type)
            if curr_node.ss_type != next_node.ss_type:
                if spread:
                    new_prob = next_node.prob - trailing_prob
                    if new_prob <= 0:
                        break
                    G.add_edge(curr_node.pos, next_node.pos)
                    G.edges[curr_node.pos, next_node.pos]['weight'] = new_prob
                    trailing_prob += next_node.prob
                else:
                    G.add_edge(curr_node.pos, next_node.pos)
                    G.edges[curr_node.pos, next_node.pos]['weight'] = next_node.prob
                    trailing_prob += next_node.prob

    new_paths, prob_sum = {}, 0
    for i, path in enumerate(nx.all_simple_paths(G, transcript.transcript_start, transcript.transcript_end)):
        curr_prob = path_weight_mult(G, path, 'weight')
        prob_sum += curr_prob
        new_paths[i] = {
            'acceptors': sorted([p for p in path if p in exon_starts.keys() and p != transcript.transcript_start],
                                reverse=transcript.rev),
            'donors': sorted([p for p in path if p in exon_ends.keys() and p != transcript.transcript_end],
                             reverse=transcript.rev),
            'path_weight': curr_prob}

    for i, d in new_paths.items():
        d['path_weight'] = round(d['path_weight'] / prob_sum, 3)
    new_paths = {k: v for k, v in new_paths.items() if v['path_weight'] > 0.01}
    return list(new_paths.values())


def path_weight_mult(G, path, weight):
    multigraph = G.is_multigraph()
    cost = 1
    if not nx.is_path(G, path):
        raise nx.NetworkXNoPath("path does not exist")
    for node, nbr in nx.utils.pairwise(path):
        if multigraph:
            cost *= min(v[weight] for v in G[node][nbr].values())
        else:
            cost *= G[node][nbr][weight]
    return cost


@dataclass
class SpliceSite(object):
    pos: int
    ss_type: int
    prob: float

    def __post_init__(self):
        pass

    def __lt__(self, other):
        return self.pos < other.pos

    def __str__(self):
        print(f"({self.ss_type}, {self.pos}, {self.prob})")


def run_spliceai_seq(seq, indices, rev):
    seq = 'N' * 5000 + seq + 'N' * 5000
    # indices = [-1] * 5000 + indices + [-1] * 5000

    ref_seq_probs_temp = sai_predict_probs(seq, sai_models)
    ref_seq_acceptor_probs, ref_seq_donor_probs = ref_seq_probs_temp[0, :], ref_seq_probs_temp[1, :]

    acceptor_indices = {a: b for a, b in list(zip(indices, ref_seq_acceptor_probs)) if b > 0.75}
    donor_indices = {a: b for a, b in list(zip(indices, ref_seq_donor_probs)) if b > 0.75}
    return acceptor_indices, donor_indices


def run_spliceai_transcript(mutations, gene_data, sai_mrg_context=5000, min_coverage=2500, sai_threshold=0.5):
    positions = mutations.positions  # [m.start for m in mutations]
    seq_start_pos = min(positions) - sai_mrg_context - min_coverage
    seq_end_pos = max(positions) + sai_mrg_context + min_coverage  # + 1

    # ref_seq, ref_indices = pull_fasta_seq_endpoints(mutations.chrom, seq_start_pos, seq_end_pos)
    fasta_obj = Fasta_segment()
    ref_seq, ref_indices = fasta_obj.read_segment_endpoints(
        config_setup['CHROM_SOURCE'] / f'chr{mutations.chrom}.fasta',
        seq_start_pos,
        seq_end_pos)

    gene_start, gene_end, rev = gene_data.transcript_start, gene_data.transcript_end, gene_data.rev

    mrna_acceptors = sorted(gene_data.acceptors)
    mrna_donors = sorted(gene_data.donors)

    visible_donors = np.intersect1d(mrna_donors, ref_indices)
    visible_acceptors = np.intersect1d(mrna_acceptors, ref_indices)

    start_pad = ref_indices.index(gene_start) if gene_start in ref_indices else 0
    end_cutoff = ref_indices.index(gene_end) if gene_end in ref_indices else len(ref_indices)  # - 1
    end_pad = len(ref_indices) - end_cutoff
    ref_seq = 'N' * start_pad + ref_seq[start_pad:end_cutoff] + 'N' * end_pad
    ref_indices = [-1] * start_pad + ref_indices[start_pad:end_cutoff] + [-1] * end_pad
    mut_seq, mut_indices = ref_seq, ref_indices

    for mut in mutations:
        mut_seq, mut_indices, _, _ = generate_mut_variant(seq=mut_seq, indices=mut_indices, mut=mut)

    ref_indices = ref_indices[sai_mrg_context:-sai_mrg_context]
    mut_indices = mut_indices[sai_mrg_context:-sai_mrg_context]

    if rev:
        ref_seq = reverse_complement(ref_seq)
        mut_seq = reverse_complement(mut_seq)
        ref_indices = ref_indices[::-1]
        mut_indices = mut_indices[::-1]

    ref_seq_probs_temp = sai_predict_probs(ref_seq, sai_models)
    mut_seq_probs_temp = sai_predict_probs(mut_seq, sai_models)

    ref_seq_acceptor_probs, ref_seq_donor_probs = ref_seq_probs_temp[0, :], ref_seq_probs_temp[1, :]
    mut_seq_acceptor_probs, mut_seq_donor_probs = mut_seq_probs_temp[0, :], mut_seq_probs_temp[1, :]

    assert len(ref_indices) == len(ref_seq_acceptor_probs), 'Reference pos not the same'
    assert len(mut_indices) == len(mut_seq_acceptor_probs), 'Mut pos not the same'

    iap, dap = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_acceptor_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_acceptor_probs))},
                               visible_acceptors,
                               threshold=sai_threshold)

    assert len(ref_indices) == len(ref_seq_donor_probs), 'Reference pos not the same'
    assert len(mut_indices) == len(mut_seq_donor_probs), 'Mut pos not the same'

    idp, ddp = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_donor_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_donor_probs))},
                               visible_donors,
                               threshold=sai_threshold)

    missplicing = {'missed_acceptors': dap, 'missed_donors': ddp, 'discovered_acceptors': iap, 'discovered_donors': idp}
    missplicing = {outk: {float(k): v for k, v in outv.items()} for outk, outv in missplicing.items()}
    return {outk: {int(k) if k.is_integer() else k: v for k, v in outv.items()} for outk, outv in missplicing.items()}


def OncospliceAnnotator(reference_transcript, variant_transcript, mut):
    affected_exon, affected_intron, distance_from_5, distance_from_3 = find_splice_site_proximity(mut,
                                                                                                  reference_transcript)

    report = {}
    report['primary_transcript'] = reference_transcript.primary_transcript
    report['transcript_id'] = reference_transcript.transcript_id
    report['mut_id'] = mut.mut_id
    report['cons_available'] = int(reference_transcript.cons_available)
    report['protein_coding'] = reference_transcript.transcript_biotype

    report['reference_mrna'] = reference_transcript.transcript_seq
    report['reference_cds_start'] = reference_transcript.TIS
    report['reference_pre_mrna'] = reference_transcript.pre_mrna
    report[
        'reference_orf'] = reference_transcript.orf  # pre_mrna[reference_transcript.transcript_indices.index(reference_transcript.TIS):reference_transcript.transcript_indices.index(reference_transcript.TTS)]
    report['reference_protein'] = reference_transcript.protein
    report['reference_protein_length'] = len(reference_transcript.protein)

    report['variant_mrna'] = variant_transcript.transcript_seq
    report['variant_cds_start'] = variant_transcript.TIS
    report[
        'variant_pre_mrna'] = variant_transcript.pre_mrna  # pre_mrna[variant_transcript.transcript_indices.index(variant_transcript.TIS):variant_transcript.transcript_indices.index(variant_transcript.TTS)]
    report['variant_orf'] = variant_transcript.orf
    report['variant_protein'] = variant_transcript.protein
    report['variant_protein_length'] = len(variant_transcript.protein)

    descriptions = define_missplicing_events(reference_transcript.exons, variant_transcript.exons,
                                             reference_transcript.rev)
    # print(descriptions)
    report['exon_changes'] = '|'.join([v for v in descriptions if v])
    report['splicing_codes'] = summarize_missplicing_event(*descriptions)
    report['affected_exon'] = affected_exon
    report['affected_intron'] = affected_intron
    report['mutation_distance_from_5'] = distance_from_5
    report['mutation_distance_from_3'] = distance_from_3
    return report


def find_splice_site_proximity(mut, transcript):
    affected_exon, affected_intron, distance_from_5, distance_from_3 = None, None, None, None
    for i, (ex_start, ex_end) in enumerate(transcript.exons):
        if min(ex_start, ex_end) <= mut.start <= max(ex_start, ex_end):
            affected_exon = i + 1
            distance_from_5 = abs(mut.start - ex_start)
            distance_from_3 = abs(mut.start - ex_end)

    for i, (in_start, in_end) in enumerate(transcript.introns):
        if min(in_start, in_end) <= mut.start <= max(in_start, in_end):
            affected_intron = i + 1
            distance_from_5 = abs(mut.start - in_end)
            distance_from_3 = abs(mut.start - in_start)

    return affected_exon, affected_intron, distance_from_5, distance_from_3


def define_missplicing_events(ref_exons, var_exons, rev):
    ref_introns = [(ref_exons[i][1], ref_exons[i + 1][0]) for i in range(len(ref_exons) - 1)]
    var_introns = [(var_exons[i][1], var_exons[i + 1][0]) for i in range(len(var_exons) - 1)]
    num_ref_exons = len(ref_exons)
    num_ref_introns = len(ref_introns)
    if not rev:
        partial_exon_skipping = ','.join(
            [f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}' for (s1, s2) in var_exons for
             exon_count, (t1, t2) in enumerate(ref_exons) if (s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)])
        partial_intron_retention = ','.join(
            [f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}' for (s1, s2)
             in var_introns for intron_count, (t1, t2) in enumerate(ref_introns) if
             (s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)])

    else:
        partial_exon_skipping = ','.join(
            [f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}' for (s1, s2) in var_exons for
             exon_count, (t1, t2) in enumerate(ref_exons) if (s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)])
        partial_intron_retention = ','.join(
            [f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}' for (s1, s2)
             in var_introns for intron_count, (t1, t2) in enumerate(ref_introns) if
             (s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)])

    exon_skipping = ','.join(
        [f'Exon {exon_count + 1}/{num_ref_exons} skipped: {(t1, t2)}' for exon_count, (t1, t2) in enumerate(ref_exons)
         if
         t1 not in [s1 for s1, s2 in var_exons] and t2 not in [s2 for s1, s2 in var_exons]])
    novel_exons = ','.join([f'Novel Exon: {(t1, t2)}' for (t1, t2) in var_exons if
                            t1 not in [s1 for s1, s2 in ref_exons] and t2 not in [s2 for s1, s2 in ref_exons]])
    intron_retention = ','.join(
        [f'Intron {intron_count + 1}/{num_ref_introns} retained: {(t1, t2)}' for intron_count, (t1, t2) in
         enumerate(ref_introns) if
         t1 not in [s1 for s1, s2 in var_introns] and t2 not in [s2 for s1, s2 in var_introns]])

    return partial_exon_skipping, partial_intron_retention, exon_skipping, novel_exons, intron_retention


def summarize_missplicing_event(pes, pir, es, ne, ir):
    event = []
    if pes:
        event.append('PES')
    if es:
        event.append('ES')
    if pir:
        event.append('PIR')
    if ir:
        event.append('IR')
    if ne:
        event.append('NE')
    if len(event) > 1:
        return event
    elif len(event) == 1:
        return event[0]
    else:
        return '-'


def find_continuous_gaps(sequence):
    """Find continuous gap sequences in an alignment."""
    return [(m.start(), m.end()) for m in re.finditer(r'-+', sequence)]


def get_logical_alignment(ref_prot, var_prot):
    """
    Aligns two protein sequences and finds the optimal alignment with the least number of gaps.

    Parameters:
    ref_prot (str): Reference protein sequence.
    var_prot (str): Variant protein sequence.

    Returns:
    tuple: Optimal alignment, number of insertions, and number of deletions.
    """

    # Perform global alignment
    alignments = pairwise2.align.globalms(ref_prot, var_prot, 1, -1, -3, 0, penalize_end_gaps=(True, True))

    # Selecting the optimal alignment
    if len(alignments) > 1:
        # Calculate continuous gaps for each alignment and sum their lengths
        gap_lengths = [sum(end - start for start, end in find_continuous_gaps(al.seqA) + find_continuous_gaps(al.seqB))
                       for al in alignments]
        optimal_alignment = alignments[gap_lengths.index(min(gap_lengths))]
    else:
        optimal_alignment = alignments[0]

    return optimal_alignment


def find_indels_with_mismatches_as_deletions(seqA, seqB):
    """
    Identify insertions and deletions in aligned sequences, treating mismatches as deletions.

    Parameters:
    seqA, seqB (str): Aligned sequences.

    Returns:
    tuple: Two dictionaries containing deletions and insertions.
    """
    if len(seqA) != len(seqB):
        raise ValueError("Sequences must be of the same length")

    mapperA, counter = {}, 0
    for i, c in enumerate(list(seqA)):
        if c != '-':
            counter += 1
        mapperA[i] = counter

    mapperB, counter = {}, 0
    for i, (c1, c2) in enumerate(list(zip(seqA, seqB))):
        if c2 != '-':
            counter += 1
        mapperB[i] = counter

    seqA_array, seqB_array = np.array(list(seqA)), np.array(list(seqB))

    # Find and mark mismatch positions in seqB
    mismatches = (seqA_array != seqB_array) & (seqA_array != '-') & (seqB_array != '-')
    seqB_array[mismatches] = '-'
    modified_seqB = ''.join(seqB_array)

    gaps_in_A = find_continuous_gaps(seqA)
    gaps_in_B = find_continuous_gaps(modified_seqB)

    insertions = {mapperB[start]: modified_seqB[start:end].replace('-', '') for start, end in gaps_in_A if
                  seqB[start:end].strip('-')}
    deletions = {mapperA[start]: seqA[start:end].replace('-', '') for start, end in gaps_in_B if
                 seqA[start:end].strip('-')}
    return deletions, insertions


def parabolic_window(window_size):
    """Create a parabolic window function with a peak at the center."""
    x = np.linspace(-1, 1, window_size)
    return 0.9 * (1 - x ** 2) + 0.1


# def calculate_window_size(conservation_vector_length):
#     return int(9 + (51 - 9) * (1 - np.exp(-0.0005 * conservation_vector_length)))
#


def transform_conservation_vector(conservation_vector):
    """
    Transforms a 1D conservation vector using different parameters.

    Args:
        conservation_vector (numpy.ndarray): Input 1D vector of conservation values.

    Returns:
        numpy.ndarray: A matrix containing transformed vectors.
    """
    window = 13
    factor = 4
    convolving_window = parabolic_window(window)
    transformed_vector = np.convolve(conservation_vector, convolving_window, mode='same') / np.sum(convolving_window)
    # Compute exponential factors
    exp_factors = np.exp(-transformed_vector * factor)

    # Normalize and scale exponential factors
    # exp_factors /= exp_factors.sum()
    return exp_factors


def find_modified_positions(sequence_length, deletions, insertions, reach_limit=16):
    """
    Identify unmodified positions in a sequence given deletions and insertions.

    :param sequence_length: Length of the sequence.
    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param reach_limit: Limit for considering the effect of insertions/deletions.
    :return: Array indicating unmodified positions.
    """
    unmodified_positions = np.zeros(sequence_length, dtype=float)

    for pos, insertion in insertions.items():
        # if pos >= sequence_length:
        #     pos = sequence_length - 1
        #     add_factor = 1

        reach = min(len(insertion) // 2, reach_limit)
        front_end, back_end = max(0, pos - reach), min(sequence_length - 1, pos + reach)
        len_start, len_end = pos - front_end, back_end - pos
        try:
            gradient_front = np.linspace(0, 1, len_start, endpoint=False)
            gradient_back = np.linspace(0, 1, len_end, endpoint=True)[::-1]
            combined_gradient = np.concatenate([gradient_front, np.array([1]), gradient_back])
            unmodified_positions[front_end:back_end + 1] = combined_gradient

        except ValueError as e:
            print(
                f"Error: {e} | Lengths: unmodified_positions_slice={back_end - front_end}, combined_gradient={len(combined_gradient)}")
            unmodified_positions[front_end:back_end] = np.zeros(back_end - front_end)

    for pos, deletion in deletions.items():
        deletion_length = len(deletion)
        unmodified_positions[pos:pos + deletion_length] = 1

    return unmodified_positions


def calculate_penalty(domains, cons_scores, W, is_insertion=False):
    """
    Calculate the penalty for mutations (either insertions or deletions) on conservation scores.

    :param domains: Dictionary of mutations (inserted or deleted domains).
    :param cons_scores: Conservation scores.
    :param W: Window size.
    :param is_insertion: Boolean flag to indicate if the mutation is an insertion.
    :return: Penalty array.
    """
    penalty = np.zeros(len(cons_scores))
    for pos, seq in domains.items():
        mutation_length = len(seq)
        weight = max(1.0, mutation_length / W)

        if is_insertion:
            reach = min(W // 2, mutation_length // 2)
            penalty[pos - reach:pos + reach] = weight * cons_scores[pos - reach:pos + reach]
        else:  # For deletion
            penalty[pos:pos + mutation_length] = cons_scores[pos:pos + mutation_length] * weight

    return penalty


def calculate_legacy_oncosplice_score(deletions, insertions, cons_vec, W):
    """
    Calculate the legacy Oncosplice score based on deletions, insertions, and conservation vector.

    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param cons_vec: Conservation vector.
    :param W: Window size.
    :return: Legacy Oncosplice score.
    """
    smoothed_conservation_vector = np.exp(np.negative(moving_average_conv(cons_vec, W, 2)))
    del_penalty = calculate_penalty(deletions, smoothed_conservation_vector, W, is_insertion=False)
    ins_penalty = calculate_penalty(insertions, smoothed_conservation_vector, W, is_insertion=True)
    combined_scores = del_penalty + ins_penalty
    return np.max(np.convolve(combined_scores, np.ones(W), mode='same'))


def moving_average_conv(vector, window_size, factor=1):
    """
    Calculate the moving average convolution of a vector.

    Parameters:
    vector (iterable): Input vector (list, tuple, numpy array).
    window_size (int): Size of the convolution window. Must be a positive integer.
    factor (float): Scaling factor for the average. Default is 1.

    Returns:
    numpy.ndarray: Convolved vector as a numpy array.
    """
    if not isinstance(vector, (list, tuple, np.ndarray)):
        raise TypeError("vector must be a list, tuple, or numpy array")
    if not isinstance(window_size, int) or window_size <= 0:
        raise ValueError("window_size must be a positive integer")
    if len(vector) < window_size:
        raise ValueError("window_size must not be greater than the length of vector")
    if factor == 0:
        raise ValueError("factor must not be zero")

    return np.convolve(vector, np.ones(window_size), mode='same') / window_size


def oncosplice(mut_id, sai_threshold=0.5, protein_coding=True, primary_transcript=False):
    mutation = Variations(mut_id)
    reference_gene = Gene(mutation.gene)
    mutated_gene = Gene(mutation.gene, mut_id)

    results = []
    for variant in mutated_gene.run_transcripts(protein_coding=protein_coding, primary_transcript=primary_transcript):
        reference = reference_gene.transcript(variant.transcript_id)
        if reference.cons_available:
            cons_vector = transform_conservation_vector(reference.cons_vector)

        missplicing = run_spliceai_transcript(mutation, reference, sai_threshold=sai_threshold)
        for i, new_boundaries in enumerate(develop_aberrant_splicing(variant, missplicing)):
            variant_isoform = deepcopy(variant)
            variant_isoform.set_intron_boundaries(acceptors=new_boundaries['acceptors'],
                                                  donors=new_boundaries['donors']).generate_protein()
            alignment = get_logical_alignment(reference.protein, variant_isoform.protein)
            deleted, inserted = find_indels_with_mismatches_as_deletions(alignment.seqA, alignment.seqB)
            modified_positions = find_modified_positions(len(cons_vector), deleted, inserted)
            temp_cons = np.convolve(cons_vector * modified_positions, np.ones(11))
            affected_cons_scores = max(temp_cons)
            temp_cons = np.convolve(cons_vector, np.ones(11))
            percentile = (
                        sorted(temp_cons).index(next(x for x in sorted(temp_cons) if x >= affected_cons_scores)) / len(
                    temp_cons))

            report = OncospliceAnnotator(reference, variant_isoform, mutation)
            report['original_cons'] = reference.cons_vector
            report['oncosplice_score'] = affected_cons_scores
            report['percentile'] = percentile
            report['modified_positions'] = modified_positions
            report['cons_vector'] = cons_vector
            report['isoform_id'] = i
            report['isoform_prevalence'] = new_boundaries['path_weight']
            report['full_missplicing'] = missplicing
            results.append(report)

    report = pd.DataFrame(results)
    return report


# import numpy as np
# import pandas as pd
# from Bio import pairwise2
# import re
# from copy import deepcopy
# from geney.splicing import PredictSpliceAI
# from .Gene import Gene, Transcript
# from geney.mutations.variant_utils import Variations, develop_aberrant_splicing
#
# sample_mut_id = 'KRAS:12:25227343:G:T'
# sample_epistasis_id = 'KRAS:12:25227343:G:T|KRAS:13:25227344:A:T'
#
# def oncosplice(mutation: str, sai_threshold=0.25, annotate=False) -> pd.DataFrame:
#     '''
#         :param mutation: str
#                         the genomic variation
#         :param sai_threshold: float
#                         the threshold for including missplicing predictions in gene builds
#         :param prevalence_threshold: float
#                         the minimum threshold needed to consider a predicted isoform as valid
#         :param target_directory: pathlib.Path
#                         the directory on the machine where the mrna annotation files are stored
#         :return: a dataframe object
#                 will contain columns pertinant to assessing mutation pathogenicity including pipelines score, GOF score, legacy pipelines score, missplicing,
#     '''
#
#     mutation = Variations(mutation)                                                         # Generate mutation object
#                                                                                             # Gene annotations should be available in the target directory under the file name mrna_gene.json
#     gene = Gene(mutation.gene)                                                              # We obtain the annotation file and convert it into a Gene object
#     # aberrant_splicing = PredictSpliceAI(mutation, gene, threshold=sai_threshold)            # SpliceAI predictions are processed and obtained for each mutation
#     # Oncosplice obtains predictions for each transcript in the annotation file
#
#     results = []
#     for reference_transcript in gene:
#         aberrant_splicing = PredictSpliceAI(mutation, reference_transcript, threshold=sai_threshold)
#         for i, new_boundaries in develop_aberrant_splicing(reference_transcript, aberrant_splicing.aberrant_splicing):
#             res_in = oncosplice_transcript(reference_transcript=reference_transcript.generate_protein(), mutation=mutation, aberrant_splicing=aberrant_splicing, annotate=annotate, plot_term=plot_term)
#             results.append(res_in)
#
#     if len(results) > 0:
#         results = pd.concat(results)
#     else:
#         return None
#
#     # Append some additional, uniform information to the results dataframe
#     results['mut_id'] = mutation.mut_id
#     results['missplicing'] = aberrant_splicing.get_max_missplicing_delta()
#     results['gene'] = mutation.gene
#     return results
#
#
# def oncosplice_transcript(reference_transcript: Transcript, mutation: Variations, aberrant_splicing: PredictSpliceAI, annotate=False, plot_term=False) -> pd.DataFrame:
#     reports = []
#     if reference_transcript.cons_available:
#         cons_available, cons_array, cons_vector = True, transform_conservation_vector(reference_transcript.cons_vector), reference_transcript.cons_vector
#
#     else:
#         cons_available, cons_array, cons_vector = False, transform_conservation_vector(np.ones(len(reference_transcript.protein), dtype=float)), np.ones(len(reference_transcript.protein), dtype=float)
#
#     # For each transcript, we generate a series of isoforms based on the splice site predictions; each isoform is assigned a prevalence score
#     # obtained using simple graph theory where the probability of the edges taken to generate the isoform are multiplied together
#     for i, new_boundaries in enumerate(develop_aberrant_splicing(reference_transcript, aberrant_splicing.aberrant_splicing)):
#
#         # The variant transcript is duplicated from the reference transcript and all needed modifications are performed
#         variant_transcript = Transcript(deepcopy(reference_transcript).__dict__).set_exons(new_boundaries).generate_mature_mrna(mutations=mutation.mut_id.split('|'), inplace=True).generate_translational_boundaries().generate_protein()
#
#         # The optimal alignment that minimizes gaps between the trnascripts is obtained
#         alignment = get_logical_alignment(reference_transcript.protein, variant_transcript.protein)
#
#         # Based on the optimal alignment, we can generate the relative locations of insertions and deletions
#         deleted, inserted = find_indels_with_mismatches_as_deletions(alignment.seqA, alignment.seqB)
#
#         report = {
#             'log': variant_transcript.log,
#             'isoform': i,
#             'isoform_prevalence': new_boundaries['path_weight'],
#             'legacy_oncosplice_score_long': calculate_legacy_oncosplice_score(deleted, inserted, cons_vector,
#                                                       min(76, len(reference_transcript.protein))),
#             'legacy_oncosplice_score_short': calculate_legacy_oncosplice_score(deleted, inserted, cons_vector,
#                                                                               min(10,
#                                                                                   len(reference_transcript.protein))),
#             'variant_length': len(variant_transcript.protein.replace('*', '')),
#         }
#
#         modified_positions = find_modified_positions(len(cons_vector), deleted, inserted)
#         # print(list(modified_positions))
#         # print(list(cons_array))
#         affected_cons_scores = cons_array.transpose() @ modified_positions[:, None]
#         # print(list(affected_cons_scores)) #[:, 0]))
#         # affected_cons_scores = sg.convolve2d(affected_cons_scores, np.ones(21), mode='same') #/ 21
#         max_score = affected_cons_scores #np.max(affected_cons_scores, axis=0)
#         report.update({'oncosplice_score': max_score, 'preserved_ratio': sum(modified_positions) / len(modified_positions)})
#
#         if annotate:
#             report.update(OncospliceAnnotator(reference_transcript, variant_transcript, mutation))
#             report['insertions'] = inserted
#             report['deletions'] = deleted
#             report['full_missplicing'] = aberrant_splicing.missplicing
#         reports.append(report)
#
#     reports = pd.DataFrame(reports)
#     reports['cons_available'] = int(cons_available)
#     reports['transcript_id'] = reference_transcript.transcript_id
#     reports['cons_sum'] = np.sum(np.exp(np.negative(cons_vector)))
#     reports['transcript_length'] = len(reference_transcript.protein)
#     reports['primary_transcript'] = reference_transcript.primary_transcript
#     return reports
#
#
# def oncosplice_reduced(df):
#     target_columns = [c for c in df.columns if 'oncosplice' in c or 'cons' in c]
#     if len(target_columns) == 0:
#         print("No oncosplice scores to reduce.")
#         return None
#     scores = [df[['mut_id', 'missplicing']].drop_duplicates().set_index('mut_id')]
#     for score in target_columns:
#         scores.append(df.groupby(['mut_id', 'transcript_id'])[score].mean().groupby('mut_id').max())
#         scores.append(df.groupby(['mut_id', 'transcript_id'])[score].mean().groupby('mut_id').min())
#     scores = pd.concat(scores, axis=1)
#     return scores
#
#
# def find_continuous_gaps(sequence):
#     """Find continuous gap sequences in an alignment."""
#     return [(m.start(), m.end()) for m in re.finditer(r'-+', sequence)]
#
#
# def get_logical_alignment(ref_prot, var_prot):
#     """
#     Aligns two protein sequences and finds the optimal alignment with the least number of gaps.
#
#     Parameters:
#     ref_prot (str): Reference protein sequence.
#     var_prot (str): Variant protein sequence.
#
#     Returns:
#     tuple: Optimal alignment, number of insertions, and number of deletions.
#     """
#
#     # Perform global alignment
#     alignments = pairwise2.align.globalms(ref_prot, var_prot, 1, -1, -3, 0, penalize_end_gaps=(True, True))
#
#     # Selecting the optimal alignment
#     if len(alignments) > 1:
#         # Calculate continuous gaps for each alignment and sum their lengths
#         gap_lengths = [sum(end - start for start, end in find_continuous_gaps(al.seqA) + find_continuous_gaps(al.seqB)) for al in alignments]
#         optimal_alignment = alignments[gap_lengths.index(min(gap_lengths))]
#     else:
#         optimal_alignment = alignments[0]
#
#     return optimal_alignment
#
#
# def find_indels_with_mismatches_as_deletions(seqA, seqB):
#     """
#     Identify insertions and deletions in aligned sequences, treating mismatches as deletions.
#
#     Parameters:
#     seqA, seqB (str): Aligned sequences.
#
#     Returns:
#     tuple: Two dictionaries containing deletions and insertions.
#     """
#     if len(seqA) != len(seqB):
#         raise ValueError("Sequences must be of the same length")
#
#     mapperA, counter = {}, 0
#     for i, c in enumerate(list(seqA)):
#         if c != '-':
#             counter += 1
#         mapperA[i] = counter
#
#     mapperB, counter = {}, 0
#     for i, (c1, c2) in enumerate(list(zip(seqA, seqB))):
#         if c2 != '-':
#             counter += 1
#         mapperB[i] = counter
#
#     seqA_array, seqB_array = np.array(list(seqA)), np.array(list(seqB))
#
#     # Find and mark mismatch positions in seqB
#     mismatches = (seqA_array != seqB_array) & (seqA_array != '-') & (seqB_array != '-')
#     seqB_array[mismatches] = '-'
#     modified_seqB = ''.join(seqB_array)
#
#     gaps_in_A = find_continuous_gaps(seqA)
#     gaps_in_B = find_continuous_gaps(modified_seqB)
#
#     insertions = {mapperB[start]: modified_seqB[start:end].replace('-', '') for start, end in gaps_in_A if
#                   seqB[start:end].strip('-')}
#     deletions = {mapperA[start]: seqA[start:end].replace('-', '') for start, end in gaps_in_B if
#                  seqA[start:end].strip('-')}
#     return deletions, insertions
#
#
#
# def parabolic_window(window_size):
#     """Create a parabolic window function with a peak at the center."""
#     x = np.linspace(-1, 1, window_size)
#     return 0.9 * (1 - x**2) + 0.1
#
#
# # def calculate_window_size(conservation_vector_length):
# #     return int(9 + (51 - 9) * (1 - np.exp(-0.0005 * conservation_vector_length)))
# #
#
#
# def transform_conservation_vector(conservation_vector):
#     """
#     Transforms a 1D conservation vector using different parameters.
#
#     Args:
#         conservation_vector (numpy.ndarray): Input 1D vector of conservation values.
#
#     Returns:
#         numpy.ndarray: A matrix containing transformed vectors.
#     """
#     window = 21
#     factor = 0.5
#     convolving_window = parabolic_window(window)
#     transformed_vector = np.convolve(conservation_vector, convolving_window, mode='same') / np.sum(convolving_window)
#     # Compute exponential factors
#     exp_factors = np.exp(-transformed_vector * factor)
#
#     # Normalize and scale exponential factors
#     exp_factors /= exp_factors.sum()
#     return exp_factors
#
#
#
# def find_modified_positions(sequence_length, deletions, insertions, reach_limit=16):
#     """
#     Identify unmodified positions in a sequence given deletions and insertions.
#
#     :param sequence_length: Length of the sequence.
#     :param deletions: Dictionary of deletions.
#     :param insertions: Dictionary of insertions.
#     :param reach_limit: Limit for considering the effect of insertions/deletions.
#     :return: Array indicating unmodified positions.
#     """
#     unmodified_positions = np.zeros(sequence_length, dtype=float)
#
#     for pos, insertion in insertions.items():
#         # if pos >= sequence_length:
#         #     pos = sequence_length - 1
#         #     add_factor = 1
#
#         reach = min(len(insertion) // 2, reach_limit)
#         front_end, back_end = max(0, pos - reach), min(sequence_length - 1, pos + reach)
#         len_start, len_end = pos - front_end, back_end - pos
#         try:
#             gradient_front = np.linspace(0, 1, len_start, endpoint=False)
#             gradient_back = np.linspace(0, 1, len_end, endpoint=True)[::-1]
#             combined_gradient = np.concatenate([gradient_front, np.array([1]), gradient_back])
#             unmodified_positions[front_end:back_end + 1] = combined_gradient
#
#         except ValueError as e:
#             print(
#                 f"Error: {e} | Lengths: unmodified_positions_slice={back_end - front_end}, combined_gradient={len(combined_gradient)}")
#             unmodified_positions[front_end:back_end] = np.zeros(back_end - front_end)
#
#     for pos, deletion in deletions.items():
#         deletion_length = len(deletion)
#         unmodified_positions[pos:pos + deletion_length] = 1
#
#     return unmodified_positions
#
#
#
# def calculate_penalty(domains, cons_scores, W, is_insertion=False):
#     """
#     Calculate the penalty for mutations (either insertions or deletions) on conservation scores.
#
#     :param domains: Dictionary of mutations (inserted or deleted domains).
#     :param cons_scores: Conservation scores.
#     :param W: Window size.
#     :param is_insertion: Boolean flag to indicate if the mutation is an insertion.
#     :return: Penalty array.
#     """
#     penalty = np.zeros(len(cons_scores))
#     for pos, seq in domains.items():
#         mutation_length = len(seq)
#         weight = max(1.0, mutation_length / W)
#
#         if is_insertion:
#             reach = min(W // 2, mutation_length // 2)
#             penalty[pos - reach:pos + reach] = weight * cons_scores[pos - reach:pos + reach]
#         else:  # For deletion
#             penalty[pos:pos + mutation_length] = cons_scores[pos:pos + mutation_length] * weight
#
#     return penalty
#
#
# def calculate_legacy_oncosplice_score(deletions, insertions, cons_vec, W):
#     """
#     Calculate the legacy Oncosplice score based on deletions, insertions, and conservation vector.
#
#     :param deletions: Dictionary of deletions.
#     :param insertions: Dictionary of insertions.
#     :param cons_vec: Conservation vector.
#     :param W: Window size.
#     :return: Legacy Oncosplice score.
#     """
#     smoothed_conservation_vector = np.exp(np.negative(moving_average_conv(cons_vec, W, 2)))
#     del_penalty = calculate_penalty(deletions, smoothed_conservation_vector, W, is_insertion=False)
#     ins_penalty = calculate_penalty(insertions, smoothed_conservation_vector, W, is_insertion=True)
#     combined_scores = del_penalty + ins_penalty
#     return np.max(np.convolve(combined_scores, np.ones(W), mode='same'))
#
#
# def moving_average_conv(vector, window_size, factor=1):
#     """
#     Calculate the moving average convolution of a vector.
#
#     Parameters:
#     vector (iterable): Input vector (list, tuple, numpy array).
#     window_size (int): Size of the convolution window. Must be a positive integer.
#     factor (float): Scaling factor for the average. Default is 1.
#
#     Returns:
#     numpy.ndarray: Convolved vector as a numpy array.
#     """
#     if not isinstance(vector, (list, tuple, np.ndarray)):
#         raise TypeError("vector must be a list, tuple, or numpy array")
#     if not isinstance(window_size, int) or window_size <= 0:
#         raise ValueError("window_size must be a positive integer")
#     if len(vector) < window_size:
#         raise ValueError("window_size must not be greater than the length of vector")
#     if factor == 0:
#         raise ValueError("factor must not be zero")
#
#     return np.convolve(vector, np.ones(window_size), mode='same') / window_size
#
#
# def OncospliceAnnotator(reference_transcript, variant_transcript, mut):
#     affected_exon, affected_intron, distance_from_5, distance_from_3 = find_splice_site_proximity(mut, reference_transcript)
#
#     report = {}
#     report['reference_mRNA'] = reference_transcript.transcript_seq
#     report['reference_CDS_start'] = reference_transcript.TIS
#     report['reference_pre_mrna'] = reference_transcript.pre_mrna
#     report['reference_ORF'] = reference_transcript.orf #pre_mrna[reference_transcript.transcript_indices.index(reference_transcript.TIS):reference_transcript.transcript_indices.index(reference_transcript.TTS)]
#     report['reference_protein'] = reference_transcript.protein
#
#     report['variant_mRNA'] = variant_transcript.transcript_seq
#     report['variant_CDS_start'] = variant_transcript.TIS
#     report['variant_pre_mrna'] = variant_transcript.pre_mrna #pre_mrna[variant_transcript.transcript_indices.index(variant_transcript.TIS):variant_transcript.transcript_indices.index(variant_transcript.TTS)]
#     report['variant_ORF'] = variant_transcript.orf
#     report['variant_protein'] = variant_transcript.protein
#
#     descriptions = define_missplicing_events(reference_transcript.exons, variant_transcript.exons,
#                               reference_transcript.rev)
#     report['exon_changes'] = '|'.join([v for v in descriptions if v])
#     report['splicing_codes'] = summarize_missplicing_event(*descriptions)
#     report['affected_exon'] = affected_exon
#     report['affected_intron'] = affected_intron
#     report['mutation_distance_from_5'] = distance_from_5
#     report['mutation_distance_from_3'] = distance_from_3
#     return report
#
#
# def find_splice_site_proximity(mut, transcript):
#     affected_exon, affected_intron, distance_from_5, distance_from_3 = None, None, None, None
#     for i, (ex_start, ex_end) in enumerate(transcript.exons):
#         if min(ex_start, ex_end) <= mut.start <= max(ex_start, ex_end):
#             affected_exon = i + 1
#             distance_from_5 = abs(mut.start - ex_start)
#             distance_from_3 = abs(mut.start - ex_end)
#
#     for i, (in_start, in_end) in enumerate(transcript.introns):
#         if min(in_start, in_end) <= mut.start <= max(in_start, in_end):
#             affected_intron = i + 1
#             distance_from_5 = abs(mut.start - in_end)
#             distance_from_3 = abs(mut.start - in_start)
#
#     return affected_exon, affected_intron, distance_from_5, distance_from_3
#
#
# def define_missplicing_events(ref_exons, var_exons, rev):
#     ref_introns = [(ref_exons[i][1], ref_exons[i + 1][0]) for i in range(len(ref_exons) - 1)]
#     var_introns = [(var_exons[i][1], var_exons[i + 1][0]) for i in range(len(var_exons) - 1)]
#     num_ref_exons = len(ref_exons)
#     num_ref_introns = len(ref_introns)
#     if not rev:
#         partial_exon_skipping = ','.join(
#             [f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}' for (s1, s2) in var_exons for
#              exon_count, (t1, t2) in enumerate(ref_exons) if (s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)])
#         partial_intron_retention = ','.join(
#             [f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}' for (s1, s2)
#              in var_introns for intron_count, (t1, t2) in enumerate(ref_introns) if
#              (s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)])
#
#     else:
#         partial_exon_skipping = ','.join(
#             [f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}' for (s1, s2) in var_exons for
#              exon_count, (t1, t2) in enumerate(ref_exons) if (s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)])
#         partial_intron_retention = ','.join(
#             [f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}' for (s1, s2)
#              in var_introns for intron_count, (t1, t2) in enumerate(ref_introns) if
#              (s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)])
#
#     exon_skipping = ','.join(
#         [f'Exon {exon_count + 1}/{num_ref_exons} skipped: {(t1, t2)}' for exon_count, (t1, t2) in enumerate(ref_exons)
#          if
#          t1 not in [s1 for s1, s2 in var_exons] and t2 not in [s2 for s1, s2 in var_exons]])
#     novel_exons = ','.join([f'Novel Exon: {(t1, t2)}' for (t1, t2) in var_exons if
#                             t1 not in [s1 for s1, s2 in ref_exons] and t2 not in [s2 for s1, s2 in ref_exons]])
#     intron_retention = ','.join(
#         [f'Intron {intron_count + 1}/{num_ref_introns} retained: {(t1, t2)}' for intron_count, (t1, t2) in
#          enumerate(ref_introns) if
#          t1 not in [s1 for s1, s2 in var_introns] and t2 not in [s2 for s1, s2 in var_introns]])
#
#     return partial_exon_skipping, partial_intron_retention, exon_skipping, novel_exons, intron_retention
#
#
# def summarize_missplicing_event(pes, pir, es, ne, ir):
#     event = []
#     if pes:
#         event.append('PES')
#     if es:
#         event.append('ES')
#     if pir:
#         event.append('PIR')
#     if ir:
#         event.append('IR')
#     if ne:
#         event.append('NE')
#     if len(event) > 1:
#         return event
#     elif len(event) == 1:
#         return event[0]
#     else:
#         return '-'
#



# def find_indels_with_mismatches_as_deletions(seqA, seqB):
#     # Convert sequences to numpy arrays for element-wise comparison
#     ta, tb = np.array(list(seqA)), np.array(list(seqB))
#
#     # Find mismatch positions
#     mismatch_positions = (ta != tb) & (ta != '-') & (tb != '-')
#
#     # Replace mismatch positions in seqB with '-'
#     tb[mismatch_positions] = '-'
#     modified_seqB = ''.join(tb)
#
#     # Function to find continuous gaps using regex
#     def find_continuous_gaps(sequence):
#         return [(m.start(), m.end()) for m in re.finditer(r'-+', sequence)]
#
#     # Find gaps in both sequences
#     gaps_in_A = find_continuous_gaps(seqA)
#     gaps_in_B = find_continuous_gaps(modified_seqB)
#
#     # Identify insertions and deletions
#     insertions = {start: modified_seqB[start:end].replace('-', '') for start, end in gaps_in_A if
#                   seqB[start:end].strip('-')}
#     deletions = {start: seqA[start:end].replace('-', '') for start, end in gaps_in_B if seqA[start:end].strip('-')}
#
#     return deletions, insertions



# def moving_average_conv(vector, window_size, factor=1):
#     """
#     Calculate the moving average convolution of a vector.
#
#     :param vector: Input vector.
#     :param window_size: Size of the convolution window.
#     :return: Convolved vector as a numpy array.
#     """
#     convolving_length = np.array([min(len(vector) + window_size - i, window_size, i)
#                                   for i in range(window_size // 2, len(vector) + window_size // 2)], dtype=float)
#
#     return np.convolve(vector, np.ones(window_size), mode='same') / (convolving_length / factor)
#


# def get_logical_alignment(ref_prot, var_prot):
#     '''
#     :param ref_prot:
#     :param var_prot:
#     :return:
#     '''
#
#     alignments = pairwise2.align.globalms(ref_prot, var_prot, 1, -1, -3, 0, penalize_end_gaps=(True, False))
#     if len(alignments) == 1:
#         optimal_alignment = alignments[0]
#     else:
#         # This calculates the number of gaps in each alignment.
#         number_of_gaps = [re.sub('-+', '-', al.seqA).count('-') + re.sub('-+', '-', al.seqB).count('-') for al in
#                           alignments]
#
#         optimal_alignment = alignments[number_of_gaps.index(min(number_of_gaps))]
#
#     num_insertions = re.sub('-+', '-', optimal_alignment.seqA).count('-')
#     num_deletions = re.sub('-+', '-', optimal_alignment.seqB).count('-')
#     return optimal_alignment
#


# def transform_conservation_vector(conservation_vector, window_size=10, verbose=False):
#     """
#     Transforms a conservation vector by applying a moving average convolution and scaling.
#
#     :param conservation_vector: Array of conservation scores.
#     :param window_size: Window size for the moving average convolution. Defaults to 10, the average binding site length.
#     :return: Transformed conservation vector.
#     """
#     factor = 100 / window_size
#     conservation_vector = moving_average_conv(conservation_vector, window_size)
#     transformed_vector = np.exp(-conservation_vector*factor)
#     transformed_vector = transformed_vector / max(transformed_vector)
#
#     if verbose:
#         import asciiplotlib as apl
#         fig = apl.figure()
#         fig.plot(list(range(len(transformed_vector))), transformed_vector, width=50, height=15, title="Conservation Vector")
#         fig.plot(list(range(len(conservation_vector))), transformed_vector, width=50, height=15, title="Entropy Vector")
#         fig.show()
#
#     return transformed_vector

# def oncosplice_report(modified_positions, cons_matrix, tplot=False):
#     """
#     Calculate pipelines scores based on conservation vectors and detected sequence modifications.
#
#     :param deletions: Dictionary of deletions in the sequence.
#     :param insertions: Dictionary of insertions in the sequence.
#     :param cons_vector: Conservation vector.
#     :param window_size: Window size for calculations.
#     :return: Dictionary of pipelines scores.
#     """
#     window_size = calculate_window_size(cons_matrix.shape[0])
#     # cons_vec_one, cons_vec_two, cons_vec_three = transform_conservation_vector(cons_matrix, tplot=tplot)
#     # results = {}
#
#     # for i, cons_vec in enumerate([cons_vec_one, cons_vec_two, cons_vec_three]):
#     affected_cons_scores = cons_matrix * modified_positions
#     # affected_sum = np.sum(affected_cons_scores)
#     modified_cons_vector = np.convolve(affected_cons_scores, np.ones(window_size), mode='same') / window_size
#
#     # obtaining scores
#     max_score = np.max(modified_cons_vector)
#     results = np.where(modified_cons_vector == max_score)[0]
#
#     # # Exclude windows within one window_size of the max scoring window
#     # exclusion_zone = set().union(*(range(max(i - window_size, 0), min(i + window_size, len(modified_cons_vector))) for i in max_score_indices))
#     # viable_secondary_scores = [score for i, score in enumerate(modified_cons_vector) if i not in exclusion_zone]
#     #
#     # if len(viable_secondary_scores) == 0:
#     #     gof_prob = 0
#     #
#     # else:
#     #     second_highest_score = np.max(viable_secondary_scores)
#     #     gof_prob = (max_score - second_highest_score) / max_score
#     # temp = {f'gof_{i}': gof_prob, f'oncosplice_score_{i}': max_score, f'affected_cons_sum_{i}': affected_sum}
#     # results.update(temp)
#     return results



# def transform_conservation_vector(conservation_vector, plot=False, tplot=False, tid=''):
#     # all_ones = np.all(conservation_vector == 1)
#     # if all_ones:
#     #     return conservation_vector, conservation_vector, conservation_vector
#
#     # Calculate dynamic window size
#     window_size = calculate_window_size(len(conservation_vector))
#
#     if window_size > len(conservation_vector):
#         window_size = int(len(conservation_vector) / 2)
#
#     # Create convolution window and transform vector
#     convolving_window = parabolic_window(window_size)
#     factor = int(100 / window_size)
#     transformed_vector = np.convolve(conservation_vector, convolving_window, mode='same') / sum(convolving_window)
#     transformed_vector = np.exp(-transformed_vector * factor)
#     transformed_vector_one = transformed_vector.copy()
#
#     transformed_vector -= np.percentile(transformed_vector, 75)
#     transformed_vector_two = transformed_vector.copy()
#
#     max_val = max(transformed_vector)
#     transformed_vector /= max_val
#
#     # Balancing negative values
#     negative_values = transformed_vector[transformed_vector < 0]
#     if negative_values.size > 0:
#         balance_factor = -np.sum(transformed_vector[transformed_vector >= 0]) / np.sum(negative_values)
#         transformed_vector[transformed_vector < 0] *= balance_factor
#
#     current_sum = np.sum(transformed_vector)
#     additional_amount_needed = len(transformed_vector) - current_sum
#     sum_positives = np.sum(transformed_vector[transformed_vector > 0])
#     if sum_positives == 0:
#         raise ValueError("Array contains no positive values to scale.")
#     scale_factor = 1 + (additional_amount_needed / sum_positives)
#     # Apply the scaling factor only to positive values
#     transformed_vector[transformed_vector > 0] *= scale_factor
#
#
#     # if plot:
#     #     # Plotting the two vectors
#     #     fig, ax1 = plt.subplots(figsize=(8, 4))
#     #     color = 'tab:blue'
#     #     ax1.set_xlabel('Position')
#     #     ax1.set_ylabel('Conservation Vector', color=color, alpha=0.5)
#     #     ax1.plot(conservation_vector, color=color)
#     #     ax1.tick_params(axis='y', labelcolor=color)
#     #
#     #     ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#     #     color = 'tab:red'
#     #     ax2.set_ylabel('Transformed Vector', color=color)  # we already handled the x-label with ax1
#     #     ax2.plot(transformed_vector, color=color)
#     #     ax2.tick_params(axis='y', labelcolor=color)
#     #     plt.axhline(0)
#     #     plt.title(tid)
#     #     fig.tight_layout()  # otherwise the right y-label is slightly clipped
#     #     plt.show()
#     #
#     # if tplot:
#     #     import termplotlib as tpl
#     #     fig = tpl.figure()
#     #     fig.plot(list(range(len(conservation_vector))), conservation_vector, width=100, height=15)
#     #     fig.plot(list(range(len(transformed_vector))), transformed_vector, width=100, height=15)
#     #     fig.show()
#
#     return transformed_vector_one, transformed_vector_two, transformed_vector


