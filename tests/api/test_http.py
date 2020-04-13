def test_health(client, database):
    res = client.get(path='/healty')
    assert res.status_code == 204


def test_unhealthy(client, database):
    # fake unhealty database connection
    with database.cursor() as cur:
        cur.execute('DROP TABLE production_db_version;')

    res = client.get(path='/healty')
    assert res.status_code == 503


def test_wrong_path(client):
    res = client.get(path='/loooooool')
    assert res.status_code == 404
