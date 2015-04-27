"""Generates apache 2.4 conf lines for -, _ work around
    requires mod_setenvif and mod_headers

"""

words = ["TRUSTED",
         "SERVERIP"
         "CHARNAME",
         "CHARID",
         "CORPNAME",
         "CORPID",
         "REGIONNAME",
         "CONSTELLATIONNAME",
         "SOLARSYSTEMID",
         "SOLARSYSTEMNAME",
         "SHIPID",
         "SHIPNAME",
         "SHIPTYPEID",
         "SHIPTYPENAME",
         "CORPROLE",
         "ALLIANCENAME",
         "ALLIANCEID",
         "STATIONNAME",
         "STATIONID",
         "WARFACTIONID"]

output = []
for word in words:
    lines = "SetEnvIfNoCase ^EVE_{}$ ^(.*)$ fix_eve_{}=$1\nRequestHeader set EVE-{} %{{fix_eve_{}}}e env=fix_eve_{}\n\n".format(word, word.lower(), word, word.lower(), word.lower())
    output.append(lines)
print("".join(output))