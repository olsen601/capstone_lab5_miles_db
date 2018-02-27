import sqlite3

db_url = 'mileage.db'   # Assumes the table miles have already been created.

"""
    Before running this test, create test_miles.db
    Create expected miles table
    create table miles (vehicle text, total_miles float);
"""

class MileageError(Exception):
    pass

class SearchError(Exception):
    pass

def add_miles(vehicle, new_miles):
    '''If the vehicle is in the database, increment the number of miles by new_miles
    If the vehicle is not in the database, add the vehicle and set the number of miles to new_miles
    If the vehicle is None or new_miles is not a positive number, raise MileageError
    '''
    vehicle = (vehicle).upper()

    if not vehicle:
        raise MileageError('Provide a vehicle name')
    if not isinstance(new_miles, (int, float))  or new_miles < 0:
        raise MileageError('Provide a positive number for new miles')

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    rows_mod = cursor.execute('UPDATE MILES SET total_miles = total_miles + ? WHERE vehicle = ?', (new_miles, vehicle))
    if rows_mod.rowcount == 0:
        cursor.execute('INSERT INTO MILES VALUES (?, ?)', (vehicle, new_miles))
    conn.commit()
    conn.close()


def search(vehicle):
    '''Find vehicle and display mileage'''
    vehicle = (vehicle).upper()

    if not vehicle:
        raise SearchError('Provide a vehicle name')

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    find = cursor.execute('SELECT total_miles FROM MILES WHERE vehicle = ?', (vehicle,))
    found = find.fetchone()
    return found


def ui():
    print('''
    Menu
    1) Add or Update Vehicle Mileage
    2) Search For vehicle
    q) Quit
    ''')

    choice = input('Enter a Menu Selection: ')

    return choice


def main():

    choice = None
    quit = 'q'

    while choice != quit:

        choice = ui()

        if choice == '1':
            vehicle = input('Enter vehicle name:')
            miles = float(input('Enter new miles for %s: ' % vehicle)) ## TODO input validation
            add_miles(vehicle, miles)

        elif choice == '2':
            vehicle = input('Enter vehicle name:')
            miles = search(vehicle)
            if miles is not None:
                print(miles[0])


if __name__ == '__main__':
    main()
