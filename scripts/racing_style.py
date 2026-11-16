"""Preserve the portfolio fan accent when regenerating cards."""
from pathlib import Path
import xml.etree.ElementTree as ET
def decorate(s):
    if 'id="tifoso-badge"' in s: return s
    p=Path(__file__).resolve().parent.parent/'assets/racing/ferrari-yellow.svg'
    logo=p.read_text(encoding='utf-8'); inner=logo[logo.index('>')+1:logo.rindex('</svg>')]
    root=ET.fromstring(s); w,h=map(float,root.get('viewBox').split()[2:]); size=34 if w<800 else 49
    x=w-size-(28 if w<800 else 38)
    return s.replace('</svg>',f'<g id="tifoso-badge"><title>Ferrari: личный фан-акцент</title><g transform="translate({x:g} 24) scale({size/344})">{inner}</g><rect x="{w-96:g}" y="{h-20:g}" width="32" height="3" fill="#ffd700"/></g></svg>')
