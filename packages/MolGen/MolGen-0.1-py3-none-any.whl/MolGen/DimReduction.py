import contextlib
from MolGen.MolGen.MolGens import MolGen
import pyemma
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
#from hde import HDE
from math import sqrt
import tensorflow as tf
import umap
import tqdm

class DimReduction(object):

    def __init__(self) -> None:
        self.transformed_data = None
        self.feat_corr = None
        self.component_number = None
        self.reducer = None
        self.molgen = None
        super().__init__()

    def apply(self):
        #implement feature selection
        self.molgen.dimred_data = self.transformed_data
        self.molgen.dimred_featcorr = self.feat_corr
        self.molgen.data = self.transformed_data

    def choose_n(self, n:int):
        # get at least 2 PCs!
        if n < 2: n=2
        self.component_number = n
        self.transformed_data = self.reducer.get_output(dimensions=np.arange(n))[0]

class PCAReducer(DimReduction):

    def __init__(self, molgen:MolGen) -> None:
        
        super().__init__()
        if molgen.data is None:
            raise Exception("No data generated with this MolGen!")
            return
        if molgen.chosen_feat_index == -1:
            raise Exception("Features not chosen yet!")
            return

        self.molgen = molgen
        if not molgen.crystal_flag:
            self.data = pyemma.coordinates.source(['/lab/hou/vchaudhari/MolGens/pdb_data/accepted/' + path for path in self.molgen.mdtraj_list], 
                                                self.molgen.featurizers[molgen.chosen_feat_index],
                                                chunksize=self.molgen.chunk_size)
        else:
            self.data = pyemma.coordinates.source(['/lab/hou/vchaudhari/MolGens/pdb_data/accepted/' + path for path in self.molgen.mdtraj_list], 
                                                self.molgen.featurizers[molgen.chosen_feat_index][0],
                                                chunksize=self.molgen.chunk_size)
        
        self.reducer = pyemma.coordinates.pca(self.data)
        self.transformed_data = self.reducer.get_output()[0]
        self.feat_corr = self.reducer.feature_PC_correlation


    def update_component_number(self, number:int):
        if number < 2: number=2
        self.component_number = number
        self.transformed_data = self.reducer.get_output(dimensions=np.arange(number))[0]

    def plot_2d(self, save_loc:str=None) -> None:
        
        y = self.transformed_data
        if y.shape[1] < 2:
            print("Too little PCs to plot!")
            return
        if self.molgen.crystal_flag:
            plt.scatter(y[:,0], y[:,1], c='g', s=14)
        else:
            pyemma.plots.plot_free_energy(y[:,0], y[:,1], cbar=True)
        plt.xlabel("PC1")
        plt.ylabel("PC2")
        if not save_loc is None: plt.savefig(save_loc)

    def plot_3d(self, save_loc:str=None) -> None:
        # Plot PC1, PC2, PC3
        pca_y = self.transformed_data
        if pca_y.shape[1] < 3:
            print("Too little PCs to plot!")
            return
        fig = px.scatter_3d(x=pca_y[:,0], y=pca_y[:,1], z=pca_y[:,2])
        fig.update_traces(marker=dict(size=1,
                                    line=dict(width=0,
                                                color='DarkSlateGrey')),
                        selector=dict(mode='markers'))


        if not save_loc is None: 
            if "html" in save_loc:
                fig.write_html(save_loc)
            else:
                fig.write_image(save_loc)
        else:
            fig.show()
        return fig

    def plot_variance(self, var_thr=90, save_loc:str=None)->None:
        pca_eigenvalues = self.reducer.eigenvalues
        variance = np.cumsum(pca_eigenvalues)/np.sum(pca_eigenvalues) * 100
        pca_num = 0
        for i, v in enumerate(variance):
            if v >= var_thr:
                pca_num = i
                break
        plt.scatter(np.arange(len(pca_eigenvalues)), variance)
        plt.axvline(pca_num, color='red')
        plt.xlabel("Principal Components (Eigenvalue Index)")
        plt.ylabel("Variance explained (%) (Eigenvalue)")
        plt.title("PCA explained variance (with thr = {})".format(var_thr))
        if not save_loc is None: plt.savefig(save_loc)

        print("Total of "+str(v)+"% of variance explaned by first "+str(pca_num)+" PCs.")

    def get_variance(self, var_thr=90, save_loc:str=None)->None:
        pca_eigenvalues = self.reducer.eigenvalues
        variance = np.cumsum(pca_eigenvalues)/np.sum(pca_eigenvalues) * 100
        pca_num = 0
        for i, v in enumerate(variance):
            if round(v, 4) >= var_thr:
                pca_num = i
                break
        print("PCA explained variance (with thr = {}) by first {} components".format(var_thr, pca_num))
        return pca_num

