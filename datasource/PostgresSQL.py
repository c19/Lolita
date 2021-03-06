#!/usr/bin/env python3
# coding=utf-8
#    postgresql queries
#    C19<caoyijun2050@gmail.com>

from datasource.sqlbase import SQLBase
import os
import sys
import xxhash
path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(path, '../'))
from base import do, xxhash, flatten, update, curry_map, chain

__all__ = ['Records']

class Records(SQLBase):
	def __init__(self, *arg, **kwarg):
		super(Records, self).__init__(*arg, **kwarg)
		self.ensurances = ["""CREATE TABLE records(
												id SERIAL PRIMARY KEY NOT NULL,
												buyorsell BOOLEAN NOT NULL,
												price INT NOT NULL,
												baseprice INT,
												mail_fee INT,
												name VARCHAR(1024),
												status VARCHAR(255),
												remark VARCHAR(1024),
												catagory VARCHAR(255),
												t_created TIMESTAMP without time zone,
												t_paid TIMESTAMP without time zone,
												t_delivering TIMESTAMP without time zone,
												t_received TIMESTAMP without time zone,
												t_close TIMESTAMP without time zone,
												paid INT

							);""",
							"""CREATE INDEX catagory_idx on records (stats, catagory);"""
							]
		self.ensure_tables()
	def get_records(self, **kwarg):
		return self.sql_real_dict('select * from records order by "id";')
	def insert_record(self, payload={}, **kwarg):
		self.sql("""insert into records (buyorsell, price, baseprice, mail_fee, name, status, remark, catagory, t_created, paid) 
			values (true, %(price)s, %(baseprice)s, %(mail_fee)s, %(name)s, %(status)s, %(remark)s, %(catagory)s, now(), %(paid)s);""", payload)

def get_batch(iterable, n = 1):
	l = len(iterable)
	for ndx in range(0, l, n):
		yield iterable[ndx:min(ndx+n, l)]
