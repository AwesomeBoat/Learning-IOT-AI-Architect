

# 1. Importation de la librairie pandas 
import pandas as pd

# 2. Importation du fichier csv 

df = pd.read_csv(r"pandas\Exos\Exercices_Pandas_athlete_events.csv")

# 3. Afficher les 5 premières lignes afin de voir si l'importation est correcte  
print(df.head())

# 4. Afficher les 5 dernières lignes  
print(df.tail())

# 5. Afficher les informations sur le dataframe (le nombre de lignes, de colonnes, le 
# nombre de NaN, le type de colonne)  
print(50*'-')
print("Nbre colonnes : ",len(df.columns))
print(50*'-')
print("Nbre lignes : ", df.shape[0])
print(50*'-')
print("Types par colonne :\n",df.dtypes)
print(50*'-')
print("nombre de NaN : ", df.isna().sum().sum() )

# 6. Afficher les dimensions du dataframe  
print("Dimensions de ma df : ", df.shape)

# 7. Afficher les statistiques descriptives du dataframe 
print("Statistiques descriptives de ma df : ", df.describe())
# 8. Compter le nombre de valeurs nulles dans le dataframe 
# 9. Sélectionner la colonne Games et l'afficher (selon 2-3 manières) 
# 10. Sélectionner la colonne Name et afficher le résultat en triant par ordre 
# alphabétique 
# 11. Sélectionner les colonnes Event, City, Name, Medal 
# 12. Slicer les lignes de 0 à 25 du dataframe au moyen du `iloc` 
# 13. Filtrer la discipline Football de 2 manières différentes 
# 14. Filtrer le dataframe sur la saison Summer et stocker les lignes dans une nouvelle 
# variable appelée `ete` 
# 15. Filtrer le dataframe sur la saison Winter et stocker les lignes dans une nouvelle 
# variable appelée `hiver`