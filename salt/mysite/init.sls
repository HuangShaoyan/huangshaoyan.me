/etc/nginx/conf.d/huangshaoyan.me.conf:
  file.managed:
    - source: salt://mysite/site.conf

extend:
  nginx:
    service:
      - watch:
        - file: /etc/nginx/conf.d/huangshaoyan.me.conf

/var/local/huangshaoyan.me:
  file.recurse:
    - source: salt://mysite/htdoc
    - clean: True
