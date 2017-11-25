#!/usr/bin/env python
# coding=utf-8
#    SQL helper class
#    C19<caoyijun2050@gmail.com>

from contextlib import contextmanager
from psycopg2.extras import DictCursor, RealDictCursor
from psycopg2.extensions import QuotedString
import psycopg2
import re


class SQLBase(object):
	def __init__(self, *arg, **kwarg):
		self.conn = psycopg2.connect(*arg, **kwarg)
		self.ensurances = []
	@contextmanager
	def get_cursor(self, *arg, **kwarg):
		cursor = self.conn.cursor(*arg, **kwarg)
		try:
			yield cursor
		finally:
			cursor.close()
			del cursor
	def ensure_tables(self):
		with self.get_cursor() as cursor:
			for sql in self.ensurances:
				try:
					cursor.execute(sql)
					self.conn.commit()
				except (Exception, e):
					print(e)
					self.conn.commit()
	def _sql(self, execute, cursor, *arg, **kwarg):
		try:
			execute(cursor)(*arg, **kwarg)
			self.conn.commit()
			return cursor.fetchall() if arg[0].lower().startswith('select') else []
		except (Exception, e):
			print(e)
			self.conn.rollback()
			raise e
	def sql_dict(self, *arg, **kwarg):
		with self.get_cursor(cursor_factory=DictCursor) as cursor:
			return self._sql(lambda c:c.execute, cursor, *arg, **kwarg)
	def sql_real_dict(self, *arg, **kwarg):
		with self.get_cursor(cursor_factory=RealDictCursor) as cursor:
			return self._sql(lambda c:c.execute, cursor, *arg, **kwarg)
	def sql(self, *arg, **kwarg):
		with self.get_cursor() as cursor:
			return self._sql(lambda c: c.execute, cursor, *arg, **kwarg)
	def sql_many(self, *arg, **kwarg):
		with self.get_cursor() as cursor:
			return self._sql(lambda c: c.executemany, cursor, *arg, **kwarg)
	def sql_quote(self, one):
		if isinstance(one, (int, long, float)):
			return str(one)
		if not isinstance(one, str) and not isinstance(one, unicode):
			one = str(one)
		return QuotedString(one).getquoted()
	def sql_guard(self, arg):
		if isinstance(arg, (int, long, float)):
			return arg
		if not isinstance(arg, str) and not isinstance(arg, unicode):
			raise ValueError("sql params only accept string and numbers")
		if not re.match('^[\w_-]+$', arg):
			raise ValueError("sql params only accept [\w_-]")
		return arg
