import logging

from tornado.httpserver import HTTPServer
import tornado.ioloop
import tornado.web

from utilities.file_utilities import FileUtilities
from definitions import XML_PATH
from OneOneOne.reciever.message_handler import MessageHandler

response = FileUtilities.get_file_string(XML_PATH / 'basic_success_response.xml')


class MessageReceiver(tornado.web.RequestHandler):

    def initialize(self, servicesdict):
        logging.basicConfig(level=logging.DEBUG)

    def post(self):
        logging.debug("Post message received ")
        mh = MessageHandler(self.request.body)
        status_code, message_response = mh.evaluate_message()

        self.set_status(status_code)
        logging.warning("Status code %i", status_code)

        logging.warning("Sending reply")
        self.write(message_response)

    def get(self):
        print("Test get method")

    def on_finish(self) -> None:
        self.flush()


if __name__ == "__main__":
    servicesDict = {'debug': True }
    application = tornado.web.Application([(r"/syncsoap", MessageReceiver, dict(servicesdict=servicesDict))],
                                          debug=True)

    httpsServer = HTTPServer(application)
    httpsServer.listen(4545)
    tornado.ioloop.IOLoop.current().start()
