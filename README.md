# Dear kids,

## Intentions

A tiny app with big hopes.
A few bottle messages thrown to the sea.
A shared memory of feelings.


## Environment

Assuming you use fish + https://virtualfish.readthedocs.io/

```
vf new --python=python3.7 dearkids
```


## Installation

```
make install
make run
=> Rolling on http://127.0.0.1:3579
```


## Development

```
make dev
make check
make test
```


## Production

```
pip install gunicorn
make prod
```

Serve statics with anything else *but* the Roll extension.
