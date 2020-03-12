class Repository:
    def show(self, name: str, version: str):
        raise NotImplementedError()

    def download(self, name: str, version: str):
        raise NotImplementedError()
