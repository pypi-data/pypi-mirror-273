import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.integrate import trapz
from geney.utils import unload_pickle, unload_json, contains
from lifelines.exceptions import ConvergenceError
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from lifelines import CoxPHFitter

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None

# epistasis_tracker = unload_pickle('epistasis2case_tracker.pkl')
# mutation_tracker = unload_pickle('mutation2case_tracker.pkl')

def prepare_clinical_data():
    CLINICAL_DATA_FILE = Path('/tamir2/yoramzar/Projects/Cancer_mut/Explore_data/reports/df_p_all.pkl')
    df = unload_pickle(CLINICAL_DATA_FILE)
    df.rename(columns={'patient_uuid': 'case_id'}, inplace=True)
    cols = list(df.columns)
    cols_days_to_followup = [col for col in cols if 'days_to_followup' in col] + [col for col in cols if 'days_to_last_followup' in col]
    cols_days_to_know_alive = [col for col in cols if 'days_to_know_alive' in col] + [col for col in cols if 'days_to_last_known_alive' in col]
    cols_days_to_death = [col for col in cols if 'days_to_death' in col]
    cols_duration = cols_days_to_followup + cols_days_to_know_alive + cols_days_to_death
    col_vital_status = 'days_to_death'
    event_col_label = 'event'
    duration_col_label = 'duration'
    df.insert(1, event_col_label, df.apply(lambda x: int(not np.isnan(x[col_vital_status])), axis=1))
    df.insert(1, duration_col_label, df.apply(lambda x: max([x[col] for col in cols_duration if not np.isnan(x[col])], default=-1), axis=1))
    df[duration_col_label] /= 365
    df = df.query(f"{duration_col_label}>=0.0")[['duration', 'event', 'case_id', 'chemotherapy', 'hormone_therapy', 'immunotherapy', 'targeted_molecular_therapy', 'Proj_name']]
    df.to_csv('/tamir2/nicolaslynn/data/tcga_metadata/tcga_clinical_data.csv')
    return df


class SurvivalAnalysis:
    def __init__(self, clindf):
        self.clindf = clindf
        self.treatment_features = ['chemotherapy', 'hormone_therapy', 'immunotherapy', 'targeted_molecular_therapy']

    def prepare_data(self, case_dict):
        df1 = self.clindf.query(f"case_id in {case_dict['affected']}")
        df2 = self.clindf.query(f"case_id in {case_dict['na1']}")
        df3 = self.clindf.query(f"case_id in {case_dict['na2']}")
        df1['group'] = 0
        df2['group'] = 1
        df3['group'] = 1
        df = pd.concat([df1, df2, df3])
        core_features = ['duration', 'event', 'group']
        treatment_features = ['chemotherapy', 'hormone_therapy', 'immunotherapy', 'targeted_molecular_therapy']
        df = df[treatment_features + core_features]
        df.fillna(0, inplace=True)

        cap_time = min([df[df.group == 0].duration.max(), df[df.group == 1].duration.max()])
        df['duration'] = df['duration'].clip(upper=cap_time)

        for col in treatment_features:
            df.loc[df[col] > 0, col] = 1

        df = df[core_features + [col for col in treatment_features if
                                 df[col].nunique() > 1 and df[col].value_counts(normalize=True).min() >= 0.01]]
        return df

    def perform_cox_analysis(self, df):
        return CoxPHFitter().fit(df, 'duration', 'event')

    def get_km_fits(self, df, feature):
        group_A = df[df[feature] == 0]
        group_B = df[df[feature] == 1]

        # Create Kaplan-Meier fitter instances
        kmf_A = KaplanMeierFitter()
        kmf_B = KaplanMeierFitter()

        # Fit the data
        if len(group_A) < 5 or len(group_B) < 5:
            return 0, 0
        label1, label2 = f'Epistasis ({len(group_A)})', f'CVs Only ({len(group_B)})'
        self.label1, self.label2 = label1, label2
        kmf_A.fit(group_A['duration'], group_A['event'], label=self.label1)
        kmf_B.fit(group_B['duration'], group_B['event'], label=self.label2)
        return kmf_A, kmf_B

    def get_km_aucs(self, kmf_A, kmf_B):
        surv_func_A = kmf_A.survival_function_
        surv_func_B = kmf_B.survival_function_

        # Numerical integration using Trapezoidal rule
        auc_A = trapz(surv_func_A[self.label1], surv_func_A.index)
        auc_B = trapz(surv_func_B[self.label2], surv_func_B.index)
        return auc_A, auc_B

    def plot_km_curve(self, kmf_A, kmf_B):
        # Plot the survival curves
        ax = kmf_A.plot()
        kmf_B.plot(ax=ax)

        # Add labels and title
        p_value = 0.01
        ax.text(0.5, 0.85, f'p-value: {p_value:.4f}', transform=ax.transAxes, fontsize=12, horizontalalignment='center')
        # ax.text(0.45, 0.85, f'AUCe: {auc_A:.4f}', transform=ax.transAxes, fontsize=12, horizontalalignment='center')
        # ax.text(0.45, 0.85, f'AUCc: {auc_B:.4f}', transform=ax.transAxes, fontsize=12, horizontalalignment='center')

        plt.title('Kaplan-Meier Survival Curves')
        plt.xlabel('Time')
        plt.ylabel('Survival Probability')
        plt.show()
        return self

    def log_rank(self, df, column):
        group1, group2 = df[df[column] == 0], df[df[column] == 1]
        result = logrank_test(group1['duration'], group2['duration'],
                              event_observed_A=group1['event'],
                              event_observed_B=group2['event'])
        return result.p_value

    def run_analysis(self, dict1, event_name):
        try:
            df = self.prepare_data(dict1)
            if len(df[df.group == 0]) < 2 or len(df[df.group == 1]) < 2:
                return None

            elif len(df[df.group == 0]) < 10 or len(df[df.group == 1]) < 10:
                temp = pd.Series()
                temp['mut_id'] = event_name
                for column in [c for c in df.columns if c != 'duration' and c != 'event']:
                    temp[column] = self.log_rank(df, column)

            else:
                auca, aucb = self.get_km_aucs(*self.get_km_fits(df, 'group'))
                cph = self.perform_cox_analysis(df)
                temp = cph.summary.p
                temp.name = ''
                temp.index.name = ''
                temp['auc_diff'] = auca - aucb
                temp['mut_id'] = event_name
            return temp

        except ConvergenceError:
            return None


