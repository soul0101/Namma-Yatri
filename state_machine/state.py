from __future__ import annotations

class State():
    pickup_locations_array = None
    drop_locations_array = None
    pickup_location = None
    drop_location = None

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context) -> None:
        self._context = context

    def flow_handler(self, data) -> None:
        pass