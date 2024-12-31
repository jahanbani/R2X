from .plexos import PlexosParser
from .sienna import SiennaParser
from .reeds import ReEDSParser

parser_list = {
    "plexos": PlexosParser,
    "reeds-US": ReEDSParser,
    "sienna": SiennaParser
}
