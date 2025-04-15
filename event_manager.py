class EventManager:
    def __init__(self):
        self.events = {}

    def register_event(self, event_name, callback):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(callback)

    def trigger_event(self, event_name, *args, **kwargs):
        if event_name in self.events:
            for callback in self.events[event_name]:
                callback(*args, **kwargs)

# Create a global instance of the event manager
event_manager = EventManager()