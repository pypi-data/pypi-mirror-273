__all__ = ['correction_effectif',
           'count_participation',
           'inscrit_sejour',
           'parse_date',
           'read_effectif',
           'read_effectif_corrected',
           'evolution_effectif',
           'builds_excel_presence_au_club',
           'statistique_vae',
           'anciennete_au_club',]
                      

def read_effectif_corrected(dic_correction_licence, list_non_licencie, part_club, ctg_path, year=None):
    
    '''Lecture du fichier effectif et correction
    '''
    # Standard library imports
    from pathlib import Path
    import datetime
   
    # 3rd party imports
    import numpy as np
    import pandas as pd
    
    if year is not None:
        file_effectif = str(year) + '.xlsx'
    else:
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")
        file_effectif = year + '.xlsx'
    df_effectif = pd.read_excel(ctg_path / Path(str(year))/Path('DATA')/ Path(file_effectif))
    df_effectif = df_effectif[['N° Licencié', 'Nom','Prénom','Sexe','Pratique VAE']]
    
        
    for num_licence in dic_correction_licence.keys():
        idx = df_effectif[df_effectif["N° Licencié"]==num_licence].index
        df_effectif.loc[idx,'Prénom'] = dic_correction_licence[num_licence]['Prénom']
        df_effectif.loc[idx,'Nom'] = dic_correction_licence[num_licence]['Nom']
        
    prenom, nom, sexe = zip(*part_club)
    part_club = {'N° Licencié':list(range(len(part_club))), 'Prénom':prenom,'Nom':nom,'Sexe':sexe}
    df_part_club = pd.DataFrame.from_dict(part_club)
    df_effectif = pd.concat([df_effectif, df_part_club], ignore_index=True, axis=0)
    
    if list_non_licencie:
        prenom, nom, sexe = zip(*list_non_licencie)
        dict_non_licencie = {'N° Licencié':np.array(range(len(nom)))+10, 'Prénom':prenom,'Nom':nom,'Sexe':sexe}
    
        df_non_licencie = pd.DataFrame.from_dict(dict_non_licencie)
        df_effectif = pd.concat([df_effectif, df_non_licencie], ignore_index=True, axis=0)
    
    df_effectif['Prénom1'] = df_effectif['Prénom'].str[0]
    df_effectif['Prénom'] = df_effectif['Prénom'].str.replace(' ','-')
    
    return df_effectif

def inscrit_sejour(file,no_match,df_effectif):

    # Standard library import
    import functools
    import os
    import unicodedata
    
    # 3rd party import
    import pandas as pd


    nfc = functools.partial(unicodedata.normalize,'NFD')
    convert_to_ascii = lambda text : nfc(text). \
                                     encode('ascii', 'ignore'). \
                                     decode('utf-8').\
                                     strip()

    df = pd.read_csv(file) 
    sejour = os.path.splitext(os.path.basename(file))[0]
    
    if len(df) != 0:
        dg = df['Unnamed: 0'].str.upper()
        dg = dg.dropna()
        dg = dg.str.replace(' \t?','',regex=False)
        dg = dg.str.replace('JO ','JOSEPH ')
        dg = dg.str.replace('HERVÉ.P','PEREZ HERVE',regex=False)
        dg = dg.str.replace('.',' ',regex=False)
        dg = dg.str.replace(' - ','-',regex=False)
        dg = dg.apply(convert_to_ascii)
        dg = dg.drop_duplicates()
        dg = dg.str.split('\s{1,10}')

        dg = dg.apply(lambda row : row+[None] if len(row)==2 else row)

        split_dg = pd.DataFrame(dg.tolist(), columns=['name1', 'name2', 'name3'])

        dic = {}
        for idx,row in split_dg.iterrows():
            if (row.name3 is None) and ( row.name2 is not None):
                if len(row.name1)==1:
                    dr = df_effectif.query('Prénom1==@row.name1[0] and Nom==@row.name2')
                    if len(dr):
                        dic[idx] =dr.iloc[0].tolist()[:-1]+[sejour]
                    else:
                        print(f'no match,{row.name2},{row.name1} dans {sejour}')
                        no_match.append((file,row.name2,row.name1))
                elif len(row.name2)==1:
                    dr = df_effectif.query('Prénom1==@row.name2 and Nom==@row.name1')
                    if len(dr):
                         dic[idx] =dr.iloc[0].tolist()[:-1]+[sejour]
                    else:
                        print(f'no match,{row.name2},{row.name1} dans {sejour}')
                        no_match.append((file,row.name2,row.name1))
                else:
                    if len((dr:=df_effectif.query('Prénom==@row.name2 and Nom==@row.name1'))):
                         dic[idx] =dr.iloc[0].tolist()[:-1]+[sejour]
                    elif len((dr:=df_effectif.query('Prénom==@row.name1 and Nom==@row.name2'))):
                         dic[idx] =dr.iloc[0].tolist()[:-1]+[sejour]
                    else:
                        print(f'{sejour} : no match, prénom/prénom:{row.name2}, nom/prénom: {row.name1}')
                        no_match.append((file,row.name2,row.name1))
            else:
                print(f'WARNING: incorrect name {row.name1}, {row.name2}, {row.name3} in sejour {sejour}')

        dg = pd.DataFrame.from_dict(dic).T 
        if len(dg) !=0:
            dg.columns = ['N° Licencié','Nom','Prénom','Sexe','Pratique VAE','sejour',]
        else:
            dg = pd.DataFrame([[None,None,None,None,sejour,]], columns=['N° Licencié','Nom','Prénom','Sexe','sejour',])
    else:
        dg = pd.DataFrame([[None,None,None,None,sejour,]], columns=['N° Licencié','Nom','Prénom','Sexe','sejour',])
    
    return dg

