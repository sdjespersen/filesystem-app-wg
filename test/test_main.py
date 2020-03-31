import json
import os
import tempfile

import pytest

from app import main


TEXT_ONE = "I don't enjoy Bob Dylan's latest song"
TEXT_TWO = "It seems littered with clichés"

def abs_path(*args):
  """Returns the absolute path obtained by appending args to the app's root dir."""
  return os.path.join(main.app.config['FS_ROOT_DIR'], *args)

# Directory structure (from root):
# /
#  |-- foo/
#  |   |-- foobar.txt, 755
#  |   |-- baz/
#  |   |    |-- .baz1.txt, 600
#  --- bar/
def build_directory_structure():
  # directories
  foo_dir = abs_path('foo') # /foo
  bar_dir = abs_path('bar') # /bar
  baz_dir = abs_path('foo', 'baz') # /foo/baz
  os.mkdir(foo_dir)
  os.mkdir(bar_dir)
  os.mkdir(baz_dir)
  # files
  foo1_txt = abs_path('foo', 'foo1.txt') # /foo/foo1.txt
  with open(foo1_txt, 'w') as foo1:
    foo1.write(TEXT_ONE)
  baz1_txt = abs_path('foo', 'baz', '.baz1.txt') # /foo/baz/.baz1.txt
  with open(baz1_txt, 'w') as baz1:
    baz1.write(TEXT_TWO)
  os.chmod(baz1_txt, 0o600)


@pytest.fixture
def client():
  main.app.config['TESTING'] = True
  with tempfile.TemporaryDirectory() as tmpdir:
    main.app.config['FS_ROOT_DIR'] = tmpdir
    build_directory_structure()
    with main.app.test_client() as client:
      yield client


def test_list_root_dir(client):
  response = json.loads(client.get('/').data)
  assert response['status'] == 'OK'
  payload = response['payload']
  assert len(payload) == 2
  foo_dir, bar_dir = payload
  if foo_dir['name'] == 'bar':
    foo_dir, bar_dir = bar_dir, foodr # swap if reversed
  # foo
  assert foo_dir['is_dir']
  assert foo_dir['name'] == 'foo'
  assert foo_dir['path'] == abs_path('foo')
  assert foo_dir['permissions'] == '755'
  # bar
  assert bar_dir['is_dir']
  assert bar_dir['name'] == 'bar'
  assert bar_dir['path'] == abs_path('bar')
  assert bar_dir['permissions'] == '755'


def test_list_foo_subdir(client):
  response = json.loads(client.get('/foo').data)
  assert response['status'] == 'OK'
  payload = response['payload']
  assert len(payload) == 2
  foo1_txt, baz_subdir = payload
  if foo1_txt['name'] == 'baz':
    foo1_txt, baz_subdir = baz_subdir, foo1_txt
  # foo1.txt
  assert not foo1_txt['is_dir']
  assert foo1_txt['name'] == 'foo1.txt'
  assert foo1_txt['path'] == abs_path('foo', 'foo1.txt')
  assert foo1_txt['permissions'] == '644'
  # baz/
  assert baz_subdir['is_dir']
  assert baz_subdir['name'] == 'baz'
  assert baz_subdir['path'] == abs_path('foo', 'baz')
  assert baz_subdir['permissions'] == '755'


def test_read_file_contents(client):
  response = json.loads(client.get('/foo/foo1.txt').data)
  assert response['status'] == 'OK'
  assert response['payload'] == TEXT_ONE


def test_correct_perms_hidden_file(client):
  response = json.loads(client.get('/foo/baz').data)
  assert response['status'] == 'OK'
  # .baz1.txt should be the only entry
  assert len(response['payload']) == 1
  baz1 = response['payload'][0]
  assert baz1['permissions'] == '600'


def test_get_nonexistent_file(client):
  response = json.loads(client.get('/bogus.txt').data)
  assert response['status'] == 'ERROR'
