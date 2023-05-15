from __future__ import annotations
from abc import ABC, abstractmethod
from time import sleep
from typing import List, Dict


class IUser(ABC):
    """ Subject Interface """

    nome: str
    sobrenome: str

    #está sendo adiado
    @abstractmethod
    def get_endereco(self) -> List[Dict]: pass

    #está sendo adiado
    @abstractmethod
    def get_dados_do_usuario(self) -> Dict: pass


class RealUser(IUser):
    """ Real Subject  ou Interface Concreta"""

    def __init__(self, nome: str, sobrenome: str) -> None:
        sleep(2)  # Simulando requisição
        self.nome = nome
        self.sobrenome = sobrenome

    def get_endereco(self) -> List[Dict]:
        sleep(2)  # Simulando requisição
        return [
            {'rua': 'JW', 'numero': 666}
        ]

    def get_dados_do_usuario(self) -> Dict:
        sleep(2)  # Simulando requisição
        return {
            'cpf': '111.111.111-11',
            'rg': 'AB111222444'
        }


class UserProxy(IUser):
    """ Proxy """

    def __init__(self, nome: str, sobrenome: str) -> None:
        self.nome = nome
        self.sobrenome = sobrenome

        # Esses objetos ainda não existem nesse
        # ponto do código
        self._real_user: RealUser # lazy instantiation, não existe até eu colocar valor nele
        self._cached_endereco: List[Dict]
        self._dados_do_usuario: Dict

    def get_real_user(self) -> None:
        if not hasattr(self, '_real_user'):
            self._real_user = RealUser(self.nome, self.sobrenome)

    def get_endereco(self) -> List[Dict]:
        self.get_real_user()

        if not hasattr(self, '_cached_endereco'):
            self._cached_endereco = self._real_user.get_endereco()

        return self._cached_endereco

    def get_dados_do_usuario(self) -> Dict:
        self.get_real_user()

        if not hasattr(self, '_dados_do_usuario'):
            self._dados_do_usuario = self._real_user.get_dados_do_usuario()

        return self._dados_do_usuario


if __name__ == "__main__":
    usuario = UserProxy('Luciano', 'Ramos')

    # Responde instantaneamente
    print(usuario.nome)
    print(usuario.sobrenome)

    # Responde em 6 segundos porque vem do objeto real
    print(usuario.get_dados_do_usuario())
    print(usuario.get_endereco())

    # Responde instantaneamente (porque está em cache)
    print('CACHED DATA:')
    for i in range(50):
        print(usuario.get_endereco())