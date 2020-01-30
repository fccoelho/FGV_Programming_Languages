"""
Este módulo oferece um escaneador de perfis de usuários do URI online
https://www.urionlinejudge.com.br/
"""

from requests_html import HTMLSession
import bs4
import sqlite3
from sqlalchemy import create_engine

import unittest


class ScanUri:
    """
    extrai informações de performance de uma conta URI
    """
    base_url = 'https://www.urionlinejudge.com.br/judge/en/profile/'

    def __init__(self, id):
        if isinstance(id, int):
            id = [id]
        self.ids = id

    @property
    def profiles(self):
        session = HTMLSession()
        for id in self.ids:
            r = session.get(self.base_url + str(id))
            profile = r.html
            yield profile

    @property
    def problems_solved(self):
        for profile in self.profiles:
            tables = profile.find('table')
            yield list(tables)

    def parse_tables(self):
        for table in self.problems_solved:
            table = table[0]
            header = [el.text for el in table.find('th')]
            pass


## Testes

class TestUri(unittest.TestCase):
    def test_fetching(self):
        S = ScanUri(191549)
        self.assertGreater(len(list(S.profiles)), 0)

    def test_extract_problems(self):
        S = ScanUri(191549)
        for t in S.problems_solved:
            self.assertEqual(len(t), 1)

    def test_parse_tables(self):
        S = ScanUri(191549)
        S.parse_tables()


if __name__ == "__main__":
    unittest.main()
