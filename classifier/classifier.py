from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly as py
from plotly.graph_objs import *
from helper.visuals import *




class Classifier:


    def __init__(self, feature_vector_list):
        self.feature_matrix = pd.DataFrame(feature_vector_list)
        self.feature_matrix.columns = ["M(GSR_Res)", "Std(GSR_Res)", "M(HBR)", "Std(HBR)", "M(RR)", "Std(RR)", \
                                        "RMSSD(RR)", "M(Motion)", "Std(Motion)", "M(ST)", "Std(ST)", "Classified"]
        # split data table into data X and class labels y
        self.data = self.feature_matrix.ix[:, 0:10].values
        self.labels = self.feature_matrix.ix[:, 11].values
        self.labels2 = self.labels.astype(str)

        pd.plotting.scatter_matrix(self.feature_matrix, alpha = 0.2, figsize = (14,10), diagonal = 'kde')
        plt.show()


    def plot_distr(self):
        traces = []
        colors = {'0': 'rgb(31, 119, 180)',
                  '1': 'rgb(255, 127, 14)'}
        for col in range(10):
            for key in colors:
                traces.append(Histogram(x=self.data[self.labels2 == key, col],
                                        opacity=0.75,
                                        xaxis='x%s' % (col + 1),
                                        marker=Marker(color=colors[key]),
                                        name=key))
        data = Data(traces)
        layout = Layout(barmode='overlay',
                        xaxis=XAxis(domain=[0, 0.09], title="M(GSR_Res)"),
                        xaxis2=XAxis(domain=[0.09, 0.18], title="Std(GSR_Res)"),
                        xaxis3=XAxis(domain=[0.18, 0.27], title="M(HBR)"),
                        xaxis4=XAxis(domain=[0.27, 0.36], title="Std(HBR)"),
                        xaxis5=XAxis(domain=[0.36, 0.45], title="M(RR)"),
                        xaxis6=XAxis(domain=[0.45, 0.54], title="Std(RR)"),
                        xaxis7=XAxis(domain=[0.54, 0.63], title="RMSSD(RR)"),
                        xaxis8=XAxis(domain=[0.63, 0.72], title="M(Motion)"),
                        xaxis9=XAxis(domain=[0.72, 0.81], title="Std(Motion)"),
                        xaxis10=XAxis(domain=[0.81, 0.9], title="M(ST)"),
                        xaxis11=XAxis(domain=[0.9, 1.0], title="Std(ST)"),
                        yaxis=YAxis(title='count'),
                        title='Distribution of different physiological features')
        fig = Figure(data=data, layout=layout)
        py.offline.plot(fig)



    def do_PCA(self):
        standardized_data = StandardScaler().fit_transform(self.data)
        # cov_mat = np.cov(standardized_data.T)
        # eig_vals, eig_vecs = np.linalg.eig(cov_mat)
        #
        # # Make a list of (eigenvalue, eigenvector) tuples
        # eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:, i]) for i in range(len(eig_vals))]
        #
        # # Sort the (eigenvalue, eigenvector) tuples from high to low
        # eig_pairs.sort()
        # eig_pairs.reverse()

        # tot = sum(eig_vals)
        # var_exp = [(i / tot) * 100 for i in sorted(eig_vals, reverse=True)]
        # cum_var_exp = np.cumsum(var_exp)
        #
        # trace1 = Bar(
        #     x=['PC %s' % i for i in range(1, 11)],
        #     y=var_exp,
        #     showlegend=False)
        #
        # trace2 = Scatter(
        #     x=['PC %s' % i for i in range(1, 11)],
        #     y=cum_var_exp,
        #     name='cumulative explained variance')
        #
        # data = Data([trace1, trace2])
        #
        # layout = Layout(
        #     yaxis=YAxis(title='Explained variance in percent'),
        #     title='Explained variance of physiological data by different principal components')
        #
        # fig = Figure(data=data, layout=layout)
        # py.offline.plot(fig)

        pca = PCA(n_components=2)
        pca = pca.fit(standardized_data)

        reduced_data = PCA.transform(standardized_data)

        reduced_data = pd.DataFrame(reduced_data, columns=['Dimension 1', 'Dimension 2'])

        traces = []

        for name in ('0', '1'):
            trace = Scatter(
                x=Y_sklearn[self.labels2 == name, 0],
                y=Y_sklearn[self.labels2 == name, 1],
                mode='markers',
                name=name,
                marker=Marker(
                    size=12,
                    line=Line(
                        color='rgba(217, 217, 217, 0.14)',
                        width=0.5),
                    opacity=0.8))
            traces.append(trace)

        data = Data(traces)
        layout = Layout(xaxis=XAxis(title='PC1', showline=False),
                        yaxis=YAxis(title='PC2', showline=False))
        fig = Figure(data=data, layout=layout)
        py.offline.plot(fig)


























