from base64 import b64encode
from gigachat import GigaChat


class GigaChatEntryPoint:
    def __init__(self, config):
        __client_id = config['gigachat_creds']['client_id']
        __client_secret = config['gigachat_creds']['client_secret']
        __creds = b64encode(f'{__client_id}:{__client_secret}'.encode('utf-8')).decode('utf-8')
        self.model = GigaChat(
            credentials=__creds,
            scope='GIGACHAT_API_CORP',
            verify_ssl_certs=False,
            model='GigaChat-Pro',
            profanity_check=False,
        )
        self.DIM = 1024
        self.ERROR_MESSAGE = 'Простите, я Вас не понял. Повторите, пожалуйста, поподробнее и другими словами'

    def __call__(self):
        return self.model

    def get_response(self, total_input: str) -> str:
        try:
            return self.model.chat(total_input).choices[0].message.content
        except:
            return self.ERROR_MESSAGE

    def get_embeddings(self, total_input: str) -> list:
        try:
            return self.model.embeddings(total_input).data[0].embedding
        except:
            return [0 for _ in range(self.DIM)]
