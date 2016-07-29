Flask for Windows installation.

I'm not upload it, because it has 70MB aproximately and you mandaorily need to install in your Windows computer.

To install it, just follow the steps:

On your Windows PowerShell:

$ python-3.5.2			        # install Python on Windows

$ md blog			              # creates directory blog

$ cd blog			              # jump into directory blog

$ python -m venv flask  		# installs flask

$ pip install virtualenv		# installs virtualenv

$ python -m pip install --upgrade pip	     # upgrades pip to the latest version (if necessary)

$ virtualenv flask		      # creates virtual environment called flask

# Now, start installing flask environment modules: 

$ .\flask\Scripts\pip install flask

$ .\flask\Scripts\pip install flask-login

$ .\flask\Scripts\pip install flask-openid

$ .\flask\Scripts\pip install flask-mail

$ .\flask\Scripts\pip install flask-sqlalchemy

$ .\flask\Scripts\pip install flask-whooshalchemy

$ .\flask\Scripts\pip install flask-wtf

Good luck !

