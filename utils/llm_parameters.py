class Params:
    model: str
    url: str
    token: str

    def __init__(self, model: str, url: str, token: str):
        self.model = model
        self.url = url
        self.token = token
