"""Façade de compatibilidade.

As implementações de página viviam todas neste arquivo (~950 linhas). Foram
divididas em módulos coesos sob ``Pages/impl/``. Este módulo apenas re-exporta
as classes para que ``from Pages.Implementation import ...`` continue válido.
"""
from Pages.impl.search_page import DefaultSearchPageImplementation
from Pages.impl.downloads_page import DownloadImplementation
from Pages.impl.historic_page import HistoricoImplementation
from Pages.impl.console_page import ConsolePageImplementation

__all__ = [
    "DefaultSearchPageImplementation",
    "DownloadImplementation",
    "HistoricoImplementation",
    "ConsolePageImplementation",
]
