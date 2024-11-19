#!/usr/bin/env python3
import asyncio
from nicegui import ui, app
from dataclasses import dataclass
from multiprocessing import Manager, Queue
import time

app.add_static_files('/images', './images')

with ui.header(bordered=True, elevated=True).style('background-color: #3874c8') as header:
    with ui.row(align_items='center').classes('content-center'):
        ui.image('images/mindlab.png').props('width=120px height=80px').classes("bg-white")
        ui.label('MIND LAB APP --- TRANSLATOR').classes("font-bold text-2xl text-white")

with ui.column():
    with ui.row().classes('content-center'):
        with ui.card().classes('w-[1000px] mx-auto items-stretch'):
            with ui.column(align_items='stretch'):
                with ui.row(align_items='stretch').classes('mx-auto items-stretch'):
                    ui.textarea(label='Input', placeholder='start typing').props('clearable').classes('w-[450px] items-stretch')
                    ui.textarea(label='Output', placeholder='start typing').props('clearable').classes('w-[450px] items-stretch')
                ui.button('Go Translating!', icon='thumb_up')

ui.run(native=False, )
