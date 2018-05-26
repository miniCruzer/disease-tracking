# This file is part of disease-tracking.

# disease-tracking is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# disease-tracking is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with disease-tracking.  If not, see <http://www.gnu.org/licenses/>.

import csv

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import (QAbstractItemView, QFileDialog, QMainWindow,
                             QMessageBox, QProgressDialog)

from .ui.mainwindow import Ui_MainWindow

HEADERS = ("ID", "Disease Code", "Disease Description", "Patient Count")

__version__ = "0.0.1"

class MainWindow(QMainWindow, Ui_MainWindow):
    """Program Main Window."""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        if not QSqlDatabase.isDriverAvailable("QSQLITE"):
            QMessageBox.critical(self, "Driver Error",
                                 "SQLite3 driver not available on this system")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("data.db")
        self.model = QSqlTableModel(self, self.db)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.actionImport.triggered.connect(self.import_csv)
        self.filterEdit.textEdited.connect(self.filter_rows)
        self.actionAbout.triggered.connect(self.about_dialog)
        self.addBtn.clicked.connect(self.insert_record)
        self.saveBtn.clicked.connect(self.commit_changes)
        self.undoBtn.clicked.connect(self.model.revertAll)
        self.delBtn.clicked.connect(self.delete_selected_rows)
        self.incBtn.clicked.connect(self.increment_selected)
        self.decBtn.clicked.connect(self.decrement_selected)
        self.init_db()

    def init_db(self):
        """Initialize the database connection and model view."""
        if not self.db.open():
            QMessageBox.critical(self, "Database connection error",
                                 self.db.lastError().text())
            return

        self.create_db()

        self.model.setTable("diseases")
        self.model.select()

        # Qt lazily loads data, so force it to load all at once
        while self.model.canFetchMore():
            self.model.fetchMore()

        if self.model.lastError().isValid():
            QMessageBox.critical(self, "Select Error",
                                 self.model.lastError().text())
        # hide primary key
        self.table.hideColumn(0)

        # set prettier column labels
        for i, header in enumerate(HEADERS):
            self.model.setHeaderData(i, Qt.Horizontal, header)

        # fit the row width to the contents size
        self.table.resizeColumnsToContents()

    def create_db(self):
        """Create the necessary table if needed."""
        query = QSqlQuery(self.db)
        query.exec_("""
        CREATE TABLE IF NOT EXISTS
            "diseases" ( `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                         `code` TEXT NOT NULL UNIQUE,
                         `name` TEXT NOT NULL UNIQUE,
                         `pcount` INTEGER NOT NULL DEFAULT 0 ) """)

        if query.lastError().isValid():
            QMessageBox.critical(self, "Query Error",
                                 query.lastError().text())


    def import_csv(self):
        """Import a CSV list of diseases.

        Column 0 should be the alphanumeric disease code, and Column 1 should
        be a name or description of the disease."""

        name = QFileDialog.getOpenFileName(self,
                                           "Import CSV", "",
                                           "Comma Separated Values (*.csv);;"
                                           "All Files (*.*)")
        if not name[0]:
            return  # user canceled

        filename = name[0]

        with open(filename, "r") as csvfile:

            reader = csv.reader(csvfile)

            # collect full row count for progress bar, then reset the file
            row_count = sum(1 for row in reader)
            csvfile.seek(0)

            progress = QProgressDialog("Importing data ...", "Abort", 0,
                                       row_count, self)
            progress.setWindowTitle("Data Import Progress")
            progress.setWindowModality(Qt.WindowModal)

            for i, row in enumerate(reader):
                progress.setValue(i)
                if progress.wasCanceled():
                    break

                query = QSqlQuery(self.db)
                query.prepare("INSERT INTO `diseases` (code, name) VALUES "
                              "(:code, :name)")
                query.bindValue(":code", row[0])
                query.bindValue(":name", row[1])
                query.exec_()

                if query.lastError().isValid():
                    QMessageBox.critical(self, "Query Error",
                                         query.lastError().text())
                    break

            progress.setValue(row_count)

        self.model.select()
        self.table.resizeColumnsToContents()

    def filter_rows(self, text):
        """Loop through all rows, and see if "text" matches the row name."""
        self.model.setFilter(f"name LIKE '%{text}%' OR code LIKE '%{text}%'")

    def insert_record(self):
        """Append a record to the end of the model."""
        if (not self.model.insertRecord(-1, self.model.record())
                and self.model.lastError().isValid()):
            QMessageBox.critical(self, "Insert Failed",
                                 self.model.lastError().text())
        else:
            self.table.scrollToBottom()

    def prompt_save_changes(self):
        """Ask the user if they'd like to save changes."""
        if self.model.isDirty():
            answer = QMessageBox.question(self,
                "Commit Changes?", "There are pending changes that have not "
                "been commited to the database. Would you like to commit "
                "now?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if answer == QMessageBox.Yes:
                self.model.submitAll()
                return QMessageBox.Yes
            elif answer == QMessageBox.No:
                self.model.revertAll()
                return QMessageBox.No
            elif answer == QMessageBox.Cancel:
                return QMessageBox.Cancel

    def delete_selected_rows(self):
        """Delete the selected rows from the model."""
        delete_rows = []
        for index in self.table.selectedIndexes():
            if index.row() not in delete_rows:
                delete_rows.append(index.row())

        nrecords = len(delete_rows)
        plural = 'record' if len(delete_rows) is 1 else 'records'


        QMessageBox.question(self, "Confirm Delete",
                             f"You are about to delete <b>{nrecords}</b> "
                             f"{plural}. Continue?<br>")

        for row in delete_rows:
            if not self.model.removeRow(row):
                # this will be annoying!
                QMessageBox.critical(self, "Delete Error",
                                     self.model.lastError().text())

    def commit_changes(self):
        if not self.model.isDirty():
            self.statusBar().showMessage("No changes to save.", 1500)
            return

        self.model.submitAll()
        self.statusBar().showMessage("Changes written to database.", 1500)
        self.model.select()

    def closeEvent(self, event):
        """Override the app close event in case there are unsaved changes."""
        if self.prompt_save_changes() == QMessageBox.Cancel:
            event.ignore()
            return

        self.model.clear()
        self.db.close()

    def selected_rows(self) -> set:
        """Get a set of selected rows."""
        selected_rows = set()

        for index in self.table.selectedIndexes():
            selected_rows.add(index.row())

        return selected_rows

    def increment_selected(self):
        """Increment the 'pcount' column of the selected row(s)."""
        for row in self.selected_rows():
            rec = self.model.record(row)  # type: QSqlRecord
            try:
                rec.setValue("pcount", rec.value("pcount") + 1)
            except TypeError:
                QMessageBox.critical(self, "Invalid Data", "Invaild <b>Patient"
                                     " Count</b> value for <b>"
                                     f"{rec.value('code')}</b>.<br>"
                                     "Must be an integer.")
                break

            self.model.setRecord(row, rec)
            self.commit_changes()


    def decrement_selected(self):
        """Decrement the 'pcount' column of the selected row(s)."""
        for row in self.selected_rows():
            rec = self.model.record(row)  # type: QSqlRecord
            try:
                rec.setValue("pcount", rec.value("pcount") - 1)
            except TypeError:
                QMessageBox.critical(self, "Invalid Data", "Invaild <b>Patient"
                                     " Count</b> value for <b>"
                                     f"{rec.value('code')}</b>.<br>"
                                     "Must be an integer.")
                break
            self.model.setRecord(row, rec)
            self.commit_changes()

    def about_dialog(self):
        """Trigger the About dialog."""
        QMessageBox.about(self, "About", "<a href='https://github.com/miniCruz"
                          "er/disease-tracking'>Disease Tracking</a>, v{} <br>"
                          "Copyright &copy; 2018 Samuel Hoffman<br>"
                          "Distributed under the GNU GPLv3 License<br><br> "
                          'Written with <font color="red">❤</font>'
                          " for Hadi Faour".format(__version__))
