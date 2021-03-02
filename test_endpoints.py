import config
import pytest
import json
import bcrypt

from sqlalchemy import create_engine, text
from app import create_app

database = create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow=0)


@pytest.fixture
def api():
    app = create_app(config.test_config)
    app.config['TEST'] = True
    api = app.test_client()
    return api


def setup_function():
    # 테스트 사용자 2명 생성
    hashed_password = bcrypt.hashpw(
        b"test password",
        bcrypt.gensalt()
    )
    test_users = [
        {
            'id': 1,
            'name': "test_name1",
            'email': "test1@test.com",
            'profile': "this is a test user1",
            'hashed_password': hashed_password
        }, {
            'id': 2,
            'name': "test_name2",
            'email': "test2@test.com",
            'profile': "this is a test user2",
            'hashed_password': hashed_password
        }
    ]
    database.execute(text("""
        INSERT INTO users (
            id,
            name,
            email,
            profile,    
            hashed_password
        ) VALUES (
            :id,
            :name,
            :email,
            :profile,
            :hashed_password
        )
    """), test_users)

    # 테스트용 사용자 2 트윗 생성
    database.execute(text("""
        INSERT INTO tweets (
            user_id,
            tweet
        ) VALUES (
            2,
            "Hello world"
        )
    """))


def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def login_user1(api):
    # 테스트 사용자1 로그인
    resp = api.post(
        '/login',
        data=json.dumps({'email': "test1@test.com", 'password': "test password"}),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']
    return access_token


def test_ping(api):
    resp = api.get('/ping')
    assert b'pong' in resp.data


def test_login(api):
    resp = api.post(
        '/login',
        data=json.dumps({'email': "test1@test.com", 'password': "test password"}),
        content_type='application/json'
    )
    assert resp.status_code == 200


def test_login_required(api):
    # access_token 이 없으면 401을 반환하는지 확인
    # 트윗
    resp = api.post(
        '/tweet',
        data=json.dumps({'tweet': "login required test"}),
        content_type='application/json'
    )
    assert resp.status_code == 401

    # 팔로우
    resp = api.post(
        '/follow',
        data=json.dumps({'follow': 2}),
        content_type='application/json'
    )
    assert resp.status_code == 401

    # 언팔로우
    resp = api.post(
        '/unfollow',
        data=json.dumps({'unfollow': 2}),
        content_type='application/json'
    )
    assert resp.status_code == 401

    # 유저 타임라인
    resp = api.get('/timeline')
    assert resp.status_code == 401


def test_tweet(api):
    # 사용자1 로그인
    access_token = login_user1(api)

    # 트윗
    resp = api.post(
        '/tweet',
        data=json.dumps({'tweet': 'Test tweet body'}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # 트윗 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 1,
                'tweet': "Test tweet body"
            }
        ]
    }


def test_follow(api):
    # 사용자1 로그인
    access_token = login_user1(api)

    # 사용자1 timeline 비었는지 확인
    resp = api.get('/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': []
    }

    # 사용자2 팔로우
    resp = api.post(
        '/follow',
        data=json.dumps({'follow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # 사용자2의 트윗 사용자1 타임라인에 표시 확인
    resp = api.get('/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 2,
                'tweet': "Hello world"
            }
        ]
    }


def test_unfollow(api):
    # 사용자1 로그인
    access_token = login_user1(api)

    # 사용자2 팔로우
    resp = api.post(
        '/follow',
        data=json.dumps({'follow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # 사용자1 타임라인에 사용자2 트윗이 있는지 확인
    resp = api.get('/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 2,
                'tweet': "Hello world"
            }
        ]
    }

    # 사용자2 언팔로우
    resp = api.post(
        '/unfollow',
        data=json.dumps({'unfollow': 2}),
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    assert resp.status_code == 200

    # 사용자1 타임라인에 사용자2 트윗이 표시 안되는지 확인
    resp = api.get('/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': []
    }