def correction_effectif(year,ctg_path):
    
    # Standard library import
    from pathlib import Path
    
    #3rd party import
    import yaml
    
    #path_cor_yaml = Path(__file__).parent / Path('CTG_RefFiles/CTG_correction.yaml')
    path_cor_yaml = ctg_path / Path(str(year)) / Path('DATA') / Path('CTG_correction.yaml')
    
    with open(path_cor_yaml, "r",encoding='utf8') as stream:
        data_list_dict = yaml.safe_load(stream)
    
    list_non_licencie  = []   
    if data_list_dict['list_non_licencie']:
        list_non_licencie = [(x.split(',')[0].strip(),x.split(',')[1].strip(),x.split(',')[2].strip())
                             for x in data_list_dict['list_non_licencie']]
    dic_part_club = [(x.split(',')[0].strip(),x.split(',')[1].strip(),x.split(',')[2].strip()) 
                         for x in data_list_dict['dic_part_club']]
    dic_correction_licence = data_list_dict['dic_correction_licence']
    dic_correction_licence = {list(x.keys())[0] : list(x.values())[0] for x in dic_correction_licence}
    
    return list_non_licencie, dic_correction_licence, dic_part_club

    
def count_participation(path,ctg_path,year,info_rando):
    
    import os
    import re
    from pathlib import Path

    import pandas as pd
    
    flag_sejour = False
    if os.path.split(path)[-1] == 'SEJOUR' : 
        flag_sejour = True

    type_sortie_default = os.path.basename(path)
    type_sortie_default = type_sortie_default.split('.', 1)[0]
    list_non_licencie, dic_correction_licence, dic_part_club = correction_effectif(year,ctg_path)

    df_effectif = read_effectif_corrected(dic_correction_licence, list_non_licencie, dic_part_club,ctg_path,year)

    no_match = []
    df_list = [] 
    sejours = [x for x in os.listdir( path / Path('CSV')) if x.endswith('.csv')]
    
    
    nbr_moyen_participants = 0
    counter = 1
    for sejour in sejours:
        dg = inscrit_sejour( path / Path('CSV') /Path(sejour),no_match,df_effectif)
        
        if re.findall(r'^\d{4}[-_]',sejour):
            date = sejour[2:10].replace('_','-')
        else:
            date = str(year)[2:4] + '-' +sejour[0:5].replace('_','-')
            
        dg['nbr_jours'] = 0    
        if date in info_rando['date'].tolist():
            dh = info_rando.query('type=="randonnee" and date==@date')
            if not flag_sejour and len(dh) != 0 : 
                dg['Type'] = "RANDONNEE"
            else:
                dg['Type'] = type_sortie_default
            
            dg['nbr_jours'] = 1
            dh = info_rando.query('type=="sejour" and date==@date')
            if flag_sejour and len(dh) != 0:
                dg['nbr_jours'] = dh['nbr_jours'].tolist()[0]    
            
        if dg.reset_index().loc[0,'Nom'] is not None:
            nbr_inscrits = len(dg)
            if nbr_inscrits != 0:
                nbr_moyen_participants = nbr_moyen_participants + (nbr_inscrits - nbr_moyen_participants)/counter
                counter += 1
                print(f"{os.path.split(path)[-1]} :{sejour}, Nombre d'inscrits : {nbr_inscrits}")
        df_list.append(dg)
        file_store = os.path.splitext(sejour)[0]+'.xlsx'
        dg.to_excel(path / Path('EXCEL') / Path(file_store))
        
    print(f"Nombre d'évènenements : {counter-1}. Nombre moyen de participants : {nbr_moyen_participants}")
    nbr_evenement = counter-1 
    if counter-1 > 0 :  #
        df_total = pd.concat(df_list,ignore_index=True)
    else:
        return (None, None, None)


    liste_licence = df_effectif['N° Licencié']
    liste_licence_sejour = df_total['N° Licencié']
    index = list(set(liste_licence)-set(liste_licence_sejour))

    df_non_inscrits = df_effectif.copy()
    df_non_inscrits = df_non_inscrits[df_non_inscrits['N° Licencié'].isin(index)]
    df_non_inscrits['sejour'] = 'aucun'
    df_total = pd.concat([df_total,df_non_inscrits],ignore_index=True)
    

    return(no_match,df_total,index)

