import io
import os
import logging
import requests
from dotenv import load_dotenv
from gtts import gTTS
 
load_dotenv()
 
logger = logging.getLogger(__name__)
 
LIBRE_SERVERS = [
    "https://libretranslate.com",
    "https://translate.argosopentech.com",
    "https://libretranslate.de",
]
 
MYMEMORY_EMAIL   = os.getenv("MYMEMORY_EMAIL", "")
MYMEMORY_API_KEY = os.getenv("MYMEMORY_API_KEY", "")
 
TTS_SUPPORTED_LANGS = {
    "af", "ar", "bn", "bs", "ca", "cs", "cy", "da", "de", "el", "en",
    "eo", "es", "et", "fi", "fr", "gu", "hi", "hr", "hu", "hy", "id",
    "is", "it", "ja", "kn", "ko", "lv", "mk", "ml", "mr", "nl", "no",
    "pl", "pt", "ro", "ru", "si", "sk", "sq", "sr", "sv", "sw", "ta",
    "te", "th", "tl", "tr", "uk", "ur", "vi", "zh-cn", "zh-tw",
}
 
 
def _try_libretranslate(text, source_lang, target_lang):
    src = "auto" if source_lang == "auto" else source_lang
    tgt = "zh" if target_lang in ("zh-cn", "zh-tw") else target_lang
    if src in ("zh-cn", "zh-tw"):
        src = "zh"
 
    for server in LIBRE_SERVERS:
        try:
            logger.info("[API] Trying LibreTranslate: %s", server)
            r = requests.post(
                f"{server}/translate",
                json={"q": text, "source": src, "target": tgt, "format": "text"},
                timeout=10,
                headers={"Content-Type": "application/json"},
            )
            if r.status_code == 200:
                translated = r.json().get("translatedText", "")
                if translated and translated != text:
                    logger.info("[API] LibreTranslate OK via %s", server)
                    return {"translated_text": translated, "detected_lang": None, "error": None}
            else:
                logger.warning("[API] %s returned %d", server, r.status_code)
        except Exception as exc:
            logger.warning("[API] %s failed: %s", server, exc)
    return None
 
 
def _try_mymemory(text, source_lang, target_lang):
    effective_source = "en" if source_lang == "auto" else source_lang
    params = {"q": text, "langpair": f"{effective_source}|{target_lang}"}
    if MYMEMORY_EMAIL:
        params["de"] = MYMEMORY_EMAIL
    if MYMEMORY_API_KEY:
        params["key"] = MYMEMORY_API_KEY
    try:
        logger.info("[API] Trying MyMemory...")
        r = requests.get("https://api.mymemory.translated.net/get", params=params, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        if data.get("responseStatus") != 200:
            return None
        translated = data["responseData"]["translatedText"]
        bad = ["QUERY LENGTH", "LIMIT EXCEDEED", "MYMEMORY", "INVALID"]
        if any(b in translated.upper() for b in bad):
            return None
        logger.info("[API] MyMemory OK")
        return {"translated_text": translated, "detected_lang": None, "error": None}
    except Exception as exc:
        logger.warning("[API] MyMemory failed: %s", exc)
        return None
 
 
def call_translation_api(text: str, source_lang: str, target_lang: str) -> dict:
    if not text.strip():
        return {"translated_text": None, "detected_lang": None, "error": "Text is empty."}
 
    result = _try_libretranslate(text, source_lang, target_lang)
    if result:
        return result
 
    logger.warning("[API] LibreTranslate failed, trying MyMemory...")
    result = _try_mymemory(text, source_lang, target_lang)
    if result:
        return result
 
    return {
        "translated_text": None,
        "detected_lang": None,
        "error": "Translation failed. Check your internet connection and try again.",
    }
 
 
def call_tts_api(text: str, lang: str) -> dict:
    lang_used = lang if lang in TTS_SUPPORTED_LANGS else "en"
    if lang_used != lang:
        logger.warning("[API] TTS: '%s' unsupported, falling back to 'en'", lang)
    try:
        tts = gTTS(text=text, lang=lang_used, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        logger.info("[API] TTS OK: lang=%s, chars=%d", lang_used, len(text))
        return {"audio_bytes": buf.read(), "lang_used": lang_used, "error": None}
    except Exception as exc:
        logger.error("[API] TTS failed: %s", exc)
        return {"audio_bytes": None, "lang_used": lang_used, "error": str(exc)}