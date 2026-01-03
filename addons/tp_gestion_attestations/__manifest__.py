{
    "name": "Gestion des Attestations",
    "version": "1.0",
    "author": "EMSI - Aya Lestoun",
    "category": "Tools",
    "depends": ["base", "mail"], # Ajout de 'mail' pour le chatter si vous l'utilisez
    "data": [
        "security/ir.model.access.csv",
        "views/attestation_views.xml",
        "views/attestation_report.xml", 
    ],
    "installable": True,
    "application": True,
}