def test_vote_on_post(authorized_client, test_posts):
    vote_data = {"post_id": test_posts[3].id, "dir": 1}
    response = authorized_client.post("/votes/", json=vote_data)
    assert response.status_code == 201

def test_vote_twice_on_post(authorized_client, test_posts):
    vote_data = {"post_id": test_posts[0].id, "dir": 1}
    response = authorized_client.post("/votes/", json=vote_data)
    assert response.status_code == 201

    # Try voting again on the same post
    response = authorized_client.post("/votes/", json=vote_data)
    assert response.status_code == 409

def test_remove_vote(authorized_client, test_posts):
    vote_data = {"post_id": test_posts[1].id, "dir": 1}
    # First, add a vote
    response = authorized_client.post("/votes/", json=vote_data)
    assert response.status_code == 201

    # Now, remove the vote
    vote_data["dir"] = 0
    response = authorized_client.post("/votes/", json=vote_data)
    assert response.status_code == 204

def test_remove_nonexistent_vote(authorized_client, test_posts):
    vote_data = {"post_id": test_posts[2].id, "dir": 0}
    response = authorized_client.post("/votes/", json=vote_data)
    assert response.status_code == 404

def test_vote_on_nonexistent_post(authorized_client):
    vote_data = {"post_id": 9999, "dir": 1}
    response = authorized_client.post("/votes/", json=vote_data)
    assert response.status_code == 404

def test_unauthorized_vote(client, test_posts):
    vote_data = {"post_id": test_posts[0].id, "dir": 1}
    response = client.post("/votes/", json=vote_data)
    assert response.status_code == 401