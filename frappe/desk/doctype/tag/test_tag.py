<<<<<<< HEAD
# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies and Contributors
# See license.txt
from __future__ import unicode_literals

# import frappe
=======
>>>>>>> ae70502f91 (test: Add test case to validate tag count query)
import unittest
import frappe

from frappe.desk.reportview import get_stats
from frappe.desk.doctype.tag.tag import add_tag

class TestTag(unittest.TestCase):
	def setUp(self) -> None:
		frappe.db.sql("DELETE from `tabTag`")
		frappe.db.sql("UPDATE `tabDocType` set _user_tags=''")

	def test_tag_count_query(self):
		self.assertDictEqual(get_stats('["_user_tags"]', 'DocType'),
			{'_user_tags': [['No Tags', frappe.db.count('DocType')]]})
		add_tag('Standard', 'DocType', 'User')
		add_tag('Standard', 'DocType', 'ToDo')

		# count with no filter
		self.assertDictEqual(get_stats('["_user_tags"]', 'DocType'),
			{'_user_tags': [['Standard', 2], ['No Tags', frappe.db.count('DocType') - 2]]})

		# count with child table field filter
		self.assertDictEqual(get_stats('["_user_tags"]',
			'DocType',
			filters='[["DocField", "fieldname", "like", "%last_name%"], ["DocType", "name", "like", "%use%"]]'),
			{'_user_tags': [['Standard', 1], ['No Tags', 0]]})