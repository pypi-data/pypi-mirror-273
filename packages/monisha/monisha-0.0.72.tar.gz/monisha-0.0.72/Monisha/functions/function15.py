import os
from pathlib import Path
from .function04 import Eimes
from .function09 import Storage
#=================================================================================================

class Messages:
    def __init__(self, **kwargs):
        self.numfiles = kwargs.get('numfiles', 0)
        self.filesize = kwargs.get('filesize', 0)
        self.allfiles = kwargs.get('allfiles', None)
        self.location = kwargs.get('location', None)

#=================================================================================================

class Location:

    async def get05(directory, stored=[], skip=Eimes.DATA00):
        for patho in directory:
            if patho.upper().endswith(skip):
                continue
            else:
                stored.append(patho)

        stored.sort()
        return Messages(allfiles=stored, numfiles=len(stored))

#=================================================================================================
    
    async def get04(directory, stored=[]):
        for item in directory:
            stored.append(str(item))

        stored.sort()
        return Messages(allfiles=stored, numfiles=len(stored))

#=================================================================================================
    
    async def get03(directory, stored=[]):
        for item in Path(directory).rglob('*'):
            if os.path.isdir(item):
                continue
            else:
                stored.append(str(item))

        stored.sort()
        return Messages(allfiles=stored, numfiles=len(stored))

#=================================================================================================

    async def get01(flocation, exo):
        try:
            location = str(flocation)
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = str(flocation) + "." + exo
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(flocation)[0]
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(flocation)[0] + str(".mkv")
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(flocation)[0] + "." + str(exo)
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            return Messages(location=None, filesize=0)

#=================================================================================================

    async def get02(dlocation, exo, exe):
        try:
            location = str(dlocation)
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = str(dlocation) + "." + exo
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = str(dlocation) + "." + exe
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0]
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + str(".mp3")
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + str(".mp4")
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + str(".mkv")
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + "." + str(exe)
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            pass
        try:
            location = os.path.splitext(dlocation)[0] + "." + str(exo)
            filesize = int(os.path.getsize(location))
            return Messages(location=location, filesize=filesize)
        except Exception:
            return Messages(location=None, filesize=0)

#=================================================================================================
