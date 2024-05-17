__all_ = ["built_lat_long",
          "plot_club_38",
          "plot_ctg",
          "stat_sorties_club",]
             

def plot_club_38(ctg_path):

    # Standard library import
    from pathlib import Path

    # 3rd party imports
    import folium
    import numpy as np
    import pandas as pd


    df = pd.read_excel(ctg_path / Path('club_38.xlsx'))
    path_villes_de_france = Path(__file__).parent.parent / Path('CTG_Func') / Path('CTG_RefFiles/villes_france_premium.csv')
    df_villes = pd.read_csv(path_villes_de_france,header=None,usecols=[2,19,20])
    dic_long = dict(zip(df_villes[2] , df_villes[19]))
    dic_lat = dict(zip(df_villes[2] , df_villes[20]))

    #df =pd.read_excel(root / Path(effectif))

    df['Ville'] = df['Ville'].str.replace(' ','-')
    df['Ville'] = df['Ville'].str.replace('ST-','SAINT-')
    df['Ville'] = df['Ville'].str.replace('\-D\-+',"-D'",regex=True)
    df['Ville'] = df['Ville'].str.replace('^LA-',"LA ",regex=True)
    df['Ville'] = df['Ville'].str.replace('^LE-',"LE ",regex=True)
    df['Ville'] = df['Ville'].str.replace('SAINT-HILAIRE-DU-TOUVET',"SAINT-HILAIRE",regex=False)
    df['Ville'] = df['Ville'].str.replace('SAINT-HILAIRE',"SAINT-HILAIRE-38",regex=False)
    df['Ville'] = df['Ville'].str.replace('LAVAL',"LAVAL-38",regex=False)
    df['Ville'] = df['Ville'].str.replace('LES-ABRETS',"LES ABRETS",regex=False)
    df['Ville'] = df['Ville'].str.lower()

    df['long'] = df['Ville'].map(dic_long)
    df['lat'] = df['Ville'].map(dic_lat)



    kol = folium.Map(location=[45.2,5.7], tiles='openstreetmap', zoom_start=12)

    for latitude,longitude,size, ville, num_ffct, club in zip(df['lat'],
                                                        df['long'],
                                                        df['number'],
                                                        df['Ville'],
                                                        df['N° FFCT'],
                                                        df['Nom Club'] ):

        long_ville, lat_ville =df.query("Ville==@ville")[['long','lat']].values[0]#.flatten()
        color='blue'

        folium.Circle(
                        location=[latitude, longitude],
                        radius=size*10,
                        popup=f'{ville} ({size}), club:{club} ',
                        color=color,
                        fill=True,
    ).add_to(kol)
    return kol
    
def built_lat_long(df):
    
    # Standard library imports
    from collections import Counter
    from pathlib import Path
    
    # 3rd party imports
    import folium
    import numpy as np
    import pandas as pd
    
    path_villes_de_france = Path(__file__).parent.parent / Path('CTG_Func/CTG_RefFiles/villes_france_premium.csv')
    
    def normalize_ville(x):
        dic_ville = {'SAINT-HILAIRE-DU-TOUVET':"SAINT-HILAIRE-38",
                     'SAINT-HILAIRE':"SAINT-HILAIRE-38",
                     'LAVAL-EN-BELLEDONNE':'LAVAL-38',
                     'LAVAL':"LAVAL-38",
                     'CRETS-EN-BELLEDONNE':"SAINT-PIERRE-D'ALLEVARD"}
        if x in dic_ville.keys(): 
            return dic_ville[x]
        else:
            return x
        
    df_villes = pd.read_csv(path_villes_de_france,header=None,usecols=[3,19,20])
    dic_long = dict(zip(df_villes[3] , df_villes[19]))
    dic_lat = dict(zip(df_villes[3] , df_villes[20]))

    df['Ville'] = df['Ville'].str.replace(' ','-')
    df['Ville'] = df['Ville'].str.replace('ST-','SAINT-')
    df['Ville'] = df['Ville'].str.replace('\-D\-+',"-D'",regex=True)
    df['Ville'] = df['Ville'].str.replace('^LA-',"LA ",regex=True)
    df['Ville'] = df['Ville'].str.replace('^LE-',"LE ",regex=True)
    
    df['Ville'] = df['Ville'].apply(normalize_ville)
    

    df['long'] = df['Ville'].map(dic_long)
    df['lat'] = df['Ville'].map(dic_lat)
    list_villes = df['Ville'].tolist()
    Counter(list_villes)
    dg = df.groupby(['Ville']).count()['N° Licencié']

    dh = pd.DataFrame.from_dict({'Ville':dg.index,
                                'long':dg.index.map(dic_long),
                                'lat':dg.index.map(dic_lat),
                                'number':dg.tolist()})
    return df,dh
    
