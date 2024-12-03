#!/usr/bin/env python3
from langchain_openai import ChatOpenAI
from log_callback_handler import NiceGuiLogElementCallbackHandler
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

from nicegui import ui, app
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, pipeline, TextStreamer
from threading import Thread


app.add_static_files('/images', './images')
model_id = "/home/flame/Llama-8B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)
streamer = TextIteratorStreamer(tokenizer)

# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForCausalLM.from_pretrained(model_id)
# pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=500)
# llm = HuggingFacePipeline(pipeline=pipe)
# chat_model = ChatHuggingFace(llm=llm)

# llm = HuggingFacePipeline.from_model_id(
#     model_id=model_id,
#     task="text-generation",
#     device_map="auto",
#     pipeline_kwargs={"max_new_tokens": 100, "top_k": 10, "trust_remote_code": True, 'do_sample': True, 'num_return_sequences': 1},
# )
# chat_model = ChatHuggingFace(llm=llm, verbose=True)
# chat_model.llm.pipeline.tokenizer.pad_token_id = chat_model.llm.pipeline.tokenizer.eos_token_id



OPENAI_API_KEY = 'not-set'  # TODO: set your OpenAI API key here


@ui.page('/')
def main():
    with ui.header(bordered=True, elevated=True).style('background-color: #3874c8') as header:
        with ui.row(align_items='center').classes('content-center'):
            ui.image('images/mindlab.png').props('width=120px height=80px').classes("bg-white")
            ui.label('MIND LAB APP --- MULTILINGUAL CHAT').classes("font-bold text-2xl text-white")
    # llm = ChatOpenAI(model_name='gpt-3.5-turbo', streaming=True, openai_api_key=OPENAI_API_KEY)

    async def send() -> None:
        question = text.value
        text.value = ''

        async def question_answer(query):
            message = [{"role": "user", "content": query}]
            conversion = tokenizer.apply_chat_template(message, add_generation_prompt=True, tokenize=False)
            encoding = tokenizer(conversion, return_tensors="pt")
            streamer = TextIteratorStreamer(tokenizer)
            generation_kwargs = dict(encoding, streamer=streamer, max_new_tokens=1000, do_sample=True, temperature=0.2)
            # thread = Thread(target=model.generate, kwargs=generation_kwargs)
            # thread.start()

            generate_text = ''
            model.generate(generation_kwargs)
            for new_text in streamer:
                output = new_text.replace(conversion, '')
                if output:
                    generate_text += output
                    yield generate_text
        
        with message_container:
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Bot', sent=False)
            spinner = ui.spinner(type='dots')

        print(question)
        response = ''
        response_message.clear()
        # async for new_text in question_answer(query):
        #     with response_message:
        #         output = new_text.replace(conversion, '')
        #         ui.html(output)
        # async for chunk in chat_model.astream(question, config={'callbacks': [NiceGuiLogElementCallbackHandler(log)]}):
        #     response += chunk.content
        #     # print(response)
        #     response_message.clear()
        #     with response_message:
        #         ui.html(response)
        #     ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')

    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Chat')
        logs_tab = ui.tab('Logs')
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
        message_container = ui.tab_panel(chat_tab).classes('items-stretch')
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('Multilingual chat by [MINDLAB](https://www.mindlab-ai.com/)') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')


ui.run(title='Chat with GPT-3 (example)')