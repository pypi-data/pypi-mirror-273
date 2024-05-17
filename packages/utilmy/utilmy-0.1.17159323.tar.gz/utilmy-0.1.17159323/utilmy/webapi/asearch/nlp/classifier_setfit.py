"""  

Docs:

        Multilabel strategies
        SetFit will initialise a multilabel classification head from sklearn - the following options are available for multi_target_strategy:

        "one-vs-rest": uses a OneVsRestClassifier head.
        "multi-output": uses a MultiOutputClassifier head.
        "classifier-chain": uses a ClassifierChain head.
        See the scikit-learn documentation for multiclass and multioutput classification for more details.

        Initializing SetFit models with multilabel strategies
        Using the default LogisticRegression head, we can apply multi target strategies like so:

        Copied
        from setfit import SetFitModel

        model = SetFitModel.from_pretrained(
            model_id, # e.g. "BAAI/bge-small-en-v1.5"
            multi_target_strategy="multi-output",
        )
        With a differentiable head it looks like so:

        Copied
        from setfit import SetFitModel

        model = SetFitModel.from_pretrained(
            model_id, # e.g. "BAAI/bge-small-en-v1.5"
            multi_target_strategy="one-vs-rest"
            use_differentiable_head=True,
            head_params={"out_features": num_classes},
        )

        https://github.com/huggingface/setfit/blob/main/notebooks/text-classification_multilabel.ipynb
         

"""


from datasets import load_dataset
from setfit import SetFitModel, Trainer, TrainingArguments, sample_dataset



def train():
    # Load a dataset from the Hugging Face Hub
    dataset = load_dataset("sst2")

    # Simulate the few-shot regime by sampling 8 examples per class
    train_dataset = sample_dataset(dataset["train"], label_column="label", num_samples=8)
    eval_dataset = dataset["validation"].select(range(100))
    test_dataset = dataset["validation"].select(range(100, len(dataset["validation"])))

    # Load a SetFit model from Hub
    model_id=         "sentence-transformers/paraphrase-mpnet-base-v2"

    model = SetFitModel.from_pretrained(
            model_id, # e.g. "BAAI/bge-small-en-v1.5"
            multi_target_strategy="one-vs-rest",
            use_differentiable_head=True,
            head_params={"out_features": num_classes},
        )

    model = SetFitModel.from_pretrained(

        labels=["negative", "positive"],
    )

    args = TrainingArguments(
        batch_size=16,
        num_epochs=4,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        metric="accuracy",
        column_mapping={"sentence": "text", "label": "label"}  # Map dataset columns to text/label expected by trainer
    )

    # Train and evaluate
    trainer.train()
    metrics = trainer.evaluate(test_dataset)
    print(metrics)
    # {'accuracy': 0.8691709844559585}

    ## Push model to the Hub
    ## trainer.push_to_hub("tomaarsen/setfit-paraphrase-mpnet-base-v2-sst2")

    # Download from Hub
    model = SetFitModel.from_pretrained("tomaarsen/setfit-paraphrase-mpnet-base-v2-sst2")
    # Run inference
    preds = model.predict(["i loved the spiderman movie!", "pineapple on pizza is the worst 🤮"])
    print(preds)
    # ["positive", "negative"]

from datasets import Dataset
import pandas as pd

def pandas_to_hf_dataset(df: pd.DataFrame) -> Dataset:
    return Dataset.from_pandas(df)



from datasets import Dataset

def save_hf_dataset(dataset: Dataset, path: str):
    dataset.save_to_disk(path)

# Example usage:
# dataset = Dataset.from_dict({'column1': [1, 2], 'column2': ['a', 'b']})
# save_hf_dataset(dataset, "path/to/save/dataset")




###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()




