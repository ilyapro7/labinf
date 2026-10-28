import auth
import menu
import database.database as db

def main():
    db.init_db()
    while True:
        print("\n======================================")
        print("      СИСТЕМА УЧЕТА ОБОРУДОВАНИЯ   ")
        print("======================================")
        print("1. Войти в аккаунт")
        print("0. Закрыть программу")

        choice = input("Выберите действие: ")
        if choice == "1":
            login = input("Логин: ")
            password = input("Пароль: ")
            user = auth.authenticate(login, password)

            if user:
                print(f" Вход выполнен успешно!")
                if user[4] == 1:
                    menu.admin_menu(user)
                elif user[4] == 2:
                    menu.employee_menu(user)
            else:
                print(" Неверный логин или пароль!")
        elif choice == "0":
            print("Программа закрыта.")
            break


if __name__ == "__main__":
    main()

