from setuptools import setup, find_packages
from projectfastapi.main import version

setup( 
	name="create-app-fastapi", 
	version= version, 
	author="Ravishnu", 
	author_email="ravishnu60@gmail.com", 
	packages=find_packages(), 
    url="https://github.com/ravishnu60/create-app-fastapi.git",
	description="Library for initializing FastAPI projects - create-app-fastapi", 
	long_description="""A package used to create fastAPI project structure with virtual environment and dependencies.
    Can setup database connection while createing a project.
    Once you install this package use below command to create fastapi project,
    
    create-app-fastapi project-name
	
    
    The Project structure will be created in current working directory.
    The structure will be,
    
		root-folder
		|-APIs
		|  |-__init__.py
		|  |-api.py
		|-models
		|  |-__init__.py
		|  |-model.py
		|-schemas
		|  |-__init__.py
		|  |-schema.py
		|-settings
		|  |-__init__.py
		|  |-auth.py
		|  |-config.py
		|  |-db.py
		|-testcase
		|  |-__init__.py
		|  |-test_main.py
		|-venv
		|-.gitignore
		|-main.py
		|-requirements.txt
    
        
        ____________________________________________ Happy coding !!! __________________________________________
    """, 
	long_description_content_type="text/markdown", 
	python_requires='>=3.9', 
	install_requires=[],
	entry_points ={ 
		'console_scripts': [ 
			'create-app-fastapi=projectfastapi.main:main'
		] 
	},
    keywords=['fastapi', 'fastapi project','project structure','api structure', 'python fastapi project structure']
) 
