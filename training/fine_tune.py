import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from datasets import load_dataset

def fine_tune_gpt2(
    model_name="gpt2",
    output_dir="./finetuned_model",
    train_file="train_data.txt",
    epochs=3,
    batch_size=4
):
    """
    Fine-tunes GPT-2 on a text file.
    
    Args:
        model_name: Base model name (e.g., 'gpt2', 'gpt2-medium')
        output_dir: Directory to save the fine-tuned model
        train_file: Path to a text file containing training data
        epochs: Number of training epochs
        batch_size: Batch size for training
    """
    
    # 1. Load Tokenizer and Model
    print(f"Loading {model_name}...")
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # GPT-2 doesn't have a pad token by default, so we add one
    tokenizer.pad_token = tokenizer.eos_token

    # 2. Prepare Dataset
    # We use the TextDataset helper for simplicity with raw text files.
    # For more complex structures (like JSON with "prompt" and "completion"), 
    # you would use the `datasets` library and a custom mapping function.
    
    print(f"Loading dataset from {train_file}...")
    if not os.path.exists(train_file):
        print(f"Error: {train_file} not found. Please create a text file with your training data.")
        return

    # Block size is the maximum length of a sequence
    block_size = 128 
    
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_file,
        block_size=block_size,
        overwrite_cache=True
    )
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )

    # 3. Training Arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        save_steps=500,
        save_total_limit=2,
        prediction_loss_only=True,
        learning_rate=5e-5,
    )

    # 4. Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )

    # 5. Train
    print("Starting training...")
    trainer.train()
    
    # 6. Save Model
    print(f"Saving model to {output_dir}...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Done!")

if __name__ == "__main__":
    # Example usage:
    # Create a dummy file if it doesn't exist for demonstration
    if not os.path.exists("train_data.txt"):
        print("Creating dummy train_data.txt...")
        with open("train_data.txt", "w") as f:
            f.write("Write a poem about Rain:\nThe rain falls gently on the roof, a rhythmic tapping, a soothing proof.\n\n")
            f.write("Story about The Sun:\nThe sun shone brightly over the valley. It was a day unlike any other, where the birds sang melodies of old.\n\n")
            f.write("Write a poem about Love:\nLove is a rose, a tender bloom, dispelling shadows, chasing gloom.\n\n")
            # Add more data here!
    
    fine_tune_gpt2()