def parse_date(s,year):
    
    import re
    from datetime import datetime 

    convert_to_date = lambda s: datetime.strptime(s,"%Y_%m_%d")
    s = re.sub(r"-","_",s)
    
    try:
        pattern = re.compile(r"(?P<year>\b\d{4}_)(?P<month>\d{1,2}_)(?P<day>\d{1,2})")
        match = pattern.search(s)
        date = convert_to_date(match.group("year")+match.group("month")+match.group("day"))
    except:
        pattern = re.compile(r"(?P<month>\d{1,2}_)(?P<day>\d{1,2})")
        match = pattern.search(s)
        date = convert_to_date(str(year)+'_'+match.group("month")+match.group("day"))
    
    return date

    
def read_effectif(ctg_path,year):
    
    from pathlib import Path
    
    import numpy as np
    import pandas as pd
    
    from CTG_Utils.CTG_Func.CTG_plot import built_lat_long

        
    def distance_(row):
        from math import asin, cos, radians, sin, sqrt
        phi1, lon1 = dh.query("Ville=='GRENOBLE'")[['long','lat']].values.flatten()
        phi1, lon1 = radians(phi1), radians(lon1)
        phi2, lon2 = radians(row['long']), radians(row['lat'])
        rad = 6371
        dist = 2 * rad * asin(
                                sqrt(
                                    sin((phi2 - phi1) / 2) ** 2
                                    + cos(phi1) * cos(phi2) * sin((lon2 - lon1) / 2) ** 2
                                ))
        return np.round(dist,1)

    
    df = pd.read_excel(ctg_path / Path(str(year))/ Path('DATA')/Path(str(year)+'.xlsx'))
        
    df['Date de naissance'] = pd.to_datetime(df['Date de naissance'], format="%d/%m/%Y")
    
    df['Age']  = df['Date de naissance'].apply(lambda x : (pd.Timestamp(year, 9, 30)-x).days/365)

    df,dh = built_lat_long(df)

    df['distance'] = df.apply(distance_,axis=1)
    
    return df
    
