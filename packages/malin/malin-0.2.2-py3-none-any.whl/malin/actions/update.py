from dataclasses import dataclass
from flask import jsonify
from typing import Callable

@dataclass
class UpdateAction(object):
    engine: Callable[[str]]

    def __call__(self, *args, **kwargs):
        # TODO
        self.engine()
        return jsonify()