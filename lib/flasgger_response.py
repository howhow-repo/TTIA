class FlasggerResponse:
    def __init__(self, result: str = 'success', error_code: int = 0, message: str = None):
        r = {
            'result': result,
            'error_code': error_code,
        }
        if message is not None:
            r['message'] = message
        self.response = r
