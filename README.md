# Filesystem App

For the Weave Grid coding exercise.

## REST API Documentation

No `POST`, `PUT`, or `DELETE` methods have been implemented. All responses are a
JSON-formatted dictionary containing two fields: `status` and `payload`.

`status` is either `OK` (the request was successful) or `ERROR` (e.g. file not
found).

The `payload` field contains one of two things:
* In the case of a directory, a list of directory entries.
* In the case of a file, the text of the file.

Each directory entry contains the following fields:
* `name`: The short name of the file or directory.
* `owner`: The owner of the file or directory.
* `path`: The full (absolute) path of the file or directory.
* `is_dir`: `True` if the entry corresponds to a directory, `False` otherwise.
* `permissions`: A 3-character string representing the permissions bits in octal
  format, e.g. `"700"` or `"644"`.
* `size_bytes`: The size of the file in bytes.

### `GET /`

Returns the entries contained in the root directory (specified at startup).

### `GET /<dir>[/<subdir>]`

Returns the entries contained in the target subdirectory, if it exists.

### `GET /<file>`

Returns the contents of `<file>`, if it exists. 

## Running the application

### Development

Use `./run-devserver.sh <root_dir>` to start up a local development version of
the server, with root directory `<root_dir>`.

### Docker

Use `./docker-build.sh` to build the Docker image.

Use `./docker-run.sh` to run the app in a Docker container. There is currently
no way to pass the desired root directory for the filesystem, since it would
have to be replicated on the container.
