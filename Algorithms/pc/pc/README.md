# pseudocode README

![Logo](images/logo.png)

This is the README for your extension "pseudocode". 
Make file with extension .pc
This extension is an help to learn pseudocode in French.  So next is in French.

Cette extension a est développée dans le but de faire apprendre aux novices l'algorithmie et surtout la rigueur de l'écriture informatique.


## Features

Pour chacun des exercices, créez un fichier portant l'extension .pc par exemple :
exo1.pc

Voici la liste des raccourcis :

<table>
        <tr>
            <th>Raccourci</th>
            <th>Code génénré</th>
            <th>Notes</th>
        </tr>
        <tr>
            <td>algo</td>
            <td>
                    <code>
                        Algorithme nomAlgo
                        DEBUT<br>                       
                        FIN
                     </code>                      
            </td>
            <td>
                    <ul>
                            <li>le curseur se place au niveau de nomAlgo afin de définir le nom </li>
                            <li>puis appuyez sur TABULATION, le curseur se place entre DEBUT et FIN </li>
                    </ul>        
            </td>
        </tr>
        <tr>
            <td>variable</td>
            <td><code>Variable nomVariable : Entier</code></td>
            <td>
                    <ul>
                        <li>le curseur se place au niveau de nomVariable afin de définir le nom de la variable</li> 
                        <li>puis appuyer sur TABULATION, le curseur se déplace et une liste déroulante apparait pour choisir le type de la variable (Entier, Reel, Chaine, Booleen, Tableau)</li>
                    </ul>
            </td>
        </tr>        
        <tr>
            <td><-</td>
            <td>phrase <- "Bonjour"</td>
            <td>
                   la variable nom reçoit la chaine de caractères "Bonjour"
            </td>
        </tr>
        <tr>
            <td>&&</td>
            <td></td>
            <td>
                   le symbole pour dire ET
            </td>
        </tr>
        <tr>
            <td>||</td>
            <td></td>
            <td>
                   le symbole pour dire OU
            </td>
        </tr>
        <tr>
            <td>!</td>
            <td></td>
            <td>
                   le symbole pour dire NON
            </td>
        </tr>
        <tr>
            <td>SI</td>
            <td>
                    <code>
                            SI condition ALORS
                                instructions
                            FINSI
                    </code>
            </td>
            <td>
                   <ul>
                        <li>le curseur se place au niveau de condition afin de définir la ou les conditions</li> 
                        <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de instructions</li>
                    </ul>
            </td>
        </tr>
        <tr>
            <td>SINONSI</td>
            <td>
                    <code>
                            SINONSI condition ALORS
                                instructions                            
                    </code>
            </td>
            <td>
                   <ul>
                        <li>le curseur se place au niveau de condition afin de définir la ou les conditions</li> 
                        <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de instructions</li>
                    </ul>
            </td>
        </tr>
        <tr>
            <td>SINON</td>
            <td>
                    <code>
                            SINON
                                instructions                        
                    </code>
            </td>
            <td>
                   <ul>                    
                        <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de instructions</li>
                    </ul>
            </td>
        </tr>
        <tr>
            <td>SELONQUE</td>
            <td>
                    <code>
                            SELONQUE nomVariable VAUT
                                valeur1 : instructions1
                                valeur2 : instructions2
                                SINON : instructions3
                            FINSQ
                    </code>
            </td>
            <td>
                   <ul>
                           <li>le curseur se place au niveau de nomVariable afin de définir le nom de la variable</li> 
                           <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de valeur1</li>
                           <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de instructions1</li>
                           <li>...</li>
                    </ul>
            </td>
        </tr>
        <tr>
            <td>TANTQUE</td>
            <td>
                    <code>
                            TANTQUE condition FAIRE
                                instructions
                            FINTQ
                    </code>
            </td>
            <td>
                   <ul>
                           <li>le curseur se place au niveau de condition afin de définir la ou les conditions</li> 
                           <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de instruction</li>                           
                    </ul>
            </td>
        </tr>
        <tr>
            <td>FAIRE</td>
            <td>
                    <code>
                            FAIRE
                                instructions
                            TANTQUE condition FINTQ
                    </code>
            </td>
            <td>
                   <ul>
                           <li>le curseur se place au niveau de instructions afin de définir la ou les instructions</li> 
                           <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de condition</li>                           
                    </ul>
            </td>
        </tr>
         <tr>
            <td>POUR</td>
            <td>
                    <code>
                            POUR nomVariable DE valeurDepart À valeurFinComprise [PAR pas] FAIRE
                                instructions
                            FINP
                    </code>
            </td>
            <td>
                   <ul>
                           <li>le curseur se place au niveau de nomVariable afin de définir la variable</li> 
                           <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de valeurDepart</li>     
                           <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de valeurFinComprise</li> 
                           <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de pas</li> 
                           <li>puis appuyer sur TABULATION, le curseur se déplace au niveau de instructions</li> 
                    </ul>
            </td>
        </tr>
    </table>

## Requirements

Aucun

### 0.0.1

Version 0.01