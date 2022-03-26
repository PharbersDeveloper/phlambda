import json
import logging

from forwardEvent import ForwardEvent
from util.phLog.phLogging import PhLogging, LOG_DEBUG_LEVEL


class Execute:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.logger = PhLogging().phLogger("创建流程入口", LOG_DEBUG_LEVEL)

    def exec(self):
        ForwardEvent(event=self.event).execute()


if __name__ == '__main__':
    with open("../events/event_create_project.json") as f:
        event = json.load(f)
    app = Execute(event=event)
    app.exec()