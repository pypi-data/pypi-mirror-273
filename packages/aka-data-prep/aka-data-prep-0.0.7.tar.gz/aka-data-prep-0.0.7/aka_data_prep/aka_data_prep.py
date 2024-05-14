
from sklearn.model_selection import train_test_split  
from sklearn import preprocessing   
import pandas as pd
import numpy as np 

 
import plotly.express as px
import plotly.graph_objects as go

import math
from plotly.subplots import make_subplots
import shap


class aka_encoding:
    def __init__(self,df) -> None:

        str_col = []
        for val in df.columns:
            for _,elm in df[val].dropna().items():
                if isinstance(elm,str):
                    str_col.append(val)
                    break

        mapping = {}
        swapMapping = {}  

        if str_col is not None:
            for val in str_col:
                mapping[val] = {}
                uniq = df[val].dropna().unique()
                for i in range(len(uniq)):
                    key = uniq[i]
                    mapping[val][key] = i
                if val == df.columns[-1]:
                    for i in range(len(uniq)):
                        key = uniq[i]
                        swapMapping[i] = key
        
        self.mapping=mapping
        self.swapMapping=swapMapping
        self.df = df
 
    def label_encoding(self):
        dfTemp = self.df.copy()
        
        if self.mapping.keys() is not None:
            for val in self.mapping.keys():
                dfTemp[val] = self.df[val].map(self.mapping[val]) 
        return dfTemp


    def label_encoding_inverse(self,y_pred):
        df = pd.DataFrame(y_pred)
        if len(self.swapMapping) > 0:
            return  df[df.columns[0]].map(self.swapMapping)
        else:
            return df[df.columns[0]]


    def Replace_item_into_str_df(self,df,col=-1):
      if col <= df.shape[1]:
        clabel = df[df.columns[col]].unique()
        Label = ['_'+str(item) for item in df[df.columns[col]].unique()]
        df[df.columns[-1]] = df[df.columns[col]].replace(clabel,Label)



class aka_df_prepare:
    def __init__(self) -> None:
        pass 
 
    def df_get(self,cvs_path):
        encodings_to_try = ['utf-8', 'latin-1', 'ISO-8859-1'] 
        for encoding in encodings_to_try:
            try:
                df = pd.read_csv(cvs_path, encoding=encoding)
                break  
            except UnicodeDecodeError:
                continue   
        return df

    def swap_features(self, df, feat_a, feat_b=None):
        if feat_b is None: 
            feat_b = df.shape[1] - 1

        if feat_a != feat_b and 0 <= feat_a < df.shape[1] and 0 <= feat_b < df.shape[1]:
            df_t = df[df.columns[[feat_b, feat_a]]]
            df_c = df.drop(df.columns[[feat_b, feat_a]], axis=1)
            return pd.concat([df_c, df_t], axis=1)
        else:
            print("Invalid feature indices or feat_a is equal to feat_b.")
            return df

    def drop_feature(self, df, feat):
        if len(feat) > 0:
            feats = [fe for fe in feat if fe <= len(df.columns)]
            return df.drop(df.columns[feats], axis=1)
        else:
            return df


    def missing_data_processing(self, df, data_nan_drop=True):
        if data_nan_drop:
            df.dropna(inplace=True)
        else:
            for column in df.columns:
                if df[column].dtype == 'object':  # Check if column is categorical
                    mode = df[column].mode()[0]
                    df[column].fillna(mode, inplace=True)
                else:  # Numerical columns change into mean 
                    mean = df[column].mean()
                    df[column].fillna(mean, inplace=True)


