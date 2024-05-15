# Standard library imports
from dotenv import load_dotenv

# Third-party imports
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

# LangChain imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams


load_dotenv()

# IMPLEMENT BLEU SCORE
class TextScorer:
    def __init__(self, references, prediction):
        self.references = references
        self.prediction = prediction
        self.bleu_weight_map = {
            "bleu1": (1, 0, 0, 0),
            "bleu2": (0, 1, 0, 0),
            "bleu3": (0, 0, 1, 0),
            "bleu4": (0, 0, 0, 1),
        }
        self.smoothie = SmoothingFunction().method1
        self.rouge_scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL', 'rougeLsum'],
            use_stemmer=True
        )

    def sentence_bleu_score(self, bleu_type="bleu1") -> float:
        tokenized_targets = [word_tokenize(reference) for reference in self.references]
        tokenized_prediction = word_tokenize(self.prediction)
        return sentence_bleu(
            tokenized_targets,
            tokenized_prediction,
            weights=self.bleu_weight_map[bleu_type],
            smoothing_function=self.smoothie
        )

    def rouge_scores(self):
        scores = self.rouge_scorer.score(self.references, self.prediction)
        concise_scores = {key: value.fmeasure for key, value in scores.items()}
        return concise_scores


class ConfusionMatrixEvaluator:
    def __init__(self, golden_output, model_output, model="gpt-4-turbo"):
        self.model = model
        self.golden_output = golden_output
        self.model_output = model_output
        self.comparison_template = """\
        For the following text comparison, extract the following information:

        Carefully read and identify issues mentioned in both the 'golden output' and 'model output' to identify any inconsistencies or errors.
        Thoroughly review and comprehend the issues listed in both outputs.
        total_issues: Calculate the number of issues in only the 'golden output'.
        true_positives: Count the number of issues that are present in both the 'golden output' and the 'model output'.
        false_negatives: Count issues that are listed in the 'golden output' but absent in the 'model output'.
        false_positives: Count issues that are listed in the 'model output' but absent in the 'golden output'.

        Format the output as JSON with the following keys:
        total_issues
        true_positives
        false_negatives
        false_positives

        golden_output = {golden_output}
        model_output = {model_output}
        """
        self.response_schemas = [
            ResponseSchema(
                name='total_issues',
                description='Calculate the total number of issues listed in the golden output. \
                    This involves reviewing the golden output data, identifying all the issues mentioned,\
                    and summing up the total count of distinct issues. It helps establish a baseline of expected issues for comparative analysis.'
            ),
            ResponseSchema(
                name='true_positives',
                description='Identify and count the number of issues that are present in both the golden output and the model output. \
                    Each issue found in both datasets is counted as a "true positive". \
                    This count helps in understanding how many of the expected issues were accurately identified and reported in the model output.'
            ),
            ResponseSchema(
                name='false_negatives',
                description='Count the issues that are listed in the golden output but absent in the model output. \
                    These are identified by comparing the issues listed in the golden output against those in the model output, \
                    marking issues unique to the golden output as "false negatives". \
                    This indicates cases where the model output correctly omitted issues that were present in the golden output.'
            ),
            ResponseSchema(
                name='false_positives',
                description='Determine the number of issues listed in the model output that are absent from the golden output. \
                This involves reviewing the model output to identify any issues not mentioned in the golden output, \
                counting each as a "false positive". \
                This measure assesses the accuracy of the model output by identifying instances where it may have reported non-existent or incorrect issues.'
            )
        ]
        self.chat = ChatOpenAI(model=self.model, temperature=0.0)
        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)

    def evaluate(self):
        format_instructions = self.output_parser.get_format_instructions()
        prompt_template = ChatPromptTemplate.from_template(template=self.comparison_template)
        messages = prompt_template.format_messages(
            golden_output=self.golden_output, model_output=self.model_output, format_instructions=format_instructions
        )
        response = self.chat.invoke(messages)
        output_dict = self.output_parser.parse(response.content)
        return output_dict


