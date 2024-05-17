import pandas as pd
from sklearn.metrics import roc_curve, precision_recall_curve
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import subprocess

from geney import config_setup
from geney.utils import download_and_gunzip
from geney.oncosplice_pipeline import oncosplice_reduced

def download_and_parse_clinvar():
    url = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz'
    local_file = download_and_gunzip(url, target_path)
    return local_file


def aggregate_clinvar_results(benchmark_path, aggregate_mode=False, benchmark_feature=None, local_clinvar_df='/tamir2/nicolaslynn/data/ClinVar/clinvar_compact.csv'):
    data = pd.concat([pd.read_csv(file) for file in Path(benchmark_path).glob('*.csv')])
    if not aggregate_mode:
        data = data[(data.cons_available) & (data.primary_transcript)]

    data = oncosplice_reduced(data)
    data = data.loc[:, ~data.columns.duplicated()]
    data = pd.merge(data, pd.read_csv(local_clinvar_df), on='mut_id')
    data['clinsig_val'] = data.apply(lambda row: {'Benign': 0, 'Pathogenic': 1}[row.clinsig], axis=1)
    for c in data.columns:
        try:
            if data[c].min() < 0:
                data[f'{c}_abs'] = abs(data[c])
        except TypeError:
            pass

    print(data.corr(numeric_only=True))
    print(data.corrwith(data['clinsig_val'], method='spearman'))
    print(data.corrwith(data['clinsig_val'], method='pearson'))
    return data


def plot_performance(true_values, predictions):
    clinsig_map = {'Benign': 0, 'Pathogenic': 1}
    true_values = [clinsig_map[t] for t in true_values]
    predictions = scale_predictions(predictions)

    fpr, tpr, thresholds_roc = roc_curve(true_values, predictions)

    # Calculate Precision-Recall curve
    precision, recall, thresholds_pr = precision_recall_curve(true_values, predictions)

    # Plotting ROC curve
    plt.figure(figsize=(20, 5))

    plt.subplot(1, 4, 1)
    plt.plot(fpr, tpr)
    plt.title('ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    # Plotting Precision-Recall curve
    plt.subplot(1, 4, 2)
    plt.plot(recall, precision)
    plt.title('Precision-Recall Curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')

    # Plotting Precision vs. Thresholds
    plt.subplot(1, 4, 3)
    plt.plot(thresholds_pr, precision[:-1])  # Precision and thresholds have off-by-one lengths
    plt.title('Precision vs. Threshold')
    plt.xlabel('Threshold')
    plt.ylabel('Precision')

    # Plotting Sample Percentage Captured vs. Thresholds
    plt.subplot(1, 4, 4)
    # Assuming 'tpr' or another appropriate metric represents the cumulative percentage
    plt.plot(thresholds_roc, tpr)  # Update 'tpr' with the correct metric if necessary
    plt.title('Cumulative Percentage vs. Threshold')
    plt.xlabel('Threshold')
    plt.ylabel('Cumulative Percentage of Population')

    plt.tight_layout()
    plt.show()



class ClinVarBenchmark:
    def __init__(self, df):
        assert 'clinsig' in df.columns, 'No clinsig column found in dataframe.'
        self.df = df


    def scale_predictions(self, p):
        max_val = max(p)
        min_val = min(p)
        return (p - min_val) / (max_val - min_val)

    def plot_performance(self, true_values, predictions):
        clinsig_map = {'Benign': 0, 'Pathogenic': 1}
        predictions = [clinsig_map[t] for t in true_values]
        predictions = self.scale_predictions(predictions)

        fpr, tpr, thresholds_roc = roc_curve(true_values, predictions)

        # Calculate Precision-Recall curve
        precision, recall, thresholds_pr = precision_recall_curve(true_values, predictions)

        # Plotting ROC curve
        plt.figure(figsize=(20, 5))

        plt.subplot(1, 4, 1)
        plt.plot(fpr, tpr)
        plt.title('ROC Curve')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')

        # Plotting Precision-Recall curve
        plt.subplot(1, 4, 2)
        plt.plot(recall, precision)
        plt.title('Precision-Recall Curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')

        # Plotting Precision vs. Thresholds
        plt.subplot(1, 4, 3)
        plt.plot(thresholds_pr, precision[:-1])  # Precision and thresholds have off-by-one lengths
        plt.title('Precision vs. Threshold')
        plt.xlabel('Threshold')
        plt.ylabel('Precision')

        # Plotting Sample Percentage Captured vs. Thresholds
        plt.subplot(1, 4, 4)
        # Assuming 'tpr' or another appropriate metric represents the cumulative percentage
        plt.plot(thresholds_roc, tpr)  # Update 'tpr' with the correct metric if necessary
        plt.title('Cumulative Percentage vs. Threshold')
        plt.xlabel('Threshold')
        plt.ylabel('Cumulative Percentage of Population')

        plt.tight_layout()
        plt.show()
        return None

    def report(self, feature):
        pass

    def find_ppv_threshold(self, feature, ppv_threshold=0.95):
        pass



if __name__ ==  '__main__':
    now = datetime.now()
    benchmark_path = config_setup['ONCOSPLICE'] / f'clinvar_benchmark_{now.strftime("%m_%d_%Y")}'
    print(f"Saving benchmark results to {benchmark_path}")
    benchmark_path.mkdir(parents=True, exist_ok=True)
    subprocess.run(['python', '-m', 'geney.pipelines.dask_utils', '-i',
                    '/tamir2/nicolaslynn/data/ClinVar/clinvar_oncosplice_input.txt', '-r', str(benchmark_path),
                    '-n', '10', '-m', '5GB'])

