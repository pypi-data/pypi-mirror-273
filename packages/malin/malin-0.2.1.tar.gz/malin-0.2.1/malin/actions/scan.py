from dataclasses import dataclass
from flask import  Response, jsonify, request
from typing import Callable
import tempfile

from malin.models import ScanSummary, ScanError
from malin.errors import InvalidOutput

@dataclass
class ScanAction(object):
    engine: Callable[[str], str]
    parser: Callable[[str], ScanSummary]
    _response: Response = Response(status=200, headers={})

    def __call__(self, *args, **kwargs):
        if 'file' not in request.files:
            return jsonify(ScanError(error='No file part')), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify(ScanError(error='No selected file')), 400


        filepath: str = f'{tempfile.gettempdir()}\{file.filename}'

        if not file:
            return jsonify(ScanError(error='Something went wrong')), 500

        # Saving the file
        file.save(filepath)

        # Call engine function
        output: str = self.engine(filepath)

        # Call parser function
        try :
            summary: ScanSummary = self.parser(output)
            return jsonify(summary)
        except InvalidOutput as err:
            return jsonify(ScanError(err.message))