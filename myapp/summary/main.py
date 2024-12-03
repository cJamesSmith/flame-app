import gradio as gr
import os
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    pipeline,
    AutoModelForCausalLM,
    TextIteratorStreamer,
    StoppingCriteria,
    StoppingCriteriaList,
)
import torch
from threading import Thread

# model_id = "/home/flame/Llama-8B-Instruct"
model_id = "/home/flame/Model/Evo2_32"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)


class StopOnTokens(StoppingCriteria):
    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        stop_ids = [29, 0, 128009]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


def generate_summary(text: str, temperature: float, max_new_tokens: int) -> str:
    """
    Generate a single-line summary from the input text using the llama3-8b model.
    Args:
        text (str): The input text to summarize.
        temperature (float): The temperature for generating the response.
        max_new_tokens (int): The maximum number of new tokens to generate.
    Returns:
        str: The generated summary in a single line.
    """

    SYSTEM_PROMPT = "Summarize the following document, covering essential parts:"
    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]
    stop = StopOnTokens()
    inputs = tokenizer.apply_chat_template(
        conversation, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([inputs], return_tensors="pt")
    streamer = TextIteratorStreamer(
        tokenizer, skip_prompt=True, skip_special_tokens=True
    )
    generate_kwargs = dict(
        model_inputs,
        streamer=streamer,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        top_p=0.95,
        top_k=1000,
        temperature=temperature,
        num_beams=1,
        stopping_criteria=StoppingCriteriaList([stop]),
    )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()
    partial_message = ""
    for new_token in streamer:
        if new_token != "<":
            partial_message += new_token
            yield partial_message


# Gradio block for text summarization
with gr.Blocks(
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 1200px;
        width:1200px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    .gradio-app-header {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 200px;
    }
    .gradio-app-header img {
        margin-left: 200px;
        margin-right: 60px;
        display: inline-block;
    }
    .gradio-app-header h1 {
        text-align: center;
        display:inline-block;
    }
    .sub-title {
        text-align: center;
        display:inline-block;
        justify-content: center;
        display: flex;
    }
    """,
    fill_height=True,
) as demo:
    gr.HTML(
        """<div class='gradio-app-header'><img src='https://static.wixstatic.com/media/57e244_1d2901d649c34d6f9ce37a75285a42f1~mv2.png' alt='App Logo' style='width: 100px; height: auto;'><h1 style="padding-bottom: 16px;">Welcome to MINDLAB</h1></div>
        <div class="sub-title" style="align-items: center;"><h2>TEXT SUMMARIZATION APPLICATION</h2></div>"""
    )
    with gr.Blocks():
        with gr.Column():
            with gr.Row():
                with gr.Column():
                    text_input = gr.Textbox(
                        lines=10, label="Input Text", placeholder="Enter text here..."
                    )
                    # file_input = gr.File(
                    #     label="Upload Text File", file_count="single", type="filepath"
                    # )
                    temperature = gr.Slider(
                        minimum=0, maximum=1, step=0.1, value=0.7, label="Temperature"
                    )
                    max_tokens = gr.Slider(
                        minimum=10,
                        maximum=512,
                        step=1,
                        value=150,
                        label="Max New Tokens",
                    )
                    submit_button = gr.Button("Generate Summary")
                with gr.Column():
                    summary_output = gr.Textbox(
                        lines=18, label="Summary", interactive=False
                    )

            # Link button to generate summary from text input
            submit_button.click(
                fn=generate_summary,
                inputs=[text_input, temperature, max_tokens],
                outputs=summary_output,
            )

    # Link file upload to summary generation
    # file_input.change(
    #     fn=summarize_file,
    #     inputs=[file_input, temperature, max_tokens],
    #     outputs=summary_output,
    # )

if __name__ == "__main__":
    demo.launch(allowed_paths=["/"])
