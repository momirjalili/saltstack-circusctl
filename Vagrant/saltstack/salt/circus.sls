python-pip:
  pkg.installed:
    - order: 2

python-dev:
  pkg.installed:
    - order: 1

libzmq-dev:
  pkg.installed:
    - order: 3

libevent-dev:
  pkg.installed:
    - order: 4

circus:
  pip.installed:
    - name: circus
    - require:
      - pkg: python-pip
