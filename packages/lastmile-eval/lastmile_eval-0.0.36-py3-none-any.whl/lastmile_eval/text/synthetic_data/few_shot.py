from typing import Sequence
import numpy as np
from openai import OpenAI
import pandas as pd


def main():
    # run_example_1()
    run_example_2()


def run_example_2():
    pd.set_option("display.max_colwidth", 200)

    # Step 1: Prepare unlabeled query, context data from RAG Query Traces
    PATH_DF_ALL_RQT = (
        "/Users/jonathan/Projects/experimentation/slackbot/df_all_rqt.xlsx"
    )

    df_all_rqt = pd.read_excel(PATH_DF_ALL_RQT)

    df_qc_unlabeled = (
        df_all_rqt.explode("context_extracted")[
            ["query_extracted", "context_extracted"]
        ]
        .dropna()
        .drop_duplicates()
    )

    # Step 2: Prepare any available labeled query, context positive pairs

    PATH_QC_POSITIVES = (
        "/Users/jonathan/Projects/experimentation/slackbot/qc_positives.xlsx"
    )
    df_cq_positives = pd.read_excel(PATH_QC_POSITIVES)

    print("Labeled positive query, context pairs:")
    print(df_cq_positives)


    # Step 3: set the number of synthetic (query, context) pairs to generate

    n_synthetic_questions = 1

    # Step 4: Extract the individual contexts from the traces.
    # These will be the unlabeled observed inputs used to generate
    # synthetic questions.
    s_observed_contexts = df_qc_unlabeled["context_extracted"]

    print("\n\nObserved contexts:")
    print(s_observed_contexts)

    # Step 5: Generate synthetic questions from the observed contexts
    df_synthetic_question_pairs = synthesize_questions_from_contexts(
        df_cq_positives, s_observed_contexts, n_synthetic_questions
    )

    print("\n\nSynthetic question pairs:")

    # pd.set_option("display.max_colwidth", None)
    print(df_synthetic_question_pairs)


def synthesize_questions_from_contexts(
    df_cq_positives, s_observed_contexts, n_synthetic_questions
):
    """
    df_cq_positives: DataFrame with columns "context" and "question"
    s_observed_contexts: Series of contexts to generate synthetic questions from
    n_synthetic_questions: Number of synthetic question pairs to generate.
    
    Out: DataFrame with columns "question" and "context", containing sampled 
    observed contexts and corresponding synthetic questions.    
    """
    # Sample from the input context so it fits in the 8192 token limit.
    # Larger context window models seem to work worse.
    def _shrink_text(text, output_len):
        full_len = len(text)
        largest_start_idx = max(0, full_len - output_len)
        random_start_idx = np.random.randint(0, 1 + largest_start_idx)
        return text[random_start_idx : random_start_idx + output_len]
    
    # This is in characters, not tokens. Used to make completion calls succeed
    # by keeping the input text within the 8192 token limit.
    output_len = 10000

    df_cq_positives = df_cq_positives.assign(
        context=df_cq_positives["context"].apply(
            lambda c: _shrink_text(c, output_len)
        ),
    )
    s_observed_contexts = s_observed_contexts.apply(
        lambda c: _shrink_text(c, output_len)
    )

    dfs = []
    for _ in range(n_synthetic_questions):
        # It seems to work better with just a single labeled pair at a time.
        df_cq_labeled = df_cq_positives.sample(1)

        df_observed = s_observed_contexts.to_frame("context")

        # It seems to work better with just a single context at a time.
        df_observed = df_observed.sample(1)

        df_new_pair = _make_synthetic_qc_pair(df_cq_labeled, df_observed)

        dfs.append(df_new_pair)

    df_synthetic_question_pairs = pd.concat(dfs)
    return df_synthetic_question_pairs


