
Features
-------

Easily build yaml classes and convert to a yaml file when done

Each class has the following functionality:

- add(string variable, value) #Adds a variable to the class

- get(string variable) #Gets a variable from the class

- yaml() #Returns a yamlized version of the class to be used as value for other yaml classes

- build(string filename) #Builds the yaml file from the yaml class and outputs to desired filename

installation
-------

pip install yaml-designer


Example
-------

####

from yaml_designer import yamlclass

myclass = yamlclass()

myclass.add("newvariable", "value")

myclass.build("output.yaml")

####


Requirements
-------

pip install pyyaml


License
-------

Distributed under the terms of the `BSD-3`_ license, "yaml-designer" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`BSD-3`: https://opensource.org/licenses/BSD-3-Clause
.. _`file an issue`: https://github.com/MichaelE55/yaml-designer/issues
