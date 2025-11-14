from app import schemas
import pytest

def test_get_posts(authorized_client, session, test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, response.json())
    posts_list = list(posts_map)

    assert response.status_code == 200
    assert isinstance(posts_list, list)

def test_get_all_posts_unauthorized(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_get_post_unauthorized(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_post_not_found(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/9999")
    assert response.status_code == 404

def test_get_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())

    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("New Post", "New post content", True),
    ("Another Post", "Another post content", False),
    ("Yet Another Post", "Yet another post content", True),
])
def test_create_post(authorized_client, session, test_posts, test_user, title, content, published):
    post_data = {"title": title, "content": content, "published": published}
    response = authorized_client.post("/posts/", json=post_data)
    created_post = schemas.PostResponse(**response.json())

    assert response.status_code == 201
    assert created_post.title == post_data['title']
    assert created_post.content == post_data['content']
    assert created_post.user_id == test_user['id']

def test_create_post_default_published(authorized_client, session, test_posts, test_user):
    post_data = {"title": "Default Published Post", "content": "Content without published field"}
    response = authorized_client.post("/posts/", json=post_data)
    created_post = schemas.PostResponse(**response.json())

    assert response.status_code == 201
    assert created_post.title == post_data['title']
    assert created_post.content == post_data['content']
    assert created_post.published is True
    assert created_post.user_id == test_user['id']

def test_unauthorized_post_creation(client, test_posts):
    post_data = {"title": "Unauthorized Post", "content": "Should not be created"}
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 401

def test_unauthorized_post_deletion(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_not_found(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/9999")
    assert response.status_code == 404

def test_delete_post_authorized(authorized_client, session, test_posts, test_user):
    post_to_delete = test_posts[0]
    response = authorized_client.delete(f"/posts/{post_to_delete.id}")
    assert response.status_code == 204

    # Verify the post is deleted
    get_response = authorized_client.get(f"/posts/{post_to_delete.id}")
    assert get_response.status_code == 404

def test_delete_other_user_post(authorized_client, session, test_posts):
    post_to_delete = test_posts[3]  # Assuming this post belongs to another user
    response = authorized_client.delete(f"/posts/{post_to_delete.id}")
    assert response.status_code == 403

def test_update_post(authorized_client, session, test_posts, test_user):
    post_to_update = test_posts[0]
    updated_data = {"title": "Updated Title", "content": "Updated Content"}
    response = authorized_client.put(f"/posts/{post_to_update.id}", json=updated_data)
    updated_post = schemas.PostResponse(**response.json())

    assert response.status_code == 200
    assert updated_post.title == updated_data['title']
    assert updated_post.content == updated_data['content']
    assert updated_post.user_id == test_user['id']

def test_update_other_user_post(authorized_client, session, test_posts):
    post_to_update = test_posts[3]  # Assuming this post belongs to another user
    updated_data = {"title": "Hacked Title", "content": "Hacked Content"}
    response = authorized_client.put(f"/posts/{post_to_update.id}", json=updated_data)
    assert response.status_code == 403