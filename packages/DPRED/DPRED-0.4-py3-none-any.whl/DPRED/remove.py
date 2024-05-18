import os

class Remove:
    def __init__(self, path: str) -> None: 
        self.path = path
        
    def remove(self) -> None:
        if os.path.isfile(self.path): os.remove(self.path)
        elif os.path.isdir(self.path): os.system(f'rm -rf {self.path}')