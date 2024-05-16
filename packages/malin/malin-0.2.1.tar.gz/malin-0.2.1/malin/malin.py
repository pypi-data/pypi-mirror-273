from typing import Callable
from flask import Flask 
from dataclasses import dataclass

from malin.models import ScanSummary
from malin.actions import ScanAction

@dataclass
class Malin :
    engine: Callable[[str], str]
    parser: Callable[[str], ScanSummary]
 
    def __post_init__(self):
        self.app = Flask("malin")
        
        self.app.add_url_rule('/api/v1/file', 'UploadFile', ScanAction(self.engine, self.parser), methods=['POST'])   
        self.app.add_url_rule('/api/v1/update', 'UpdateEngine', ScanAction(self.engine, self.parser), methods=['POST'])   
        
        
    def run(self, host='0.0.0.0', port=5000):
        # Run the malin flask api
        # Parameters
        # Port
        self.app.run(host=host, port=port)
