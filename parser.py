import base64

class Parser:
    def __init__(self, filenames):
        self.filenames = filenames
        self.data = []
        
    def load(self):
        """Encode image to base64"""
        for filename in self.filenames:
            with open(filename, "rb") as image_file:
                self.data.append(base64.b64encode(image_file.read()).decode("utf-8"))
    
    def get_data(self):
        if not self.data:
            self.load()
        return self.data
