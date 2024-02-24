# This Python file uses the following encoding: utf-8
import os
import sys
import pandas as pd

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QSizePolicy, QHeaderView
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import QFile, Qt, QPointF
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPainter, QAction, QIcon, QColor
from PySide6.QtCharts import QChart, QValueAxis, QBarCategoryAxis, QLineSeries
from PySide6.QtCharts import QBarSet, QBarSeries, QChartView, QPieSeries


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.df = pd.read_csv('../Pokemon.csv')
        self.load_ui()
        self.createTableSimplificada()
        self.window.setWindowTitle("Pokémon Analytics")
        self.window.setWindowIcon(QIcon("../pokebola.png"))

        menuBar = self.window.menuBar()
        tabelasMenu = menuBar.addMenu('Tables')
        graficosMenu = menuBar.addMenu('Graphs')
        outrosMenu = menuBar.addMenu('Others')

        tabelaGeralAction = QAction(QIcon("../table.png"),
                                    'All Pokémon Data', self)
        tabelaGeralAction.triggered.connect(self.createTable)
        tabelasMenu.addAction(tabelaGeralAction)

        tabelaSimplificadaAction = QAction(QIcon("../tablet.png"),
                                           'Simplified Pokémon Data', self)
        tabelaSimplificadaAction.triggered.connect(self.
                                                   createTableSimplificada)
        tabelasMenu.addAction(tabelaSimplificadaAction)

        quantTipoAction = QAction(QIcon("../pie-chart.png"),
                                  'Number of Types', self)
        quantTipoAction.triggered.connect(self.createPieChart)
        graficosMenu.addAction(quantTipoAction)

        typeStatusAction = QAction(QIcon("../bar-chart.png"),
                                   'Status Comparison by Type', self)
        typeStatusAction.triggered.connect(self.createBar)
        graficosMenu.addAction(typeStatusAction)

        lineGrafhAction = QAction(QIcon("../line-chart.png"),
                                  'Status Comparison by Generation', self)
        lineGrafhAction.triggered.connect(self.createLine)
        graficosMenu.addAction(lineGrafhAction)

        sairAction = QAction(QIcon("../exit.png"), 'Exit', self)
        sairAction.triggered.connect(self.sairPrograma)
        outrosMenu.addAction(sairAction)

    def sairPrograma(self):
        sys.exit(app.exec())

    def createBar(self):
        df = self.df
        sets = []

        statusPorTipo = {
            'Normal': [0, 0, 0, 0, 0, 0],
            'Fighting': [0, 0, 0, 0, 0, 0],
            'Flying': [0, 0, 0, 0, 0, 0],
            'Poison': [0, 0, 0, 0, 0, 0],
            'Ground': [0, 0, 0, 0, 0, 0],
            'Rock': [0, 0, 0, 0, 0, 0],
            'Bug': [0, 0, 0, 0, 0, 0],
            'Ghost': [0, 0, 0, 0, 0, 0],
            'Steel': [0, 0, 0, 0, 0, 0],
            'Fire': [0, 0, 0, 0, 0, 0],
            'Water': [0, 0, 0, 0, 0, 0],
            'Grass': [0, 0, 0, 0, 0, 0],
            'Electric': [0, 0, 0, 0, 0, 0],
            'Psychic': [0, 0, 0, 0, 0, 0],
            'Ice': [0, 0, 0, 0, 0, 0],
            'Dragon': [0, 0, 0, 0, 0, 0],
            'Dark': [0, 0, 0, 0, 0, 0],
            'Fairy': [0, 0, 0, 0, 0, 0], }

        quantPokeTipo = {
            'Normal': [0, QColor("#c0c0b2")],
            'Fighting': [0, QColor("#a65a42")],
            'Flying': [0, QColor("#79a4ff")],
            'Poison': [0, QColor("#a85fa0")],
            'Ground': [0, QColor("#eecd5b")],
            'Rock': [0, QColor("#cfbb74")],
            'Bug': [0, QColor("#c2d11e")],
            'Ghost': [0, QColor("#7b75d7")],
            'Steel': [0, QColor("#c4c1db")],
            'Fire': [0, QColor("#fb5643")],
            'Water': [0, QColor("#55aefe")],
            'Grass': [0, QColor("#8cd851")],
            'Electric': [0, QColor("#ffe640")],
            'Psychic': [0, QColor("#f660b1")],
            'Ice': [0, QColor("#95f1fe")],
            'Dragon': [0, QColor("#8974fc")],
            'Dark': [0, QColor("#856650")],
            'Fairy': [0,  QColor("#fbadff")], }

        nRows, nColumns = df.shape
        maior = int(df.iloc[0, 5])
        for i in range(nRows):
            tipoPoke = str(df.iloc[i, 2])
            for j in range(6):
                statusAtual = int(df.iloc[i, j+5])
                statusPorTipo[tipoPoke][j] += statusAtual
                quantPokeTipo[tipoPoke][0] += 1
                if maior < statusAtual:
                    maior = statusAtual

        keyNames = list(quantPokeTipo.keys())

        for name, [value, color] in quantPokeTipo.items():
            bar = QBarSet(name)
            bar.setBrush(color)
            sets.append(bar)
            for i in range(6):
                statusPorTipo[name][i] /= quantPokeTipo[name][0]

        i = 0
        for name in keyNames:
            sets[i].append(statusPorTipo[name])
            i += 1

        series = QBarSeries()

        for set in sets:
            series.append(set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Average of each Status by Primary Type")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(True)

        axisX = QBarCategoryAxis()
        axisX.append(('HP', 'Attack', 'Defense', 'SP Atk', 'SP Def', 'Speed'))

        axisY = QValueAxis()
        axisY.setTickCount(10)
        axisY.setRange(0, maior)
        axisY.setLabelFormat("%d")

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart_view = QChartView(chart)
        self.window.setCentralWidget(chart_view)

    def createLine(self):
        df = self.df

        quantPokeGen = []
        statusPorGen = []
        for i in range(6):
            statusPorGen.append([0, 0, 0, 0, 0, 0])
            quantPokeGen.append(0)

        nRows, nColumns = df.shape
        maior = int(df.iloc[0, 5])
        menor = int(df.iloc[0, 5])
        for i in range(nRows):
            genPoke = int(df.iloc[i, 11])-1
            quantPokeGen[genPoke] += 1
            for j in range(6):
                statusAtual = int(df.iloc[i, j+5])
                statusPorGen[genPoke][j] += statusAtual
                if maior < statusAtual:
                    maior = statusAtual
                elif menor > statusAtual:
                    menor = statusAtual

        series = []

        lineColor = [QColor("#8cd851"),
                     QColor("#fb5643"),
                     QColor("#c4c1db"),
                     QColor("#f660b1"),
                     QColor("#7b75d7"),
                     QColor("#79a4ff")]

        for i in range(6):
            series.append(QLineSeries())
            pen = series[i].pen()
            pen.setBrush(lineColor[i])
            pen.setWidth(2)
            series[i].setPen(pen)
            series[i].setPointsVisible()
            for j in range(6):
                series[i].append(QPointF(j, round(statusPorGen[j][i]
                                         / quantPokeGen[j])))

        chart = QChart()
        for i in range(6):
            chart.addSeries(series[i])
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Average of each Status per Generation")

        chart.legend().setVisible(True)

        chart.createDefaultAxes()

        axisX = QValueAxis()
        axisX.setRange(1, 6)
        axisX.setTickCount(6)
        axisX.setLabelFormat("%d")
        axisX.setTitleText("Generations")

        axisY = QValueAxis()
        axisY.setRange(menor, maior)
        axisY.setTickCount(6)
        axisY.setLabelFormat("%d")
        axisY.setTitleText("Value")

        chart.setAxisX(axisX)
        chart.setAxisY(axisY)

        chart.setAnimationOptions(QChart.SeriesAnimations)

        chart.legend().markers(series[0])[0].setLabel('HP')
        chart.legend().markers(series[1])[0].setLabel('Attack')
        chart.legend().markers(series[2])[0].setLabel('Defense')
        chart.legend().markers(series[3])[0].setLabel('SP Atk')
        chart.legend().markers(series[4])[0].setLabel('SP Def')
        chart.legend().markers(series[5])[0].setLabel('Speed')

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        self.window.setCentralWidget(chartView)

    def createTable(self):
        df = self.df

        table = QTableWidget()

        table.setStyleSheet('font-size: 15px;')

        # set table dimension
        nRows, nColumns = df.shape
        table.setRowCount(nRows)
        table.setColumnCount(nColumns)

        table.setHorizontalHeaderLabels(('ID', 'Name', 'Type 1', 'Type 2',
                                         'Total', 'HP', 'Attack', 'Defense',
                                         'SP Atk', 'SP Def', 'Speed',
                                         'Generation', 'Legendary'))

        # data insertion
        for i in range(table.rowCount()):
            for j in range(table.columnCount()):
                item = str(df.iloc[i, j])
                if item == 'nan':
                    item = '-'
                elif item == 'False':
                    item = 'No'
                elif item == 'True':
                    item = 'Yes'
                table.setItem(i, j, QTableWidgetItem(item))

        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.window.setCentralWidget(table)

    def createTableSimplificada(self):
        df = self.df

        table = QTableWidget()

        table.setStyleSheet('font-size: 15px;')

        # set table dimension
        nRows, nColumns = df.shape
        table.setRowCount(nRows)
        table.setColumnCount(nColumns-4)

        table.setHorizontalHeaderLabels(('Name', 'Type 1', 'Type 2',
                                         'HP', 'Attack', 'Defense',
                                         'SP Atk', 'SP Def', 'Speed'))

        columns = [1, 2, 3, 5, 6, 7, 8, 9, 10]
        # data insertion
        for i in range(table.rowCount()):
            for j in range(table.columnCount()):
                item = str(df.iloc[i, columns[j]])
                if item == 'nan':
                    item = '-'
                table.setItem(i, j, QTableWidgetItem(item))

        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.window.setCentralWidget(table)

    def createPieChart(self):
        df = self.df
        nRows, nColumns = df.shape

        quantPokeTipo = {
            'Normal': [0, QColor("#c0c0b2")],
            'Fighting': [0, QColor("#a65a42")],
            'Flying': [0, QColor("#79a4ff")],
            'Poison': [0, QColor("#a85fa0")],
            'Ground': [0, QColor("#eecd5b")],
            'Rock': [0, QColor("#cfbb74")],
            'Bug': [0, QColor("#c2d11e")],
            'Ghost': [0, QColor("#7b75d7")],
            'Steel': [0, QColor("#c4c1db")],
            'Fire': [0, QColor("#fb5643")],
            'Water': [0, QColor("#55aefe")],
            'Grass': [0, QColor("#8cd851")],
            'Electric': [0, QColor("#ffe640")],
            'Psychic': [0, QColor("#f660b1")],
            'Ice': [0, QColor("#95f1fe")],
            'Dragon': [0, QColor("#8974fc")],
            'Dark': [0, QColor("#856650")],
            'Fairy': [0,  QColor("#fbadff")], }

        for i in range(nRows):
            tipoPoke = str(df.iloc[i, 2])
            quantPokeTipo[tipoPoke][0] += 1

        series = QPieSeries()
        keyList = list(quantPokeTipo.keys())

        for (name, [value, color]) in quantPokeTipo.items():
            slice = series.append(name, value)
            slice.setBrush(color)
            slice.setLabelVisible()

        slices = series.slices()
        lenSlices = len(slices)
        for i in range(lenSlices):
            slices[i].setLabel(str(quantPokeTipo[keyList[i]][0]) +
                               " ({:.2f}%)"
                               .format(100 * slices[i].percentage()))

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Number of each first type of Pokémon')
        chart.setAnimationOptions(QChart.SeriesAnimations)
        legendsList = chart.legend().markers(series)

        i = 0
        for name in keyList:
            legendsList[i].setLabel(name)
            i += 1

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self.window.setCentralWidget(chart_view)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

    def show(self):
        self.window.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
