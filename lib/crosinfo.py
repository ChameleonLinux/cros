"""
  This file contains only informations about release.

  Changes to this file may disable auto-updates when
  it's implemented.
"""

DetailedVersion = "2a"
Final = False
FinalVersion = "1.0"
# build date may be different than commit date
BuildDate = "Thu Jan  7 21:54:03    2016"
if Final: Version = FinalVersion
else: Version = DetailedVersion + "   (" + BuildDate + ")"