def evolution_effectif(ctg_path):

    # Evolution des effectifs hommes et femme de 2016 à 2022
    import os
    import re
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    def addlabels(x,y,z=None):
        for i in range(len(x)):
            if z is None:
                plt.text(x[i]-0.4,y[i]+5,y[i],size=10)
            else:
                plt.text(x[i]-0.4,y[i]+5,z[i],size=10,rotation='vertical')
    
    
    def _evolution_effectif(years):
        nbr_hommes = []
        nbr_femmes = []
        nbr_total = []
        ratio_femmes = []
        for year in years:
            if year == 2006:
                nbr_femmes.append(41)
                nbr_hommes.append(100)
                nbr_total.append(141)
                ratio_femmes.append(str(29)+'%')
            else:  
                df_effectif = read_effectif(ctg_path,year)
                nh = len(df_effectif.query('Sexe =="M"'))
                nbr_hommes.append(nh)
                nf = len(df_effectif.query('Sexe =="F"'))
                nbr_femmes.append(nf)
                nbr_total.append(nh + nf)
                ratio_femmes.append(str(int(100*nf/(nh+nf)))+'%')
        return nbr_hommes, nbr_femmes,nbr_total,ratio_femmes
    
    years = [2006] + [int(x) for x in os.listdir(ctg_path) if re.findall('^\d{4}$',x)]
    nbr_hommes, nbr_femmes,nbr_total,ratio_femmes = _evolution_effectif(years)
    
    title='Evolution du nombre de licenciés CTG'
    
    ax = plt.axes() 
    plt.bar(years, nbr_femmes,label= 'Femme')
    addlabels(years, nbr_femmes)
    plt.bar(years, nbr_hommes,bottom=nbr_femmes,label= 'Hommes')
    plt.legend()
    addlabels(years, nbr_total)
    ax.set_xticks(years)
    plt.xticks(rotation=90)    
    plt.tight_layout()
    plt.show()
    
def evolution_age_median(ctg_path):

    from pathlib import Path
    from collections import Counter
    import os
    import re
    
    import matplotlib.pyplot as plt
    import numpy as np 
    import pandas as pd
    
    
    def addlabels(x,y,z=None):
        for i in range(len(x)):
            if z is None:
                plt.text(x[i]-0.3,y[i]+0.1,y[i],size=10)
            else:
                plt.text(x[i]-0.2,y[i]+0.1,z[i],size=10,rotation='vertical')
        
    xt = range(55,90)
    years = [int(x) for x in os.listdir(ctg_path) if re.findall('^\d{4}$',x)]
    nbr_femmes = []
    ratio_femmes = []
    nbr_total = []
    age_mean = [] 
    for year in years:
        df_effectif = pd.read_excel(ctg_path / Path(str(year)) / Path('DATA') / Path(str(year)+'.xlsx'))
        df_effectif['Date de naissance'] = pd.to_datetime(df_effectif['Date de naissance'], format="%d/%m/%Y")
        df_effectif['Age']  = df_effectif['Date de naissance'].apply(lambda x : (pd.Timestamp(year, 9, 30)-x).days/365)#.astype(int)
        #print(year,df_effectif['Age'].median())
        age_mean.append(df_effectif['Age'].median())
        
    fig, ax = plt.subplots()
    plt.bar(years,age_mean)
    plt.ylabel('Age moyen')
    plt.ylim(50,71)
    addlabels(years,[round(x,1) for x in age_mean])
    linear_model = np.polyfit(years,age_mean,1)
    linear_model_fn = np.poly1d(linear_model)
    plt.xticks(years,years)
    plt.tick_params(axis='x', labelsize=20,rotation=90)
    plt.tick_params(axis='y', labelsize=20)
    plt.ylabel('Age median',size=20)
    x_s =[years[0]-1] + years + [years[-1]+1]
    plt.plot(x_s,linear_model_fn(x_s),"--g")
    plt.title(f'Pente vieillissement : {round(linear_model[0]*12,1)} mois par ans')
    plt.tight_layout()
    plt.show()
    
