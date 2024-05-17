
import subprocess
import logging
import tempfile


class NetChop(object):
    """
    Wrapper around netChop tool. Assumes netChop is in your PATH.
    """

    def predict_epitopes(self, sequences min_len=8):
        """
        Return netChop predictions for each position in each sequence.

        Parameters
        -----------
        sequences : list of string
            Amino acid sequences to predict cleavage for

        Returns
        -----------
        list of list of float

        The i'th list corresponds to the i'th sequence. Each list gives
        the cleavage probability for each position in the sequence.
        """
        with tempfile.NamedTemporaryFile(suffix=".fsa", mode="w") as input_fd:
            for (i, sequence) in enumerate(sequences):
                input_fd.write("> %d\n" % i)
                input_fd.write(sequence)
                input_fd.write("\n")
            input_fd.flush()
            try:
                output = subprocess.check_output(["netChop", input_fd.name])
            except subprocess.CalledProcessError as e:
                logging.error("Error calling netChop: %s:\n%s" % (e, e.output))
                raise

        parsed = self.parse_netchop(output)
        assert len(parsed) == len(sequences), \
            "Expected %d results but got %d" % (
                len(sequences), len(parsed))
        assert [len(x) for x in parsed] == [len(x) for x in sequences]
        filtered_proteosomes = []
        for scores, seq in list(zip(parsed, sequences)):
            proteosome = self.chop_protein(seq, [s > threshold for s in scores])
            filtered_proteosomes.append([e for e in proteosome if len(e) > min_len])
        return proteosomes

    @staticmethod
    def parse_netchop(netchop_output):
        """
        Parse netChop stdout.
        """
        line_iterator = iter(netchop_output.decode().split("\n"))
        scores = []
        for line in line_iterator:
            if "pos" in line and 'AA' in line and 'score' in line:
                scores.append([])
                if "----" not in next(line_iterator):
                    raise ValueError("Dashes expected")
                line = next(line_iterator)
                while '-------' not in line:
                    score = float(line.split()[3])
                    scores[-1].append(score)
                    line = next(line_iterator)
        return scores

    def chop_protein(self, seq, pos):
        # Generate subsequences using list comprehension and slicing
        start = 0
        subsequences = [seq[start:(start := i+1)] for i, marker in enumerate(pos) if marker == 1]
        # Check if the last part needs to be added
        if start < len(seq):
            subsequences.append(seq[start:])
        return subsequences

