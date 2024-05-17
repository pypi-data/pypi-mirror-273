from geney.oncosplice_pipeline import *

class PairwiseEpistasis:
    def __init__(self, epistasis):
        # need some check here making sure format of mtuations isi good
        self.epistasis = epistasis
        self.mut_id1, self.mut_id2 = epistasis.split('|')

    def compare_functional_changes(self):
        self.results_mut1 = oncosplice(self.mut_id1, sai_threshold=0.5)
        self.results_mut2 = oncosplice(self.mut_id2, sai_threshold=0.5)
        self.results_epi = oncosplice(self.epistasis, sai_threshold=0.5)

        splicing1, splicing2, splicing_epi = 0, 0, 0
        oncosplice_score1, oncosplice_score2, oncosplice_score_epi = 0, 0, 0
