1) Installation:  What steps are required for someone to take your zip file and make the program work. Please make sure to include the target environment and any additional steps required for setup.
- Move the .zip file to a directory of your choice
- Extract the files to that location
- Using command prompt, navigate to the directory you chose
- Navigate into the HealthNet folder
- Run the batch file by doing the following for your OS:

Windows: run 

	>	rebuilddatabase.bat

	from windows command line


	
macOS/Linux: run

	>	bash rebuilddatabase.command

	from Terminal
	(on masOS/Linux only: use the flag ‘-r’ to immediately start the server after the 	database is reset: 
	>	bash rebuilddatabase.command -r
	)
	
- Run the command "python manage.py runserver"
- Using a browser of your choosing, go to the URL "127.0.0.1:8000"
- If all goes well you should be able to use the site

2) Known bugs and disclaimers
-None

3) Known missing Release-x features
-None

4) Basic execution and usage instructions (logins & passwords)
- Register as Patient
- Fill out info
- Access website with new account

Doctors
	User: doctor1
	pass: P@ssword
	
	User: doctor2
	pass: P@ssword

Patients
	User: patient1
	pass: P@ssword

Nurses
	User: nurse1
	pass: P@ssword

	User: nurse2
	pass: P@ssword

HAdmins
	User: admin1
	pass: P@ssword

Populate Database:


Windows: run

        >       rebuilddatabase.bat

        from windows command line



macOS/Linux: run

        >       bash rebuilddatabase.command

        from Terminal
        (on masOS/Linux only: use the flag ‘-r’ to immediately start the server after the       database is reset:
        >       bash rebuilddatabase.command -r
        )
