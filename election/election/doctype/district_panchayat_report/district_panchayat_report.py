# -*- coding: utf-8 -*-
# Copyright (c) 2017, Sagar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr
from frappe import msgprint, _ , db
from frappe.model.document import Document

class DistrictPanchayatReport(Document):
	def get_data(self):
		self.set('vote_history', [])
		self.set('voters', [])

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


		totalvote=0
		for d in rec2:
			totalvote +=d[1]
			self.append("voters", {
				"cast_a": d[0],
				"vote_a" : d[1]
			
			})
			self.total_vote = totalvote
			
		for d in rec3:
			self.dpm = d[0]
			self.dpm_contact = d[1]
				
			
			
		for d in rec1:		
			self.append("vote_history", {
				"buth_name": d[1],
				"voting_year" : d[2],
				"party": d[3],
				"vote": d[4]
			})
		frappe.db.commit()
		
			