class TICAReducer(DimReduction):

    def __init__(self, molgen:MolGen, TICA_lagtimes:list=[1,2, 5, 10, 25, 50]) -> None:
        
        super().__init__()

        if molgen.crystal_flag==True:
            raise Exception("Attempting TICA for crustal structures!! Please use PCA")
            return        
        if molgen.data is None:
            raise Exception("No data generated with this MolGen!")
            return
        if molgen.chosen_feat_index == -1:
            raise Exception("Features not chosen yet!")
            return
        self.molgen = molgen
        if not molgen.crystal_flag:
            self.data = pyemma.coordinates.source(self.molgen.mdtraj_list, 
                                                self.molgen.featurizers[molgen.chosen_feat_index],
                                                chunksize=self.molgen.chunk_size)
        else:
            self.data = pyemma.coordinates.source(self.molgen.mdtraj_list, 
                                                self.molgen.featurizers[molgen.chosen_feat_index][0],
                                                chunksize=self.molgen.chunk_size)

        self.TICA_lagtimes = TICA_lagtimes
        print("Transforming with TICA - might take some time!")
        self.tica_objs = []
        self.tica_objs_ts = []
        for l in TICA_lagtimes:
            print("lag:",l)
            tica_obj = pyemma.coordinates.tica(self.data, lag=l, var_cutoff=1)
            self.tica_objs.append(tica_obj)
            tica_timescales = tica_obj.timescales
            self.tica_objs_ts.append(tica_timescales)
        self.tica_obj = None
        self.transformed_data = None
        self.component_number = None

    def update_component_number(self, number:int):
        
        if number < 2: number=2
        self.component_number = number
        self.transformed_data = self.tica_obj.get_output(dimensions=np.arange(number))[0]

    def plot_lag_analysis(self, timescale_num:int=10, chosen_lag:int=50, save_loc:str=None):
        # Plot tica timescales as a function of lag time
        lags = self.TICA_lagtimes
        nlags = len(lags)
        timescale_num = min(timescale_num, self.tica_objs_ts[0].shape[0])
        ts_list = np.zeros((nlags, timescale_num))
        for i, lag in enumerate(lags):
            timescales = self.tica_objs_ts[i]
            ts_list[i, :] = timescales[:timescale_num]


        plt.semilogy(lags, ts_list)
        plt.ylabel('Timescales (ns)')
        plt.xlabel('Lag time (ns)')
        plt.fill_between(lags, 1, lags, facecolor='Gray')
        plt.axvline(chosen_lag, linewidth=2, color='black')
        if not save_loc is None: plt.savefig(save_loc)

    def choose_lag(self, lag:int, tic_thr:int=None):
        self.tica_obj = pyemma.coordinates.tica(self.data, lag=lag, var_cutoff=1)
        self.reducer = self.tica_obj
        self.transformed_data = self.tica_obj.get_output()[0]
        self.feat_corr = self.tica_obj.feature_TIC_correlation

    def resolved_processes(self, timescales, lag):
        tmp_diff = np.sort(np.abs(np.diff(timescales)))[::-1]
        signifficant_thr = np.mean(tmp_diff)+2*np.std(tmp_diff)
        diff = np.abs(np.diff(timescales))
        resolved_p = []
        for i, elem in enumerate(list(diff)):
            if elem < signifficant_thr: break
            if elem < lag: break
            resolved_p.append((i,elem))
        return resolved_p

    def choose_lag_auto(self):
        lag_num = len(self.TICA_lagtimes)
        best_lags = []
        #for all processes 
        for i in range(lag_num):
            process_ts = [ts[i] for ts in self.tica_objs_ts]

            #if process time scale is below lagtime - do not count it
            if process_ts[-1] < self.TICA_lagtimes[-1]:
                break 

            x1, y1 = self.TICA_lagtimes[0], process_ts[0]
            x2, y2 = self.TICA_lagtimes[lag_num-1], process_ts[lag_num-1]
            distances = []
            for j in range(lag_num):
                x0 = self.TICA_lagtimes[j]
                y0 = process_ts[j]
                numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
                denominator = sqrt((y2 - y1)**2 + (x2 - x1)**2)
                distances.append(numerator/denominator)
            optimal_j = distances.index(max(distances))
            optimal_lag = self.TICA_lagtimes[optimal_j]
            best_lags.append(optimal_lag)

        if len(best_lags) == 0:
            print("No lags found appropriate - adjust your list of lags (make upper bound lower).")
            return None

        best_lag = int(min(best_lags))
        best_lag_index = self.TICA_lagtimes.index(best_lag)
        print("Chosen lag time: {}".format(best_lag))
        self.tica_obj = pyemma.coordinates.tica(self.data, lag=best_lag, var_cutoff=1)
        self.reducer = self.tica_obj
        self.transformed_data = self.tica_obj.get_output()[0]
        self.feat_corr = self.tica_obj.feature_TIC_correlation
        res_proc_n = i
        print("Number of processes above lag time: {}".format(res_proc_n))
        res_ps = self.resolved_processes(self.tica_objs_ts[best_lag_index], best_lag_index)
        print("Number of clearly resolved processes with TICA: {}".format(len(res_ps)))
        print("Processes (index, timescale): ")
        print(res_ps)
        self.choose_lag(best_lag)
        return best_lag
    
    def plot_2d(self, save_loc:str=None) -> None:
        
        if self.tica_obj is None: raise Exception("Lag not chosen!")
        y = self.transformed_data
        if y.shape[1] < 2:
            print("Too little PCs to plot!")
            return
        Y_concat = y
        pyemma.plots.plot_free_energy(Y_concat[:,0], Y_concat[:,1], cbar=True)
        plt.xlabel("TIC1")
        plt.ylabel("TIC2")
        if not save_loc is None: plt.savefig(save_loc)

    def plot_3d(self, save_loc:str=None) -> None:
        if self.tica_obj is None: raise Exception("Lag not chosen!")
        # Plot PC1, PC2, PC3
        y = self.transformed_data
        if y.shape[1] < 3:
            print("Too little PCs to plot!")
            return
        fig = px.scatter_3d(x=y[:,0], y=y[:,1], z=y[:,2], color=list(range(y.shape[0])))
        fig.update_traces(marker=dict(size=1,
                                    line=dict(width=0,
                                                color='DarkSlateGrey')),
                        selector=dict(mode='markers'))
        fig.layout.coloraxis.colorbar.title = 'frame number'
        fig.show()
        if not save_loc is None: fig.write_image(save_loc)

    def plot_variance(self, var_thr=90, save_loc:str=None)->None:
        
        if self.tica_obj is None: raise Exception("Lag not chosen!")
        tica_eigenvalues = self.tica_obj.eigenvalues
        variance = np.cumsum(tica_eigenvalues**2)/ np.sum(tica_eigenvalues**2)*100
        tica_num = 0
        for i, v in enumerate(variance):
            if v >= var_thr:
                tica_num = i
                break
                
        plt.scatter(np.arange(len(tica_eigenvalues)), variance)
        plt.xlabel("TICA Components (Eigenvalue Index)")
        plt.ylabel("Kinetic variance explained (%) (Eigenvalue^2)")
        plt.axvline(tica_num, color='red')
        print("Total of "+str(v)+"% of variance explaned by first "+str(tica_num)+" ICs.")
        if not save_loc is None: plt.savefig(save_loc)
        
    def get_variance(self, var_thr=90, save_loc:str=None)->None:
        
        if self.tica_obj is None: raise Exception("Lag not chosen!")
        tica_eigenvalues = self.tica_obj.eigenvalues
        variance = np.cumsum(tica_eigenvalues**2)/ np.sum(tica_eigenvalues**2)*100
        tica_num = 0
        for i, v in enumerate(variance):
            if round(v, 4) >= var_thr:
                tica_num = i
                break
        print("TICA explained variance (with thr = {}) by first {} components".format(var_thr, tica_num))
        return tica_num
                
