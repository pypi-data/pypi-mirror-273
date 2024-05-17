from geney.utils import reverse_complement, find_files_by_gene_name, unload_json, dump_json, unload_pickle
from geney.Fasta_segment import Fasta_segment
from geney.mutations.variant_utils import generate_mut_variant
from geney import config_setup
import networkx as nx
import random
from dataclasses import dataclass

'''
SpliceAI util functions.
'''
import numpy as np
import tensorflow as tf
from keras.models import load_model
from pkg_resources import resource_filename
from spliceai.utils import one_hot_encode

tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

sai_paths = ('models/spliceai{}.h5'.format(x) for x in range(1, 6))
sai_models = [load_model(resource_filename('spliceai', x)) for x in sai_paths]

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
    return y[0,:,1:].T


def get_actual_sai_seq(seq: str, sai_mrg_context: int=5000) -> str:
    '''
    This dfunction assumes that the input seq has the following structure:

         seq = |<sai_mrg_context NTs><L NTs><sai_mrg_context NTs>|.

    Then, the function returns the sequence: |<L NTs>|
    '''
    return seq[sai_mrg_context:-sai_mrg_context]


############################################################################################
############################################################################################
############# BEGIN CUSTOM SAI USE CASES ###################################################
############################################################################################
############################################################################################


def find_ss_changes(ref_dct, mut_dct, known_splice_sites, threshold=0.5):
    '''
    :param ref_dct:  the spliceai probabilities for each nucleotide (by genomic position) as a dictionary for the reference sequence
    :param mut_dct:  the spliceai probabilities for each nucleotide (by genomic position) as a dictionary for the mutated sequence
    :param known_splice_sites: the indices (by genomic position) that serve as known splice sites
    :param threshold: the threshold for detection (difference between reference and mutated probabilities)
    :return: two dictionaries; discovered_pos is a dictionary containing all the positions that meat the threshold for discovery
            and deleted_pos containing all the positions that meet the threshold for missing and the condition for missing
    '''

    new_dict = {v: mut_dct.get(v, 0) - ref_dct.get(v, 0) for v in
                list(set(list(ref_dct.keys()) + list(mut_dct.keys())))}

    discovered_pos = {k: {'delta': round(float(v), 3), 'absolute': round(float(mut_dct[k]), 3)} for k, v in
                      new_dict.items() if (k not in known_splice_sites and v >= threshold) or (v > 0.45)}

    deleted_pos = {k: {'delta': round(float(v), 3), 'absolute': round(float(mut_dct.get(k, 0)), 3)} for k, v in
                   new_dict.items() if k in known_splice_sites and v <= -threshold}


    return discovered_pos, deleted_pos


def run_spliceai(mutations, gene_data, sai_mrg_context=5000, min_coverage=2500, sai_threshold=0.5):
    positions = mutations.positions #[m.start for m in mutations]
    seq_start_pos = min(positions) - sai_mrg_context - min_coverage
    seq_end_pos = max(positions) + sai_mrg_context + min_coverage  # + 1

    # ref_seq, ref_indices = pull_fasta_seq_endpoints(mutations.chrom, seq_start_pos, seq_end_pos)
    fasta_obj = Fasta_segment()
    ref_seq, ref_indices = fasta_obj.read_segment_endpoints(config_setup['CHROM_SOURCE'] / f'chr{mutations.chrom}.fasta',
                                                seq_start_pos,
                                                seq_end_pos)


    # gene_data = unload_pickle(
    #     find_files_by_gene_name(gene_name=mutations.gene))
    gene_start, gene_end, rev = gene_data.gene_start, gene_data.gene_end, gene_data.rev

    mrna_acceptors = sorted(list(set([lst for lsts in
                                      [mrna.get('acceptors', []) for mrna in gene_data.transcripts.values() if
                                       mrna['transcript_biotype'] == 'protein_coding'] for lst in lsts])))
    mrna_donors = sorted(list(set([lst for lsts in
                                   [mrna.get('donors', []) for mrna in gene_data.transcripts.values() if
                                    mrna['transcript_biotype'] == 'protein_coding'] for lst in lsts])))

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



class PredictSpliceAI:
    def __init__(self, mutation, gene_data, threshold=0.5, force=False, sai_mrg_context=5000, min_coverage=2500):
        self.modification = mutation
        self.threshold = threshold

        # if '|' in mutation.mut_id:
        self.spliceai_db = config_setup['MISSPLICING_PATH'] / f'spliceai_epistatic'
        # else:
        #     self.spliceai_db = config_setup['MISSPLICING_PATH'] / f'spliceai_individual'

        self.missplicing = {}

        if self.prediction_file_exists() and not force:
            self.missplicing = self.load_sai_predictions()

        else:
            self.missplicing = run_spliceai(self.modification, gene_data=gene_data, sai_mrg_context=sai_mrg_context, min_coverage=min_coverage, sai_threshold=0.1)
            self.save_sai_predictions()

    def __repr__(self):
        return f'Missplicing({self.modification.mut_id}) --> {self.missplicing}'

    def __str__(self):
        return self.aberrant_splicing
    def __bool__(self):
        for event, details in self.aberrant_splicing.items():
            if details:
                return True
        return False

    def __eq__(self, alt_splicing):
        flag, _ = check_splicing_difference(self.missplicing, alt_splicing, self.threshold)
        return not flag

    @property
    def aberrant_splicing(self):
        return self.apply_sai_threshold(self.missplicing, self.threshold)

    @property
    def prediction_file(self):
        return self.spliceai_db / self.modification.gene / self.modification.file_identifier_json

    def prediction_file_exists(self):
        return self.prediction_file.exists()

    def load_sai_predictions(self):
        missplicing = unload_json(self.prediction_file)
        missplicing = {outk: {float(k): v for k, v in outv.items()} for outk, outv in missplicing.items()}
        missplicing = {outk: {int(k) if k.is_integer() or 'missed' in outk else k: v for k, v in outv.items()} for
                       outk, outv in
                       missplicing.items()}
        return missplicing

    def save_sai_predictions(self):
        self.prediction_file.parent.mkdir(parents=True, exist_ok=True)
        dump_json(self.prediction_file, self.missplicing)
    def apply_sai_threshold(self, splicing_dict=None, threshold=None):
        splicing_dict = self.missplicing if not splicing_dict else splicing_dict
        threshold = self.threshold if not threshold else threshold
        new_dict = {}
        for event, details in splicing_dict.items():
            for e, d in details.items():
                if abs(d['delta']) >= threshold:
                    return splicing_dict
            new_dict[event] = {}        #{k: v for k, v in details.items() if abs(v['delta']) >= threshold}
        return new_dict

    def get_max_missplicing_delta(self):
        max_delta = 0
        for event, details in self.missplicing.items():
            for e, d in details.items():
                if abs(d['delta']) > max_delta:
                    max_delta = abs(d['delta'])
        return max_delta

