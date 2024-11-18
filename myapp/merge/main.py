#!/usr/bin/env python3
import asyncio
from nicegui import ui, app
from utils.utils import ToDoList, todo_ui, TodoItem
import utils.utils as dnd
from dataclasses import dataclass
from multiprocessing import Manager, Queue
import time

app.add_static_files('/images', './images')

with ui.header(bordered=True, elevated=True).style('background-color: #3874c8') as header:
    with ui.row(align_items='center').classes('content-center'):
        ui.image('images/mindlab.png').props('width=120px height=80px').classes("bg-white")
        ui.label('MIND LAB APP --- MODEL MERGE').classes("font-bold text-2xl text-white")

def handle_drop(todo: TodoItem, location: str):
    ui.notify(f'"{todo.name}" is now in {location}')

todos = ToDoList('Model Adjusting', on_change=todo_ui.refresh)

def add_model_pool(todos: ToDoList):
    card = ui.card().classes('w-50 items-stretch')
    with card:
        ui.label().bind_text_from(todos, 'title').classes('text-bold ml-1 text-2xl')
        todo_ui(todos)
    global model_pool
    global model_merge
    model_pool = dnd.column('Model Pool', on_drop=handle_drop)
    model_merge = dnd.column('Models to be merged', on_drop=handle_drop)
    with card:
        add_input = ui.input('New Models').classes('mx-12').mark('new-item')
        add_input.on('keydown.enter', lambda: todos.add(add_input.value, model_pool))
        add_input.on('keydown.enter', lambda: add_input.set_value(''))

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

with ui.column():
    with ui.row().classes('content-center'):
        add_model_pool(todos)
        # add_drag(model_pool, model_merge)

    with ui.card().classes('w-50 items-stretch'):
        with ui.column():
            ui.label('Merge Options').classes('text-bold text-2xl')
            with ui.row():
                with ui.row(align_items='center'):
                    ui.checkbox("architectural space").classes('text-lg flex-grow')
                ui.space()
                with ui.row(align_items='center'):
                    # ui.label("Maximum number of iterations:").classes('text-lg flex-grow')
                    ui.input("Maximum number of iterations:" , value=10).classes('text-lg flex-grow').props('clearable')
                ui.space()
                with ui.row(align_items='center'):
                    # ui.label().classes('text-lg flex-grow')
                    ui.input("Population size:", value=10).classes('text-lg flex-grow').props('clearable')
                ui.space()
                with ui.row(align_items='center'):
                    ui.label("Select the EA algorithm:").classes('text-lg flex-grow')
                    ui.select({1: 'One', 2: 'Two', 3: 'Three'}, value=1).classes('text-lg flex-grow')
            # Create the UI
        ui.button('Go Merging!', on_click=compute, icon='thumb_up')

ui.run(native=False, )