class aka_filter:
    def __init__(self) -> None:
        pass


    def filter_std(self,df,cols,std_number=[-3,3]):
        if std_number:
            lower_limit = df.mean() + std_number[0]*df.std()
            upper_limit = df.mean() + std_number[1]*df.std() 
            for i in cols:
                df_i = df[df.columns[i]] 
                ind = df_i[~ ((df_i>lower_limit[i]) & (df_i<upper_limit[i]))].index 
                df = df.drop(ind) 
        return df


    def filter_z_score(self,df,cols,std_inter=[-3,3]):

        for i in cols:
            df_i = df[df.columns[i]] 
            df_z=(df_i - df_i.mean())/df_i.std()
            ind = df_i[~ ((df_z>std_inter[0]) & (df_z<std_inter[1]))].index 
            df = df.drop(ind)
        return df
    

    def filter_IQR(self,df,cols,IQR_number=[-1.5,1.5]):

        for i in cols:
            df_i = df[df.columns[i]]
            q25,q75 = np.percentile(a = df_i,q=[25,75])
            IQR = q75 - q25 
            lower_limit = q25 + IQR_number[0] * IQR
            upper_limit = q75 + IQR_number[1] * IQR 
            if 10**-10*round(10**10*np.abs(IQR)) > 0.0: 
                ind = df_i[~((df_i>lower_limit) & (df_i<upper_limit))].index
                df = df.drop(ind)
        return df
    
    def Columns_Correlated(self,df,percent_correlation):
        cm = df.corr()
        n = cm.shape[0]
        corr_tmp = [] 

        for i in range(n): 
            for j in range(i): 
                if abs(cm.iloc[i,j]) >= percent_correlation:
                    corr_tmp.append([i,j])
        return corr_tmp,cm
        
    def df_standardized(self,df):
        df_tmp = (df - df.mean()) / df.std()
        return df_tmp
   

