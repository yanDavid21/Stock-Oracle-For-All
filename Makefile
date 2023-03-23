PY=python3
PI=pip install

ROOT_PATH = .

REQ=requirements.txt
REQDEV=requirements.dev.txt

install: precommit install-workspace check sync

install-workspace:
		cat ${REQDEV} >  ${REQ}; ${PI} -r ${REQ}

precommit:
		pre-commit install

sync: check
		pip freeze > requirements.txt

check:
		pip check
