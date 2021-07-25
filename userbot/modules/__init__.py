# U S Σ R Δ T O R / Ümüd

""" U S Σ R Δ T O R """
from userbot import LOGS
from telethon.tl.types import DocumentAttributeFilename 

def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3] for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return all_modules


ALL_MODULES = sorted(__list_all_modules())
LOGS.info("Yüklənəcək modullar: %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]


async def MEDIACHECK(reply): 
 type = "img" 
 if reply and reply.media: 
  if reply.photo: 
   data = reply.photo 
  elif reply.document: 
   if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in reply.media.document.attributes: 
    return False 
   if reply.gif or reply.video: 
    type = "vid" 
   if reply.audio or reply.voice: 
    return False 
   data = reply.media.document 
  else: 
   return False 
 else: 
  return False 
 if not data or data is None: 
  return False 
 else: 
  return (data, type)