def builds_excel_presence_au_club(ctg_path):
    import os
    import re
    from pathlib import Path
    
    import pandas as pd
    
    import CTG_Utils as ctg
    
    list_date = [int(x) for x in os.listdir(ctg_path) if re.findall('^\d{4}$',x)]
    list_df = []
    
    for date in list_date:
        df = pd.read_excel(ctg_path /Path(str(date)) / Path('DATA') / Path(str(date)+'.xlsx'))
        df['date'] = date
        list_df.append(df[['N° Licencié','Nom','Prénom','date']])
        
    df = pd.concat(list_df) #.to_excel(file / Path('effectif_total.xlsx'),index=False)
    
    dic = {}
    list_num_licence = []
    list_nom = []
    list_prenom = []
    list_date_ = []
    for licence in df.groupby('N° Licencié'):
        list_c = [x if x in licence[1]['date'].to_list() else None for x in list_date]
        #if len(list_c) - list_c.count(None) == 1: singleton
        list_num_licence.append(licence[0])
        list_nom.append(licence[1]['Nom'].unique()[0])
        list_prenom.append(licence[1]['Prénom'].unique()[0])
        list_date_.append(list_c)
    
        
    dic['N° Licencié'] = list_num_licence
    dic['Nom'] = list_nom
    dic['Prénom'] = list_prenom
    dic['date'] = list_date_
    
    df = pd.DataFrame.from_dict(dic)
    split_df = pd.DataFrame(df['date'].tolist(), columns=list_date)
    
    df = pd.concat([df, split_df], axis=1)
    df = df.drop('date',axis=1)
    out_path = ctg_path / Path(str(list_date[-1])) / Path('DATA') / Path('effectif_history.xlsx')
    df.to_excel(out_path)
    return out_path
    
def statistique_vae(ctg_path):

    from datetime import datetime
    from pathlib import Path
    
    import matplotlib.pyplot as plt
    import pandas as pd
    
    # Internal import
    import CTG_Utils as ctg
    # function to add value labels
    def addlabels(x,y):
        for i in range(1,len(x)):
            plt.text(x[i]-0.2,y[i]+0.5,y[i],size=10)
    
    current_year = datetime.now().year
    
    last_year = 2018
    years =[]
    nb_vae_m = []
    nb_vae_f = []
    nb_vae_tot = []
    for year in range(last_year,current_year+1):
        df_N1 = pd.read_excel(ctg_path / Path(str(year)) / Path('DATA') /Path(str(year)+'.xlsx'))
        years.append(year)
        nb_vae_m.append(sum((df_N1['Pratique VAE'] == 'Oui') & (df_N1['Sexe'] == 'M')))
        nb_vae_f.append(sum((df_N1['Pratique VAE'] == 'Oui') & (df_N1['Sexe'] == 'F')))
        nb_vae_tot.append(sum((df_N1['Pratique VAE'] == 'Oui') & (df_N1['Sexe'] == 'F')) +
                          sum((df_N1['Pratique VAE'] == 'Oui') & (df_N1['Sexe'] == 'M')))
    plt.bar(years, nb_vae_m,label= 'Homme')
    plt.bar(years, nb_vae_f,bottom=nb_vae_m,label= 'Femme')
    plt.tick_params(axis='x', labelsize=15)
    plt.tick_params(axis='y', labelsize=15)
    plt.ylabel('nombre de VAEs',size=15)
    plt.xticks(rotation=90)
    plt.legend()
    plt.ylabel('nombre de VAE')
    addlabels(years, nb_vae_m)
    addlabels(years, [x+y for x,y in zip(nb_vae_m,nb_vae_f)])
    plt.tight_layout()
    plt.show()

def anciennete_au_club(ctg_path):

    import datetime
    from pathlib import Path
    
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    
    import CTG_Utils as ctg
    
    def addlabels(x,y,offset):
        for i in range(len(x)):
            if y[i] != 0:
                plt.text(x[i]-0.2,y[i]+offset,round(y[i],1),size=15)
                
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    current_year = int(date.strftime("%Y"))
    
    in_path = ctg_path / Path(str(current_year)) / Path('DATA') / Path('effectif_history.xlsx')
    df = pd.read_excel(in_path)
    eff = []
    
    years = list(range(2012,current_year+1))
    for year in years:
        dg = df.dropna(subset=[year,current_year])
        eff.append(len(dg))
    eff = [eff[0]] + list(np.diff(eff))
    
    # creating the bar plot
    fig = plt.figure(figsize = (10, 5))
    plt.bar(years, eff, color ='maroon', 
            width = 0.4)
     
    plt.xlabel("")
    plt.ylabel("# adhérents")
    plt.title("Ancienneté au CTG")
    addlabels(list(range(2012,2025)), eff,0)
    plt.tight_layout()
    plt.show()
