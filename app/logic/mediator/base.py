from dataclasses import dataclass
from typing import Iterable

from logic.commands.base import CT, BaseCommandHandler, CR
from logic.events.base import ET, ER, BaseEventHandler
from logic.exceptions.mediator import CommandHandlerNotRegisteredException
from logic.mediator.command import CommandMediator
from logic.mediator.event import EventMediator
from logic.mediator.query import QueryMediator
from logic.queries.base import QT, BaseQueryHandler, QR


@dataclass
class Mediator(CommandMediator, EventMediator, QueryMediator):
    def register_command(self, command: CT, command_handlers: Iterable[BaseCommandHandler[CT, CR]]):
        self.commands_map[command].extend(command_handlers)

    def register_event(self, event: ET, event_handlers: Iterable[BaseEventHandler[ET, ER]]):
        self.events_map[event].extend(event_handlers)

    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]):
        self.queries_map[query] = query_handler

    async def handle_command(self, command: CT) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlerNotRegisteredException(command_type=command_type)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: QT) -> QR:
        return await self.queries_map[query.__class__].handle(query)

    async def handle_event(self, events: Iterable[ET]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers = self.events_map[event.__class__]
            result.extend([await handler.handle(event) for handler in handlers])

        return result
