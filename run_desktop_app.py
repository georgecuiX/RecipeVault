import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from werkzeug.serving import make_server
from app import app  # Import the Flask app

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

server_thread = ServerThread()

class MainWindow(QMainWindow):
    def closeEvent(self, event):
        server_thread.shutdown()
        super().closeEvent(event)

if __name__ == '__main__':
    server_thread.start()

    qt_app = QApplication(sys.argv)
    window = MainWindow()

    web = QWebEngineView(window)
    web.load(QUrl("http://127.0.0.1:5000"))
    window.setCentralWidget(web)
    window.show()

    sys.exit(qt_app.exec_())
