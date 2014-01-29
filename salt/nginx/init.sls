nginx_repo:
  pkgrepo.managed:
    - name: deb http://nginx.org/packages/ubuntu/ precise nginx
    - file: /etc/apt/sources.list.d/nginx.list
    - key_url: http://nginx.org/keys/nginx_signing.key
    - require_in:
      - pkg: nginx

nginx:
  pkg.installed
