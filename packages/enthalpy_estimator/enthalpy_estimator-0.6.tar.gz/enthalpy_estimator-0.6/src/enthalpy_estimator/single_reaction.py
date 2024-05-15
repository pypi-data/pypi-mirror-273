from .cfg import *

import numpy as np
import scipy as sp
import os

class EnthalpyEstimator:
    def __init__(self, target, reference, vectorizer, isodesmic=False):
        self.target = target
        self.reference = reference
        self.all_species = [self.target] + [r for r in self.reference if r != self.target]
        
        self.excluded = []
        self.reaction = None
        self.directions = None
        self.dfH_grad = None
        self.u_grad = None

        self.vectorizer = vectorizer(self.all_species, isodesmic=isodesmic)

        self.init_dfH()

    def get_basis(self):
        return self.vectorizer.basis

    def init_dfH(self):
        def read_energies(entry, r):
            try:
                with open(r['energies'], 'r') as f:
                    for l in f.readlines()[2:]:
                        if '=' in l:
                            l_split = [s.strip() for s in l.split('=')]
                            entry[l_split[0]] = float(l_split[-1])
            except Exception:
                print(f'Error reading file {r["energies"]}')

        def read_Hcorr(entry, r):
            try:
                with open(r['hcorr'], 'r') as f:
                    entry['Hcorr'] = [float(l.split()[-1]) for l in f
                                    if 'Thermal correction to Enthalpy' in l][0]
            except Exception:
                print(f'Error reading file {r["hcorr"]}')

        def calc_drH(E_all):
            if not 'E' in E_all:
                E_CV = E_all['E(CV correction (TZ))']
                E_IT = E_all['E(DLPNO-CCSD(T)/TZ-IT)']-E_all['E(DLPNO-CCSD(T)/CC-PVTZ)']
                E_SO = E_all['E(DKH correction)']
                E_r = E_all['E(DLPNO-CCSD(T)/CBS)'] + E_CV + E_IT + E_SO
            else:
                E_r = E_all['E']
            H_r = (E_r + E_all['Hcorr'])*eh_to_cal
            
            return H_r
        
        self.drH = []
        self.dfH = []
        self.u = []
        for r in self.all_species:
            E_all = {}
            read_energies(E_all, r)
            read_Hcorr(E_all, r)

            drH = calc_drH(E_all)
            self.drH.append(drH)
            
            if r != self.target:
                self.dfH.append(r['dfH'] - drH)
                self.u.append(r['u'])
            else:
                self.dfH.append(-drH)
                self.u.append(0)

        self.drH = np.array(self.drH)
        self.dfH = np.array(self.dfH)
        self.u = np.array(self.u)
    
    def run(self, out_dir=None, optimize=False, minimize=True, dfH_thres=0.5, min_ref=8):
        dfH, u = self.calc(minimize=minimize)

        if out_dir is not None:
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            f = open(out_dir + self.target['xyz'].split('/')[-1].replace('.xyz', '.sgr'), 'w+')
        else:
            f = None

        if optimize:
            print('dfH\t', 'u\t', 'grad', 'excluded', file=f, sep='\t')
            to_exclude = []
            while (np.linalg.norm(self.dfH_grad) > dfH_thres 
                   and len(self.get_basis()) - len(to_exclude) > min_ref):
                e = np.argmax(np.abs(self.dfH_grad[1:]))
                
                to_exclude.append(e)
                to_exclude.sort()
                
                dfH, u = self.calc(to_exclude, minimize=minimize)
                
                if f is not None:
                    print(np.round(dfH, 3), np.round(u, 3), 
                          np.round(np.linalg.norm(self.dfH_grad), 3), 
                          self.vectorizer.species_to_name(e), 
                          file=f, sep='\t')
            
            self.excluded = to_exclude
            
        if f is not None:
            print('\nFinal: ', np.round(dfH, 3), np.round(u, 3), file=f, sep='\t')
            f.close()
        
        return dfH, u
    
    def calc(self, to_exclude=[], minimize=False):
        A = np.delete(self.get_basis()[1:].T, to_exclude, axis=1)
        b = self.get_basis()[0]
        NS = sp.linalg.null_space(A)
        
        if minimize:
            U_inv = np.linalg.pinv(np.diag(np.delete(self.u[1:], to_exclude)))
            x0 = U_inv@np.linalg.lstsq(A@U_inv, b, rcond=-1)[0]
        else:
            x0 = np.linalg.lstsq(A, b, rcond=-1)[0]
        
        rxn = np.r_[-1, self._fill_zeros(x0, to_exclude)]
        dirs = np.r_[np.zeros(NS.shape[1])[None], self._fill_zeros(NS, to_exclude)]
        dfH, self.dfH_grad = self.evaluate(self.dfH, rxn, dirs)
        u = np.linalg.norm(np.diag(self.u)@rxn)
        
        self.reaction = rxn
        self.directions = dirs
        
        return dfH, u
    
    def evaluate(self, func, x0, dirs):
        y = func.dot(x0)
        grad = dirs.dot(np.linalg.inv(dirs.T.dot(dirs))).dot(dirs.T).dot(func) # projection onto subspace
        return y, grad
    
    @staticmethod
    def _fill_zeros(array, at, axis=0):
        if len(at) > 0:
            return np.insert(array, np.array(at) - np.arange(len(at)), 0, axis)
        return array
