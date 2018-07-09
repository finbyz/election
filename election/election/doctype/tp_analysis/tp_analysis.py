# -*- coding: utf-8 -*-
# Copyright (c) 2017, Sagar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr
from frappe import msgprint, _ , db
from frappe.model.document import Document

class TPAnalysis(Document):
	def do_analysis(self):
		self.set('voting_any', [])
		where_clause = self.dis_p and " and `tabBase`.taluka_p = '%s'" % \
			self.dis_p.replace("'", "\'") or ""

		rec1 = frappe.db.sql("""select cast,count(F_NAME) as total from `tabVoters` inner join `tabBase` on `tabBase`.eng_ps_name = `tabVoters`.eng_ps_name
				where `tabVoters`.docstatus < 2 %s""" % where_clause + """ group by Cast order by total DESC """)
		frappe.msgprint(where_clause)

		for d in rec1:
			iremark = int(d[1])/100
			self.append("voting_any", {
				"cast": d[0],
				"vote" : d[1],
				"remark" : iremark 


			})
