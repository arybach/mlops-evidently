from typing import Text

from evidently import ColumnMapping
from evidently.metrics import (
    RegressionQualityMetric,
    RegressionPredictedVsActualScatter,
    RegressionPredictedVsActualPlot,
    RegressionErrorPlot,
    RegressionAbsPercentageErrorPlot,
    RegressionErrorDistribution,
    RegressionErrorNormality,
    RegressionTopErrorMetric
)
from evidently.metric_preset import TargetDriftPreset
from evidently.report import Report
import pandas as pd
import os

def get_column_mapping(**kwargs) -> ColumnMapping:

    column_mapping = ColumnMapping()
    column_mapping.target = kwargs['target_col']
    column_mapping.prediction = kwargs['prediction_col']
    column_mapping.numerical_features = kwargs['num_features']
    # Check if cat_features is empty
    if kwargs['cat_features']:
        column_mapping.categorical_features = kwargs['cat_features']
    else:
        column_mapping.categorical_features = None

    return column_mapping


def build_model_performance_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping,
    model_name: str
) -> Text:

    model_performance_report = Report(metrics=[
        RegressionQualityMetric(),
        RegressionPredictedVsActualScatter(),
        RegressionPredictedVsActualPlot(),
        RegressionErrorPlot(),
        RegressionAbsPercentageErrorPlot(),
        RegressionErrorDistribution(),
        RegressionErrorNormality(),
        RegressionTopErrorMetric()
    ])
    model_performance_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )
    os.makedirs(f'reports/{model_name}', exist_ok=True)
    report_path = f'reports/{model_name}/model_performance.html'
    model_performance_report.save_html(report_path)

    return report_path


def build_target_drift_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping,
    model_name: str
) -> Text:

    target_drift_report = Report(metrics=[TargetDriftPreset()])
    target_drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )
    os.makedirs(f'reports/{model_name}', exist_ok=True)
    report_path = f'reports/{model_name}/target_drift.html'
    target_drift_report.save_html(report_path)

    return report_path
