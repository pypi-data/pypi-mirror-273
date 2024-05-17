
## Preguntas
- Mirar si cambiar como se indican las labels en los csv datasets, en la libreria de java estan distintas.
https://github.com/kdis-lab/MIML/blob/master/mavenProject/src/main/java/miml/data/MIMLInstances.java -> 
https://github.com/tsoumakas/mulan/blob/master/mulan/src/main/java/mulan/data/MultiLabelInstances.java
- Ver si hacer funciones a parte para load_cada_dataset y no tener que llamar a pkg_resources que queda feo, se
  puede mirar como esta implementado en https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/datasets/_base.py, esta ya implementado en dataset_utils.py
- Llamar evaluate fuera report pasandoselo al init, si hago esto tengo que pasar dataset.get_features_by_bag(), 
  resultado_evaluate y nombre_etiquetas. Tampoco podria pasarle detalles como el clasificador, algoritmo y transformacion usada
- sk multilearn brknn, mlknn. Lo he probado pero no funciona, parece que esta desactualizada la libreria
- A la hora de ejecutar un label powerset classifier, los clasificadores mi que hay implementados solo son capaces de 
  realizar una clasificacion binaria. Probar a incorporar CitationKNN https://github.com/arjunssharma/Citation-KNN/tree/master


### Documentacion
- Revisar todos los nombres

### Data
- Revisar split dataset

### Datasets
- Tener todos dataset en arff y csv
- Load from libray
- Transformacion lp to multilabel que convierta lp label to lista de label binarias
- Random MI

### Classifiers
- Que el predict_bag de ml devuelva un array solo, y ver el tipo con el que devuelve las labels
- Arreglar predict_proba MILESClassifier

### Report


### Tutorials
- tutorial particionado datasets con varios clasificadores y sus reports
- Ejecutarlos todos de nuevo
- Que se entienda mejor, mas prints y tal.

### Otros
- Añadir info a pyproject.toml
- documentacion bonita del codigo a web. Usar sphinx
- Train_test experiment
- Pequeño experimento