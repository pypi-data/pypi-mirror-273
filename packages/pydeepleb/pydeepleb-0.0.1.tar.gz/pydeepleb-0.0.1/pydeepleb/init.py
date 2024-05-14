"""
import sys
from PyQt5.QtWidgets import  QApplication,QMainWindow,QLineEdit,QPushButton,QLabel,QComboBox,QMessageBox,QFrame
from PyQt5.uic import loadUi
from connection import  connection

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("untitled.ui",self)
        self.db=connection(host="localhost",user="root",password="",database="B2")
        self.loadFoodCategory()
        self.comboBoxFoodCategory()
        self.comboBoxWaiter()
        self.Waiter()

    def comboBoxFoodCategory(self):
        try:
            query = "SELECT id, name FROM FoodCategories"
            self.db.cursor.execute(query)
            foodcategories = self.db.cursor.fetchall()
            for foodcategori in foodcategories:
                self.comboBox.addItem(foodcategori[1], foodcategori[0])

            self.comboBox.currentIndexChanged.connect(self.loadFoodCategory)

        except Exception as e:
            QMessageBox.critical(self,"", str(e))

    def loadFoodCategory(self):
        try:
            foodcategory_id = self.comboBox.currentData()
            query = "SELECT FoodName.name, FoodName.price, FoodName.ingredients FROM FoodName INNER JOIN FoodCategories ON FoodName.id_FoodCategories = FoodCategories.id WHERE FoodCategories.id = %s"
            self.db.cursor.execute(query, (foodcategory_id,))
            results = self.db.cursor.fetchall()

            # Очистка вертикального макета
            for i in reversed(range(self.verticalLayout.count())):
                widget = self.verticalLayout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            labels = ["Блюдо", "Цена", "Ингредиенты"]

            for result in results:
                for label, value in zip(labels, result):
                    labelWidget = QLabel(label, self)
                    self.verticalLayout.addWidget(labelWidget)

                    valueLabel = QLabel(str(value), self)
                    self.verticalLayout.addWidget(valueLabel)

                separator = QFrame(self)
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)
                self.verticalLayout.addWidget(separator)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def comboBoxWaiter(self):
        try:
            query = "SELECT id,secondname FROM Waiter"
            self.db.cursor.execute(query)
            waiters = self.db.cursor.fetchall()
            for waiter in waiters:
                self.comboBox_2.addItem(waiter[1], waiter[0])

            self.comboBox_2.currentIndexChanged.connect(self.Waiter)


        except Exception as e:
            QMessageBox.critical("dsd", str(e))

    def Waiter(self):
        try:
            waiter_id = self.comboBox_2.currentData()
            query = "SELECT w.secondname, w.firstname, w.lastname, o.datetime FROM Waiter w JOIN Clients c ON w.id = c.id_Waiter JOIN Ordering o ON c.id = o.id_Client  WHERE w.id = %s ORDER BY o.datetime ASC"
            self.db.cursor.execute(query,(waiter_id,))
            results = self.db.cursor.fetchall()

            for i in reversed(range(self.verticalLayout_2.count())):
                widget = self.verticalLayout_2.itemAt(i).widget()

                if widget:
                    widget.deleteLater()

            labels = ["Имя", "Фамилия", "Отчество", "Время заказа"]

            for result in results:
                for label, value in zip(labels, result):
                    labelWidget = QLabel(label, self)
                    self.verticalLayout_2.addWidget(labelWidget)

                    valueLabel = QLabel(str(value), self)
                    self.verticalLayout_2.addWidget(valueLabel)

        except Exception as e:
            QMessageBox.critical("fdf", f"{str(e)}")

class Admin(QMainWindow):
    def __init__(self):
        super(Admin, self).__init__()
        loadUi("Admin.ui", self)
        self.db = connection(host="localhost", user="root", password="", database="B2")
        self.comboBox_FoodCategory()
        self.loadFoodCategory()
        self.pushButton.clicked.connect(self.SaveFoodCategory)
        self.comboBox_Category()
        self.addFoodCategory()
        self.pushButton_2.clicked.connect(self.saveFoodCategory)
        self.setupDeleteFoodName()

    def comboBox_FoodCategory(self):
        try:
            query = "SELECT id, name FROM FoodName"
            self.db.cursor.execute(query)
            FoodCategories = self.db.cursor.fetchall()
            for FoodCategori in FoodCategories:
                self.comboBox.addItem(FoodCategori[1], FoodCategori[0])

            self.comboBox.currentIndexChanged.connect(self.loadFoodCategory)
            self.comboBox.currentIndexChanged.connect(self.setupDeleteFoodName)

        except Exception as e:
            QMessageBox.critical("hh", str(e))
    def loadFoodCategory(self):
        try:
            FoodCategory_id = self.comboBox.currentData()
            query = "SELECT name,price,ingredients FROM FoodName WHERE id=%s"
            self.db.cursor.execute(query,(FoodCategory_id,))
            result = self.db.cursor.fetchone()

            if result:
                labels = ["Имя","Цена","Ингредиенты"]

                for i in reversed(range(self.verticalLayout.count())):
                    widget = self.verticalLayout.itemAt(i).widget()
                    if widget:
                        widget.deleteLater()


                self.lineEditss = []

                for label, value in zip(labels, result):
                    labelWidget = QLabel(label, self)
                    self.verticalLayout.addWidget(labelWidget)

                    newLineEdit = QLineEdit(str(value), self)
                    self.verticalLayout.addWidget(newLineEdit)
                    self.lineEditss.append(newLineEdit)
        except Exception as e:
            QMessageBox.critical(self, "qq", str(e))

    def SaveFoodCategory(self):
        try:
            FoodCategory_id = self.comboBox.currentData()
            data = [lineEdit.text() for lineEdit in self.lineEditss]
            query = "UPDATE FoodName SET name=%s, price=%s, ingredients=%s WHERE id=%s"
            self.db.cursor.execute(query, (data[0],data[1], data[2], FoodCategory_id))  # Исправлено здесь
            self.db.connection.commit()

            QMessageBox.information(self, "Успешно", "Данные успешно сохранены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def addFoodCategory(self):
        try:
            labels =["Блюдо","Цена","Ингредиенты"]


            self.lineEdits =[]

            for label in labels:
                labelWidget = QLabel(self)
                labelWidget.setText(label)
                self.verticalLayout_2.addWidget(labelWidget)

                newLineEdit = QLineEdit(self)
                self.verticalLayout_2.addWidget(newLineEdit)
                self.lineEdits.append(newLineEdit)

        except Exception as e:
            QMessageBox.critical(self, "" , str(e))

    def comboBox_Category(self):
        try:
            self.comboBoxCategory = QComboBox(self)
            self.comboBoxCategory.setObjectName("comboBoxCategory")
            self.verticalLayout_2.addWidget(self.comboBoxCategory)

            query_category = "SELECT id, name FROM FoodCategories"
            self.db.cursor.execute(query_category)
            categories = self.db.cursor.fetchall()
            for categori in categories:
                self.comboBoxCategory.addItem(f"{categori[0]} - {categori[1]}")
        except Exception as e:
            QMessageBox.critical(self, "", str(e))


    def saveFoodCategory(self):
        try:
            name = self.lineEdits[0].text()
            price = self.lineEdits[1].text()
            ingredients = self.lineEdits[2].text()
            id_FoodCategories = int(self.comboBoxCategory.currentText().split()[0])

            query = "INSERT INTO FoodName (name, price ,ingredients, id_FoodCategories) VALUES(%s,%s,%s,%s)"
            self.db.cursor.execute(query, (name, price,ingredients,id_FoodCategories))
            self.db.connection.commit()

            QMessageBox.information(self,"sa","sa")
            self.close()

        except Exception as e:
            QMessageBox.critical(self,"", str(e))

    def setupDeleteFoodName(self):
        try:
            foodname_id = self.comboBox.currentData()
            query = "SELECT name,price,ingredients FROM FoodName WHERE id=%s"
            self.db.cursor.execute(query,(foodname_id,))
            result = self.db.cursor.fetchone()

            if result:
                labels = ["Имя","Цена","Ингедиенты"]

                for i in reversed(range(self.verticalLayout_3.count())):
                    widget = self.verticalLayout_3.itemAt(i).widget()

                    if widget:
                        widget.deleteLater()

                for label , value in zip(labels,result):
                    labelWidget = QLabel(self)
                    self.verticalLayout_3.addWidget(labelWidget)

                    valueLineEdit = QLineEdit(str(value), self)
                    valueLineEdit.setReadOnly(True)
                    self.verticalLayout_3.addWidget(valueLineEdit)

                deleteButton = QPushButton("dsd", self)
                deleteButton.clicked.connect(self.deleteFoodName)
                self.verticalLayout_3.addWidget(deleteButton)

        except Exception as e:
            QMessageBox.critical(self, "", str(e))

    def deleteFoodName(self):
        try:
            foodName_id = self.comboBox.currentData()
            confirm = QMessageBox.question(self,"","",QMessageBox.Yes | QMessageBox.No)

            if confirm == QMessageBox.Yes:
                query = "DELETE FROM FoodName WHERE id = %s"
                self.db.cursor.execute(query,(foodName_id,))
                self.db.connection.commit()
                QMessageBox.information(self,"","")
                self.close()
        except Exception as e:
            QMessageBox.critical(self,"", str(e))


class AdminAuto(QMainWindow):
    def __init__(self):
        super(AdminAuto, self).__init__()
        loadUi("AdminAuto.ui",self)
        self.db=connection(host="localhost",user="root",password="",database="B2")
        self.pushButton.clicked.connect(self.openMainWindow)
        self.pushButton_2.clicked.connect(self.openAdmin)

    def openAdmin(self):
        try:
            self.login_window = Admin()
            self.login_window.show()
        except Exception as e:
            QMessageBox.critical(self, "", str(e))

    def openMainWindow(self):
        try:
            self.Main_Window = MainWindow()
            self.Main_Window.show()
        except Exception as e:
            QMessageBox.critical(self, "", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminAuto()
    window.show()
    sys.exit(app.exec())
"""