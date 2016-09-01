import kronos


@kronos.register('/1 0 * * *')
def test():
    print('test')


@kronos.register('*/5 * * * * djangouser /usr/bin/python2.5 /home/project/manage.py cleanup)')
def cleanup():
    print('manage.py cleanup called')
