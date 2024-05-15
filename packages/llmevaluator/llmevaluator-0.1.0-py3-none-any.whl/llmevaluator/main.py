from .evaluators import run_evaluation
from .file_handler import read_file

def evaluate_texts(file1, file2):
    """
    Reads the contents of two files and evaluates them using a predefined evaluation function.

    Args:
        file1 (str): The file path for the first text file.
        file2 (str): The file path for the second text file.

    Returns:
        dict: The evaluation results comparing the contents of the two files.
    """
    text1 = read_file(file1)
    text2 = read_file(file2)
    return run_evaluation(text1, text2)

def evaluate_list(file_list1, file_list2):
    """
    Evaluates pairs of files from two lists using a predefined evaluation function.

    This function reads each pair of files from the provided lists, evaluates them,
    and collects the results into a list.

    Args:
        file_list1 (list of str): A list of file paths for the first set of text files.
        file_list2 (list of str): A list of file paths for the second set of text files.

    Returns:
        list: A list of evaluation results for each pair of files.
    """
    if not isinstance(file_list1, list) or not isinstance(file_list2, list):
        raise ValueError("Both file_list1 and file_list2 must be lists of file paths.")
    
    results = []
    for file1, file2 in zip(file_list1, file_list2):
        text1 = read_file(file1)
        text2 = read_file(file2)
        result = run_evaluation(text1, text2)
        results.append(result)
    return results

def evaluate_files(golden_file, model_files):
    """
    Evaluates a set of model files against a golden file using a predefined evaluation function.

    This function reads the golden file and each of the model files, evaluates each model file's output
    against the golden file's output, and stores the results in a dictionary with the model file names as keys.

    Args:
        golden_file (str): The file path for the golden text file.
        model_files (list of str): A list of file paths for the model text files.

    Returns:
        dict: A dictionary containing the evaluation results for each model file.
    """
    if not isinstance(model_files, list):
        raise ValueError("model_files must be a list of file paths.")
    
    golden_output = read_file(golden_file)
    results = {}
    for model_file in model_files:
        model_output = read_file(model_file)
        result = run_evaluation(golden_output, model_output)
        results[model_file] = result
    return results




# golden_output = """
# [{'args': {'scratchpad': "The code provided by the Assistant includes a class definition for a TreeNode and two functions: `inorder_traversal` and `sorted_array_to_bst`. The `sorted_array_to_bst` function is designed to convert a sorted array into a height-balanced binary search tree (BST). The implementation uses a recursive approach to find the middle of the array, make it the root, and recursively do the same for the left and right halves of the array. The `inorder_traversal` function is used to verify the structure of the BST by printing the elements in sorted order.\n\n**Issues**:\n1. The code is correct and adheres to Python best practices.\n2. The recursive approach used in `sorted_array_to_bst` is efficient for this problem, as it ensures the BST remains height-balanced.\n3. The code is well-commented, enhancing readability and understanding.\n4. The example usage in the second code cell effectively demonstrates how to use the `sorted_array_to_bst` function and verify its output using `inorder_traversal`.\n\n**Evaluation**:\n- The code is correct, efficient, and well-documented.\n- The Assistant's response is complete as it includes both the implementation and an example usage, fulfilling the user's request comprehensively.", 'issues': [], 'scoring_explanation': "The code is correct, efficient, and adheres to best practices. It is well-documented and readable, making it easy to understand and maintain. The example usage demonstrates the function's effectiveness, and the conversation ends with a complete solution to the user's query. Therefore, the highest score is justified.", 'score': 5}, 'type': 'NotebookWiseFeedback'}]
# """

