from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import train_test_split  
from sklearn import preprocessing

import pandas as pd
import numpy as np 
import math
import shap

 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

 
from scipy import stats




 # Class for encoding categorical variables using label encoding

class aka_encoding:
    def __init__(self, df) -> None:
        # Initialize the class with the DataFrame
        # Identify columns with string values
        str_col = []
        for val in df.columns:
            for _, elm in df[val].dropna().items():
                if isinstance(elm, str):
                    str_col.append(val)
                    break

        # Create mapping for label encoding
        mapping = {}
        swapMapping = {}
 
        if str_col is not None:
            for val in str_col:
                # Initialize mapping for each column
                mapping[val] = {}
                # Get unique values in the column
                uniq = df[val].dropna().unique()
                # Create mapping of unique values to integers
                for i in range(len(uniq)):
                    key = uniq[i]
                    mapping[val][key] = i
                # If it's the last column, create a reverse mapping
                if val == df.columns[-1]:
                    for i in range(len(uniq)):
                        key = uniq[i]
                        swapMapping[i] = key

        # Save mapping and DataFrame
        self.mapping = mapping
        self.swapMapping = swapMapping
        self.df = df

    # Method for label encoding
    def label_encoding(self):
        dfTemp = self.df.copy()

        # If there are columns to encode
        if self.mapping.keys() is not None:
            for val in self.mapping.keys():
                # Map values to integers
                dfTemp[val] = self.df[val].map(self.mapping[val])
        return dfTemp

    # Method for inverse label encoding
    def label_encoding_inverse(self, y_pred):
        df = pd.DataFrame(y_pred)
        # If there's a reverse mapping
        if len(self.swapMapping) > 0:
            return df[df.columns[0]].map(self.swapMapping)
        else:
            return df[df.columns[0]]

    # Method for replacing items into string DataFrame
    def Replace_item_into_str_df(self, df, col=-1):
        # If the column index is valid
        if col <= df.shape[1]:
            # Get unique values in the column
            clabel = df[df.columns[col]].unique()
            # Generate labels with underscores
            Label = ['_' + str(item) for item in df[df.columns[col]].unique()]
            # Replace items in the last column with labels
            df[df.columns[-1]] = df[df.columns[col]].replace(clabel, Label)



