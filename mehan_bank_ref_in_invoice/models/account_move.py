from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def _get_reconciled_info_JSON_values(self):
        """
        Extend the method to include the bank statement reference from the payment.
        For each payment found in the invoice's reconciled info, we iterate over its move lines.
        If a move line is linked to a bank statement line (via statement_line_id), we retrieve its ref.
        """
        res = super(AccountMove, self)._get_reconciled_info_JSON_values()
        for payment_vals in res:
            payment_id = payment_vals.get('id')
            bank_ref = ''
            if payment_id:
                payment = self.env['account.payment'].browse(payment_id)
                # Iterate over the payment's move lines
                for move_line in payment.move_line_ids:
                    # If this move line is linked to a bank statement line, use its ref
                    if move_line.statement_line_id:
                        bank_ref = move_line.statement_line_id.ref or ''
                        # Exit after finding the first reference
                        break
            payment_vals['bank_ref'] = bank_ref
        return res
