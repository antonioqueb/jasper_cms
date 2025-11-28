from odoo import models, fields, api
from odoo.exceptions import UserError

class HomeManager(models.Model):
    _name = 'jasper.home'
    _description = 'Home Page Manager'
    _rec_name = 'name_ui'

    name_ui = fields.Char(string='Name', default='Home Page Configuration', readonly=True)

    # ==========================
    # SEO CONFIGURATION
    # ==========================
    meta_title = fields.Char(string='Meta Title', required=True)
    meta_description = fields.Text(string='Meta Description')
    meta_keywords = fields.Char(string='Meta Keywords')
    meta_image = fields.Binary(string='OG Image')
    meta_image_filename = fields.Char(string='OG Image Filename')

    # ==========================
    # SECTION 1: HERO
    # ==========================
    hero_layout = fields.Selection([
        ('image_left', 'Image Left'), ('image_right', 'Image Right'), 
        ('centered', 'Centered'), ('fullwidth', 'Full Width')
    ], string='Hero Layout', default='image_left')
    
    hero_bg_text = fields.Char(string='Background Text', help='Decorative text e.g. JASPER')
    hero_badge_text = fields.Char(string='Badge Text')
    hero_badge_icon = fields.Selection([
        ('star', 'Star'), ('sparkle', 'Sparkle'), ('gem', 'Gem'), 
        ('fire', 'Fire'), ('heart', 'Heart')
    ], string='Badge Icon', default='star')
    
    hero_subtitle = fields.Char(string='Hero Subtitle')
    hero_title_normal = fields.Char(string='Hero Title (Normal)')
    hero_title_highlight = fields.Char(string='Hero Title (Highlight)')
    hero_description = fields.Text(string='Hero Description')
    
    hero_cta_text = fields.Char(string='CTA Text')
    hero_cta_sub_text = fields.Char(string='CTA Sub Text')
    hero_cta_href = fields.Char(string='CTA Link')
    
    hero_image = fields.Binary(string='Hero Image')
    hero_image_filename = fields.Char(string='Hero Img Filename')
    hero_image_src = fields.Char(string='Hero Image URL (Manual)', help='Use this OR upload an image')
    hero_image_alt = fields.Char(string='Hero Image Alt')

    # ==========================
    # SECTION 2: FEATURE
    # ==========================
    feat_layout = fields.Selection([
        ('image_left', 'Image Left'), ('image_right', 'Image Right')
    ], string='Feature Layout', default='image_right')

    feat_subtitle = fields.Char(string='Feature Subtitle')
    feat_title_normal = fields.Char(string='Feature Title (Normal)')
    feat_title_highlight = fields.Char(string='Feature Title (Highlight)')
    feat_description = fields.Text(string='Feature Description')
    
    feat_cta_text = fields.Char(string='Feature CTA Text')
    feat_cta_href = fields.Char(string='Feature CTA Link')
    
    feat_image = fields.Binary(string='Feature Image')
    feat_image_filename = fields.Char(string='Feat Img Filename')
    feat_image_src = fields.Char(string='Feature Image URL (Manual)')
    feat_image_alt = fields.Char(string='Feature Image Alt')

    # ==========================
    # SECTION 3: BRAND STORY
    # ==========================
    brand_layout = fields.Selection([
        ('image_left', 'Image Left'), ('image_right', 'Image Right')
    ], string='Brand Layout', default='image_left')

    brand_subtitle = fields.Char(string='Brand Subtitle')
    brand_title_normal = fields.Char(string='Brand Title (Normal)')
    brand_title_highlight = fields.Char(string='Brand Title (Highlight)')
    brand_description = fields.Text(string='Brand Description')
    
    brand_cta_text = fields.Char(string='Brand CTA Text')
    brand_cta_href = fields.Char(string='Brand CTA Link')
    
    brand_image = fields.Binary(string='Brand Image')
    brand_image_filename = fields.Char(string='Brand Img Filename')
    brand_image_src = fields.Char(string='Brand Image URL (Manual)')
    brand_image_alt = fields.Char(string='Brand Image Alt')
    brand_show_badge = fields.Boolean(string='Show Rotating Badge', default=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Prevent creating more than one Home configuration"""
        if self.search_count([]) >= 1:
            raise UserError('You cannot create more than one Home Page configuration. Please edit the existing one.')
        return super().create(vals_list)

    def _get_image_url(self, prefix, field_name='image'):
        """Helper to resolve image URL (manual or binary)"""
        manual_url = getattr(self, f'{prefix}_{field_name}_src')
        binary_data = getattr(self, f'{prefix}_{field_name}')
        
        if manual_url:
            return manual_url
        if binary_data:
            return f"/web/image?model={self._name}&id={self.id}&field={prefix}_{field_name}"
        return ""

    def get_home_data(self):
        """Return complete structure for the Frontend"""
        self.ensure_one()
        
        # 1. Build SEO Data
        seo_data = {
            'title': self.meta_title,
            'description': self.meta_description or '',
            'keywords': self.meta_keywords or '',
            'image': f"/web/image?model={self._name}&id={self.id}&field=meta_image" if self.meta_image else ''
        }

        # 2. Build Sections List (Fixed Order)
        sections = []

        # --- HERO ---
        sections.append({
            'id': 'hero-section',
            'type': 'hero',
            'layout': self.hero_layout,
            'content': {
                'background_text': self.hero_bg_text or '',
                'badge': {
                    'text': self.hero_badge_text or '',
                    'icon': self.hero_badge_icon
                },
                'subtitle': self.hero_subtitle or '',
                'title': {
                    'normal': self.hero_title_normal or '',
                    'highlight': self.hero_title_highlight or ''
                },
                'description': self.hero_description or '',
                'cta': {
                    'text': self.hero_cta_text or '',
                    'sub_text': self.hero_cta_sub_text or '',
                    'href': self.hero_cta_href or '#'
                },
                'image': {
                    'src': self._get_image_url('hero'),
                    'alt': self.hero_image_alt or ''
                }
            }
        })

        # --- FEATURE ---
        sections.append({
            'id': 'feature-section',
            'type': 'feature',
            'layout': self.feat_layout,
            'content': {
                'subtitle': self.feat_subtitle or '',
                'title': {
                    'normal': self.feat_title_normal or '',
                    'highlight': self.feat_title_highlight or ''
                },
                'description': self.feat_description or '',
                'cta': {
                    'text': self.feat_cta_text or '',
                    'href': self.feat_cta_href or '#'
                },
                'image': {
                    'src': self._get_image_url('feat'),
                    'alt': self.feat_image_alt or ''
                }
            }
        })

        # --- BRAND STORY ---
        sections.append({
            'id': 'brand-section',
            'type': 'brand_story',
            'layout': self.brand_layout,
            'content': {
                'subtitle': self.brand_subtitle or '',
                'title': {
                    'normal': self.brand_title_normal or '',
                    'highlight': self.brand_title_highlight or ''
                },
                'description': self.brand_description or '',
                'cta': {
                    'text': self.brand_cta_text or '',
                    'href': self.brand_cta_href or '#'
                },
                'image': {
                    'src': self._get_image_url('brand'),
                    'alt': self.brand_image_alt or '',
                    'show_badge': self.brand_show_badge
                }
            }
        })

        return {
            'seo': seo_data,
            'sections': sections
        }