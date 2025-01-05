def test_index(client):
    rv = client.get("/")
    assert "로그인" in rv.data.decode()
    assert "이미지 신규 등록" in rv.data.decode()