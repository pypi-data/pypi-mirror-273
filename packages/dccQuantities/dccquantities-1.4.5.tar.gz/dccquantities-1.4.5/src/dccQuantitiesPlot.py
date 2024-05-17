# This file is part of dccQuantities (https://gitlab1.ptb.de/digitaldynamicmeasurement/dccQuantities)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB), Thomas Bruns(PTB)]
# (PTB) Physikalisch Technsiche Bundesanstalt, Bundesallee 100, 38116 Braunschweig, Germany
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from copy import copy
import numpy as np
import pandas as pd
from pylatexenc.latexencode import unicode_to_latex

try:
    from bokeh.layouts import column, row
    from bokeh.models import ColumnDataSource, Ellipse, RadioButtonGroup, DataTable, TableColumn, Div
    from bokeh.plotting import figure
except ImportError:
    raise ImportError(
        "Please install bokeh~=3.0.3 in order to use the MultiVectorPlot module."
    )

# tab10 colors see https://stackoverflow.com/questions/64369710/what-are-the-hex-codes-of-matplotlib-tab10-palette
tab10ColorsHEX = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
    "#d62728",
]  # tab:red is last element now


def getTab10ColorFromInt(index):
    return tab10ColorsHEX[int(index) % 10]


class dccQuantityTablePlot:
    def __init__(self, quantTab, colors=None,width=1800):
        self.quntTab = copy(quantTab)
        self.quantityNames = self.quntTab.valueQuantityNames
        self.indexQuantityNames = self.quntTab.indexQuantityNames
        self.axisLogLin = "log"
        self.selectedIndex = 0
        self.guiElements = []
        self.figures = []
        self.width=width
        self.plotsGenerated = False
        self.lang = self.quntTab.language[0]
        if colors == None:
            self.tableColors = {}
            for idx, qn in enumerate(
                    self.quntTab.valueQuantityNames + self.quntTab.indexQuantityNames
            ):
                self.tableColors[qn] = tab10ColorsHEX[idx % 10]
        else:
            self.tableColors = colors
        try:
            dscpText=self.quntTab.multiLangDscp[self.lang]
        except:
            dscpText=""

        radioButtonGroups = []
        # RadioButtonGroup to select current index
        self.indexSelectorRadioButtonGroup = RadioButtonGroup(
            labels=self.indexQuantityNames, active=0
        )
        radioButtonGroups.append(self.indexSelectorRadioButtonGroup)
        self.indexSelectorRadioButtonGroup.on_change(
            "active", self.indexSelectionCallback
        )
        # RadioButtonGroup to toggle lin or log axis
        self.linLogSelectorRadioButtonGroup = RadioButtonGroup(
            labels=["linear", "log"], active=1
        )
        radioButtonGroups.append(self.linLogSelectorRadioButtonGroup)
        self.linLogSelectorRadioButtonGroup.on_change(
            "active", self.linLogSelectionCallback
        )
        self.langRadioButtonGroup = RadioButtonGroup(labels=self.quntTab.language, active=0)
        self.langRadioButtonGroup.on_change("active", self.langSelectionCB)
        radioButtonGroups.append(self.langRadioButtonGroup)
        self.guiElements.append(row(children = radioButtonGroups))

        self.dscpDiv = Div(text=dscpText)
        self.guiElements.append(self.dscpDiv)
        self.generatePlots()
        self.fillPlots()

        self.tableDataFrame=pd.concat(self.quntTab.dump_pdDataFrames())
        idx={}
        for Ci in self.tableDataFrame.columns:
             idx[Ci]=self.tableDataFrame[Ci]['quantity']
        self.tableDataFrame.rename(columns=idx,inplace=True)
        self.tabDataSource = ColumnDataSource(data=self.tableDataFrame) #ColumnDataSource(self.tableDataFrame)
        self.columns = []
        for Ci in self.tableDataFrame.columns:
            print(Ci)
            self.columns.append(TableColumn(field=Ci, title=Ci))
        self.data_table = DataTable(source=self.tabDataSource, columns=self.columns, width=self.width, height=600)
        self.guiElements.append(self.data_table)

        self.widget = column(self.guiElements)

    def indexSelectionCallback(self, attr, old, new):
        self.selectedIndex = new
        self.fillPlots()
        #self.updateTabel()

    def linLogSelectionCallback(self, attr, old, new):
        self.axisLogLin = self.linLogSelectorRadioButtonGroup.labels[new]
        self.generatePlots()
        self.fillPlots()
        self.widget.children = self.guiElements
        self.updateTabel()

    def langSelectionCB(self, attr, old, new):
        self.lang = self.langRadioButtonGroup.labels[new]
        self.generatePlots()
        self.fillPlots()
        self.widget.children = self.guiElements
        try:
            dscpText=self.quntTab.multiLangDscp[self.lang]
        except:
            dscpText=""
        self.dscpDiv.text=dscpText
        self.updateTabel()

    def generatePlots(self):
        if not self.plotsGenerated:
            for count, name in enumerate(self.quantityNames):
                label = unicode_to_latex(self.quntTab[name].multilangnames[self.lang])
                figureTitle = self.quntTab[name]["unit"].toLatex(prefix=r"\text{" + label + r" in }\\")
                if count == 0:
                    fig = figure(
                        width=self.width,
                        height=400,
                        background_fill_color="#fafafa",
                        title=figureTitle,
                        title_location="left",
                        x_axis_type=self.axisLogLin,
                    )
                else:
                    fig0IDX = self.guiElements.index(self.figures[0])
                    fig = figure(
                        width=self.width,
                        height=400,
                        background_fill_color="#fafafa",
                        x_range=self.guiElements[fig0IDX].x_range,
                        title=figureTitle,
                        title_location="left",
                        x_axis_type=self.axisLogLin,
                    )
                self.guiElements.append(fig)
                self.figures.append(fig)
            indexLatexStr = self.quntTab["index"][self.selectedIndex]["unit"].toLatex(prefix=r"\text{" + label + " in }")
            self.figures[-1].xaxis.axis_label = indexLatexStr
            self.plotsGenerated = True
        else:
            for count, name in enumerate(self.quantityNames):
                label = unicode_to_latex(self.quntTab[name].multilangnames[self.lang])
                figureTitle = self.quntTab[name]["unit"].toLatex(prefix=r"\text{" + label + r" in }\\")
                if count == 0:
                    fig = figure(
                        width=self.width,
                        height=400,
                        background_fill_color="#fafafa",
                        title=figureTitle,
                        title_location="left",
                        x_axis_type=self.axisLogLin,
                    )
                else:
                    fig0IDX = self.guiElements.index(self.figures[0])
                    fig = figure(
                        width=self.width,
                        height=400,
                        background_fill_color="#fafafa",
                        x_range=self.guiElements[fig0IDX].x_range,
                        title=figureTitle,
                        title_location="left",
                        x_axis_type=self.axisLogLin,
                    )
                figIDX=self.guiElements.index(self.figures[count])
                self.guiElements[figIDX] = fig
                self.figures[count] = fig
            quant = self.quntTab["index"][self.selectedIndex].multilangnames[self.lang]
            indexLatexStr = self.quntTab["index"][self.selectedIndex]["unit"].toLatex(prefix=r"\textbf{" + unicode_to_latex(quant) + " in }")
            self.figures[-1].xaxis.axis_label = indexLatexStr

    def fillPlots(self):
        if not self.plotsGenerated:
            self.generatePlots()
            raise RuntimeWarning("Generating plots before populating")
        for count, name in enumerate(self.quantityNames):
            label = self.quntTab[name].multilangnames[self.lang]
            color = self.tableColors[name]
            fig = self.figures[count]
            fig.renderers = []
            fig.circle(
                self.quntTab["index"][self.selectedIndex]["values"],
                self.quntTab[name]["values"],
                legend_label=label,
                size=12,
                color=color,
                alpha=0.8,
            )
            if not all(np.isnan(self.quntTab[name]["uncer"])):
                # create the coordinates for the error bars
                xs = []
                ys = []
                err_xs = []
                err_ys = []
                for x, y, yerr, xerr in zip(
                    self.quntTab["index"][self.selectedIndex]["values"],
                    self.quntTab[name]["values"],
                    np.nan_to_num(self.quntTab[name]["uncer"]),
                    np.nan_to_num(self.quntTab["index"][self.selectedIndex]["uncer"]),
                ):
                    xs.append((x, x))
                    ys.append((y, y))
                    err_xs.append((x - xerr, x + xerr))
                    err_ys.append((y - yerr, y + yerr))
                # plot them
                fig.multi_line(
                    xs=xs, ys=err_ys, color=color, legend_label="uncer. " + label
                )
                fig.multi_line(xs=err_xs, ys=ys, color=color)
                source = ColumnDataSource(
                    dict(
                        x=self.quntTab["index"][self.selectedIndex]["values"],
                        y=self.quntTab[name]["values"],
                        w=2.0
                        * np.nan_to_num(self.quntTab["index"][self.selectedIndex]["uncer"]),
                        h=2.0 * np.nan_to_num(self.quntTab[name]["uncer"]),
                    )
                )
                glyph = Ellipse(
                    x="x",
                    y="y",
                    width="w",
                    height="h",
                    fill_color=color,
                    fill_alpha=0.5,
                )
                fig.add_glyph(source, glyph)
            quant = unicode_to_latex(
                self.quntTab["index"][self.selectedIndex].multilangnames[self.lang]
            )
            self.figures[-1].xaxis.axis_label = self.quntTab["index"][self.selectedIndex]["unit"].toLatex(prefix=r"\textbf{" + quant + r" in }")

    def updateTabel(self):
        oldTabelIDX=self.guiElements.index(self.data_table)
        idx = {}
        for Ci in self.tableDataFrame.columns:
             idx[Ci]=self.tableDataFrame[Ci]['quantity']
        self.tableDataFrame.rename(columns=idx,inplace=True)
        self.tabDataSource = ColumnDataSource(data=self.tableDataFrame) #ColumnDataSource(self.tableDataFrame)
        self.columns = []
        for Ci in self.tableDataFrame.columns:
            print(Ci)
            self.columns.append(TableColumn(field=Ci, title=Ci))
        print("OLD TAB"+str(self.data_table))
        self.data_table = DataTable(source=self.tabDataSource, columns=self.columns, width=self.width, height=400)
        print("NEW TAB" + str(self.data_table))
        self.guiElements[oldTabelIDX]=self.data_table

        # self.tabDataSource.source.data=self.tableDataFrame #ColumnDataSource(self.tableDataFrame)
        # self.data_table.columns = self.columns