\
class UMAPReducer(DimReduction):

    def __init__(self, molgen:MolGen, n_neighbors:int = 15, min_dist:float = 0.1, n_components:int = 2) -> None:
        
        super().__init__()
        if molgen.data is None:
            raise Exception("No data generated with this MolGen!")
            return
        if molgen.chosen_feat_index == -1:
            raise Exception("Features not chosen yet!")
            return
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist
        self.component_number = n_components
        self.molgen = molgen

        # extract data into a memmap
        if not molgen.crystal_flag:
            pyemma_data = pyemma.coordinates.source(['/lab/hou/vchaudhari/MolGens/pdb_data/accepted/' + path for path in self.molgen.mdtraj_list], 
                                        molgen.featurizers[molgen.chosen_feat_index], 
                                        chunksize = molgen.chunk_size)
        else:
            pyemma_data = pyemma.coordinates.source(['/lab/hou/vchaudhari/MolGens/pdb_data/accepted/' + path for path in self.molgen.mdtraj_list], 
                                        molgen.featurizers[molgen.chosen_feat_index][0], 
                                        chunksize = molgen.chunk_size)

        pyemma_data_dimension = pyemma_data.dimension()
        pyemma_data_n_frames = pyemma_data.n_frames_total()
        pyemma_iter = pyemma_data.iterator()
        # initialize array
        self.data = np.memmap('tmp_data.mymemmap', 
                                dtype='float32', 
                                mode='w+',
                                shape=(pyemma_data_n_frames,pyemma_data_dimension))
        shape_cnt = 0
        for i, elem in tqdm.tqdm(enumerate(pyemma_iter),total = pyemma_data.n_chunks(pyemma_data.chunksize)):
            data = elem[1]
            self.data[shape_cnt : shape_cnt+data.shape[0], :] = data
            shape_cnt += data.shape[0]

        if not shape_cnt == pyemma_data_n_frames:
            print("Warning: output data dimensions don't match the number of frames")

        self.reducer = umap.UMAP(n_neighbors= self.n_neighbors, min_dist=self.min_dist, n_components=self.component_number)
        self.transformed_data = self.reducer.fit_transform(self.data)
        self.feat_corr = None # TODO: how to imeplement feature importance for UMAP is a future step

    def update_component_number(self, number:int):
        if number < 2: number=2
        self.component_number = number
        self.reducer = umap.UMAP(n_neighbors= self.n_neighbors, min_dist=self.min_dist, n_components=self.component_number)
        self.transformed_data = self.reducer.fit_transform(self.data)

    
    def plot_2d(self, save_loc:str=None) -> None:
        
        y = self.transformed_data
        print(y)
        if y.shape[1] < 2:
            print("Too little PCs to plot!")
            return
        if self.molgen.crystal_flag:
            plt.scatter(y[:,0], y[:,1], c='g', s=14)
        else:
            pyemma.plots.plot_free_energy(y[:,0], y[:,1], cbar=True)
        plt.xlabel("UMAP-1")
        plt.ylabel("UMAP-2")
        if not save_loc is None: plt.savefig(save_loc)

    def plot_3d(self, save_loc:str=None) -> None:
        # Plot PC1, PC2, PC3
        y = self.transformed_data
        if y.shape[1] < 3:
            print("Too little PCs to plot!")
            return
        fig = px.scatter_3d(x=y[:,0], y=y[:,1], z=y[:,2])
        fig.update_traces(marker=dict(size=1,
                                    line=dict(width=0,
                                                color='DarkSlateGrey')),
                        selector=dict(mode='markers'))


        if not save_loc is None: 
            if "html" in save_loc:
                fig.write_html(save_loc)
            else:
                fig.write_image(save_loc)
        else:
            fig.show()
        return fig
        
    '''
    def plot_variance(self, var_thr=90, save_loc:str=None)->None:
        pca_eigenvalues = self.reducer.eigenvalues
        variance = np.cumsum(pca_eigenvalues)/np.sum(pca_eigenvalues) * 100
        pca_num = 0
        for i, v in enumerate(variance):
            if v >= var_thr:
                pca_num = i
                break
        plt.scatter(np.arange(len(pca_eigenvalues)), variance)
        plt.axvline(pca_num, color='red')
        plt.xlabel("Principal Components (Eigenvalue Index)")
        plt.ylabel("Variance explained (%) (Eigenvalue)")
        plt.title("PCA explained variance (with thr = {})".format(var_thr))
        if not save_loc is None: plt.savefig(save_loc)

        print("Total of "+str(v)+"% of variance explaned by first "+str(pca_num)+" PCs.")
    '''

    '''
    def get_variance(self, var_thr=90, save_loc:str=None)->None:
        pca_eigenvalues = self.reducer.eigenvalues
        variance = np.cumsum(pca_eigenvalues)/np.sum(pca_eigenvalues) * 100
        pca_num = 0
        for i, v in enumerate(variance):
            if round(v, 4) >= var_thr:
                pca_num = i
                break
        print("PCA explained variance (with thr = {}) by first {} components".format(var_thr, pca_num))
        return pca_num
    '''


