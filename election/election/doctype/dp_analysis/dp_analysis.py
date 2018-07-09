# -*- coding: utf-8 -*-
# Copyright (c) 2017, Sagar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr
from frappe import msgprint, _ , db
from frappe.model.document import Document

class DPAnalysis(Document):
	def do_analysis(self):


		where_clause = self.dis_p and " and `tabBase`.district_p = '%s'" % \
			self.dis_p.replace("'", "\'") or ""
		where_clause_old = self.dis_p and " and districtname = '%s'" % \
			self.dis_p.replace("'", "\'") or ""

		rec1 = frappe.db.sql("""select `tabBase`.eng_ps_name as eng_ps_name, buth_name, voting_year, party, sum(vote) as vote from
					`tabVoting History` inner join `tabBase` on `tabBase`.`old_booth`= `tabVoting History`.`buth_name` where
					`tabVoting History`.docstatus < 2 %s""" % where_clause + """ group by party,voting_year,`tabBase`.district_p""")
		rec2 = frappe.db.sql("""select cast,count(F_NAME) as total from `tabVoters` inner join `tabBase` on `tabBase`.eng_ps_name = `tabVoters`.eng_ps_name
				where `tabVoters`.docstatus < 2 %s""" % where_clause + """ group by Cast order by total DESC """)
		rec3 = frappe.db.sql("""select dpm,dpm_mobileno from
				`tabDistrict Panchayat`
				where docstatus < 2 %s""" % where_clause_old)


		self.voting_any = "Somthing! \n sagar"



		
