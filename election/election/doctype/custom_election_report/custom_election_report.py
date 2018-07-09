# -*- coding: utf-8 -*-
# Copyright (c) 2017, Sagar and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr
from frappe import msgprint, _ , db
from frappe.model.document import Document

class CustomElectionReport(Document):
	def get_cast(self):
		chk_dp=self.check_d_p
		chk_tp=self.check_t_p
		chk_gp=self.check_g_p
		chk_pb=self.check_p_b
		if chk_dp == 1:
			frappe.msgprint("Checked")
		else:
			frappe.msgprint("Unchecked")

		where_clause=""

		data = "<table border='1px'>"
		data += "<tr><th>ક્રમ</th><th>તાલુકા પંચાયત</th><th>જ્ઞાતિ</th><th>વોટ</th>"

		rec1 = frappe.db.sql("""select `tabBase`.taluka_p,cast,count(F_NAME) as total
							from `tabVoters`
							inner join `tabBase` on `tabBase`.eng_ps_name=`tabVoters`.eng_ps_name

							where (select count(F_NAME) as total from `tabVoters`) > 50 group by Cast,`tabBase`.taluka_p
							order by total DESC  """)

		i=1
		for d in rec1:
			data += "<tr>"
			data += "<td>" + str(i) + "</td>"
			data +="<td>  '%s' </td>"  %(d[0])
			data +="<td>  '%s' </td>"  %(d[1])
			data +="<td>  '%s' </td>"  %(d[2])
			data += "</tr>"
			i = i + 1

		data += "<tr></table>"

		self.select_field=data


	def get_voting_history(self):
		data=""

		Party1 = self.party and "'%s'" % \
			self.party.replace("'", "\'") or ""
		Party2 = self.party1 and "'%s'" % \
			self.party1.replace("'", "\'") or ""

		VotingYear1 = self.voting_year and "'%s'" % \
			self.voting_year.replace("'", "\'") or ""
		VotingYear2 = self.voting_year1 and "'%s'" % \
			self.voting_year1.replace("'", "\'") or ""

		Condition = self.cond and "%s" % \
			self.cond.replace("'", "\'") or ""




		rec = frappe.db.sql(""" select boothname from `tabBooth` """)
		Qry=""

		data = "<table class='table' border='1px'>"
		data += "<tr><th>ક્રમ</th><th>બુથ નું નામ</th><th>વોટ 1</th><th>વોટ 2</th><th>જ્ઞાતિ</th><th>જ્ઞાતિ ના વોટ</th>"
		i=1
		for d in rec:
			#frappe.msgprint(Condition)

			Qry="""select buth_name,(select vote  from `tabVoting History` where party = %s and buth_name = '%s' and voting_year = %s) as vote1,
				(select vote  from `tabVoting History` where party = %s and buth_name='%s'  and voting_year = %s) as vote2
				from `tabVoting History`
				  where buth_name='%s' group by buth_name  """ %(Party1,d[0],VotingYear1,Party2,d[0],VotingYear2,d[0])



			rec1 = frappe.db.sql(Qry)
			rec2 = frappe.db.sql("""select cast,count(F_NAME) as total from `tabVoters` inner join `tabBase` on `tabBase`.eng_ps_name = `tabVoters`.eng_ps_name
					where `tabBase`.old_booth = '%s' group by Cast order by total DESC LIMIT 1 """ %(d[0]))
			for d in rec1:
					data += "<tr>"
					if d[1] is None:
						"""OK"""
					elif d[2] is None:
						"""SKip"""
					else:
						if Condition == "greater than":
							if (int(d[1])>int(d[2])):
								data += "<td>" + str(i) + "</td>"
								data +="<td>  %s </td>"  %(d[0])
								data +="<td>  %s </td>"  %(d[1])
								data +="<td>  %s </td>"  %(d[2])
								for e in rec2:
									data +="<td>  %s </td>"  %(e[0])
									data +="<td>  %s </td>"  %(e[1])
							i = i + 1
						elif Condition == "less than":
							if (int(d[1])<int(d[2])):
								data += "<td>" + str(i) + "</td>"
								data +="<td>  %s </td>"  %(d[0])
								data +="<td>  %s </td>"  %(d[1])
								data +="<td>  %s </td>"  %(d[2])
								for e in rec2:
									data +="<td>  %s </td>"  %(e[0])
									data +="<td>  %s </td>"  %(e[1])
							i = i + 1
						elif Condition == "equal to":
							if (int(d[1])==int(d[2])):
								data += "<td>" + str(i) + "</td>"
								data +="<td>  %s </td>"  %(d[0])
								data +="<td>  %s </td>"  %(d[1])
								data +="<td>  %s </td>"  %(d[2])
								for e in rec2:
									data +="<td>  %s </td>"  %(e[0])
									data +="<td>  %s </td>"  %(e[1])
							i = i + 1


		data += "<tr></table>"
		self.select_field=data
