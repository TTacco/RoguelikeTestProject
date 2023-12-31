#Handles map, entity drawing and player inputs
from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            #print("THE EVENT - ", event)
            action = self.event_handler.dispatch(event)
            #print("THE ACTION - ", action)
            if action is None:
                continue

            action.perform(self, self.player)
            self.update_fov()

    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view"""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"], 
            (self.player.x, self.player.y),
            radius=3,
        )

        self.game_map.explored |= self.game_map.visible


    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            #console.print(entity.x, entity.y, entity.char, fg=entity.color)
            #Only print entities that are in the FOV
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)
        
        context.present(console)
        console.clear()
