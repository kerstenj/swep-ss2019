pip install virtualenv
virtualenv ..\env
cmd /k "..\env\scripts\activate & pip install -r ..\requirements.in & deactivate"