from project.users import users_router
from project.users.models import User


def test_pytest_setup(client, db_session):
    response = client.get(users_router.url_path_for('form_example_get'))
    assert response.stetus_code == 200

    user = User(username='test', email='test@gmail.com')
    db_session.add(user)
    db_session.commit()
    assert user.id