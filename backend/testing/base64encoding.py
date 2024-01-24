import base64


test_file = open(f"../../test_data/FakeTest1/IMG_4162.jpg", 'rb').read()
test_base64_str = base64.b64encode(test_file).decode('utf8')

ex_b64_str = open(f"b64_img.txt", 'w').write(test_base64_str)