class QuestionGenerator:
    def __init__(self, model="gpt-4-turbo"):
        self.model = model
        self.chat = ChatOpenAI(model=self.model, temperature=0, max_tokens=4096)
        self.question_gen_schema = ResponseSchema(
            name='questions',
            description='Generate a set of Yes/No questions that enable reviewers to compare another piece of text to a golden output.'
        )
        self.response_schemas = [self.question_gen_schema]
        self.output_parser = StructuredOutputParser.from_response_schemas(self.response_schemas)

    def generate_questions(self, golden_output):
        prompt = """\
        Task: Generate a set of 20 Yes/No questions that will help evaluate whether other texts replicate the specific textual and stylistic properties present in the 'golden_output'. Focus on structural and formatting aspects that can be objectively observed and matched in another text, rather than on the functionality or specific content.
        The questions should be focused specifically on the meaning, structure, stylistic properties, format and etc of what the golden output has.

        Golden Output Analysis:
        - Begin by thoroughly analyzing the 'golden_output' to identify key textual and stylistic properties. Focus on aspects such as formatting (e.g., use of Markdown, JSON structures), language clarity, and organizational structure (e.g., use of headers, division into sections).
        - Take note of the general presentation styles, such as emphasis on certain words using Markdown, or the layout of information including lists or tables.

        Question Formulation Strategy:
        1. Property Identification: Catalog each distinct structural and stylistic property observed in the golden_output. Consider properties like the formatting styles, document organization, and any generic language features (e.g., formal vs. informal tone, use of passive vs. active voice).

        2. Direct Question Generation: For each identified property, develop a Yes/No question that simply asks whether this structural or stylistic property is also present in the text being compared. Ensure these questions are focused on the form and presentation rather than the content's substance.
        - Example: If the golden_output uses JSON for data snippets, a suitable question might be: "Does the compared text also use JSON formatting for data snippets?"
        - Example: If the golden_output is organized with clear section headers, a question could be: "Does the compared text have clearly defined section headers?"

        Output Format:
        - After completing the identification and formulation steps, present the questions as a JSON list:
        questions: []

        This method ensures that the questions generated are strictly related to matching the format and stylistic presentation of the golden_output, facilitating a straightforward comparison of text properties.

        golden_output = {golden_output}
        """

        format_instructions = self.output_parser.get_format_instructions()
        prompt_template = ChatPromptTemplate.from_template(template=prompt)
        messages = prompt_template.format_messages(
            golden_output=golden_output, format_instructions=format_instructions
        )

        response = self.chat.invoke(messages)
        output_dict = self.output_parser.parse(response.content)
        return output_dict



class OpenEndedQuestionEvaluator:
    def __init__(self, golden_output, model_output, questions, model="gpt-4-turbo"):
        self.model = model
        self.golden_output = golden_output
        self.model_output = model_output
        self.questions = questions
        self.chat = ChatOpenAI(model=self.model, temperature=0, max_tokens=4096)
        self.reviewer_task_schema = ResponseSchema(
            name='reviewer_results',
            description='This schema defines the task of a skilled reviewer to evaluate and score `model_output` against a golden output detailing coding conventions and documentation practices. The reviewer uses provided Yes/No questions to assess alignment in areas like content accuracy and formatting consistency. The task includes scoring based on positive responses and identifying failure modes where the text deviates from the reference, with results structured in a JSON format specifying the score and failure modes.'
        )
        self.output_parser = StructuredOutputParser.from_response_schemas([self.reviewer_task_schema])

    def evaluate(self):
        evaluation_template = """\
            You are a highly skilled reviewer tasked with evaluating an `model_output` against a set of standards defined by a `golden_output`. 
            
            Task:
            Evaluate the Model Output: Using the Yes/No `questions` provided, assess how well the model_output aligns with the golden output. 
            These questions focus on content accuracy, formatting consistency, presentation and organization, and technical depth.
            Scoring: Calculate the score for the model_output by dividing the number of 'Yes' answers by the total number of questions. 
            This will provide a percentage score indicating the degree of alignment between the model_output and the golden output.
            Failure Modes Analysis: Identify and articulate the reasons for any discrepancies between the model_output and the golden output. 
            Explain each deviation, focusing on areas where the model_output fails to meet the reference standards.

            Output Format:
            Provide your assessment in the following JSON structure:

            reviewer_results:
                "score": <calculated_score>,
                "failure_modes": <list_of_failure_modes>

            Where:

            <calculated_score> is a floating-point number reflecting the percentage of 'Yes' responses.
            <list_of_failure_modes> is an array of strings that detail each specific area where the model_output deviates from the reference standards.
            
            Example of Output:

            reviewer_results:
                "score": 0.80,
                "failure_modes": [
                    "The actual text lacks the required JSON formatting.",
                    "The function descriptions in the actual text are less detailed than those in the reference."
                ]
            Note:
            Ensure that your assessment is thorough and that your explanations for the failure modes are specific, providing clear insights 
            into how the model_output can be improved.

            model_output = {model_output}
            golden_output = {golden_output}
            Questions = {questions}
        
        """

        format_instructions = self.output_parser.get_format_instructions()
        prompt_template = ChatPromptTemplate.from_template(template=evaluation_template)
        messages = prompt_template.format_messages(
            golden_output=self.golden_output, model_output=self.model_output, questions=self.questions, format_instructions=format_instructions
        )

        response = self.chat.invoke(messages)
        output_dict = self.output_parser.parse(response.content)
        return output_dict


