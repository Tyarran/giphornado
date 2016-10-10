import json
import os

import tornado.ioloop
import tornado.web

from tornado.httpclient import AsyncHTTPClient
from tornado import gen


RANDOM_URL = 'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={}'


class MainHandler(tornado.web.RequestHandler):

    def _get_response(self, response):
        response_payload = json.loads(response.body.decode('utf-8'))
        image_url = response_payload['data']['image_url']
        result = {
            "response_type": "in_channel",
            'text': image_url,
        }
        return json.dumps(result)

    @gen.coroutine
    def post(self):
        tag = self.get_arguments('text')[0]
        http_client = AsyncHTTPClient()
        giphy_response = yield http_client.fetch(RANDOM_URL.format(tag))
        response = self._get_response(giphy_response)
        self.set_header("Content-Type", "application/json")
        self.write(response)


def make_app():
    return tornado.web.Application([
        (r"/random/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(os.environ.get('GIPHORNADO_PORT', 8888))
    tornado.ioloop.IOLoop.current().start()
