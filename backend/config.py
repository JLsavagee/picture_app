import os

class Config:
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fonts')
    FIXED_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'Positionsfeld-Grün.png')
    CAMP_LOGO_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'WLS_Logo.png')
    SPONSOR_LOGO_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'DominosLogo.png')
    BACKSIDE_PNG_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'dominos_backside.png')
    BACKSIDE_PDF_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'assets', 'fixed_layers', 'backside_pdf')
