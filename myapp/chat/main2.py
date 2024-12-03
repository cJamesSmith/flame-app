import gradio as gr
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer,
)
from threading import Thread
import sys
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "3,4,5"

sys.path.append(".")
print(sys.path)

# model_id = "/home/flame/Llama-8B-Instruct"
model_id = "/home/flame/Model/Evo2_32"
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

task_str = ["Q&A", "Multi-turn Chat"]

class StopOnTokens(StoppingCriteria):
    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        stop_ids = [29, 0, 128009]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


def predict(message, history, task):
    history_transformer_format = list(zip(history[:-1], history[1:])) + [[message, ""]]
    print(task)
    stop = StopOnTokens()

    if task == task_str[0]:
        message = [{"role": "user", "content": "Please answer this question by choosing a following option, do not explain the answer: \n<" + message + ">"}]
    else:
        # message = "".join(["".join(["\n<human>:"+item[0], "\n<bot>:"+item[1]])
        #     for item in history_transformer_format])
        message = [{"role": "system", "content": "Please chat with me in terms of the information I give you."},
                   {"role": "user", "content": message}]
    messages = tokenizer.apply_chat_template(
        message, add_generation_prompt=True, tokenize=False
    )
    model_inputs = tokenizer([messages], return_tensors="pt")
    streamer = TextIteratorStreamer(
        tokenizer, skip_prompt=True, skip_special_tokens=True
    )
    generate_kwargs = dict(
        model_inputs,
        streamer=streamer,
        max_new_tokens=1024,
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
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    .gradio-app-header {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 120px
    }
    .gradio-app-header img {
        margin-left: 120px;
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
    footer {visibility: hidden}
    """,
    fill_height=True,
    fill_width=True,
    title="MINDLAB",
) as demo:
    with gr.Column():
        gr.HTML(
            """<div class='gradio-app-header'><img src='https://static.wixstatic.com/media/57e244_1d2901d649c34d6f9ce37a75285a42f1~mv2.png' alt='App Logo' style='width: 150px; height: auto;'><h1 style="padding-bottom: 16px;">Welcome to MINDLAB</h1></div>
            <div class="sub-title" style="align-items: center;padding-left: 400px;padding-right: 400px;"><h2>Multilingul Chatter</h2></div>"""
        )
        # gr.Markdown("Start typing below and then click **Run** to see the output.")
        with gr.Row():
            with gr.Column(scale=0.3):
                with gr.Blocks(title="Model Pool"):
                    gr.Button("Merged Multilingul LLM", variant="primary")
                    gr.Button("Qwen2.5-7B-Instruct")
                    gr.Button("Qwen-7B-Chat")
                    gr.Button("Ministral-8B-Instruct")
                    gr.Button("Llama-3-8B-French")
                    gr.Button("Llama-3-8B-Chinese")
                    gr.Button("Llama-3-8B-Arabic")
                    gr.Button("Llama-3-8B-Turkish")
                    gr.Button("Llama-3-8B-Spanish")
                    gr.Button("Llama-3-8B-English")
                    task = gr.Dropdown(task_str, value=task_str[0], label="Task Choices")
            with gr.Column(scale=0.7, elem_classes="chat_inter"):
                chatbot = gr.ChatInterface(
                    predict,
                    theme=gr.themes.Soft(),
                    chatbot=gr.Chatbot(avatar_images=["human.png", "robot.png"], height=600, min_height=600),
                    additional_inputs=[task]
                )

demo.launch(allowed_paths=["/"], favicon_path="./human.png")
