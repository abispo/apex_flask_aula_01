import uuid
from flask import render_template

import requests


class User:
    def __init__(self, name, birth_date, gender, cep, id=None):
        self._id = id if id else str(uuid.uuid4())
        self._name = name
        self._birth_date = birth_date
        self._gender = gender
        self._cep = cep

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = value

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def cep(self):
        return self._ce

    @cep.setter
    def cep(self, value):
        self._cep = value

    def serialize(self, detail=False):
        if detail:
            self._cep = requests.get(
                f'https://viacep.com.br/ws/{self._cep}/json/'
            ).json()

        return {
            'id': self._id,
            'name': self._name,
            'birth_date': self._birth_date,
            'gender': self._gender,
            'cep': self._cep
        }
