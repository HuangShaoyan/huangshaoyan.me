nginx_repo:
  pkgrepo.managed:
    - name: deb http://nginx.org/packages/ubuntu/ precise nginx
    - file: /etc/apt/sources.list.d/nginx.list
    - key_url: http://nginx.org/keys/nginx_signing.key
    - require_in:
      - pkg: nginx

nginx:
  pkg:
    - installed
  service:
    - running
    - reload: True
    - watch:
      - pkg: nginx
      - file: /etc/nginx/nginx.conf
      - file: /etc/nginx/conf.d/no-default.conf
      - file: /etc/nginx/conf.d/example_ssl.conf
      - file: /etc/nginx/conf.d/default.conf

/etc/nginx/nginx.conf:
  file.managed:
    - source: salt://nginx/nginx.conf

/etc/nginx/conf.d/no-default.conf:
  file.managed:
    - source: salt://nginx/no-default.conf

/etc/nginx/conf.d/example_ssl.conf:
  file.absent

/etc/nginx/conf.d/default.conf:
  file.absent
