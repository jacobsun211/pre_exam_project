# Source - https://stackoverflow.com/a/3470583
# Posted by Blair Conrad, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-05, License - CC BY-SA 4.0

import base64
coded_string = '''R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlz
cGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvb
ixSZWZ1Z2VlcyxJQ0MsQkRT'''
hostil_list = base64.b64decode(coded_string)
string_data = hostil_list.decode("utf-8")


