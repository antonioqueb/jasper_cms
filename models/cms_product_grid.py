from odoo import models, fields, api


class CmsProductGrid(models.Model):
    _name = 'jasper.cms.product.grid'
    _description = 'CMS Product Grid'
    _order = 'sequence, id'

    name = fields.Char(string='Grid Name', required=True)
    title = fields.Char(string='Display Title', required=True, help='e.g., Latest Treasures')
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)
    
    # Page assignment
    page_id = fields.Many2one('jasper.cms.meta', string='Page')
    
    # Grid items
    item_ids = fields.One2many('jasper.cms.product.grid.item', 'grid_id', string='Grid Items')
    
    # Configuration
    max_items = fields.Integer(string='Max Items to Display', default=8)
    show_new_badge = fields.Boolean(string='Show New Badge', default=True)
    
    def get_grid_dict(self):
        """Return grid as dictionary for JSON API"""
        self.ensure_one()
        items = self.item_ids.filtered(lambda i: i.active)[:self.max_items]
        return {
            'title': self.title,
            'items': [item.get_item_dict() for item in items],
        }


class CmsProductGridItem(models.Model):
    _name = 'jasper.cms.product.grid.item'
    _description = 'CMS Product Grid Item'
    _order = 'sequence, id'

    name = fields.Char(string='Item Name', compute='_compute_name', store=True)
    grid_id = fields.Many2one('jasper.cms.product.grid', string='Grid', ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)
    
    # Product link (optional - can be manual or linked)
    product_id = fields.Many2one('product.template', string='Linked Product')
    
    # Manual fields (used if no product linked)
    manual_name = fields.Char(string='Product Name')
    manual_slug = fields.Char(string='Slug')
    manual_price = fields.Float(string='Price', digits=(10, 2))
    manual_currency = fields.Selection([
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('MXN', 'MXN'),
        ('GBP', 'GBP'),
    ], string='Currency', default='USD')
    manual_image = fields.Binary(string='Image')
    manual_image_filename = fields.Char(string='Image Filename')
    manual_image_src = fields.Char(string='Image URL')
    manual_category = fields.Char(string='Category')
    
    # Flags
    is_new = fields.Boolean(string='Is New', default=False)
    is_featured = fields.Boolean(string='Is Featured', default=False)
    
    @api.depends('product_id', 'manual_name')
    def _compute_name(self):
        for record in self:
            if record.product_id:
                record.name = record.product_id.name
            else:
                record.name = record.manual_name or 'New Item'
    
    def get_item_dict(self):
        """Return item as dictionary for JSON API"""
        self.ensure_one()
        
        # 1. Determinar URL de imagen
        img_src = self.manual_image_src
        
        # Si no hay URL texto, pero hay imagen binaria subida en el ITEM MANUAL
        if not img_src and self.manual_image:
            img_src = f"/web/image?model={self._name}&id={self.id}&field=manual_image"
            
        # Si sigue sin haber imagen y es un producto vinculado, usar la del producto
        if not img_src and self.product_id:
            img_src = f"/web/image/product.template/{self.product_id.id}/image_1024"

        # 2. Construir respuesta
        if self.product_id:
            return {
                'id': self.product_id.id,
                'name': self.product_id.name,
                'slug': self.product_id.website_slug or self.manual_slug or '',
                'price': self.product_id.list_price,
                'currency': self.manual_currency,
                'image': img_src or '', # Usamos la variable calculada
                'category': self.product_id.categ_id.name if self.product_id.categ_id else '',
                'is_new': self.is_new,
                'is_featured': self.is_featured,
            }
        else:
            return {
                'id': self.id,
                'name': self.manual_name or '',
                'slug': self.manual_slug or '',
                'price': self.manual_price,
                'currency': self.manual_currency,
                'image': img_src or '', # Usamos la variable calculada
                'category': self.manual_category or '',
                'is_new': self.is_new,
                'is_featured': self.is_featured,
            }