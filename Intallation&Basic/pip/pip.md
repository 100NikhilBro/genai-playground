- ```pip freeze > requirements.txt```  -- Save all installed python packages & versions in requirements.txt.

- ```pip freeze``` -- to Shows all installed packages in current virtual environment

- ```>``` -- Send output into file 

- ```requirements.txt``` -- filename where dependencies are stored 

-``` pip install ``` -- After your pip install , u have to run the ```pip frezze >  requirements.txt```

<b> Why this is Important ? </b>

If someone downloads our project then he does not install all packages manually so he have to have to run a single cmd -- 
``` pip install -r requirements.txt ```
