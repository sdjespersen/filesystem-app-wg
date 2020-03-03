from flask import Flask, abort, make_response
import os
import pwd

app = Flask(__name__)


def format_dir_entry(entry: os.DirEntry) -> dict:
  """Returns a dict containing the relevant pieces of an os.DirEntry."""
  stat = entry.stat()
  return {
    'name': entry.name,
    'owner': pwd.getpwuid(stat.st_uid).pw_name,
    'path': entry.path,
    'is_dir': entry.is_dir(),
    'permissions': oct(stat.st_mode)[-3:],
  }


def ok_response(payload):
  """Returns a payload wrapped in a response with OK status."""
  return {'status': 'OK', 'payload': payload}


def error_response(payload, status):
  """Returns a response indicating an HTTPException."""
  return make_response({'status': 'ERROR', 'error': payload}, status)


def list_dir_contents(path):
  """Lists directory contents at the given path."""
  return ok_response(list(map(format_dir_entry, os.scandir(path))))


def read_file_contents(path):
  """Reads contents of the file at the given path."""
  with open(path) as f:
    return ok_response(f.read())


@app.route('/')
def list_root_dir_contents():
  """Lists the contents of the root directory."""
  if not os.path.isdir('.'):
    abort(error_response("Invalid root directory specified at startup!", 400))
  return list_dir_contents('.')


@app.route('/<path:pathname>')
def list_path_contents(pathname):
  """
  Returns the directory listing or file contents at the given pathname,
  depending on the type of path.

  If pathname corresponds to a directory, the response will contain the file
  listing for the directory.

  If pathname corresponds to a file, the response will contain the contents of
  the file.

  If pathname does not correspond to an existing file or directory, returns an
  error.
  """
  if os.path.isdir(pathname):
    return list_dir_contents(pathname)
  elif os.path.isfile(pathname):
    return read_file_contents(pathname)
  abort(error_response(f"{pathname}: No such file", 404))