class aka_plot :

    def __init__(self, tcouleur='plotly_dark', bcouleur='navy', fcouleur='white', fsize=20):
        self.tcouleur = tcouleur
        self.bcouleur = bcouleur
        self.fcouleur = fcouleur 
        self.fsize = fsize 
        self.update_layout_parameter = dict(        
                                        barmode='overlay',  
                                        font=dict(color=fcouleur,size=fsize),  
                                        title_x=0.5,
                                        title_y=0.9,
                                        template=self.tcouleur
                                        )
        self.update_axes = dict(  
                            title_font = {"size": 14},
                            title_standoff = 25
                            )
    
    def plot_history(self,df,feat):
        fig = px.histogram(data_frame= df,x=feat,opacity= 0.7)
        fig.update_layout(**self.update_layout_parameter) 
        return fig

    def plot_history_compare(self,df,df_,feat):
      df_0 = df[df.columns[feat]]
      df_0['filtered'] = df_[df.columns[feat]]
      fig = px.histogram(data_frame= df_0,opacity= 0.7)
      fig.update_xaxes(categoryorder='total descending')
      fig.update_layout(**self.update_layout_parameter) 
      return fig

    def plot_history_all(self,df):
        fig  = px.histogram(data_frame= df,opacity= .7).update_xaxes(categoryorder='total descending')
        fig.update_layout(**self.update_layout_parameter) 
        fig.update_xaxes(**self.update_axes)
        return fig


    def Plot_histogram_Features(self, df, columns_to_treat, fig_size_row=390, fig_size_col=490, subplot_col=3):
        if len(columns_to_treat) > 0:
            nrow = math.ceil(len(columns_to_treat) / subplot_col)
            
            # Create subplots
            fig = make_subplots(rows=nrow, cols=subplot_col, subplot_titles=df.columns[columns_to_treat])

            for i, col_index in enumerate(columns_to_treat):
                row_num = 1 + i // subplot_col
                col_num = 1 + i % subplot_col
 
                # Plot histogram for the current column
                hist_trace = go.Histogram(x=df[df.columns[col_index]] )

                hist_trace['showlegend'] = False
                fig.add_trace(hist_trace, row=row_num, col=col_num)
            # Update layout
            fig.update_layout(height=fig_size_row, width=fig_size_col)
            # fig.update_layout(height=fig_size_row, width=fig_size_col, title_text="Histograms of Features")
        
             
            fig.update_layout(**self.update_layout_parameter)
            # fig.update_xaxes(**update_axes)
            fig.update_layout(
                height=fig_size_row * nrow,
                width=fig_size_col * subplot_col           # Adjust the width as needed
            )
            return fig
        else:
            print("Empty list is provided.")


 
    def plot_pie(self,df, col):
        fig = px.pie(df[df.columns[col]], names=df[df.columns[col]].value_counts().index, values=df[df.columns[col]].value_counts().values, 
             title=f'Pie Chart of {df.columns[col]}') 
        fig.update_layout(**self.update_layout_parameter) 
        fig.update_xaxes(**self.update_axes)
        return fig

        
    def Plot_box_2_Features(self,df,df_filtered,corr_tmp=[],fig_size_row=390,fig_size_col=490,subplot_col=3):

        if len(corr_tmp) > 0:
            nrow = math.ceil(len(corr_tmp)/subplot_col)
            # Create subplots
            fig = make_subplots(
                rows=nrow, cols=subplot_col,
                subplot_titles=[df.columns[corr] for corr in corr_tmp])

            for i, corr in enumerate(corr_tmp, 1):
                                
                df_0 = pd.DataFrame()
                df_0['true'] = df[df.columns[corr]]
                df_0['filtered'] = df_filtered[df_filtered.columns[corr]]
                scatter_fig = px.box(data_frame= df_0).update_xaxes(categoryorder='total descending')
                ind_col = int((i+subplot_col-1)%subplot_col+1)
                ind_row = int(1+(i-ind_col)/subplot_col)

                for j,trace in enumerate(scatter_fig.data):
                    if j != 1 or j != 2 or j != 3:
                        fig.add_trace(scatter_fig.data[j], row=ind_row, col=ind_col)
                    # fig.update_xaxes(title_text=df.columns[corr[0]], row=ind_row, col=ind_col)
                    # fig.update_yaxes(title_text=df.columns[corr[1]], row=ind_row, col=ind_col)

            fig.update_layout(**self.update_layout_parameter)
            # fig.update_xaxes(**update_axes)
            fig.update_layout(
                height=fig_size_row * nrow,
                width=fig_size_col * subplot_col     
            )
            return fig
        else:
            print("Empty list is provided.")

 
    def plot_box(self,df,index_col_box = [0,-1]): 
        df_description = pd.DataFrame(df.describe())
        for i in range(2):
            if index_col_box[i]<0:
                index_col_box[i] += df_description.shape[1]+1 

        fig = px.box(df, y=df_description.T['max'].sort_values()[max(0,index_col_box[0]-1):min(index_col_box[1],df_description.shape[1])].index) 
        fig.update_layout(**self.update_layout_parameter) 
        fig.update_xaxes(**self.update_axes)
        return fig


    def plot_heatmap(self,df, lab=True):
      x_label = df.columns
      y_label = df.index
      if len(len(x_label)) > 0:
        cm = df.select_dtypes(exclude=['object']).values.round(3)

        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=x_label,
            y=y_label,
            colorscale='Viridis', 
            hoverongaps=False))

        if lab:
            for i in range(len(y_label)):
                for j in range(len(x_label)):
                    fig.add_annotation(
                        x=x_label[j],
                        y=y_label[i],
                        text=str(cm[i, j]),
                        showarrow=False,
                        font=dict(color='black', size=12),
                        xanchor='center',
                        yanchor='middle'
                    )
            fig.update_layout(**self.update_layout_parameter)
            fig.update_xaxes(**self.update_axes)
            fig.update_yaxes(**self.update_axes)
            return fig
      else:
            print("Empty list is provided.")
 
 
    def Plot_Correlation_Matrix(self, df, height=900,  width=1000):
        cm = df.corr()

        fig = px.imshow(cm, labels=dict(color="Correlation"), x=cm.columns, y=cm.index)

        fig.update_layout(**self.update_layout_parameter)
        fig.update_xaxes(**self.update_axes)
        fig.update_layout(
            height=height,
            width=width
        )
        return fig


    def Plot_scatter(self,df,corr_tmp, fig_size_row=390, fig_size_col=490, subplot_col=3):

        if len(corr_tmp) > 0:
            nrow = math.ceil(len(corr_tmp)/subplot_col)
            # Create subplots
            fig = make_subplots(
                rows=nrow, cols=subplot_col,
                subplot_titles=[""] * len(corr_tmp))

            for i, corr in enumerate(corr_tmp, 1):
                scatter_fig = px.scatter(df, x=df.columns[corr[0]], y=df.columns[corr[1]],
                                        trendline="ols")
                ind_col = int((i+subplot_col-1)%subplot_col+1)
                ind_row = int(1+(i-ind_col)/subplot_col)

                for j,trace in enumerate(scatter_fig.data):
                    if j != 1 or j != 2 or j != 3:
                        trace['showlegend'] = False
                        fig.add_trace(scatter_fig.data[j], row=ind_row, col=ind_col)
                    fig.update_xaxes(title_text=df.columns[corr[0]], row=ind_row, col=ind_col)
                    fig.update_yaxes(title_text=df.columns[corr[1]], row=ind_row, col=ind_col)

            fig.update_layout(**self.update_layout_parameter)
            # fig.update_xaxes(**update_axes)
            fig.update_layout(
                height=fig_size_row * nrow,
                width=fig_size_col * subplot_col           # Adjust the width as needed
            )
            return fig
        else:
            print("Empty list is provided.")


