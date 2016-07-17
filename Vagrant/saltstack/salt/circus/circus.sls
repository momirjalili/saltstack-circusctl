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

circus-web:
  pip.installed:
    - name: circus-web
    - require:
      - pkg: python-pip

/etc/init/circusd.conf:
  file.managed:
    - source: salt://circus/circusd.conf
    - user: root
    - group: root
    - mode: 644

/etc/circus/circusd.ini:
  file.managed:
    - source: salt://circus/circusd.ini
    - user: root
    - group: root
    - mode: 644
    - makedirs: True