# Class for preparing a DataFrame
class aka_df_prepare:
    def __init__(self) -> None:
        pass

    # Method to read a DataFrame from a CSV file with handling different encodings
    def df_get(self, cvs_path):
        encodings_to_try = ['utf-8', 'latin-1', 'ISO-8859-1']
        # Try different encodings until one works
        for encoding in encodings_to_try:
            try:
                df = pd.read_csv(cvs_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        return df

    # Method to swap the positions of two features in the DataFrame
    def swap_features(self, df, feat_a, feat_b=None):
        # If feat_b is not provided, set it to the last feature
        if feat_b is None:
            feat_b = df.shape[1] - 1

        # If feat_a and feat_b are valid and not equal
        if feat_a != feat_b and 0 <= feat_a < df.shape[1] and 0 <= feat_b < df.shape[1]:
            # Swap the positions of the two features
            df_t = df[df.columns[[feat_b, feat_a]]]
            df_c = df.drop(df.columns[[feat_b, feat_a]], axis=1)
            return pd.concat([df_c, df_t], axis=1)
        else:
            print("Invalid feature indices or feat_a is equal to feat_b.")
            return df

    # Method to drop specified features from the DataFrame
    def drop_feature(self, df, feat):
        # Ensure the feature indices are valid
        if len(feat) > 0:
            feats = [fe for fe in feat if fe <= len(df.columns)]
            # Drop the specified features
            return df.drop(df.columns[feats], axis=1)
        else:
            return df

    # Method for processing missing data in the DataFrame
    def missing_data_processing(self, df, data_nan_drop=True):
        if data_nan_drop:
            # Drop rows with missing values
            df.dropna(inplace=True)
        else:
            # Fill missing values with mode for categorical columns and mean for numerical columns
            for column in df.columns:
                if df[column].dtype == 'object':  # Check if column is categorical
                    mode = df[column].mode()[0]
                    df[column].fillna(mode, inplace=True)
                else:  # Numerical columns changed into mean
                    mean = df[column].mean()
                    df[column].fillna(mean, inplace=True)





# Class for filtering DataFrame based on various methods
class aka_filter:
    def __init__(self) -> None:
        pass

    # Method for filtering data based on standard deviation
    def filter_std(self, df, cols, std_number=[-3, 3]):
        if std_number:
            # Calculate lower and upper limits based on standard deviation
            lower_limit = df.mean() + std_number[0] * df.std()
            upper_limit = df.mean() + std_number[1] * df.std()
            for i in cols:
                df_i = df[df.columns[i]]
                # Find indices of rows outside the limits
                ind = df_i[~((df_i > lower_limit[i]) & (df_i < upper_limit[i]))].index
                # Drop rows outside the limits
                df = df.drop(ind)
        return df

    # Method for filtering data based on z-scores
    def filter_z_score(self, df, cols, std_inter=[-3, 3]):
        for i in cols:
            df_i = df[df.columns[i]]
            # Calculate z-scores
            df_z = (df_i - df_i.mean()) / df_i.std() 
            ind = df_i[~((df_z > std_inter[0]) & (df_z < std_inter[1]))].index
            # Drop rows outside the z-score limits
            df = df.drop(ind)
        return df

    # Method for filtering data based on interquartile range (IQR)
    def filter_IQR(self, df, cols, IQR_number=[-1.5, 1.5]):
        for i in cols:
            df_i = df[df.columns[i]]
            # Calculate quartiles and IQR
            q25, q75 = np.percentile(a=df_i, q=[25, 75])
            IQR = q75 - q25
            lower_limit = q25 + IQR_number[0] * IQR
            upper_limit = q75 + IQR_number[1] * IQR
            # If IQR is not close to zero, filter the data
            if 10**-10 * round(10**10 * np.abs(IQR)) > 0.0:
                # Find indices of rows outside the IQR limits
                ind = df_i[~((df_i > lower_limit) & (df_i < upper_limit))].index
                # Drop rows outside the IQR limits
                df = df.drop(ind)
        return df

    # Method for identifying columns that are highly correlated
    def Columns_Correlated(self, df, percent_correlation):
        cm = df.corr()
        n = cm.shape[0]
        corr_tmp = []

        # Iterate over upper triangle of correlation matrix
        for i in range(n):
            for j in range(i):
                # If correlation coefficient is above the threshold, record the indices
                if abs(cm.iloc[i, j]) >= percent_correlation:
                    corr_tmp.append([i, j])
        return corr_tmp, cm

    # Method for standardizing the DataFrame
    def df_standardized(self, df):
        # Standardize the DataFrame
        df_tmp = (df - df.mean()) / df.std()
        return df_tmp



# Class for various plotting functionalities
class aka_plot_prep:
    def __init__(self, tcouleur='plotly_dark', bcouleur='navy', fcouleur='white', fsize=20):
        # Initialize plot parameters
        self.tcouleur = tcouleur
        self.bcouleur = bcouleur
        self.fcouleur = fcouleur
        self.fsize = fsize
        self.update_layout_parameter = dict(
            barmode='overlay',
            font=dict(color=fcouleur, size=fsize),
            title_x=0.5,
            title_y=0.9,
            template=self.tcouleur
        )
        self.update_axes = dict(
            title_font={"size": 14},
            title_standoff=25
        )

    # Method to plot a histogram
    def plot_history(self, df, feat):
        fig = px.histogram(data_frame=df, x=feat, opacity=0.7)
        fig.update_layout(**self.update_layout_parameter)
        return fig

    # Method to plot a histogram for comparison
    def plot_history_compare(self, df, df_, feat):
        df_0 = df[df.columns[feat]]
        df_0['filtered'] = df_[df.columns[feat]]
        fig = px.histogram(data_frame=df_0, opacity=0.7)
        fig.update_xaxes(categoryorder='total descending')
        fig.update_layout(**self.update_layout_parameter)
        return fig

    # Method to plot histograms for all features
    def plot_history_all(self, df):
        fig = px.histogram(data_frame=df, opacity=.7).update_xaxes(categoryorder='total descending')
        fig.update_layout(**self.update_layout_parameter)
        fig.update_xaxes(**self.update_axes)
        return fig

    # Method to plot histograms for selected features
    def Plot_histogram_Features(self, df, columns_to_treat, fig_size_row=390, fig_size_col=490, subplot_col=3):
        if len(columns_to_treat) > 0:
            nrow = math.ceil(len(columns_to_treat) / subplot_col)
            # Create subplots
            fig = make_subplots(rows=nrow, cols=subplot_col, subplot_titles=df.columns[columns_to_treat])

            for i, col_index in enumerate(columns_to_treat):
                row_num = 1 + i // subplot_col
                col_num = 1 + i % subplot_col

                # Plot histogram for the current column
                hist_trace = go.Histogram(x=df[df.columns[col_index]])

                hist_trace['showlegend'] = False
                fig.add_trace(hist_trace, row=row_num, col=col_num)

            # Update layout
            fig.update_layout(height=fig_size_row, width=fig_size_col)
            fig.update_layout(**self.update_layout_parameter)
            fig.update_layout(
                height=fig_size_row * nrow,
                width=fig_size_col * subplot_col  # Adjust the width as needed
            )
            return fig
        else:
            print("Empty list is provided.")

    # Method to plot a pie chart
    def plot_pie(self, df, col):
        fig = px.pie(df[df.columns[col]], names=df[df.columns[col]].value_counts().index,
                     values=df[df.columns[col]].value_counts().values,
                     title=f'Pie Chart of {df.columns[col]}')
        fig.update_layout(**self.update_layout_parameter)
        fig.update_xaxes(**self.update_axes)
        return fig

    # Method to plot box plots for two features
    def Plot_box_2_Features(self, df, df_filtered, corr_tmp=[], fig_size_row=390, fig_size_col=490, subplot_col=3):

        if len(corr_tmp) > 0:
            nrow = math.ceil(len(corr_tmp) / subplot_col)
            # Create subplots
            fig = make_subplots(
                rows=nrow, cols=subplot_col,
                subplot_titles=[df.columns[corr] for corr in corr_tmp])

            for i, corr in enumerate(corr_tmp, 1):
                df_0 = pd.DataFrame()
                df_0['true'] = df[df.columns[corr]]
                df_0['filtered'] = df_filtered[df_filtered.columns[corr]]
                scatter_fig = px.box(data_frame=df_0).update_xaxes(categoryorder='total descending')
                ind_col = int((i + subplot_col - 1) % subplot_col + 1)
                ind_row = int(1 + (i - ind_col) / subplot_col)

                for j, trace in enumerate(scatter_fig.data):
                    if j != 1 or j != 2 or j != 3:
                        fig.add_trace(scatter_fig.data[j], row=ind_row, col=ind_col)

            fig.update_layout(**self.update_layout_parameter)
            fig.update_layout(
                height=fig_size_row * nrow,
                width=fig_size_col * subplot_col
            )
            return fig
        else:
            print("Empty list is provided.")

    # Method to plot a box plot

    def plot_box(self,df,index_col_box = [0,-1]):   
        for i in [0,1]:
            if index_col_box[i]<0:
                index_col_box[i] += df.shape[1]+1 

        fig = px.box(df, y=df.max().sort_values()[max(0,index_col_box[0]-1):min(index_col_box[1],df.shape[1])].index) 
        fig.update_layout(**self.update_layout_parameter) 
        fig.update_xaxes(**self.update_axes)
        return fig

    # Method to plot a heatmap
    def plot_heatmap(self, df, show_label=True):
        x_label = df.columns
        y_label = df.index
        if df.shape[1] > 0:
            cm = df.select_dtypes(exclude=['object']).values.round(3)

            fig = go.Figure(data=go.Heatmap(
                z=cm,
                x=x_label,
                y=y_label,
                colorscale='Viridis',
                hoverongaps=False)
            )

            if show_label:
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

    # Method to plot a scatter plot
    def Plot_scatter(self, df, corr_tmp, fig_size_row=390, fig_size_col=490, subplot_col=3):
        if len(corr_tmp) > 0:
            nrow = math.ceil(len(corr_tmp) / subplot_col)
            # Create subplots
            fig = make_subplots(
                rows=nrow, cols=subplot_col,
                subplot_titles=[""] * len(corr_tmp))

            for i, corr in enumerate(corr_tmp, 1):
                scatter_fig = px.scatter(df, x=df.columns[corr[0]], y=df.columns[corr[1]],
                                          trendline="ols")
                ind_col = int((i + subplot_col - 1) % subplot_col + 1)
                ind_row = int(1 + (i- ind_col) / subplot_col)

                for j, trace in enumerate(scatter_fig.data):
                    if j != 1 or j != 2 or j != 3:
                        trace['showlegend'] = False
                        fig.add_trace(scatter_fig.data[j], row=ind_row, col=ind_col)
                    fig.update_xaxes(title_text=df.columns[corr[0]], row=ind_row, col=ind_col)
                    fig.update_yaxes(title_text=df.columns[corr[1]], row=ind_row, col=ind_col)

            fig.update_layout(**self.update_layout_parameter)
            fig.update_layout(
                height=fig_size_row * nrow,
                width=fig_size_col * subplot_col
            )
            return fig
        else:
            print("Empty list is provided")





 # Class for plotting ML report 
class aka_plot_ML:
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

    def regression_summary(self, X_train, y_train, y_pred, params, feat_name, reg = 1):

        nn, kk = X_train.shape
        # Degrees of freedom.
        degf = float(nn-kk-1)
        dff = pd.DataFrame(X_train)
        dff.columns = feat_name
        if reg == 1:
            df_tmp = pd.DataFrame({"Constant":np.ones(nn)}).join(dff)
        else:
            df_tmp = dff

        MSE = (sum((y_train-y_pred)**2))/degf
        

        var_beta = MSE*(np.linalg.inv(np.dot(df_tmp.T,df_tmp)).diagonal())
        sd_beta = np.sqrt(var_beta) 
        ts_beta = params/ sd_beta

        p_values =[2*(1-stats.t.cdf(np.abs(its),degf)) for its in ts_beta]

        sd_beta = np.round(sd_beta,3)
        ts_beta = np.round(ts_beta,3)
        p_values = np.round(p_values,4)
        params = np.round(params,4)



        alpha = 0.05  # Significance level (1 - confidence level)
        critical_value = stats.t.ppf(1-alpha/2, degf)

        # Compute the confidence intervals for the coefficients
        low_bound = params - critical_value * sd_beta
        up_bound = params + critical_value * sd_beta

        low_bound = np.round(low_bound,3)
        up_bound = np.round(up_bound,3)

        df_res = pd.DataFrame()
        df_res["features"],df_res["Coef"],df_res["str err"],df_res["t values"],df_res["P > |t|"],df_res["[0.025  "],df_res["   0.975]"] = [df_tmp.columns,params,sd_beta,ts_beta,p_values,low_bound,up_bound]
    
        return df_res



    def plot_regression_summary(self, X_train, y_train, y_pred, params, cmLabel, lab=1): 
        # Generate classification report
        df_res = self.regression_summary(X_train, y_train, y_pred, params, cmLabel)
        colss =  [mn for mn in df_res.columns[1:]] 
    
        df_name = [mn for mn in df_res[df_res.columns[0]]] 
        # df_name.reverse() 

        cm = df_res[df_res.columns[1:]].fillna(0).values 

        if lab == 1:
            fig = ff.create_annotated_heatmap(cm,
                                            x=colss,
                                            y=df_name,
                                            # annotation_text=cm.round(3),
                                            colorscale='Viridis',)
        else:
            fig = ff.create_annotated_heatmap(cm,
                                            x=colss,
                                            colorscale='Viridis')
            fig.update_yaxes(title_text='y', showticklabels=False)
 
        fig.update_layout(**self.update_layout_parameter) 
        fig.update_xaxes(**self.update_axes)
        fig.update_yaxes(**self.update_axes) 
        fig.update_layout(title='Regression Summary',font=dict(size=self.fsize)) 

        return fig





    def plot_classification_report(self, y, y_predict, cmLabel, lab=1): 
        # Generate classification report
        report_str = classification_report(y, y_predict, target_names=cmLabel, output_dict=True) 
        colss = ['precision', 'recall', 'f1-score', 'support']

        # Convert to a DataFrame
        report_df = pd.DataFrame(report_str)
        report_df = report_df.drop(report_df.columns[-3],axis=1)
        df_name = [mn for mn in report_df.columns] 
        df_name.reverse() 

        cm = report_df.apply(pd.to_numeric, errors='coerce').fillna(0).values.T 
        if lab == 1:
            fig = ff.create_annotated_heatmap(cm,
                                            x=colss,
                                            y=df_name,
                                            annotation_text=cm.round(3),
                                            colorscale='Viridis')
        else:
            fig = ff.create_annotated_heatmap(cm,
                                            x=colss,
                                            colorscale='Viridis')
            fig.update_yaxes(title_text='y', showticklabels=False)

        fig.update_layout(**self.update_layout_parameter) 
        fig.update_xaxes(**self.update_axes)
        fig.update_yaxes(**self.update_axes)
        fig.update_layout(
                title='Correlation Matrix',
                font=dict(size=self.fsize)
            ) 

        return fig 


    # Method to plot the correlation matrix
    def Plot_Correlation_Matrix(self, df, height=900, width=1000):
        cm = df.corr()

        fig = px.imshow(cm, labels=dict(color="Correlation"), x=cm.columns, y=cm.index)

        fig.update_layout(**self.update_layout_parameter)
        fig.update_xaxes(**self.update_axes)
        fig.update_layout(
            height=height,
            width=width
        )
        fig.update_layout(
            title='Correlation Matrix',
            font=dict(size=self.fsize)
        )
        return fig

    # Method to plot a confusion matrix
    def plot_confusion_matrix(self, y, y_predict, feature_name, show_label=True):
        cm = confusion_matrix(y, y_predict)
        if show_label:
            fig = ff.create_annotated_heatmap(cm,
                                               x=feature_name[:cm.shape[1]],
                                               y=feature_name[:cm.shape[1]],
                                               colorscale='Viridis', showscale=True)
            fig.update_xaxes(
                title_text='Predicted labels',
                side='bottom')
            fig.update_yaxes(title_text='True labels')
        else:
            annotation_text = [['' for _ in range(cm.shape[1])] for _ in range(cm.shape[0])]
            fig = ff.create_annotated_heatmap(cm,
                                               x=feature_name[:cm.shape[1]],
                                               y=feature_name[:cm.shape[1]],
                                               colorscale='Viridis',
                                               annotation_text=annotation_text,
                                               showscale=True)
            fig.update_xaxes(
                title_text='Prediction',
                side='bottom')
            fig.update_xaxes(showticklabels=True)
            fig.update_yaxes(title_text='True Solution')
            fig.update_yaxes(showticklabels=True)

        fig.update_layout(**self.update_layout_parameter)
        fig.update_xaxes(**self.update_axes)
        fig.update_yaxes(**self.update_axes)
        fig.update_layout(
            title='Confusion Matrix',
            font=dict(size=self.fsize)
        )

        return fig


# Class for plotting SHAP summary
class aka_plot_shap:
    def __init__(self, model, X_train, feat_names, tcouleur='plotly_dark', bcouleur='navy', fcouleur='white', fsize=20,
                 height=700, width=1000):
        # Initialize plot parameters
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

    # Method to plot SHAP summary
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
            xaxis_title='SHAP Value',
            yaxis_title='Feature',
            barmode='relative',
            height=self.height,
            width=self.width,
            margin=dict(l=150, r=20, t=50, b=50),
        )
        fig.update_layout(**self.update_layout_parameter)
        fig.update_xaxes(**self.update_axes)
        fig.update_layout(
            title='SHAP Summary Plot',
            font=dict(size=20)
        )

        return fig




