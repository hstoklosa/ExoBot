
class BaseModel():

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

    def api(self):

        if self._api is None:
            raise Exception('API key cannot be None!')

        return self._api