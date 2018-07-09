# -*- coding: utf-8 -*-
# Copyright (c) 2017, Sagar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr
from frappe import msgprint, _ , db
from frappe.model.document import Document

class Testing(Document):
	def get_data(self):
		
		rec1 = frappe.db.sql("""select buth_name, voting_year, party, vote, gram_p from
			`tabVoting History` where docstatus < 2 """)
			
		for d in rec1:
			
			where_clause = d[0] and " and buth_name = '%s'" % \
			self.d[0].replace("'", "\'") or ""
			show_alert(where_clause);
			aa = frappe.db.sql("""select buth_name, voting_year, party, vote, gram_p from
			`tabVoting History` where docstatus < 2 %s""" % where_clause)
			
		
		
		
		
		
	
	