class QuestionGenModel(BaseModel):
    reason: str = Field(description="Reason for the answer provided")
    answer: str = Field(description="An answer based on the question asked")

class ChatAndParserSetup:
    def __init__(self, template, model="gpt-4-turbo"):
        self.template = template
        self.model = model
        self.json_parser = JsonOutputParser(pydantic_object=QuestionGenModel)
        self.format_instructions = self.json_parser.get_format_instructions()
        self.prompt_template = ChatPromptTemplate.from_template(template=self.template)
        self.chat = ChatOpenAI(model=self.model, temperature=0, max_tokens=4096)

    def get_components(self):
        return self.chat, self.json_parser, self.prompt_template, self.format_instructions
    

class BinaryQuestionEvaluator:
    def __init__(self, model_output, question):
        self.model_output = model_output
        self.question = question
        self.template = """
            Task: Act as a judge to determine if the "model_output" aligns with the expected properties based on the provided binary question.

            Model Output: {model_output}

            Question: {question}

            Analysis:
            - Carefully read the "model_output" and focus on the specific property or feature highlighted by the question.
            - Evaluate if the mentioned property or feature is present in the "model_output."

            Reasoning:
            - Discuss how the presence or absence of this feature in the "model_output" answers the question.
            - Draw a conclusion based on the observation of this specific feature or property.

            Conclusion:
            - Answer: Yes/No (choose based on the detailed reasoning above)
            - Justification: Provide a clear explanation supporting the answer, based on your analysis of the "model_output" in relation to the question.

            Format instructions:
            {format_instructions}
        """

    def evaluate(self):
        chat_and_parser_setup = ChatAndParserSetup(self.template)
        chat, json_parser, prompt_template, format_instructions = chat_and_parser_setup.get_components()
        messages = prompt_template.format_messages(
            model_output=self.model_output, question=self.question, format_instructions=format_instructions
        )
        response = chat.invoke(messages)
        output_dict = json_parser.parse(response.content)
        return output_dict



class QuestionMetricEvaluator:
    def __init__(self, golden_output, model_output):
        self.golden_output = golden_output
        self.model_output = model_output
        self.question_generator = QuestionGenerator()
        self.questions = self.generate_questions()

    def generate_questions(self):
        return self.question_generator.generate_questions(self.golden_output)['questions']

    def evaluate_open_questions(self):
        formatted_questions = [f"{i}: {q}" for i, q in enumerate(self.questions)]
        open_ended_questions = OpenEndedQuestionEvaluator(self.golden_output, self.model_output, formatted_questions)
        return open_ended_questions.evaluate()


    def evaluate_binary_questions(self):
        results = []
        scoring = 0
        for question in self.questions:
            answers = BinaryQuestionEvaluator(self.model_output, question)
            answer = answers.evaluate()
            result = {"Question": question, "Answer": answer}
            if answer['answer'] == 'Yes':
                scoring += 1
            results.append(result)

        scores = scoring / len(self.questions)  # Use the actual number of questions for scoring
        return {'result': results, 'scores': scoring, 'marks': scores}


