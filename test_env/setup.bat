pip install virtualenv
virtualenv env
cmd /k ".\env\Scripts\activate & pip install -r requirements.in & deactivate"
exit