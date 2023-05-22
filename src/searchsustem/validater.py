class ValidaterSearchText:
    """
    Сделать валидацию на ругательства
    """
    def __init__(self, text):
        self.text = text

    def __call__(self):
        return len(self.text) > 3