class rna_UMAPReducer(DimReduction):

    def __init__(self, molgen: MolGen, data, n_neighbors=15, min_dist=0.1, n_components=2):
        self.molgen = molgen
        self.data = data
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist
        self.n_components = n_components
        self.transformed_data = None

    def fit_transform(self):
        if self.data is None:
            raise Exception("No data provided!")
        
        self.reducer = umap.UMAP(
            n_neighbors=self.n_neighbors,
            min_dist=self.min_dist,
            n_components=self.n_components
        )
        self.transformed_data = self.reducer.fit_transform(self.data)
    
    def plot_2d(self, save_loc=None):
        if self.transformed_data is None:
            print("Data has not been transformed yet. Call fit_transform() first.")
            return
        if self.transformed_data.shape[1] < 2:
            print("Too few components to plot in 2D!")
            return
        plt.scatter(self.transformed_data[:, 0], self.transformed_data[:, 1])
        plt.xlabel("UMAP-1")
        plt.ylabel("UMAP-2")
        if save_loc:
            plt.savefig(save_loc)
        else:
            plt.show()

    def plot_3d(self, save_loc=None):
        if self.transformed_data is None:
            print("Data has not been transformed yet. Call fit_transform() first.")
            return
        if self.transformed_data.shape[1] < 3:
            print("Too few components to plot in 3D!")
            return
        fig = px.scatter_3d(
            x=self.transformed_data[:, 0],
            y=self.transformed_data[:, 1],
            z=self.transformed_data[:, 2]
        )
        if save_loc:
            if save_loc.endswith('.html'):
                fig.write_html(save_loc)
            else:
                fig.write_image(save_loc)
        else:
            fig.show()




dimreds = {
    "PCA": PCAReducer,  
    "TICA": TICAReducer,
    #"HDE": HDEReducer,
    "UMAP": UMAPReducer,
    "R_UMAP": rna_UMAPReducer,
}


