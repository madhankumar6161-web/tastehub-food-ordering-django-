# menu/patches.py
"""
Workaround for Django 5.0.x + Python 3.14 incompatibility.
Python 3.14 made `super` objects copyable, which breaks Django's
BaseContext.__copy__() trick (copy(super())).
This patch replaces it with a safe manual shallow copy.
"""
from django.template.context import BaseContext


def _safe_copy(self):
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.__dict__.update(self.__dict__)
    duplicate.dicts = self.dicts[:]
    return duplicate


def apply_context_copy_patch():
    BaseContext.__copy__ = _safe_copy