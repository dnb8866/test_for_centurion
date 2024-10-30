from http import HTTPStatus


async def test_home(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {'text': 'ok'}


async def test_get_products(client, many_categories_and_products):
    response = await client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 100
    response = await client.get("/products?limit=15")
    assert response.status_code == 200
    assert len(response.json()) == 15
    assert 'name' in response.json()[0]
    assert 'price' in response.json()[0]
    assert 'description' in response.json()[0]
    assert 'category_id' in response.json()[0]
    assert 'created' in response.json()[0]
    assert 'updated' in response.json()[0]
    response = await client.get("/products?min_price=1000")
    assert len(response.json()) == 0


async def test_get_one_product(client, one_product_in_db):
    response = await client.get(f'/products/{one_product_in_db.id}')
    assert response.status_code == 200
    assert response.json()['name'] == one_product_in_db.name
    assert response.json()['price'] == str(one_product_in_db.price)
    assert response.json()['category_id'] == one_product_in_db.category_id
    assert response.json()['description'] == one_product_in_db.description
    assert (await client.get(f'/products/777')).status_code == 404


async def test_post_products(client, one_category_in_db, product_repo):
    data = {'name': 'Тестовый продукт', 'price': 100.5, 'category_id': 1}
    products = await product_repo.list()
    response = await client.post("/products", json=data)
    assert response.status_code == 201
    assert response.json()['name'] == 'Тестовый продукт'
    assert response.json()['price'] == '100.5'
    assert response.json()['category_id'] == 1
    assert len(products) + 1 == len(await product_repo.list())
    data = {'name': 'Тестовый продукт', 'price': 'qwe', 'category_id': 1}
    response = await client.post("/products", json=data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_update_products(client, one_product_in_db):
    data = {
        'id': one_product_in_db.id,
        'name': 'Обновленный тестовый продукт',
        'price': 105.5,
        'category_id': 1
    }
    response = await client.put(f'/products/{one_product_in_db.id}', json=data)
    assert response.status_code == 200
    assert response.json()['name'] == 'Обновленный тестовый продукт'
    assert response.json()['price'] == '105.5'


async def test_delete_product(client, one_product_in_db, product_repo):
    products = await product_repo.list()
    response = await client.delete(f'/products/{one_product_in_db.id}')
    assert response.status_code == 204
    assert len(products) - 1 == len(await product_repo.list())


async def test_get_products_in_category(client, many_categories_and_products):
    response = await client.get('/category/1')
    assert response.status_code == 200
    assert len(response.json()) == 10
