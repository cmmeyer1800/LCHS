def check_status_code_good(client, url):
    response = client.get(url)
    assert (response.status_code == 302 or response.status_code == 200)

def check_status_code_bad(client, url):
    response = client.get(url)
    assert (response.status_code == 404)

def test_index_response(client):
    check_status_code_good(client, '/')

def test_video_response(client):
    check_status_code_good(client, '/video')

def test_photo_response(client):
    check_status_code_good(client, '/photo')

def test_video_specific_response(client):
    check_status_code_good(client, '/video/test_15s.mp4')

def test_nonexistent_endpoint(client):
    check_status_code_bad(client, "/badpath")