To install all packages (via pip):
> pip install -r requirements.txt

Then create a database in wamps/mamps/lamps.

Theck that infos are good on line 15 of app.py about database connexion :
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/ydays2020'

Where the connexion string goes like :
> mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

Then open prompt in the folder and type:
> flask db init
> flask db migrate
> flask db update

You can now run this command:
> python app.py

And enjoy the API.

