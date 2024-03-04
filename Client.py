import time
import requests


class Copter:
    def __init__(self, server_url: str):
        self.start_point = (0, 0)
        self.start_time = time.time()
        self.server_url = server_url

    def get_coordinates(self):
        return self.__move_func(time.time())

    def __move_func(self, current_time):
        """Diagonal linear moving"""
        return (
            self.start_point[0] + (current_time - self.start_time),
            self.start_point[1] + (current_time - self.start_time)
        )

    def send_coordinates_to_server(self):
        coordinates = self.get_coordinates()
        print(coordinates)
        payload = {
            'center': {
                'x': coordinates[0],
                'y': coordinates[1]
            }
        }

        r = requests.post(self.server_url, json=payload)


SERVER_URL = 'http://127.0.0.1:8000/'

copter = Copter(SERVER_URL)
while True:
    copter.send_coordinates_to_server()
    time.sleep(1)
