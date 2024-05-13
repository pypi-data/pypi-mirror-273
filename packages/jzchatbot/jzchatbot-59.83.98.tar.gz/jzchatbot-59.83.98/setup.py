import setuptools 

with open("README.md", "r") as fh: 
	description = fh.read() 

setuptools.setup( 
	name="jzchatbot", 
	version="59.83.98", 
	author="JZ Enterprises", 
	packages=setuptools.find_packages(), 
	description="A package that creates advanced AI chatbots", 
	long_description=description, 
	long_description_content_type="text/markdown", 
	license='MIT', 
	python_requires='>=3.8', 
	install_requires=[
        'pyttsx3',
        'speechrecognition',
        'nltk',
        'textblob'
    ]
) 