class MetricEvaluator:
    def __init__(self, golden_output, model_output, template):
        self.golden_output = golden_output
        self.model_output = model_output
        self.template = template
        self.chat_and_parser_setup = ChatAndParserSetup(self.template)
        self.chat, self.json_parser, self.prompt_template, self.format_instructions = self.chat_and_parser_setup.get_components()

    def evaluate(self):
        messages = self.prompt_template.format_messages(
            golden_output=self.golden_output, model_output=self.model_output, format_instructions=self.format_instructions
        )
        response = self.chat.invoke(messages)
        output_dict = self.json_parser.parse(response.content)
        return output_dict

class LikertQuestionEvaluator(MetricEvaluator):
    def __init__(self, golden_output, model_output):
        template = """Task: You are to compare the 'model_output' with the 'golden_output' and determine how closely the model output aligns 
                with the golden output. Rate the model output on a scale from 1 to 5, where each score has a specific meaning reflecting 
                the level of alignment. 

                2. Score Definitions:
                - 1 (Poor): The model output shows significant divergence from the golden output in most key aspects including structure, content accuracy, and formatting.
                - 2 (Fair): There are considerable discrepancies, but the model output attempts some alignment with the golden output.
                - 3 (Average): The model output generally resembles the golden output but has noticeable differences that moderately affect overall alignment.
                - 4 (Good): The model output closely aligns with the golden output, with only minor discrepancies observed.
                - 5 (Excellent): The model output nearly perfectly matches the golden output in all key aspects.

                3. Analysis Phase:
                - Read both 'model_output' and 'golden_output' carefully.
                - Identify key aspects such as structure, content accuracy, formatting, and presentation style.

                4. Detailed Comparison:
                - Compare structure, content, formatting, and presentation between the two outputs.
                - Discuss each element, noting where the model output matches or diverges from the golden output.

                5. Scoring Reasoning:
                - Analyze how each comparison factor influences the overall alignment.
                - Discuss why observed similarities or differences lead to a higher or lower score.

                6. Conclusion and Scoring:
                - Based on your analysis and comparison, assign a score from 1 to 5.
                - Justify the score clearly, detailing how each aspect of the comparison influenced the decision.

                Output:
                - Document your final score along with a comprehensive justification, reflecting on each step of your thought process.

                Golden Output: {golden_output}
                Model Output: {model_output}

                Format Instructions:
                {format_instructions}
            """
        super().__init__(golden_output, model_output, template)

class MappingMetricEvaluator(MetricEvaluator):
    def __init__(self, golden_output, model_output):
        self.template = """"Task: Compare the 'model_output' with the 'golden_output' and determine its quality based on the following
          descriptive mappings for each score. Use a Chain of Thought approach to analyze and reason through your scoring decision.

            
            2. Score Definitions:
            - 1 (Sucks): The model output is severely lacking in comparison to the golden output, with major discrepancies in almost all aspects.
            - 2 (A Bit Better): While still inadequate, the model output shows marginal improvements over a score of 1, with some elements slightly aligning with the golden output.
            - 3 (Meh, Formatting Issues): The model output is average; it meets some basic criteria but has notable problems, particularly with formatting, that prevent a higher score.
            - 4 (Almost Perfect): The model output closely aligns with the golden output across most criteria, with only minor and non-critical discrepancies.
            - 5 (Perfection, Nothing to Fix): The model output is exemplary in every respect, matching or even surpassing the golden output in quality and execution.

            3. Analysis Phase:
            - Carefully read both 'model_output' and 'golden_output'.
            - Identify key aspects such as content, structure, formatting, and overall presentation.

            4. Detailed Comparison:
            - Discuss the alignment or misalignment in structure, content accuracy, and formatting.
            - Evaluate whether the presentation style and clarity match the standards set by the golden output.

            5. Scoring Reasoning:
            - Analyze each component of the comparison, determining how closely the model output matches the descriptions provided for each score.
            - Consider how significant deviations or alignments contribute to a specific score.

            6. Conclusion and Scoring:
            - Based on the comprehensive comparison, assign a score from 1 to 5, matching the most fitting description.
            - Provide a detailed justification for the selected score, explaining how specific findings correlate with the score’s criteria.

            Output:
            - Summarize the final score and a comprehensive justification, incorporating reflections on each step of your thought process."


                Golden Output: {golden_output}
                Model Output: {model_output}

                Format Instructions:
                {format_instructions}
            """
        super().__init__(golden_output, model_output, self.template)

