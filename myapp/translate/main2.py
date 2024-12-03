import gradio as gr
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    pipeline,
    AutoModelForCausalLM,
    TextIteratorStreamer,
    StoppingCriteria,
    StoppingCriteriaList,
)
from threading import Thread

import torch
import sys
import os

# this model was loaded from https://hf.co/models
# model_id = "/home/flame/Llama-8B-Instruct"
model_id = "/home/flame/Model/Evo2_32"
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)
LANGS = ["English", "Chinese", "Spanish", "French", "Arabic"]
# print(tokenizer._id)
# sys.exit(-1)

class StopOnTokens(StoppingCriteria):
    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        stop_ids = [29, 0, 128009]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

def translate(text, src_lang, tgt_lang):
    """
    Translate the text from source lang to target lang
    """
    SYSTEM_PROMPT = f"Acts as a translator. Translate {src_lang} sentences into {tgt_lang} sentences in written style."
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
        max_new_tokens=256,
        do_sample=True,
        top_p=0.95,
        top_k=1000,
        temperature=1.0,
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
        margin-right: 200px
    }
    .gradio-app-header img {
        margin-left: 200px;
        margin-right: 60px
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
            """<div class='gradio-app-header'><img src='https://static.wixstatic.com/media/57e244_1d2901d649c34d6f9ce37a75285a42f1~mv2.png' alt='App Logo' style='width: 150px; height: auto;'><h1 style="padding-bottom: 16px;">Welcome to MINDLAB</h1></div>
            <div class="sub-title" style="align-items: center;padding-left: 400px;padding-right: 400px;"><h2>Multilingul Translator</h2></div>"""
    )
    with gr.Row():
        with gr.Column():
            src_lang = gr.components.Dropdown(label="Source Language", choices=LANGS)
            text = gr.components.Textbox(lines=14, label="Text")
            submit_button = gr.Button("Go for Translation!")
        with gr.Column():
            tgt_lang = gr.components.Dropdown(label="Target Language", choices=LANGS)
            output = gr.components.Textbox(
                lines=14, label="Translated Text", interactive=False
            )
    submit_button.click(
        fn=translate,
        inputs=[text, src_lang, tgt_lang],
        outputs=output,
    )

demo.launch()
