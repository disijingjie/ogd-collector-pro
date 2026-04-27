import zipfile
z = zipfile.ZipFile('/tmp/test.zip')
z.extractall('/tmp/ogd-new')
print('OK')
