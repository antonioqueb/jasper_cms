from odoo import models, fields, api


class CmsSection(models.Model):
    _name = 'jasper.cms.section'
    _description = 'CMS Content Section'
    _order = 'sequence, id'

    name = fields.Char(string='Section Name', required=True)
    section_id = fields.Char(string='Section ID', required=True, help='Unique identifier, e.g., hero-section-01')
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)
    
    # Section Type
    section_type = fields.Selection([
        ('hero', 'Hero Section'),
        ('feature', 'Feature Section'),
        ('brand_story', 'Brand Story'),
        ('testimonial', 'Testimonial'),
        ('cta', 'Call to Action'),
    ], string='Section Type', required=True, default='hero')
    
    # Layout
    layout = fields.Selection([
        ('image_left', 'Image Left'),
        ('image_right', 'Image Right'),
        ('centered', 'Centered'),
        ('fullwidth', 'Full Width'),
    ], string='Layout', default='image_left')
    
    # Content Relations
    content_id = fields.Many2one('jasper.cms.section.content', string='Content', ondelete='cascade')
    
    # Page assignment
    page_id = fields.Many2one('jasper.cms.meta', string='Page')
    
    def get_section_dict(self):
        """Return section as dictionary for JSON API"""
        self.ensure_one()
        result = {
            'id': self.section_id,
            'type': self.section_type,
            'layout': self.layout,
            'content': self.content_id.get_content_dict() if self.content_id else {},
        }
        return result


class CmsSectionContent(models.Model):
    _name = 'jasper.cms.section.content'
    _description = 'CMS Section Content'

    name = fields.Char(string='Content Name', required=True)
    section_ids = fields.One2many('jasper.cms.section', 'content_id', string='Sections')
    
    # Background/Decorative
    background_text = fields.Char(string='Background Text', help='Large decorative text, e.g., JASPER')
    
    # Badge
    badge_text = fields.Char(string='Badge Text')
    badge_icon = fields.Selection([
        ('star', 'Star'),
        ('sparkle', 'Sparkle'),
        ('gem', 'Gem'),
        ('fire', 'Fire'),
        ('heart', 'Heart'),
    ], string='Badge Icon')
    
    # Subtitle
    subtitle = fields.Char(string='Subtitle')
    
    # Title (split for styling)
    title_normal = fields.Char(string='Title (Normal)')
    title_highlight = fields.Char(string='Title (Highlight/Italic)')
    
    # Description
    description = fields.Text(string='Description')
    
    # CTA (Call to Action)
    cta_text = fields.Char(string='CTA Text')
    cta_sub_text = fields.Char(string='CTA Sub Text')
    cta_href = fields.Char(string='CTA Link')
    
    # Image
    image = fields.Binary(string='Image')
    image_filename = fields.Char(string='Image Filename')
    image_src = fields.Char(string='Image URL', help='External URL or path like /producto5.png')
    image_alt = fields.Char(string='Image Alt Text')
    show_badge = fields.Boolean(string='Show Rotating Badge', default=False)
    
    def get_content_dict(self):
        """Return content as dictionary for JSON API"""
        self.ensure_one()
        result = {}
        
        if self.background_text:
            result['background_text'] = self.background_text
            
        if self.badge_text:
            result['badge'] = {
                'text': self.badge_text,
                'icon': self.badge_icon or 'star',
            }
            
        if self.subtitle:
            result['subtitle'] = self.subtitle
            
        if self.title_normal or self.title_highlight:
            result['title'] = {
                'normal': self.title_normal or '',
                'highlight': self.title_highlight or '',
            }
            
        if self.description:
            result['description'] = self.description
            
        if self.cta_text:
            result['cta'] = {
                'text': self.cta_text,
                'href': self.cta_href or '#',
            }
            if self.cta_sub_text:
                result['cta']['sub_text'] = self.cta_sub_text
        
        # --- CORRECCIÓN AQUÍ ---
        # Determinamos la fuente de la imagen
        img_src = self.image_src
        
        # Si no hay URL manual, pero SI hay imagen binaria subida, generamos la ruta de Odoo
        if not img_src and self.image:
            # Esta es la ruta estándar para obtener imágenes binarias en Odoo
            img_src = f"/web/image?model={self._name}&id={self.id}&field=image"
            
        if img_src:
            result['image'] = {
                'src': img_src,
                'alt': self.image_alt or '',
                'show_badge': self.show_badge,
            }
        # -----------------------
            
        return result