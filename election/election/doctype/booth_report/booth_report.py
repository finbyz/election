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
		self.set('voting_history', [])
		self.set('booth_cat', [])


		where_clause = self.p_booth and " and `tabBase`.eng_ps_name = '%s'" % \
			self.p_booth.replace("'", "\'") or ""
		where_clause_old = self.p_booth and " and eng_ps_name = '%s'" % \
			self.p_booth.replace("'", "\'") or ""

		where_clause += self.g_p and " and `tabBase`.gram_p = '%s'" % \
			self.g_p.replace("'", "\'") or ""
		where_clause_old += self.g_p and " and gram_p = '%s'" % \
			self.g_p.replace("'", "\'") or ""

		where_clause += self.t_p and " and `tabBase`.taluka_p = '%s'" % \
			self.t_p.replace("'", "\'") or ""
		where_clause_old += self.t_p and " and taluka_p = '%s'" % \
			self.t_p.replace("'", "\'") or ""


		where_clause += self.d_p and " and dis_panchayat = '%s'" % \
			self.d_p.replace("'", "\'") or ""
		frappe.msgprint(where_clause_old)



		rec1 = frappe.db.sql("""select cast,count(F_NAME) as total from `tabVoters` inner join `tabBase` on `tabBase`.eng_ps_name = `tabVoters`.eng_ps_name
				where `tabVoters`.docstatus < 2 %s""" % where_clause + """ group by Cast order by total DESC """)
		if self.t_p != "":
			rec2 = frappe.db.sql("""select `tabBase`.eng_ps_name as eng_ps_name, buth_name, voting_year, party, sum(vote) as vote from
					`tabVoting History` inner join `tabBase` on `tabBase`.`old_booth`= `tabVoting History`.`buth_name` where `tabVoting History`.docstatus < 2 %s""" % where_clause + """ group by party,voting_year,`tabBase`.taluka_p""")
		else:
			rec2 = frappe.db.sql("""select `tabBase`.eng_ps_name as eng_ps_name, buth_name, voting_year, party, sum(vote) as vote from
					`tabVoting History` inner join `tabBase` on `tabBase`.`old_booth`= `tabVoting History`.`buth_name` where `tabVoting History`.docstatus < 2 %s""" % where_clause + """ group by `tabBase`.Gram_p,party,voting_year,`tabBase`.taluka_p""")
		rec3 = frappe.db.sql("""select `tabBase`.eng_ps_name as eng_ps_name, buthc_wardname, buthc_membername, buthc_mobileno, buth_cm_type from
				`tabBooth Committe` inner join `tabBase` on `tabBase`.`old_booth`= `tabBooth Committe`.`buthc_wardname` where `tabBooth Committe`.docstatus < 2 %s""" % where_clause + """ order by priority ASC""" )
		rec4 = frappe.db.sql("""select `tabBase`.eng_ps_name as eng_ps_name, ps_no, `tabBase`.district_p, `tabBase`.taluka_p, `tabBase`.gram_p, `tabBase`.new_booth, `tabGram Panchayat`.sarpanch ,  `tabGram Panchayat`.cat, `tabGram Panchayat`.remark, `tabGram Panchayat`.sar_cont,`tabTaluka Panchayat`.tpm,`tabTaluka Panchayat`.tpm_mobileno,`tabDistrict Panchayat`.dpm,`tabDistrict Panchayat`.dpm_mobileno from
				`tabPolling Booth` inner join `tabBase` on `tabBase`.`new_booth`= `tabPolling Booth`.`ps_name` inner join `tabGram Panchayat` on `tabGram Panchayat`.`village_name`= `tabBase`.`gram_p` inner join `tabTaluka Panchayat` on `tabTaluka Panchayat`.`talukaname`= `tabBase`.`taluka_p` inner join `tabDistrict Panchayat` on `tabDistrict Panchayat`.`districtname`= `tabBase`.`district_p` where `tabPolling Booth`.docstatus < 2 %s""" % where_clause)
		totalvote=0
		for d in rec1:
			totalvote +=d[1]
			self.append("voters", {
				"cast_a": d[0],
				"vote_a" : d[1]

			})
		self.total_vote = totalvote

		for d in rec4:
			self.d_p = d[2]
			self.t_p = d[3]
			self.g_p = d[4]
			#frappe.msgprint("Clicked")
			self.booth_cat = d[7]
			self.remark = d[8]
			self.buth_no = d[1]
			self.sarapanch_name = d[6]
			self.sarapanch_contact = d[9]
			self.tpm = d[10]
			self.tpm_contact = d[11]
			self.dpm = d[12]
			self.dpm_contact = d[13]





		for d in rec2:
			self.append("voting_history", {
				"buth_name": d[1],
				"voting_year" : d[2],
				"party": d[3],
				"vote": d[4]
			})


		for d in rec3:
			self.append("booth_comm", {
				"buthc_membername": d[2],
				"buthc_mobileno" : d[3],
				"buth_cm_type": d[4]
			})
		frappe.db.commit()
