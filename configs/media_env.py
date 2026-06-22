"""Configuração de mídia/DRM do QtWebEngine.

Precisa rodar ANTES de o QApplication/QtWebEngine inicializar, porque ajusta
variáveis de ambiente (QTWEBENGINE_CHROMIUM_FLAGS) lidas na inicialização do
motor.

Contexto (descoberto por diagnóstico em 2026-06):
- O QtWebEngine dos wheels do PySide6 NÃO traz codecs proprietários (H.264/AAC).
  Isso quebra a maioria dos vídeos MP4 e lives via HLS/DASH. Só se resolve com
  um QtWebEngineCore compilado com -webengine-proprietary-codecs.
- O Widevine CDM (DRM: Netflix, Spotify, etc.) não vem com o Qt, mas o Qt sabe
  usar o CDM já instalado pelo Chrome/Edge se apontarmos o caminho. É isso que
  `configure_media_env()` faz automaticamente.
"""
import glob
import os

# Locais comuns do widevinecdm.dll no Windows (Chrome e Edge mantêm o CDM
# atualizado, então normalmente é compatível com o Chromium do Qt).
_WIDEVINE_GLOBS = (
    r"%LOCALAPPDATA%\Google\Chrome\User Data\WidevineCdm\*\_platform_specific\win_x64\widevinecdm.dll",
    r"%PROGRAMFILES%\Google\Chrome\Application\*\WidevineCdm\_platform_specific\win_x64\widevinecdm.dll",
    r"%PROGRAMFILES(X86)%\Google\Chrome\Application\*\WidevineCdm\_platform_specific\win_x64\widevinecdm.dll",
    r"%LOCALAPPDATA%\Microsoft\Edge\User Data\WidevineCdm\*\_platform_specific\win_x64\widevinecdm.dll",
)


def find_widevine_cdm() -> str | None:
    """Retorna o caminho do widevinecdm.dll mais recente encontrado, ou None."""
    candidates: list[str] = []
    for pattern in _WIDEVINE_GLOBS:
        candidates += glob.glob(os.path.expandvars(pattern))
    if not candidates:
        return None
    # ordena por nome (a versão vem no caminho) e devolve o mais recente
    return sorted(candidates)[-1]


def configure_media_env(verbose: bool = True) -> str | None:
    """Aponta o Widevine CDM do Chrome/Edge para o QtWebEngine, se existir.

    Deve ser chamada antes de criar o QApplication. Retorna o caminho do CDM
    usado (ou None). É idempotente.
    """
    cdm = find_widevine_cdm()
    flags = os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS", "")
    if cdm and "--widevine-path" not in flags:
        flags = f'{flags} --widevine-path="{cdm}"'.strip()
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = flags
    if verbose:
        # ASCII puro: o console do Windows (cp1252) pode quebrar com acentos.
        if cdm:
            print(f"[midia] Widevine CDM encontrado: {cdm}")
        else:
            print("[midia] Widevine CDM nao encontrado (DRM como Netflix/Spotify "
                  "nao vai funcionar). Instale o Chrome ou o Edge.")
        print("[midia] Aviso: este build do QtWebEngine nao tem codecs "
              "proprietarios (H.264/AAC) - muitos videos MP4 e lives HLS/DASH "
              "nao tocam. Veja configs/media_env.py.")
    return cdm
