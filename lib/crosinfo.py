"""
  This file contains only informations about release.

  Changes to this file may disable auto-updates when
  it's implemented.
"""

DetailedVersion = "3a"
Insecure = True
Final = False
FinalVersion = "1.0"
# build date may be different than commit date
BuildDate = "Sat Jan  9 01:01:48 CET 2016"

if Final: Version = FinalVersion
else: Version = DetailedVersion + "   (" + BuildDate + ")\nInsecure: " + str(Insecure)
