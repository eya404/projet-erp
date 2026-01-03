from odoo import models, fields, api

class TpAttestation(models.Model):
    _name = "tp.attestation"
    _description = "Gestion des Attestations"
    # L'héritage mail.thread permet d'avoir l'historique (Chatter) en bas de page
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Champs principaux
    name = fields.Char(string="Référence", required=True, readonly=True, 
                   copy=False, default=lambda self: 'Nouveau')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            # Génère une référence basée sur l'ID (simplifié)
            vals['name'] = self.env['ir.sequence'].next_by_code('tp.attestation') or 'ATT-000'
        return super(TpAttestation, self).create(vals)

    beneficiaire = fields.Char(string="Nom du Bénéficiaire", required=True, tracking=True)
    date_emission = fields.Date(string="Date d'émission", default=fields.Date.today)
    
    date_expiration = fields.Date(string="Valable jusqu'au", compute="_compute_expiration")

    @api.depends('date_emission')
    def _compute_expiration(self):
        for record in self:
         if record.date_emission:
            # Ajoute 365 jours à la date d'émission
            record.date_expiration = fields.Date.add(record.date_emission, years=1)
        
    # Type d'attestation avec tracking pour voir les changements
    type_attestation = fields.Selection([
        ('travail', 'Attestation de Travail'),
        ('stage', 'Attestation de Stage'),
        ('reussite', 'Attestation de Réussite')
    ], string="Type", default='travail', tracking=True)

    # Champ pour télécharger la signature ou le tampon
    signature_image = fields.Binary(string="Signature / Cachet")
    
    # Statut simplifié (Brouillon ou Validé)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('valide', 'Validé')
    ], string="Statut", default='draft', tracking=True)

    description_generee = fields.Text(string="Contenu de l'attestation")

    # Fonction pour changer l'état sans envoyer d'email
    def action_valider(self):
        for record in self:
            record.state = 'valide'

    # Optionnel : Remplissage automatique de la description lors du changement de bénéficiaire
    @api.onchange('beneficiaire', 'type_attestation')
    def _onchange_description(self):
        if self.beneficiaire:
            self.description_generee = f"Nous certifions par la présente que M./Mme {self.beneficiaire} a complété son dossier de type {self.type_attestation}."