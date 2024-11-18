from __future__ import annotations

from typing import Callable, Optional, Protocol

from nicegui import ui

from dataclasses import dataclass, field
from typing import List



class Item(Protocol):
    title: str


dragged: Optional[card] = None


class column(ui.column):

    def __init__(self, name: str, on_drop: Optional[Callable[[Item, str], None]] = None) -> None:
        super().__init__()
        with self.classes('bg-blue-grey-2 w-80 p-4 rounded shadow-2'):
            ui.label(name).classes('text-bold ml-1 text-2xl')
        self.name = name
        self.on('dragover.prevent', self.highlight)
        self.on('dragleave', self.unhighlight)
        self.on('drop', self.move_card)
        self.on_drop = on_drop

    def highlight(self) -> None:
        self.classes(remove='bg-blue-grey-2', add='bg-blue-grey-3')

    def unhighlight(self) -> None:
        self.classes(remove='bg-blue-grey-3', add='bg-blue-grey-2')

    def move_card(self) -> None:
        global dragged  # pylint: disable=global-statement # noqa: PLW0603
        self.unhighlight()
        dragged.parent_slot.parent.remove(dragged)
        with self:
            dragged.item.card = card(dragged.item)
        self.on_drop(dragged.item, self.name)
        dragged = None


class card(ui.card):

    def __init__(self, item: TodoItem) -> None:
        super().__init__()
        self.item = item
        with self.props('draggable').classes('w-full cursor-pointer bg-grey-1'):
            ui.label(item.name)
        self.on('dragstart', self.handle_dragstart)

    def handle_dragstart(self) -> None:
        global dragged  # pylint: disable=global-statement # noqa: PLW0603
        dragged = self

@dataclass
class TodoItem:
    name: str
    chosen: bool = False
    weight: float = 0.5
    card: ui.card = None

@dataclass
class ToDoList:
    title: str
    on_change: Callable
    items: List[TodoItem] = field(default_factory=list)

    def add(self, name: str, model_pool: column, chosen: bool = False) -> None:
        todo_item = TodoItem(name, chosen)
        with model_pool:
            todo_item.card = card(todo_item)
        self.items.append(todo_item)
        self.on_change()

    def remove(self, item: TodoItem) -> None:
        item.card.delete()
        self.items.remove(item)
        self.on_change()

@ui.refreshable
def todo_ui(todos: ToDoList):
    if not todos.items:
        ui.label('There is no model.').classes('mx-auto')
        return
    ui.linear_progress(sum(item.chosen for item in todos.items) / len(todos.items), show_value=False)
    with ui.row().classes('justify-center w-full'):
        ui.label(f'Selected: {sum(item.chosen for item in todos.items)}')
        ui.label(f'Total: {len(todos.items)}')
    for item in todos.items:
        with ui.row().classes('items-center'):
            ui.checkbox(value=item.chosen, on_change=todo_ui.refresh).bind_value(item, 'chosen') \
                .mark(f'checkbox-{item.name.lower().replace(" ", "-")}')
            ui.label(item.name).classes('flex-grow')
            ui.space()
            ui.slider(value=0.5, min=0, max=1, step=0.1).classes("w-40").bind_value(item, 'weight')
            ui.input(value=item.weight).classes('w-10').bind_value(item, 'weight').set_enabled(False)
            ui.button(on_click=lambda item=item: todos.remove(item), icon='delete').props('flat fab-mini color=grey')
