# Fine-Tuning GPT-2 for Poems and Stories

This directory contains scripts to fine-tune GPT-2 on your own dataset.

## Prerequisites

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Data Preparation

To train the model to generate poems or stories based on a theme, you should prepare your data in a specific format. Create a file named `train_data.txt` (or modify the script to point to your file).

**Recommended Format:**
Use a consistent prompt structure so the model learns to respond to it.

```text
Story about Rainy Day:
The rain tapped against the window pane, a steady rhythm that echoed the beating of her heart...

Write a poem about Love:
In the garden of my heart, a rose began to bloom...

Story about Space Adventure:
Captain Reynolds looked out at the vast expanse of stars...
```

The more data you have (thousands of examples), the better the results.

## Running the Training

Run the script:

```bash
python fine_tune.py
```

This will:
1. Load GPT-2.
2. Load your `train_data.txt`.
3. Fine-tune the model.
4. Save the new model to `./finetuned_model`.

## Using the Fine-Tuned Model

### Locally
You can load the model in your backend code:

```python
generator = pipeline('text-generation', model='./finetuned_model')
```

### On Hugging Face
1. Create a new model repository on Hugging Face.
2. Upload the contents of `./finetuned_model` to that repository.
3. Update your backend code to use your new model ID:

```python
generator = pipeline('text-generation', model='your-username/your-model-name')
```

## Training on Google Colab (Free GPU)

If you don't have a powerful GPU locally, you can use Google Colab.

1.  **Download the Notebook**:
    Download the `AI_Story_Poem_Trainer.ipynb` file from this directory.

2.  **Open in Colab**:
    - Go to [Google Colab](https://colab.research.google.com/).
    - Click **File > Upload notebook**.
    - Upload `AI_Story_Poem_Trainer.ipynb`.

3.  **Enable GPU**:
    - In Colab, go to **Runtime > Change runtime type**.
    - Select **T4 GPU** (or any available GPU) under Hardware accelerator.
    - Click **Save**.

4.  **Run the Steps**:
    Follow the instructions in the notebook cells.
    - You will need to upload your `train_data.txt` to the Colab file system (drag and drop it into the folder icon on the left).
    - If you want to deploy the model, follow the last step in the notebook to push it to Hugging Face.