# model_output = """
# [{'args': {'scratchpad': 'The code provided by the Assistant seems to be correct and implements the conversion of a sorted array into a height-balanced binary search tree using a recursive approach. The time complexity analysis provided by the Assistant is also accurate.', 'issues': [{'cell_position': 4, 'what': 'The code is correct and implements the conversion of a sorted array into a height-balanced binary search tree using a recursive approach.', 'why': 'The code follows the correct algorithm and structure to achieve the desired functionality.', 'where': 'Code cell 4', 'severity': 'Low', 'fix': 'No action needed, code is correct and functional.'}, {'cell_position': 8, 'what': 'Accurate time complexity analysis provided by the Assistant.', 'why': 'The time complexity explanation aligns with the recursive nature of the function and the number of elements processed in the input array.', 'where': 'Markdown cell 8', 'severity': 'Low', 'fix': 'No action needed, explanation is accurate.'}], 'scoring_explanation': "The code provided by the Assistant is correct, efficient, and follows best practices. The time complexity analysis is accurate, and the code is readable and useful for the user's request. The conversation is complete and the user's request has been fully satisfied.", 'score': 5}, 'type': 'NotebookWiseFeedback'}]
# """
# # questionsa = QuestionGenerator()
# # question = questionsa.generate_questions(golden_output)
# # print(question)
# metrices = run_evaluation(golden_output, model_output)



# file_name = "matrices_v2"
# # Write the list to a JSON file
# with open(file_name, 'w') as file:
#      json.dump(metrices, file, indent=4)

# def main(expected_output, actual_output):
#     # Using BLEU and ROUGE metrics
#     bleu_score = sentence_bleu_score(expected_output, actual_output)
#     rouge_score = rouge_scores(expected_output, actual_output)
#     confusion_matrix = partial_confusion_matrix(expected_output, actual_output)

#     # Using GEval metric
#     geval_results = gevalMetric(expected_output, actual_output)
#     open_ended_questions_metric = open_questions_metric(expected_output, actual_output)

#     final_score = {
#         'coherence_score': geval_results['Coherence_Metric']['coherence_score'],
#         'consistency_score': geval_results['Consistency_Metric']['consistency_score'],
#         'fluency_score': geval_results['Fluency_Metric']['fluency_score'],
#         'perplexity_score': geval_results['Perplexity_Metric']['perplexity_score'],
#         'correctness_score': geval_results['Correctness_Metric']['correctness_score'],
#         'average_score': geval_results['average_score']
#     }

#     final_results = {
#         "BLEU Score": bleu_score,
#         "ROUGE Scores:": rouge_score,
#         "GEVal Scores": final_score,
#         "Confusion Matrix": confusion_matrix,
#         "open_questions": open_ended_questions_metric
#     }
#     return final_results

# if __name__ == "__main__":
#     with open('evaluation_results_cbc_gpt4_vs_gpt4.json', 'r') as file:
#         data = json.load(file)

#     with open('evaluation_results_nb_all_models.json', 'r') as file2:
#         data2 = json.load(file2)


#     results = []
#     item = 0
#     for expected, actual in zip(data, data2):
#         print(f"==== EVALUATING NOTEBOOK NUMBER {item+1} ===================")
#         actual_output = actual.get('raw_results_cbc_dbrx-instruct', None)
#         expected_output = expected.get('raw_results_cbc_gpt-4-turbo_x', None)
#         actual_output, expected_output = f"{actual_output}", f"{expected_output}"
#         result = main(expected_output, actual_output)
#         results.append(result)

#         item += 1

#     file_name = 'metric4_gpt-dbrx-instruct-vrs-gpt-4-turbo_x.json'
#     with open(file_name, 'w') as file:
#         json.dump(results, file, indent=4)

    # with open(file_name, 'r') as file:
    #     existing_data = json.load(file)

    # existing_data.extend(results)

    # Write the list to a JSON file
    # with open(file_name, 'w') as file:
    #     json.dump(results, file, indent=4)

    # results = []
    # count = 0
    # for item, values in enumerate(data):
    #     # if item >= 10 and item < 30:
    #     print(f"==== EVALUATING NOTEBOOK NUMBER {item+1} ===================")
    #     actual_output = values.get('raw_results_cbc_gpt-4-turbo', None)
    #     expected_output = values.get('raw_results_cbc_gpt-4-turbo', None)

    #     actual_output, expected_output = f"{actual_output}", f"{expected_output}"
    #     result = main(expected_output, actual_output)
    #     results.append(result)

    # file_name = 'gpt-4-turbo-vrs-gpt-4-turbo_v2.json'

    # with open(file_name, 'r') as file:
    #     existing_data = json.load(file)

    # # existing_data.extend(results)

    # Write the list to a JSON file
    # with open(file_name, 'w') as file:
    #     json.dump(results, file, indent=4)