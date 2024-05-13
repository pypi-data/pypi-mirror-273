
class EffectifCtg():
    
    
    def __init__(self,year,ctg_path):
        
        # Standard library imports
        from pathlib import Path

        # Third party imports
        import pandas as pd

        # Internal imports
        from CTG_Utils.CTG_Func.CTG_plot import built_lat_long

        self.year = year
        self.ctg_path = ctg_path
        df = pd.read_excel(self.ctg_path / Path(str(year))/ Path('DATA')/Path(str(year)+'.xlsx'))
        
        year_1 = int(year)-1
        df_1 = pd.read_excel(self.ctg_path / Path(str(year_1))/ Path('DATA')/Path(str(year_1)+'.xlsx'))

        df['Date de naissance'] = pd.to_datetime(df['Date de naissance'], format="%d/%m/%Y")
        df_1['Date de naissance'] = pd.to_datetime(df_1['Date de naissance'], format="%d/%m/%Y")

        df['Age']  = df['Date de naissance'].apply(lambda x : (pd.Timestamp(int(year), 9, 30)-x).days/365)
        df_1['Age']  = df_1['Date de naissance'].apply(lambda x : (pd.Timestamp(int(year), 9, 30)-x).days/365)

        df,dh = built_lat_long(df)

        df['distance'] = df.apply(lambda row: self.distance_(row, dh),axis=1)
        
        self.effectif = df
        self.effectif_1 = df_1
        
    @staticmethod
    def distance_(row,dh):
    
        # Standard library imports
        from math import asin, cos, radians, sin, sqrt
        
        # Third party imports        
        import numpy as np
        
        phi1, lon1 = dh.query("Ville=='GRENOBLE'")[['long','lat']].values.flatten()
        phi1, lon1 = radians(phi1), radians(lon1)
        phi2, lon2 = radians(row['long']), radians(row['lat'])
        rad = 6371
        dist = 2 * rad * asin(sqrt(sin((phi2 - phi1) / 2) ** 2
                                 + cos(phi1) * cos(phi2) * sin((lon2 - lon1) / 2) ** 2))
        return np.round(dist,1)
    
    def stat(self):
    
        # Standard library imports
        from tkinter import messagebox
        
        # Internal imports
        from CTG_Utils.CTG_Func.CTG_utility import read_correction_effectifs

        da = self.effectif.groupby('Sexe')['Age'].agg(['count','median','max','min'])
        res = self.effectif['Age'].agg(['count','median','max','min']).tolist()
        stat = []
        nbr_membres = round(res[0],0)
        stat.append(f"Nombre d'adhérents : {nbr_membres}")
        nbr_femmes = da.loc['F','count']
        stat.append(f"Nombre de femmes : {nbr_femmes} ({round(100*nbr_femmes/nbr_membres,1)} %)")
        nbr_hommes = da.loc['M','count']
        stat.append(f"Nombre d'hommes : {nbr_hommes} ({round(100*nbr_hommes/nbr_membres,1)} %)")
        stat.append(' ')
        stat.append(f"Age médian total : {round(res[1],1)} ans")
        stat.append(f"Age maximum : {round(res[2],1)} ans")
        stat.append(f"Age minimum : {round(res[3],1)} ans")
        stat.append(f"Age médian des femmes : {round(da.loc['F','median'],1)} ans")
        stat.append(f"Age médian des hommes : {round(da.loc['M','median'],1)} ans")
        stat.append(f"Age maximum des femmes : {round(da.loc['F','max'],1)} ans")
        stat.append(f"Age maximum des hommes : {round(da.loc['M','max'],1)} ans")
        stat.append(f"Age minimum des femmes : {round(da.loc['F','min'],1)} ans")
        stat.append(f"Age minimum des hommes : {round(da.loc['M','min'],1)} ans")
        stat.append(' ')
        
        correction = read_correction_effectifs(self.year,self.ctg_path)
        if correction["dic_part_club"] is not None:
            stat.append(f'Nombre de membres sympatisant : {len(correction["dic_part_club"])} ')
        else:
            stat.append(f'Nombre de membres sympatisant : inconnu ')
        stat.append(' ')
        
        nouveaux_licenciés = set(self.effectif["N° Licencié"])-set(self.effectif_1["N° Licencié"])
        licencies_non_renouvelles = set(self.effectif_1["N° Licencié"]) - set(self.effectif["N° Licencié"])
        moy_age_entrants = self.effectif[self.effectif['N° Licencié'].isin(nouveaux_licenciés)]['Age'].mean() + 1
        moy_age_sortants = self.effectif_1[self.effectif_1['N° Licencié'].isin(licencies_non_renouvelles)]['Age'].mean()
        stat.append(f"{len(nouveaux_licenciés)} nouveaux licenciés de moyenne d'âge de {round(moy_age_entrants,1)} ans")
        stat.append(f"{len(licencies_non_renouvelles)} licences non renouvellées de moyenne d'âge de {round(moy_age_sortants,1)} ans")
        stat.append(' ')
        
        if 'Pratique VAE' in self.effectif.columns:
            da = self.effectif.groupby(['Sexe','Pratique VAE'])['Nom'].agg(['count'])
            nbr_vae_femme = nbr_femmes-da.loc['F','Non']['count']
            nbr_vae_homme = nbr_hommes-da.loc['M','Non']['count']
            nbr_vae_tot = nbr_vae_femme + nbr_vae_homme
            stat.append(f"Nombre de membres équippées de VAE : {nbr_vae_tot} ({round(100*nbr_vae_tot/nbr_membres,1)} %)")
            stat.append(f"Nombre de femmes équippées de VAE : {nbr_vae_femme} ({round(100*nbr_vae_femme/nbr_femmes,1)} %)")
            stat.append(f"Nombre d'hommes équippés de VAE: {nbr_vae_homme} ({round(100*nbr_vae_homme/nbr_hommes)} %)")
        
        stat.append(' ')    
        da = self.effectif.groupby(['Discipline'])['Nom'].agg('count')
        for pratique in da.index:
            stat.append(f'{pratique} : {da[pratique]}')
        stat.append(' ')
        
        self.effectif = self.effectif.rename(columns={'\n\t\t\t\tAbonnements':'Abonnements'})
        nbr_abonnements = len(self.effectif.query('Abonnements == "Oui"'))
        stat.append(f"Nombre d'abonnés à la revue FFCT : {nbr_abonnements} ({round(100*nbr_abonnements/nbr_membres)} %)")
        
        stat ='\n'.join(stat)
        messagebox.showinfo(f'Statistique {self.year}',stat)
        
    def plot_histo(self):
    
        # Third party imports
        import matplotlib.pyplot as plt
        import pandas as pd
        
        fig, ax = plt.subplots(figsize=(10,10))
        self.effectif['age group'] = pd.cut(self.effectif.Age, bins=range(0, 95, 5), right=False)
        result_hist = self.effectif.groupby('Sexe')['age group'].value_counts().unstack().T.plot.bar(width=1, stacked=False,ax=ax)
        
        plt.tick_params(axis='x', labelsize=20)
        plt.tick_params(axis='y', labelsize=20)
        plt.title(self.year,fontsize=20)
        plt.legend()
        plt.tight_layout()
        plt.show()
        