def check_splicing_difference(missplicing1, missplicing2, threshold=None):
    flag = False
    true_differences = {}
    for event in ['missed_acceptors', 'missed_donors']:
        td = {}
        dct1 = missplicing1[event]
        dct2 = missplicing2[event]
        for k in list(set(list(dct1.keys()) + list(dct2.keys()))):
            diff = abs(dct1.get(k, {'delta': 0})['delta']) - abs(dct2.get(k, {'delta': 0})['delta'])
            if abs(diff) >= threshold:
                flag = True
                td[k] = diff
        true_differences[event] = td
    for event in ['discovered_acceptors', 'discovered_donors']:
        td = {}
        dct1 = missplicing1[event]
        dct2 = missplicing2[event]
        for k in list(set(list(dct1.keys()) + list(dct2.keys()))):
            diff = abs(dct1.get(k, {'delta': 0})['delta']) - abs(dct2.get(k, {'delta': 0})['delta'])
            if abs(diff) >= threshold:
                flag = True
                td[k] = diff
        true_differences[event] = td
    return flag, true_differences




def develop_aberrant_splicing(transcript, aberrant_splicing):
    boundaries = [lst for lsts in [[a, b] for a, b in transcript.exons] for lst in lsts]
    exon_starts, exon_ends = list(zip(*transcript.exons))
    transcript_start, transcript_end = exon_starts[0], exon_ends[-1]
    next_exon_end = exon_ends[-2]
    rev = transcript.rev
    upper_range, lower_range = max(boundaries), min(boundaries)
    exon_starts = {v: 1 for v in exon_starts}
    exon_ends = {v: 1 for v in exon_ends}
    for k, v in aberrant_splicing.get('missed_donors', {}).items():
        if k in exon_ends.keys():
            exon_ends[k] = max(v['absolute'], 0.001)
    exon_ends.update(
        {k: v['absolute'] for k, v in aberrant_splicing.get('discovered_donors', {}).items() if lower_range <= k <= upper_range})
    for k, v in aberrant_splicing.get('missed_acceptors', {}).items():
        if k in exon_starts.keys():
            exon_starts[k] = max(v['absolute'], 0.001)
    exon_starts.update(
        {k: v['absolute'] for k, v in aberrant_splicing.get('discovered_acceptors', {}).items() if lower_range <= k <= upper_range})
    nodes = [SpliceSite(pos=pos, ss_type=0, prob=prob) for pos, prob in exon_ends.items() if
             lower_range <= pos <= upper_range] + \
            [SpliceSite(pos=pos, ss_type=1, prob=prob) for pos, prob in exon_starts.items() if
             lower_range <= pos <= upper_range]
    nodes = [s for s in nodes if s.prob > 0]
    nodes.sort(key=lambda x: x.pos, reverse=rev)
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
    for i, path in enumerate(nx.all_simple_paths(G, transcript_start, transcript_end)):
        curr_prob = path_weight_mult(G, path, 'weight')
        prob_sum += curr_prob
        new_paths[i] = {'acceptors': sorted([p for p in path if p in exon_starts.keys() and p != transcript_start], reverse=rev),
                        'donors': sorted([p for p in path if p in exon_ends.keys() and p != transcript_end], reverse=rev),
                        'path_weight': curr_prob}
        continuance = i + 1

    if prob_sum < 0.1:
        for j, path in enumerate(nx.all_simple_paths(G, transcript_start, next_exon_end)):
            curr_prob = path_weight_mult(G, path, 'weight')
            if curr_prob < 0.1:
                continue
            prob_sum += curr_prob
            new_paths[continuance+j] = {'acceptors': sorted([p for p in path if p in exon_starts.keys() and p != transcript_start],
                                                reverse=rev),
                            'donors': sorted([p for p in path if p in exon_ends.keys() and p != transcript_end],
                                             reverse=rev),
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

def generate_random_as(transcript):
    ma = random.sample(transcript.acceptors, 1)[0]
    md = random.sample(transcript.donors, 1)[0]
    da = random.sample(list(range(min(transcript.acceptors), max(transcript.acceptors))), 1)[0]
    dd = random.sample(list(range(min(transcript.donors), max(transcript.donors))), 1)[0]
    return {
        'discovered_acceptors': {da: {'absolute': 0.9}},
        'discovered_donors': {dd: {'absolute': 0.6}},
        'missed_donors': {ma: {'absolute': 0.2}},
        'missed_acceptors': {md: {'absolute': 0.1}},
    }
