import random

from fastapi import FastAPI
from pydantic import BaseModel


class Vector(BaseModel):
    x: float
    y: float


class Rectangle(BaseModel):
    half_size: float
    center: Vector

    def check_intersection(self, other: "Rectangle") -> bool:
        min_distance = self.half_size + other.half_size
        return (min_distance >= abs(self.center.x - other.center.x) and
                min_distance >= abs(self.center.y - other.center.y))

    def __str__(self):
        return f'({self.center.x:.2f}, {self.center.y:.2f})'


class Client(Rectangle):
    half_size: float = 0.1


class Obstacle(Rectangle):
    half_size: float = 0.5


class Field:
    def __init__(self, length: int, width: int, obstacle_number: int):
        self.length = length
        self.width = width
        self.obstacles = [Obstacle(center=self.__generate_coordinates()) for _ in range(obstacle_number)]

    def __generate_coordinates(self) -> Vector:
        return Vector(
            x=random.random() * self.length,
            y=random.random() * self.width
        )

    def check_intersection(self, client: Client):
        for obstacle in self.obstacles:
            if obstacle.check_intersection(client):
                print(f'Got intersection with obstacle {obstacle}')


FIELD_LENGTH = 100
FIELD_WIDTH = 100
OBSTACLE_NUMBER = 10000

field = Field(FIELD_LENGTH, FIELD_WIDTH, OBSTACLE_NUMBER)

app = FastAPI(title='Move tracker')


@app.post('/')
def get_coordinates(client: Client) -> None:
    field.check_intersection(client)
