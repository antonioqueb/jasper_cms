from odoo import models, fields, api


class CmsMeta(models.Model):
    _name = 'jasper.cms.meta'
    _description = 'CMS Meta Tags'
    _order = 'sequence, id'

    name = fields.Char(string='Page Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)
    
    # Meta fields
    meta_title = fields.Char(string='Meta Title', required=True)
    meta_description = fields.Text(string='Meta Description')
    meta_keywords = fields.Char(string='Meta Keywords')
    meta_image = fields.Binary(string='OG Image')
    meta_image_filename = fields.Char(string='OG Image Filename')
    
    # Page reference
    page_url = fields.Char(string='Page URL', help='e.g., /home, /about, /collections')
    
    def get_meta_dict(self):
        """Return meta as dictionary for JSON API"""
        self.ensure_one()
        return {
            'title': self.meta_title,
            'description': self.meta_description or '',
            'keywords': self.meta_keywords or '',
        }
