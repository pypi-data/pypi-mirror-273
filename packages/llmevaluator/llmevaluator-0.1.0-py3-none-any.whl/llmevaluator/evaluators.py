import json
import concurrent.futures
from .file_handler import read_file, write_results_to_json
from metrics import (
    PointBasedMetricEvaluator,
    MappingMetricEvaluator,
    LikertQuestionEvaluator,
    QuestionMetricEvaluator,
    ConfusionMatrixEvaluator,
    TextScorer,
    GEvalMetrics,
)


def run_evaluation(golden_output, model_output):
    # Initialize necessary classes
    text_scorer = TextScorer(references=golden_output, prediction=model_output)
    confusion_matrix_evaluator = ConfusionMatrixEvaluator(golden_output=golden_output, model_output=model_output)
    question_metric_evaluator = QuestionMetricEvaluator(golden_output=golden_output, model_output=model_output)
    likert_question_evaluator = LikertQuestionEvaluator(golden_output=golden_output, model_output=model_output)
    mapping_metric_evaluator = MappingMetricEvaluator(golden_output=golden_output, model_output=model_output)
    point_based_metric_evaluator = PointBasedMetricEvaluator(golden_output=golden_output, model_output=model_output)
    geval_metrics = GEvalMetrics(expected_output=golden_output, actual_output=model_output)

    # Define tasks
    tasks = {
        'BLEU_Score': lambda: text_scorer.sentence_bleu_score(),
        'ROUGE_Scores': lambda: text_scorer.rouge_scores(),
        'Confusion_Matrix': lambda: confusion_matrix_evaluator.evaluate(),
        'Open_Question_Evaluation': lambda: question_metric_evaluator.evaluate_open_questions(),
        'Binary_Question_Evaluation': lambda: question_metric_evaluator.evaluate_binary_questions(),
        'Likert_Question_Evaluation': lambda: likert_question_evaluator.evaluate(),
        'Mapping_Metric_Evaluation': lambda: mapping_metric_evaluator.evaluate(),
        'Point_Based_Metric_Evaluation': lambda: point_based_metric_evaluator.evaluate(),
        'GEval_Metrics': lambda: geval_metrics.evaluate()
    }

    # Collect metrics using ThreadPoolExecutor
    metrics = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_metric = {executor.submit(task): name for name, task in tasks.items()}
        for future in concurrent.futures.as_completed(future_to_metric):
            metric_name = future_to_metric[future]
            try:
                metrics[metric_name] = future.result()
            except Exception as exc:
                print(f'{metric_name} generated an exception: {exc}')

    return metrics


def evaluate_texts(text1, text2):
    return run_evaluation(text1, text2)

def evaluate_list(list1, list2):
    results = []
    for text1, text2 in zip(list1, list2):
        result = run_evaluation(text1, text2)
        results.append(result)
    return results

def evaluate_files(golden_file, model_files):
    golden_output = read_file(golden_file)
    results = {}
    for model_file in model_files:
        model_output = read_file(model_file)
        result = run_evaluation(golden_output, model_output)
        results[model_file] = result
    return results