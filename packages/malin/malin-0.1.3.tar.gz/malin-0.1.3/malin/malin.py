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
         
        self.app.add_url_rule('/', 'UploadFile', ScanAction(self.engine, self.parser), methods=['POST'])   
        
    def run(self, host='127.0.0.1', port=5000):
        self.app.run(host=host, port=port)
