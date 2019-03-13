import re
import sys

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wgdi.base as base


class block_ks():
    def __init__(self, options):
        self.wgd = 1
        self.markersize = 0.5
        self.figsize = 'default'
        for k, v in options:
            setattr(self, str(k), v)
            print(str(k), ' = ', v)
        self.main()

    def main(self):
        global gff_1, gff_2, ks, colinearity
        colinearity = base.read_colinearscan(self.colinearity)
        gff_1 = pd.read_csv(self.gff1, sep='\t', header=None)
        gff_2 = pd.read_csv(self.gff2, sep='\t', header=None)
        gff_1[0] = gff_1[0].astype(str)
        gff_2[0] = gff_2[0].astype(str)
        ks = base.read_ks(self.ks)

    def block_positon(self, colinearity, loc1, loc2, ks):
        pos = []
        for block in colinearity:
            a, b, blk_ks = [], [], []
            if len(block[0]) < int(self.block_length):
                continue
            for k in block[0]:
                if (k[0] not in loc1) or (k[2] not in loc2):
                    continue
                if k[0]+","+k[2] in ks.index:
                    blk_ks.append(ks.at[str(k[0])+","+str(k[2]), 3])
                a.append(loc1[k[0]])
                b.append(loc2[k[2]])
            if len(a) == 0:
                continue
            x, y, l, h = min(a), min(b), max(a)-min(a), max(b)-min(b)
            pos.append([x, y, l, h, base.get_median(blk_ks)])
        return pos

    def plot_chr1(self, lens, gl, gl2, step, mark, name):
        gl_start, n, start_x = 0.95, 0, 0.05
        mark_y = 0.04
        align = dict(family='Times New Roman', style='normal',
                     horizontalalignment="center", verticalalignment="center")
        for k in lens.index:
            n += float(lens.at[k, 1])
            mark_new = str(mark) + str(k)
            x = gl_start - float(n) * step
            mark_x = x + 0.5 * float(lens.at[k, 1]) * step
            plt.plot([start_x, start_x + gl2], [x, x],
                     linestyle='-', color='black', linewidth=0.5)
            plt.text(mark_y, mark_x, mark_new, color='black',
                     fontsize=12, rotation=90, weight='semibold', **align)
        plt.plot([start_x, start_x + gl2], [gl_start, gl_start],
                 linestyle='-', color='black', linewidth=1)
        plt.text(mark_y - 0.02, 0.5 * (2 * gl_start - gl), name, color='black', fontsize=18, rotation=90,
                 weight='semibold', **align)

    def plot_chr2(self, lens, gl, gl2, step, mark, name):
        gl_start, n, start_x = 0.05, 0, 0.95
        mark_y = 0.96
        align = dict(family='Times New Roman', style='normal',
                     horizontalalignment="center", verticalalignment="center")
        for k in lens.index:
            n += float(lens.at[k, 1])
            mark_new = str(mark) + str(k)
            x = gl_start + float(n) * step
            mark_x = x - 0.5 * float(lens.at[k, 1]) * step
            plt.plot([x, x], [start_x, start_x - gl2],
                     linestyle='-', color='black', linewidth=0.5)
            plt.text(mark_x, mark_y, mark_new, color='black',
                     fontsize=12, rotation=0, weight='semibold', **align)
        plt.plot([gl_start, gl_start], [start_x, start_x - gl2],
                 linestyle='-', color='black', linewidth=1)
        plt.text(0.5 * (2 * gl_start + gl), mark_y + 0.02, name, color='black', fontsize=18, rotation=0,
                 weight='semibold', **align)

    def gene_location(self, gff, lens, step):
        loc_gene, dict_chr, n = {}, {}, 0
        for i in lens.index:
            dict_chr[str(i)] = n
            n += float(lens.at[i, 1])
        for k in gff.index:
            if gff.loc[k, 0] not in dict_chr:
                continue
            loc = (float(dict_chr[gff.loc[k, 0]]) +
                   float(gff.loc[k, 5])) * step
            loc_gene[gff.loc[k, 1]] = loc
        return loc_gene

    def run(self):

        lens_1 = pd.read_csv(self.lens1, sep="\t", header=None, index_col=0)
        lens_2 = pd.read_csv(self.lens2, sep="\t", header=None, index_col=0)
        gl1, gl2 = 0.92, 0.92
        if self.position == 'order':
            lens_1 = lens_1[2]
            lens_2 = lens_2[2]

        else:
            lens_1 = lens_1[1]
            lens_2 = lens_2[1]
        if re.search('\d', self.figsize):
            self.figsize = [float(k) for k in self.figsize.split(',')]
        else:
            self.figsize = np.array(
                [1, float(lens_1.sum())/float(lens_2.sum())])*10
        step1 = gl1 / float(lens_1.sum())
        step2 = gl2 / float(lens_2.sum())
        fig = plt.figure(figsize=self.figsize)
        plt.axis('off')
        self.plot_chr1(lens_1, gl1, gl2, step1, '', self.genome1_name)
        self.plot_chr2(lens_2, gl1, gl2, step2, '', self.genome2_name)
        gene_loc_1 = self.gene_location(gff_1, lens_1, step1)
        gene_loc_2 = self.gene_location(gff_2, lens_2, step2)
        pos = self.block_positon(colinearity, gene_loc_1, gene_loc_2, ks)
        for k in pos:
            y, x = 0.95-k[0]-0.5*k[2], 0.05+k[1]+0.5*k[3]
            plt.text(x, y, round(k[4], 2), color='red', fontsize=6)
        blast = pd.read_csv(self.blast, sep="\t", header=None)
        score, evalue, repnum = 200, 1e-5, 20
        blast = blast[(blast[11] >= score) & (
            blast[10] < evalue) & (blast[1] != blast[0])]
        blast = blast[(blast[0].isin(gene_loc_1.keys())) &
                      (blast[1].isin(gene_loc_2.keys()))]
        blast.drop_duplicates(subset=[0, 1], keep='first', inplace=True)
        homopairs = []
        for name, group in blast.groupby([0])[1]:
            newgroup = group.values.tolist()
            homopairs.append([name] + newgroup[:repnum])
        colors = ['red', 'blue', 'grey']
        hitnum = 4+int(self.wgd)
        x, y, colors = self.pair_positon(
            homopairs, gene_loc_1, gene_loc_2, hitnum, colors)
        plt.scatter(x, y, s=float(self.markersize), c=colors,
                    alpha=0.5, edgecolors=None, linewidths=0, marker='o')
        plt.subplots_adjust(left=0.02, right=1, top=0.98, bottom=0)
        plt.savefig(self.savefile, dpi=500)
        sys.exit(0)

    def pair_positon(self, data, loc1, loc2, hitnum, colors):
        pos1, pos2, newcolor = [], [], []
        gl_start1, gl_start2 = 0.95, 0.05
        for k in data:
            x = gl_start1 - loc1[k[0]]
            for i in range(1, len(k)):
                if i <= int(self.wgd):
                    color = colors[0]
                elif i <= hitnum:
                    color = colors[1]
                else:
                    color = colors[2]
                y = gl_start2 + loc2[k[i]]
                pos1.append(y)
                pos2.append(x)
                newcolor.append(color)
        return pos1, pos2, newcolor

    def gene_location(self, gff, lens, step):
        loc_gene, dict_chr, n = {}, {}, 0
        for i in lens.index:
            dict_chr[str(i)] = n
            n += float(lens.at[i, 1])
        for k in gff.index:
            if gff.loc[k, 0] not in dict_chr:
                continue
            loc = (float(dict_chr[gff.loc[k, 0]]) +
                   float(gff.loc[k, 5])) * step
            loc_gene[gff.loc[k, 1]] = loc
        return loc_gene
