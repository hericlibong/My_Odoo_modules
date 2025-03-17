from odoo import models, fields

class NewsArticle(models.Model):
    _name = 'news.article'
    _description = "Article de pouvant être traité par le workflow éditorial de Newsroom Manager"

    name = fields.Char(string="Titre", required=True, help="Titre de l'article")
    content = fields.Text(string="Contenu", required=True, help="Contenu de l'article")
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('review', 'En relecture'),
        ('published', 'Publié'),
        ('rejected', 'Rejeté'),
    ], string='Statut', default='draft', help="Etat de l'article")
    author_id = fields.Many2one('res.users', string="Auteur", help="Auteur de l'article")
    editor_id = fields.Many2one('res.users', string="Editeur", help="Relecteur de l'article")
    tags_ids = fields.Many2many('news.tag', string="Tags", help="Tags de l'article")
    category_id = fields.Many2one('news.category', string="Catégorie", help="Catégorie de l'article")
    published_date = fields.Date(string="Date de publication", help="Date de publication de l'article")
    
