docker exec -it backend python3 manage.py collectstatic --noinput && cp ./static_media/* ./static/admin/img/
