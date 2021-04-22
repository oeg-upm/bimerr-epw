
# **BIMERR EPW CODE**

## **Install libraries for Python3**

The [`requirements.txt`](./requirements.txt) file should list all Python libraries that your notebooks
depend on, and they will be installed using:

```
pip install -r requirements.txt
```

Should also install [Java 1.8](https://www.oracle.com/es/java/technologies/javase/javase-jdk8-downloads.html)

## **HOW TO**

- Go into [TDATA2RDFANDV](./TDATA2RDFANDV)
- Execute the following command:
    ```
    python3 manage.py runserver
    ```
- Open a web browser at the address: http://127.0.0.1:8000
- Select File2RDF &rarr; Weather Data &rarr; Select between the three Databases (Climate One Building, Energy Plus, OpenWeatherMap)
- Climate One Building and Energy Plus files will be saved into [Results folder](./TDATA2RDFANDV/converter/Results)