def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install',package])
    finally:
        globals()[package] = importlib.import_module(package)

# No Linux eh necessario baixar o package:  sudo apt-get -y install python-dev

print "INSTALLING PACKAGES"
install_and_import('flask_mobility')
install_and_import('reportlab')
install_and_import('geopy')


print "INSTALLED"

#!flask/bin/python
from app import app

app.run(debug=True,threaded=True,host='0.0.0.0', port=21027)
# app.run(debug=True,threaded=True,host='0.0.0.0', port=80 )

# Collection: Rastreadores
# dev_id = 11305516
# modelo = mxt142
# usuario= Felipe
# db.Rastreadores.insert({ dev_id:NumberInt(11304783), modelo:"MXT-142", usuario:"Felipe"})
#
#
#
#