class aka_plot_shap: 
    def __init__(self, model, X_train, feat_names, tcouleur='plotly_dark', bcouleur='navy', fcouleur='white', fsize=20,height=700,
            width=1000,):
        self.tcouleur = tcouleur
        self.bcouleur = bcouleur
        self.fcouleur = fcouleur 
        self.fsize = fsize 
        self.height = height
        self.width = width
        self.update_layout_parameter = dict(        
                                        barmode='overlay',  
                                        font=dict(color=fcouleur, size=fsize),  
                                        title_x=0.5,
                                        title_y=0.9,
                                        template=self.tcouleur,
                                        # showlegend=False  # Remove legend
                                        )
        self.update_axes = dict(  
                            title_font={"size": 14},
                            title_standoff=25
                            )
     
        self.feat_names = feat_names
        explainer = shap.Explainer(model, X_train)
        self.shap_values = explainer(X_train)


    def plot_summary_shap(self):
        fig = go.Figure()
        shap_summary_vals = self.shap_values.values
        shap_summary_data = self.shap_values.data

        for feature_idx in np.abs(shap_summary_vals).mean(axis=0).argsort():
            feature_name = self.feat_names[feature_idx]
            sorted_shap_vals = shap_summary_vals[:, feature_idx]
            sorted_shap_data = shap_summary_data[:, feature_idx]

            fig.add_trace(go.Bar(
                y=[feature_name] * len(sorted_shap_vals),
                x=sorted_shap_vals,
                orientation='h',
                name=feature_name,
                marker=dict(color=sorted_shap_data), 
            ))

        # Add horizontal color bar
        # fig.update_layout(coloraxis=dict(colorscale='Viridis', colorbar=dict(title='SHAP Value'), showscale=True))
        fig.update_layout(
            # title='SHAP Summary Plot',
            xaxis_title='SHAP Value',
            yaxis_title='Feature',
            barmode='relative',
            height=self.height,
            width=self.width,
            margin=dict(l=150, r=20, t=50, b=50),
        )
        fig.update_layout(**self.update_layout_parameter) 
        fig.update_xaxes(**self.update_axes)
        
        return fig


class aka_cleaned_data:
    def __init__(self) -> None:
        pass 
 
    def train_test_cleaned_data(self,df,pre_proc=0): 
        transform = preprocessing.StandardScaler()
        try:
            X = df[df.columns[:-1]] 
            Y = df[df.columns[-1]] 
            
            if pre_proc == 'XY':  
                X = transform.fit_transform(X)  
                Y = transform.fit_transform(df[df.columns[-2:-1]]).reshape(-1,1)

            elif pre_proc == 'X':
                X = transform.fit_transform(X)
            elif pre_proc == 'Y': 
                Y = transform.fit_transform(df[df.columns[-2:-1]]).reshape(-1,1)
        
        except Exception as e: 
            print(f"Error: {e}") 
            
        X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size=0.3, random_state=42)
        
        return X_train, X_test, y_train, y_test 


    def filter_drop_corr_df(self,df,confidence_interval_limit,correlation_percentage_threshold,filt='std'):
        cols = range(df.shape[1]) 

        df_tmp = df.copy()
        corr_tmp,_ = aka_filter().Columns_Correlated(df_tmp,correlation_percentage_threshold)


        if filt == 'std':
            df_tmp = aka_filter().filter_std(df_tmp,cols,confidence_interval_limit)
        elif filt == 'z_score':
            df_tmp = aka_filter().filter_z_score(df_tmp,cols,confidence_interval_limit)
        elif filt == 'IQR':
            df_tmp = aka_filter().filter_IQR(df_tmp,cols,confidence_interval_limit)
        else:
            df_tmp = df.copy()
             
        if corr_tmp :
            uniq_ = np.unique([item[1] for item in corr_tmp])
            df_tmp = df_tmp.drop( df_tmp.columns[uniq_], axis=1)

        return df_tmp,corr_tmp


    def balance_df(self,df,chose = 'nimority'):
        from imblearn.under_sampling import RandomUnderSampler

        dff = df.copy()

        if chose == 'minority':
            randS = RandomUnderSampler(sampling_strategy=1)  
            titleS = 'Under-sampling'
        else:
            randS = RandomUnderSampler(sampling_strategy="not minority") # String
            titleS = 'Over-sampling'

        dff[df.columns[:-1]],dff[df.columns[-1]] = randS.fit_resample(df[df.columns[:-1]],df[df.columns[-1]] )
 
        return dff

