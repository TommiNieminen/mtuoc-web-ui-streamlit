# mtuoc-web-ui-streamlit

Web user interface for translating text and documents (.docx at the moment) with MTUOC machine translation servers. Built on Streamlit.

# Installation

1. Clone the repository.
2. Install requirements: `pip install streamlit pyperclip PyYAML lxml JPype1`

### Install Java and the MTUOC Okapi wrapper:

The Web UI uses the Okapi framework to parse and generate files. Okapi is built on Java, so using it requires a Java runtime engine.

1. Download OpenJDK22 for your system from here: [https://jdk.java.net/22/](https://jdk.java.net/22/)
2. Extract the OpenJDK22 tar.gz archive that you downloaded in the previous step (at the time of writing, the archive name is openjdk-22.0.1_linux-x64_bin.tar.gz): `tar -xvf openjdk-22.0.1_linux-x64_bin.tar.gz`
3. Export the path of the extracted tar.gz archive as JAVA_HOME environment variable. For instance, if you extracted the archive into your home directory: `export JAVA_HOME="$HOME/jdk-22.0.1"`
4. Download the MTUOC Okapi wrapper jar file from here: [https://github.com/TommiNieminen/mtuoc-web-ui-streamlit/releases/tag/okapi_wrapper_v1](https://github.com/TommiNieminen/mtuoc-web-ui-streamlit/releases/download/okapi_wrapper_v1/mtuocokapiwrapper-1.0.jar)
5. Create a _jars_ directory in the top directory of the mtuoc-web-ui-streamlit repository, and move the mtuocokapiwrapper-1.0.jar there.

# Usage

1. The Web UI reads the server information from a file called _mtSystems.yaml_. There is an example file in the top folder of the repository. Modify the file to contain the servers you wish to use.
2. Change the working dir to the top directory of the mtuoc-web-ui-streamlit repository (the one containing the _jars_ subdirectory and the _mtSystems.yaml_ file).
3. Start the Web UI with the following command: `streamlit run mtuoc_ui.py`.
4. The API is now available at localhost:8501
