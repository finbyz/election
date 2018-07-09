# -*- coding: utf-8 -*-
# Copyright (c) 2017, Sagar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr
from frappe import msgprint, _ , db
from frappe.model.document import Document

class BoothReport(Document):
	def get_data(self):	
		self.set('voters', [])
		self.set('booth_comm', [])
		where_clause = self.p_booth and " and eng_ps_name = '%s'" % \
			self.p_booth.replace("'", "\'") or ""
		where_clause += self.d_p and " and gram_p = '%s'" % \
			self.d_p.replace("'", "\'") or ""
		where_clause += self.d_p and " and dis_panchayat = '%s'" % \
			self.d_p.replace("'", "\'") or ""
		rec1 = frappe.db.sql("""select f_name, m_name, surname, age, contactno, cast from
			`tabVoters` where docstatus < 2 %s""" % where_clause)
		rec2 = frappe.db.sql("""select buth_name, voting_year, party, vote, gram_p from
			`tabVoting History` where docstatus < 2 %s""" % where_clause)
			
		
		for d in rec1:
			self.append("voters", {
				"f_name": d[0],
				"m_name" : d[1],
				"surname": d[2],
				"age": d[3],
				"contactno": d[4],					
				"cast": d[5]
			})
		
		for d in rec2:
			self.append("voting_history", {
				"buth_name": d[0],
				"voting_year" : d[1],
				"party": d[2],
				"vote": d[3],
				"gram_p": d[4]
			})		