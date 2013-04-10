--python manage.py reset south
--python manage.py convert_to_south inwin
--python manage.py convert_to_south cms
python manage.py syncdb --all
python manage.py migrate --list
python manage.py schemamigration inwin --auto
python manage.py migrate inwin
python manage.py schemamigration cms --auto
python manage.py migrate cms
-- python manage.py test finance_trading