def _make_synthetic_qc_pair(df_cq_labeled, df_observed):
    synthetic_question = synthesize_helper(
        df_cq_labeled, df_observed, "question"
    )

    df_new_pair = df_observed.assign(question=synthetic_question)[
        ["question", "context"]
    ]

    return df_new_pair


def run_example_1():
    labeled_questions = ["Who is Rossdan?", "Who is Jonathan?"]

    labeled_contexts = [
        "Rossdan Craig: Head of Memes",
        "Jonathan Lessinger: Lead Clown",
    ]

    answers = [
        "the guy who keeps it real",
        "The funny guy",
    ]

    unlabeled_questions = [
        "Who is Ankush?",
        "Who is Zak?",
    ]

    unlabeled_contexts = [
        "Ankush Pala: Amazon (Web Services) Warrior",
        "Zak Assoul: Chief Wizard",
    ]

    synthetic_answers = generate_synthetic_answers(
        labeled_questions,
        labeled_contexts,
        answers,
        unlabeled_questions,
        unlabeled_contexts,
    )

    print("Labeled input data:")
    df_labeled = pd.DataFrame(
        {
            "Question": labeled_questions,
            "Context": labeled_contexts,
            "Answer": answers,
        }
    )

    print(df_labeled)

    df_synthesized = pd.DataFrame(
        {
            "Input Question": unlabeled_questions,
            "Input Context": unlabeled_contexts,
            "Synthesized Answer": synthetic_answers,
        }
    )

    print("\n\nExample synthetic data:")
    print(df_synthesized)


def synthesize_one_from_full_user_message(user_message: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """
                    You will see some example text combinations, and will be asked
                    to output a prediction for a new example.
                    Example input:
                        
                        Question: What color is the sky?
                        Answer: Blue

                        New example: 
                        Question: What is the capital of France?
                        Answer: 

                    Expected output:
                            
                            Paris
                """,
            },
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content


def synthesize_one_helper(
    df_labeled_examples, record_observed, column_to_predict
):
    """
    Example input:
    df_labeled_examples: | Question | Answer |
                         |----------|--------|
                         | What is the capital of France? | Paris |
                         | What color is the sky? | Blue |

    record_observed: {"Answer": "Yellow}

    Example output: "What color is a banana?
    """

    columns = set(df_labeled_examples.columns)
    observed_columns = set(record_observed.keys())
    if observed_columns | {column_to_predict} != columns:
        raise ValueError(
            "union of observed and columns to predict must be the same"
            "as the columns in the labeled examples"
        )

    if len(observed_columns & {column_to_predict}) > 0:
        raise ValueError(
            "observed columns and column to predict must be disjoint"
        )

    def _few_shot_example(row: pd.Series):
        out = ""
        for k, v in row.items():
            out += "\t" + str(k) + ": " + str(v) + "\n"

        return out

    few_shot_str = "\n".join(
        df_labeled_examples.apply(_few_shot_example, axis=1)
    )

    observed_str = "\n".join(f"{k}: {v}" for k, v in record_observed.items())

    user_message = f"""
        {few_shot_str}
        
        New example:
        {observed_str}
        {column_to_predict}:
    """

    return synthesize_one_from_full_user_message(user_message)


def synthesize_helper(df_labeled_examples, df_observed, column_to_predict):
    return [
        synthesize_one_helper(df_labeled_examples, record, column_to_predict)
        for record in df_observed.to_dict(orient="records")
    ]


def generate_synthetic_answers(
    labeled_questions: Sequence[str],
    labeled_contexts: Sequence[str],
    answers: Sequence[str],
    unlabeled_questions: Sequence[str],
    unlabeled_contexts: Sequence[str],
):
    df = pd.DataFrame(
        {
            "Question": labeled_questions,
            "Context": labeled_contexts,
            "Answer": answers,
        }
    )

    df_observed = pd.DataFrame(
        {"Question": unlabeled_questions, "Context": unlabeled_contexts}
    )

    return synthesize_helper(df, df_observed, "Answer")


if __name__ == "__main__":
    main()
