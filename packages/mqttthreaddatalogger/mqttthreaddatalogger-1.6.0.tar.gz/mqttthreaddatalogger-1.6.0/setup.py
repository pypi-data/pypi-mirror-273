import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mqttthreaddatalogger", # Replace with your own username
    version="1.6.0",
    author="Didier Orlandi",
    author_email="didier.orlandi@wanadoo.fr",
    description="Connexion mqtt et enregistrement des données dans un fichier csv",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=[
          'paho-mqtt',
      ],
)