class PointBasedMetricEvaluator(MetricEvaluator):
    def __init__(self, golden_output, model_output):
        self.template = """Task: Assess the 'model_output' by comparing it to the 'golden_output' using a point-based system. 
                Start with a score of 0 and add or subtract points based on the presence of specific qualities or errors. 

                2. Scoring Criteria:
                - Add 1 point for each of the following qualities:
                    - Clear Formatting: If the model output is formatted clearly and consistently.
                    - Accurate Content: If the content is accurate and aligns well with the information in the golden output.
                    - Organized Structure: If the model output is organized logically and mirrors the structure of the golden output.
                    - Effective Presentation: If the presentation is engaging and maintains the style of the golden output.
                    - Technical Correctness: If technical details are correct and effectively communicated.
                - Subtract 1 point for each of the following errors:
                    - Major Inaccuracies: If there are significant factual errors.
                    - Poor Formatting: If formatting is inconsistent or hinders understanding.
                    - Disorganized Content: If the content lacks a logical flow or structure.
                    - Ineffective Presentation: If the presentation style is unclear or fails to engage the reader.

                3. Detailed Analysis:
                - Evaluate each aspect of the model output, comparing it to the golden output.
                - Determine whether each quality is present or if any errors are apparent.

                4. Calculation and Reasoning:
                - For each identified quality or error, calculate the addition or subtraction of points.
                - Discuss how each specific aspect contributes to the overall score.

                5. Conclusion and Scoring:
                - Sum up the total points accumulated from the analysis.
                - Provide a final score out of 5, with a detailed justification based on the cumulative assessment of qualities and errors.

                Example for Scoring:
                - Start with 0 points. If the model output shows clear formatting (+1), organized structure (+1), and accurate content (+1) but suffers from poor presentation (-1), the total would be 2 points. Convert this to a final score on a scale of 1 to 5.

                Output:
                - Document the final score along with a comprehensive explanation, detailing how each criterion influenced the overall evaluation."

                Golden Output: {golden_output}
                Model Output: {model_output}

                Format Instructions:
                {format_instructions}
            """
        super().__init__(golden_output, model_output, self.template)


class GEvalMetrics:
    def __init__(self, expected_output, actual_output):
        self.expected_output = expected_output
        self.actual_output = actual_output
        self.test_case = LLMTestCase(actual_output=self.actual_output, expected_output=self.expected_output)
        self.metrics = {
            "Coherence": GEval(
                name="Coherence",
                criteria="Evaluate whether the 'model output' presents a logical, orderly progression of ideas, maintaining the integrity and structure of the 'golden_output'.",
                evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT]
            ),
            "Consistency": GEval(
                name="Consistency",
                criteria="Check if the 'model output' maintains internal logical consistency and adheres to the same facts or rules presented in the 'golden_output'.",
                evaluation_params=[LLMTestCaseParams.EXPECTED_OUTPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
            ),
            "Fluency": GEval(
                name="Fluency",
                criteria="Determine if the 'model output' is grammatically correct, uses appropriate vocabulary, and flows smoothly, mirroring the linguistic style of the 'golden_output'.",
                evaluation_params=[LLMTestCaseParams.EXPECTED_OUTPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
            ),
            "Perplexity": GEval(
                name="Perplexity",
                criteria="Measure how straightforward and understandable the 'model output' is, ensuring it maintains the clarity and ease of comprehension exhibited in the 'golden_output'.",
                evaluation_params=[LLMTestCaseParams.EXPECTED_OUTPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
            ),
            "Correctness": GEval(
                name="Correctness",
                criteria="Assess whether the 'model output' provides information that is factually accurate and aligns with the information stated in the 'golden_output'.",
                evaluation_params=[LLMTestCaseParams.EXPECTED_OUTPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
            )
        }

    def evaluate(self):
        scores = []
        results = {}
        for metric_name, metric in self.metrics.items():
            metric.measure(self.test_case)
            scores.append(metric.score)
            results[f"{metric_name}_Metric"] = {
                "score": metric.score,
                "reason": metric.reason
            }
        average_score = sum(scores) / len(scores)
        results["average_score"] = average_score
        return results
    


