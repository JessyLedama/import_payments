# -*- coding: utf-8 -*-
import csv
import os
from odoo import models, fields, api
from odoo.exceptions import UserError

class PaymentImport(models.TransientModel):
    _name = 'payment.import'
    _description = 'Payment Import'

    directory_path = fields.Char(string='Directory Path')
    frequency = fields.Selection([('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], string='Import Frequency', default='daily')

    def import_payments(self):
        
        # Journal for entering the data
        directory = self.env['payment.import'].search([], limit=1)

        
        if not directory.directory_path:
            raise UserError("Please provide a directory path.")

        if not os.path.exists(directory.directory_path):
            raise UserError("The specified directory does not exist.")

        # List all CSV files in the specified directory
        csv_files = [file for file in os.listdir(directory.directory_path) if file.endswith('.csv')]

        if not csv_files:
            raise UserError("No CSV files found in the specified directory.")

        payment_obj = self.env['account.payment']

        for file_name in csv_files:
            file_path = os.path.join(directory.directory_path, file_name)

            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    # Columns: 'partner_id', 'amount', 'date', 'journal_id', ''
                    partner_id = '"' + row.get('partner_id') + '"'
                    amount = float(row.get('amount'))
                    date = row.get('date')  
                    journal_id = row.get('journal_id')
                    currency_id = row.get('currency_id')

                    # get the user making payment.
                    partner = self.env['res.users'].search([('name', '=', partner_id)], limit=1)

                    # Journal for entering the data
                    journal = self.env['account.journal'].search([('name', '=', journal_id)], limit=1)

                    # Currency used in transaction (Mostly KES).
                    currency = self.env['res.currency'].search([('name', '=', currency_id)], limit=1)

                    # Payment Method.
                    payment_method = self.env['account.payment.method'].search([('name', '=', 'Manual')], limit=1)


                    # Create payment records
                    payment_vals = {
                        'partner_id': partner.id,
                        'amount': amount,
                        'date': date,
                        'journal_id': journal.id,
                        'payment_type': 'inbound',
                        'currency_id': currency.id,
                        'payment_method_line_id': payment_method.id,
                    }
                    
                    print("Partner ==>", partner_id)
                    print("Partner ==>", partner.id)

                    payment_obj.create(payment_vals)

            # Remove the processed CSV file
            os.remove(file_path)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