def plot_ctg(df):
    
    # 3rd party imports
    import folium
    trace_radius = True
    _,dh = built_lat_long(df)

    group_adjacent = lambda a, k: list(zip(*([iter(a)] * k))) 

    dict_cyclo = {}
    for ville,y in df.groupby(['Ville'])['Nom']:
        chunk = []
        for i in range(0,len(y),3):
            chunk.append(','.join(y[i:i+3] ))

        dict_cyclo[ville] = '\n'.join(chunk)

    kol = folium.Map(location=[45.2,5.7], tiles='openstreetmap', zoom_start=12)

    long_genoble, lat_grenoble = dh.query("Ville=='GRENOBLE'")[['long','lat']].values.flatten()
    if trace_radius:
        folium.Circle(
                      location=[lat_grenoble, long_genoble],
                      radius=8466,
                      popup='50 km ',
                      color="black",
                      fill=False,
                      ).add_to(kol)        
    for latitude,longitude,size, ville in zip(dh['lat'],dh['long'],dh['number'],dh['Ville']):

        long_ville, lat_ville =dh.query("Ville==@ville")[['long','lat']].values.flatten()
        dist_grenoble_ville = _distance(lat_grenoble, long_genoble,lat_ville, long_ville )
        color='red' if dist_grenoble_ville>19.35 else 'blue'
        if ville == "grenoble":
            folium.Circle(
                location=[latitude, longitude],
                radius=size*50,
                popup=f'{ville} ({size}): {dict_cyclo[ville]} ',
                color="yellow",
                fill=True,
            ).add_to(kol)
        else:
                folium.Circle(
                location=[latitude, longitude],
                radius=size*100,
                popup=f'{ville} ({size}): {dict_cyclo[ville]}',
                color=color,
                fill=True,
            ).add_to(kol)
    return kol
    
