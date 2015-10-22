#!/usr/bin/env python

import json
import logging
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

import berlin
import ai

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("berlin API, send POST please")

    def post(self):
        body = self.request.body
        logging.debug("received POST: " + body)
        request = {
            'action': self.get_argument('action'),
            'infos': json.loads(self.get_argument('infos')),
            'map': json.loads(self.get_argument('map')),
            'state': json.loads(self.get_argument('state'))
            }
        logging.debug("decoded request: " + str(request))
        g = berlin.parse_request(request)
        if g is None:
            self.set_status(500, 'could not parse request')
            return
        if g.action in ['ping', 'turn']:
            response = g.generate_turn()
            logging.debug("response: " + str(response))
            self.write(str(response))
            self.flush()
            return
        self.set_status(200)
        return

def main():
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()