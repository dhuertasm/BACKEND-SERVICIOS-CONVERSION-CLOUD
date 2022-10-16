import json
from unittest import TestCase
from wsgiref import headers

from faker import Faker
from faker.generator import random

from app import app


class TestApuesta(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()
        password = self.data_factory.word()
        self.nuevo_usuario = {
            "username": self.data_factory.name(),
            "email": self.data_factory.name(),
            "password1": password,
            "password2": password,
        }

    def test_crear_usuario(self):
        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(self.nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})

        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())

        self.token = respuesta_al_crear_usuario["token"]
        self.usuario_code = respuesta_al_crear_usuario["id"]

        self.assertTrue(self.token)

    def test_falta_campo_crearusuario(self):
        nuevo_usuario = {

            "email": self.data_factory.random_int(100, 200),
            "password1": self.data_factory.word(),
            "password2": self.data_factory.random_int(100, 200)
        }

        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})
        dato_faltante = json.loads(solicitud_nuevo_usuario.get_data())['mensaje']

        self.assertEqual(dato_faltante, "falta 'username'")
