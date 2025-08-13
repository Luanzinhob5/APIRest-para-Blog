import json

def test_create_post(client):
        
    new_post_data = {
        "titulo": "Um Título de Teste",
        "conteudo": "Conteúdo vindo de um teste automatizado.",
        "descricao": "Pytest"
    }

    response = client.post("/api/posts",
                           data=json.dumps(new_post_data),
                           content_type='application/json')
    
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data['titulo'] == "Um Título de Teste"
    assert 'id' in response_data


def test_get_all_posts_empty(client):
    response = client.get('/api/posts')
    assert response.status_code == 200
    assert response.get_json() == []