# Provides methods for cleaning and preprocessing data.
class aka_cleaned_data:
    def __init__(self) -> None:
        pass

    # Splits the data into training and testing sets and applies preprocessing if specified.
    def train_test_cleaned_data(self, df, pre_proc=0):
        transform = preprocessing.StandardScaler()
        try:
            X = df[df.columns[:-1]]
            Y = df[df.columns[-1]]

            if pre_proc == 'XY':
                X = transform.fit_transform(X)
                Y = transform.fit_transform(df[df.columns[-2:-1]]).reshape(-1, 1)
            elif pre_proc == 'X':
                X = transform.fit_transform(X)
            elif pre_proc == 'Y':
                Y = transform.fit_transform(df[df.columns[-2:-1]]).reshape(-1, 1)

        except Exception as e:
            print(f"Error: {e}")

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

        return X_train, X_test, y_train, y_test

    # Filters the dataframe based on specified criteria and drops correlated columns.
    def filter_drop_corr_df(self, df, confidence_interval_limit, correlation_percentage_threshold, filt='std'):
        cols = range(df.shape[1])

        df_tmp = df.copy()
        corr_tmp, _ = aka_filter().Columns_Correlated(df_tmp, correlation_percentage_threshold)

        if filt == 'std':
            df_tmp = aka_filter().filter_std(df_tmp, cols, confidence_interval_limit)
        elif filt == 'z_score':
            df_tmp = aka_filter().filter_z_score(df_tmp, cols, confidence_interval_limit)
        elif filt == 'IQR':
            df_tmp = aka_filter().filter_IQR(df_tmp, cols, confidence_interval_limit)
        else:
            df_tmp = df.copy()

        if corr_tmp:
            uniq_ = np.unique([item[1] for item in corr_tmp])
            df_tmp = df_tmp.drop(df_tmp.columns[uniq_], axis=1)

        return df_tmp, corr_tmp

    # Balances the dataframe using under-sampling or over-sampling techniques.
    def balance_df(self, df, chose='nimority'):
        from imblearn.under_sampling import RandomUnderSampler

        dff = df.copy()

        if chose == 'minority':
            randS = RandomUnderSampler(sampling_strategy=1)
            titleS = 'Under-sampling'
        else:
            randS = RandomUnderSampler(sampling_strategy="not minority")  # String
            titleS = 'Over-sampling'

        dff[df.columns[:-1]], dff[df.columns[-1]] = randS.fit_resample(df[df.columns[:-1]], df[df.columns[-1]])

        return dff
