import json
from pathlib import Path
from database.conexao import Database

class DataManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.db = Database()
        self.load_from_json('dados_json.json')
        

    def load_from_json(self, filename: str):
        file_path = self.data_dir / filename
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            
            for item in data['acoes']:
                self.db.inserir_acao(item)
            
        
        