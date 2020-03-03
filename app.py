from flask import Flask, Response, abort, jsonify, request
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
    # 'stat': stat,
  }


def list_dir_contents(path):
  """Lists directory contents at the given path."""
  return jsonify(list(map(format_dir_entry, os.scandir(path))))


def list_file_contents(path):
  """Lists contents of the file at the given path."""
  with open(path) as f:
    contents = f.read()
  return jsonify(contents)


@app.route('/')
def list_root_dir_contents():
  """Lists the contents of the root directory."""
  if not os.path.isdir('.'):
    abort(Response("Invalid root directory specified at startup!"))
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
    return list_file_contents(pathname)
  abort(Response(f"{pathname}: No such file"))