def stat_sorties_club(path_sorties_club, ctg_path, ylim=None, file_label=None,year = None):

    # Standard library imports
    import datetime
    import os
    from pathlib import Path
    from collections import Counter
    from tkinter import messagebox
    
    # Third party imports
    import matplotlib.pyplot as plt 
    import pandas as pd
    
    # Internal imports
    from CTG_Utils.CTG_Func.CTG_effectif import read_effectif
    from CTG_Utils.CTG_Func.CTG_effectif import correction_effectif
    from CTG_Utils.CTG_Func.CTG_effectif import read_effectif_corrected
    from CTG_Utils.CTG_Func.CTG_effectif import count_participation
    from CTG_Utils.CTG_Func.CTG_effectif import parse_date
    
    def addlabels(x,y):
        import os
        for i in range(len(x)):
            d = x[i]
            color = 'g'
            if os.path.split(path_sorties_club)[-1] == "SEJOUR" :
                v = info_rando.query('date==@d and type=="sejour"')['name_activite'].tolist()
            else:
                v = info_rando.query('date==@d and type!="sejour"')['name_activite'].tolist()
                t = info_rando.query('date==@d and type!="sejour"')['type'].tolist()
                if len(t) != 0:
                    color = "k" if t[0] =='randonnee' else "g"
                
            name = v[0] if len(v) != 0 else ""
        
            plt.text(i-0.2,y[i]+1,
                     name,
                     size=10,
                     rotation=90,
                     color=color #info_rando['color']
                     )
            
    if file_label is not None and os.path.isfile(file_label):
        flag_labels = True
        info_rando = pd.read_excel(file_label)
    else:
        flag_labels = False
        print(file_label)
    
    no_match,df_total,_ = count_participation(path_sorties_club,ctg_path,year,info_rando)
    if no_match is None:
        messagebox.showinfo('WARNING',"Aucun participant n'a participé à ce type de sortie" )
    else:
        text_message = ''
        for tup in no_match:
              text_message += f'Le nom {tup[1]}, {tup[2]} est inconnu dans le fichier : "{os.path.split(tup[0])[-1]}"'
              text_message += '\n'
           
        if len(text_message) : messagebox.showinfo('WARNING',text_message )
    
    if year is None:
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")
        
    list_non_licencie, dic_correction_licence, dic_part_club = correction_effectif(year,ctg_path)
    df_effectif = read_effectif_corrected(dic_correction_licence,
                                          list_non_licencie,
                                          dic_part_club,
                                          ctg_path,
                                          year)
    
    dic_sexe = dict(zip(df_effectif['N° Licencié'], df_effectif['Sexe']))
    dic_sexe[None] = 'irrelevant'
    dic_vae =dict(zip(df_effectif['N° Licencié'],df_effectif['Pratique VAE']))

    df_total['sexe'] = df_total['N° Licencié'].map(dic_sexe)
    
    df_total = df_total[df_total['sejour']!='aucun' ]
    df_total['sejour'] = df_total['sejour'].apply(lambda s:parse_date(s,str(year)).strftime('%y-%m-%d'))
    df_total['VAE'] = df_total['N° Licencié'].map(dic_vae)
    df_total['VAE'].fillna('Non',inplace=True)
    dic_sexe = dict(M="Homme",F="Femme")
    dic_vae = dict(Oui="VAE",Non="Musculaire")
    df_total = df_total.replace({"sexe": dic_sexe})
    df_total = df_total.replace({"VAE": dic_vae})
    if df_total['Nom'].isna().all():
        return None
    dg = df_total.groupby(['sexe','VAE'])['sejour'].value_counts().unstack().T
   
    try:
        dg['irrelevant'] = dg['irrelevant'] - 1
    except KeyError as error:
        pass
        
    fig, ax = plt.subplots(figsize=(15, 5))
    
    
    dg[['Femme','Homme']].plot(kind='bar',
                       ax=ax,
                       width=0.5,
                       stacked=True,
                       color = {('Femme', 'Musculaire'): '#1f77b4',
                                ('Femme', 'VAE'): '#ff7f0e',
                                ('Homme', 'Musculaire'): '#2ca02c',
                                ('Homme', 'VAE'): '#d62728',} )
    
    if flag_labels : addlabels(dg.index,dg.sum(axis=1).astype(int).tolist())
    
    plt.xlabel('')
    plt.tick_params(axis='x', rotation=90,labelsize=15)
    plt.ylabel('Nombre de licenciers',size=15)
    plt.xlabel('')
    plt.tick_params(axis='x', rotation=90,labelsize=15)
    plt.tick_params(axis='y',labelsize=15)
    type_sortie = os.path.split(path_sorties_club)[-1] + ' ' + str(year)
    plt.title(type_sortie,fontsize=15,pad=50)
    
    if ylim is not None:
        plt.ylim(ylim)
    else:
        ylim = (0,1.5*max(Counter(df_total['sejour']).values()))
        plt.ylim(ylim)

    
    plt.legend(bbox_to_anchor =(0.75, 1.15), ncol = 2)
    plt.tight_layout()
    plt.show()
    fig_file = os.path.split(path_sorties_club)[-1].replace(' ','_')+'.png'
    plt.savefig(ctg_path / Path(str(year)) / Path('STATISTIQUES') / Path(fig_file),bbox_inches='tight')
    
    return df_total
    
def _distance(ϕ1, λ1,ϕ2, λ2):
    from math import asin, cos, radians, sin, sqrt
    ϕ1, λ1 = radians(ϕ1), radians(λ1)
    ϕ2, λ2 = radians(ϕ2), radians(λ2)
    rad = 6371
    dist = 2 * rad * asin(
                            sqrt(
                                sin((ϕ2 - ϕ1) / 2) ** 2
                                + cos(ϕ1) * cos(ϕ2) * sin((λ2 - λ1) / 2) ** 2
                            ))
    return dist