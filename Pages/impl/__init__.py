"""Implementacoes de paginas, divididas do antigo Implementation.py."""
from Pages.impl.search_page import DefaultSearchPageImplementation
from Pages.impl.downloads_page import DownloadImplementation
from Pages.impl.historic_page import HistoricoImplementation
from Pages.impl.console_page import ConsolePageImplementation

__all__ = ["DefaultSearchPageImplementation", "DownloadImplementation",
           "HistoricoImplementation", "ConsolePageImplementation"]
