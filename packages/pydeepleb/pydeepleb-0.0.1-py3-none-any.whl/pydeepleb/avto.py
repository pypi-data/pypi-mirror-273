"""
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel,QLineEdit,QMessageBox,QPushButton,QComboBox
from PyQt5.uic import loadUi
from connection import connection

class MainWindow(QMainWindow):
    def __init__(self,user_id):
        super(MainWindow, self).__init__()
        self.user_id = user_id
        loadUi("untitled.ui",self)
        self.db=connection(host="localhost",user="root",password="",database="B13")
        self.loadDoctor()
        self.pushButton.clicked.connect(self.Save)
        self.comboInfa()
        self.loadDoctorDetails()
        self.pushButton_2.clicked.connect(self.showWork)


    def loadDoctor(self):
        try:
            query = "SELECT name, fname, patronymic, education, email, password FROM Doctor WHERE id = %s"
            self.db.cursor.execute(query, (self.user_id,))
            result = self.db.cursor.fetchone()

            if result:
                labels = ["Имя", "Фамилие","Отчество","Оброзование","email","Пароль",]

                for i in reversed(range(self.verticalLayout.count())):
                    widget = self.verticalLayout.itemAt(i).widget()
                    if widget:
                        widget.deleteLater()

                self.lineEdit =[]

                for i , label in enumerate(labels):
                    labelWidget = QLabel(self)
                    labelWidget.setText(label)
                    self.verticalLayout.addWidget(labelWidget)

                    newLineEdit = QLineEdit(self)
                    newLineEdit.setText(result[i])
                    self.verticalLayout.addWidget(newLineEdit)
                    self.lineEdit.append(newLineEdit)

        except Exception as e:
            QMessageBox.critical("",f"{str(e)}")

    def Save(self):
        try:
            data = [lineEdit.text() for lineEdit in self.lineEdit]
            query = "UPDATE Doctor SET name=%s, fname=%s, patronymic=%s, education=%s, email=%s, password=%s WHERE id=%s"
            self.db.cursor.execute(query, (data[0],data[1],data[2],data[3],data[4],data[5], self.user_id))
            self.db.connection.commit()

            QMessageBox.information(self, "" ,"")
        except Exception as e:
            QMessageBox.critical(self, "" f"{str(e)}")

    def comboInfa(self):
        try:
            query = "SELECT id, name_category FROM Category"
            self.db.cursor.execute(query)
            categories = self.db.cursor.fetchall()
            for category in categories:
                self.comboBox.addItem(category[1], category[0])

            self.comboBox.currentIndexChanged.connect(self.loadDoctorDetails)


        except Exception as e:
            QMessageBox.critical(self,"", str(e))
    def loadDoctorDetails(self):
        try:
            doctor_id = self.comboBox.currentData()
            query = "SELECT Service.services, Service.price, Category.name_category FROM Service INNER JOIN Category ON Service.id_Category = %s;"
            self.db.cursor.execute(query, (doctor_id,))
            result = self.db.cursor.fetchone()

            for i in reversed(range(self.verticalLayout_2.count())):
                widget = self.verticalLayout_2.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            if result:
                labels = ["Услуга", "Цена"]  # Определите labels здесь


                self.lineEdits = []

                for label, value in zip(labels, result):
                    labelWidget = QLabel(label, self)
                    self.verticalLayout_2.addWidget(labelWidget)

                    valueLabel = QLabel(str(value), self)
                    self.verticalLayout_2.addWidget(valueLabel)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def showWork(self):
        try:
            query = "SELECT day_of_work, shift, time FROM Work_schedule WHERE id_Doctor = %s"
            self.db.cursor.execute(query, (self.user_id,))
            result = self.db.cursor.fetchall()

            if not result:
                QMessageBox.warning(self,"Информация","График работы не найден")
                return

            table_text = "График Работы:\n"
            table_text += "{:} {:} {:}\n".format("День","Смена","Время")
            for row in result:
                table_text += "{:} {:} {:}\n".format(row[0], row[1], row[2])
                QMessageBox.information(self,"График Работы", table_text)
        except Exception as e:
            QMessageBox.critical(self,"", str(e))
class Admin(QMainWindow):
    def __init__(self):
        super(Admin, self).__init__()
        loadUi("Admin.ui", self)
        self.db = connection(host="localhost", user="root", password="", database="B13")
        self.comboBox.currentIndexChanged.connect(self.loadDoctor)  # Добавление обработчика события изменения индекса
        self.comboBoxDoctor()
        self.loadDoctor()
        self.pushButton.clicked.connect(self.Save)
        self.setupDeleteDoctor()
        self.loadUnderDoctor()
        self.pushButton.clicked.connect(self.UnderSave)
        self.setupDeleteUnderDoctor()
        self.addDoctor()
        self.pushButton_3.clicked.connect(self.saveDoctor)
        self.setComboBox()

    def comboBoxDoctor(self):
        try:
            query = "SELECT id, name FROM Doctor"
            self.db.cursor.execute(query)
            doctors = self.db.cursor.fetchall()
            for doctor in doctors:
                # Добавление варианта в комбо-бокс с использованием форматирования строк
                self.comboBox.addItem(doctor[1], doctor[0])

                self.comboBox.currentIndexChanged.connect(self.setupDeleteUnderDoctor)
                self.comboBox.currentIndexChanged.connect(self.setupDeleteDoctor)

        except Exception as e:
            QMessageBox.critical(self, "", f"{str(e)}")

    def loadDoctor(self):
        try:
            doctor_id = self.comboBox.currentData()
            query = "SELECT id_Category FROM Doctor WHERE id=%s"
            self.db.cursor.execute(query, (doctor_id,))
            result = self.db.cursor.fetchone()


            if result:
                labels = ["Категория"]

                # Удаление существующих элементов
                for i in reversed(range(self.verticalLayout.count())):
                    widget = self.verticalLayout.itemAt(i).widget()
                    if widget:
                        widget.deleteLater()

                self.lineEdits = []

                for label, value in zip(labels, result):
                    labelWidget = QLabel(label, self)
                    self.verticalLayout.addWidget(labelWidget)

                    newLineEdit = QLineEdit(str(value), self)
                    self.verticalLayout.addWidget(newLineEdit)
                    self.lineEdits.append(newLineEdit)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Save(self):
        try:
            doctor_id = self.comboBox.currentData()
            data = [lineEdit.text() for lineEdit in self.lineEdits]
            query = "UPDATE Doctor SET id_Category=%s WHERE id=%s"
            self.db.cursor.execute(query, (data[0], doctor_id))
            self.db.connection.commit()

            QMessageBox.information(self, "Успешно", "Данные успешно сохранены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def setupDeleteDoctor(self):
        try:
            doctor_id = self.comboBox.currentData()
            query = "SELECT id_Category FROM Doctor WHERE id=%s"
            self.db.cursor.execute(query,(doctor_id,))
            result = self.db.cursor.fetchone()

            if result:
                # Создайте виджеты для отображения информации о докторе
                labels = ["Категория",]

                for i in reversed(range(self.verticalLayout_2.count())):
                    widget = self.verticalLayout_2.itemAt(i).widget()
                    if widget:
                        widget.deleteLater()


                for label, value in zip(labels, result):
                    labelWidget = QLabel(label, self)
                    self.verticalLayout_2.addWidget(labelWidget)

                    valueLineEdit = QLineEdit(str(value), self)
                    valueLineEdit.setReadOnly(True)
                    self.verticalLayout_2.addWidget(valueLineEdit)

                # Добавьте кнопку удаления доктора
                deleteButton = QPushButton("Удалить категорию", self)
                deleteButton.clicked.connect(self.deleteDoctor)
                self.verticalLayout_2.addWidget(deleteButton)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def deleteDoctor(self):
        try:
            doctor_id = self.comboBox.currentData()
            # Получите подтверждение от пользователя
            confirm = QMessageBox.question(self, "Подтверждение",
                                           "Вы уверены, что хотите удалить этого категорию?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                # Удалите запись о докторе из базы данных
                query = "UPDATE Doctor SET id_Category = NULL WHERE id = %s"
                self.db.cursor.execute(query, (doctor_id,))
                self.db.connection.commit()
                QMessageBox.information(self, "Успешно", "Категория успешно удален")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def loadUnderDoctor(self):
        try:
            doctor_id = self.comboBox.currentData()
            query = "SELECT id_UnderCotegor FROM Doctor WHERE id=%s"
            self.db.cursor.execute(query, (doctor_id,))
            result = self.db.cursor.fetchone()

            if result:
                labels = ["Подкатегория"]



                self.lineEdits = []

                for label, value in zip(labels, result):
                    labelWidget = QLabel(label, self)
                    self.verticalLayout_3.addWidget(labelWidget)

                    newLineEdit = QLineEdit(str(value), self)
                    self.verticalLayout_3.addWidget(newLineEdit)
                    self.lineEdits.append(newLineEdit)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def UnderSave(self):
        try:
            doctor_id = self.comboBox.currentData()
            data = [lineEdit.text() for lineEdit in self.lineEdits]
            query = "UPDATE Doctor SET id_UnderCotegor=%s WHERE id=%s"
            self.db.cursor.execute(query, (data[0], doctor_id))
            self.db.connection.commit()

            QMessageBox.information(self, "Успешно", "Данные успешно сохранены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")


    def setupDeleteUnderDoctor(self):
        try:
            doctor_id = self.comboBox.currentData()
            query = "SELECT id_UnderCotegor FROM Doctor WHERE id=%s"
            self.db.cursor.execute(query,(doctor_id,))
            result = self.db.cursor.fetchone()



            if result:
                # Создайте виджеты для отображения информации о докторе
                labels = ["Подкатегория",]

                for i in reversed(range(self.verticalLayout_4.count())):
                    widget = self.verticalLayout_4.itemAt(i).widget()
                    if widget:
                        widget.deleteLater()

                for label, value in zip(labels, result):
                    labelWidget = QLabel(label, self)
                    self.verticalLayout_4.addWidget(labelWidget)
                    valueLineEdit = QLineEdit(str(value), self)
                    valueLineEdit.setReadOnly(True)
                    self.verticalLayout_4.addWidget(valueLineEdit)

                # Добавьте кнопку удаления доктора
                deleteButton = QPushButton("Удалить подкатегорияю", self)
                deleteButton.clicked.connect(self.deleteDoctor)
                self.verticalLayout_4.addWidget(deleteButton)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def deleteDoctor(self):
        try:
            doctor_id = self.comboBox.currentData()
            # Получите подтверждение от пользователя
            confirm = QMessageBox.question(self, "Подтверждение",
                                           "Вы уверены, что хотите удалить этого подкатегорию?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                # Удалите запись о докторе из базы данных
                query = "UPDATE Doctor SET id_UnderCotegor = NULL WHERE id = %s"
                self.db.cursor.execute(query, (doctor_id,))
                self.db.connection.commit()
                QMessageBox.information(self, "Успешно", "Подгатегория успешно удален")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def addDoctor(self):
        try:
            labels = ["Имя", "Фамилия", "Отчество", "Образование", "Email", "Пароль"]

            self.lineEdits = []

            for label in labels:
                labelWidget = QLabel(self)
                labelWidget.setText(label)
                self.verticalLayout_5.addWidget(labelWidget)

                newLineEdit = QLineEdit(self)
                self.verticalLayout_5.addWidget(newLineEdit)
                self.lineEdits.append(newLineEdit)

        except Exception as e:
            QMessageBox.critical(self, "" f"{str(e)}")

    def setComboBox(self):
        try:
            self.comboBox_category = QComboBox(self)
            self.comboBox_category.setObjectName("comboBox_category")
            self.verticalLayout_5.addWidget(self.comboBox_category)

            self.comboBox_undercategory = QComboBox(self)
            self.comboBox_undercategory.setObjectName("comboBox_undercategory")
            self.verticalLayout_5.addWidget(self.comboBox_undercategory)

            self.comboBox_position = QComboBox(self)
            self.comboBox_position.setObjectName("comboBox_position")
            self.verticalLayout_5.addWidget(self.comboBox_position)

            self.comboBox_services = QComboBox(self)
            self.comboBox_services.setObjectName("comboBox_services")
            self.verticalLayout_5.addWidget(self.comboBox_services)

            query_category = "SELECT id, name_category FROM Category"
            self.db.cursor.execute(query_category)
            categories = self.db.cursor.fetchall()
            for category in categories:
                self.comboBox_category.addItem(f"{category[0]} - {category[1]}")

            query_undercategory = "SELECT id, name_under_cotegor FROM UnderCotegor"
            self.db.cursor.execute(query_undercategory)
            undercategories = self.db.cursor.fetchall()
            for undercategory in undercategories:
                self.comboBox_undercategory.addItem(f"{undercategory[0]} - {undercategory[1]}")

            query_position = "SELECT id, name_position FROM Position"
            self.db.cursor.execute(query_position)
            positions = self.db.cursor.fetchall()
            for position in positions:
                self.comboBox_position.addItem(f"{position[0]} - {position[1]}")

            query_service = "SELECT id, services FROM Service"
            self.db.cursor.execute(query_service)
            services = self.db.cursor.fetchall()
            for service in services:
                self.comboBox_services.addItem(f"{service[0]} - {service[1]}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def saveDoctor(self):
        try:
            name = self.lineEdits[0].text()
            fname = self.lineEdits[1].text()
            patronymic = self.lineEdits[2].text()
            education = self.lineEdits[3].text()
            email = self.lineEdits[4].text()
            password = self.lineEdits[5].text()
            id_Category = int(self.comboBox_category.currentText().split()[0])
            id_UnderCotegor = int(self.comboBox_undercategory.currentText().split()[0])
            id_Position = int(self.comboBox_position.currentText().split()[0])
            id_Service = int(self.comboBox_services.currentText().split()[0])

            query = "INSERT INTO Doctor (name, fname, patronymic, education, email, password, id_Category, id_UnderCotegor, id_Position, id_Service) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.db.cursor.execute(query, (
            name, fname, patronymic, education, email, password, id_Category, id_UnderCotegor, id_Position, id_Service))
            self.db.connection.commit()

            QMessageBox.information(self, "Успешно", "Доктор успешно добавлен")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
class AdminAuto(QMainWindow):
    def __init__(self):
        super(AdminAuto, self).__init__()
        loadUi("AdminAuto.ui",self)
        self.db=connection(host="localhost",user="root",password="",database="B13")
        self.pushButton.clicked.connect(self.admin)


    def admin(self):

        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        try:
            query = "SELECT id, login, password FROM Admin WHERE login=%s AND password=%s"
            self.db.cursor.execute(query, (login,password))
            result = self.db.cursor.fetchone()

            if result:
                self.close()
                self.window = Admin()
                self.window.show()

            else:
                QMessageBox.critical(self,"Ошибка","Неверный пароль или логин")


        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f" Неверный логин или пароль{str(e)}")
class Aut(QMainWindow):
    def __init__(self):
        super(Aut, self).__init__()
        loadUi("Login.ui",self)
        self.db=connection(host="localhost",user="root",password="",database="B13")
        self.pushButton.clicked.connect(self.aut)

    def aut (self):

        login = self.lineEdit.text()
        password = self.lineEdit_2.text()

        try:
            query = "SELECT id, email,password FROM Doctor WHERE email=%s AND password=%s"
            self.db.cursor.execute(query,(login,password))
            result = self.db.cursor.fetchone()

            if result:
                self.user_id =result[0]
                self.close()
                self.window = MainWindow(self.user_id)
                self.window.show()

            else:
                QMessageBox.critical(self, "Ошибка", "Неверный пароль или логин")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка" f" Произошла ошибка{str(e)}")

class Entry(QMainWindow):
    def __init__(self):
        super(Entry, self).__init__()
        loadUi("entry.ui", self)
        self.db = connection(host="localhost", user="root", password="", database="B13")
        self.pushButton.clicked.connect(self.openLoginUI)
        self.pushButton_2.clicked.connect(self.openAdmin)

    def openLoginUI(self):
        try:
            self.login_window = Aut()
            self.login_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def openAdmin(self):
        try:
            self.admin_window = AdminAuto()
            self.admin_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Entry()
    window.show()
    sys.exit(app.exec())




"""