#!/usr/bin/env python3
import asyncio
from nicegui import ui, app
from utils.utils import ToDoList, todo_ui, TodoItem
import utils.utils as dnd
from dataclasses import dataclass
from multiprocessing import Manager, Queue
import time

app.add_static_files('/images', './images')


def handle_drop(todo: TodoItem, location: str):
    ui.notify(f'"{todo.name}" is now in {location}')

todos = ToDoList('', on_change=todo_ui.refresh)

def add_model_pool(todos: ToDoList):
    pass
    # card = ui.card().classes(' items-stretch')
    # with card:
    #     ui.label().bind_text_from(todos, 'title').classes('text-bold ml-1 text-2xl')
    #     todo_ui(todos)

def add_drag(model_pool: dnd.column, model_merge: dnd.column):
    with model_pool:
        dnd.card(TodoItem('Simplify Layouting'))
    with model_merge:
        dnd.card(TodoItem('Improve Documentation'))

def compute_():
    with ui.dialog() as dialog, ui.card():
        ui.label('Hello world!')
        ui.button('Close', on_click=dialog.close)
    dialog.open()

ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')
src = 'https://assets1.lottiefiles.com/datafiles/HN7OcWNnoqje6iXIiZdWzKxvLIbfeCGTmvXmEm1h/data.json'
src = 'images/kobe.gif'
async def compute():
    with ui.dialog() as dialog, ui.card():
        with ui.column(align_items='center'):
            ui.label('Merging...').classes('text-2xl')
            # ui.html(f'<lottie-player src="{src}" loop autoplay />')
            ui.image(src).props("width=400px height=400px")
            ui.button('Close', on_click=dialog.close)
    dialog.open()
    n = ui.notification(timeout=None)
    for i in range(10):
        n.message = f'Computing {i/10:.0%}'
        n.spinner = True
        await asyncio.sleep(0.2)
    n.message = 'Done!'
    n.spinner = False
    await asyncio.sleep(1)
    n.dismiss()


with ui.row().classes('w-full mx-auto items-stretch'):
    # with ui.row().classes('mx-auto content-center items-stretch'):
    with ui.column().classes(' mx-auto content-center items-stretch'):
        add_model_pool(todos)
        model_pool = dnd.column('Model Pool', on_drop=handle_drop)
        model_merge = dnd.column('Models to be merged', on_drop=handle_drop)
        todos.add('Llama', model_pool)
        todos.add('QWen', model_pool)
        todos.add('Llama', model_pool)
        todos.add('QWen', model_pool)
        todos.add('Llama', model_merge)
        todos.add('QWen', model_merge)
        # add_drag(model_pool, model_merge)
    # with ui.row(align_items='center').classes('w-full mx-auto content-center items-stretch'):
    with ui.column().classes('mx-auto content-center items-stretch'):
        ui.label('').classes('h-[100px] text-bold text-2xl')
        with ui.card().classes('w-[1100px] mx-auto items-stretch'):
            with ui.column(align_items='center'):
                with ui.column(align_items='center'):
                    with ui.row(align_items='center').classes('content-center'):
                        ui.image('images/mindlab.png').props('width=300px height=').classes("bg-white")
                        ui.label('MINDLAB APP --- MODEL MERGE').classes("font-bold text-5xl text-black")
                    ui.label('Merge Options').classes('text-bold text-2xl')
                    with ui.row():
                        with ui.column():
                            with ui.row(align_items='center'):
                                ui.checkbox("architectural space").classes('text-lg flex-grow')
                            ui.space()
                            with ui.row(align_items='center'):
                                ui.label("Select the EA algorithm:").classes('text-lg flex-grow')
                                ui.select({1: 'One', 2: 'Two', 3: 'Three'}, value=1).classes('text-lg flex-grow')
                        ui.space()
                        with ui.column():
                            with ui.row(align_items='center'):
                                # ui.label("Maximum number of iterations:").classes('text-lg flex-grow')
                                ui.input("Maximum number of iterations:" , value=10).classes('text-lg flex-grow').props('clearable')
                            ui.space()
                            with ui.row(align_items='center'):
                                # ui.label().classes('text-lg flex-grow')
                                ui.input("Population size:", value=10).classes('text-lg flex-grow').props('clearable')
                    # Create the UI
                # ui.button('', icon='thumb_up').classes('w-1/2 h-[50px]')
                with ui.row().classes('items-stretch'):
                    ui.button('Go Merging!', on_click=compute, icon='published_with_changes').classes('w-[500px] h-[80px] text-xl flex-grow')
                    ui.button('Go Chatting', icon='diversity_3').classes('w-[500px] h-[80px] text-xl flex-grow')
                    ui.button('Go Translation', icon='translate').classes('w-[500px] h-[80px] text-xl flex-grow')
                    ui.button('Go Summary', icon='grading').classes('w-[500px] h-[80px] text-xl flex-grow')

ui.run(native=False, )
