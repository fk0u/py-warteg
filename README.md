# Warteg Actune Self-Service Application

This repository contains a Python-based self-service application for Warteg Actune, a local Indonesian restaurant. The application allows customers to browse the menu, select food and drink items, place orders, and generate payment receipts.

## Features

- User-friendly graphical interface built with Python's Tkinter library
- Menu categorized into food and drink sections
- Ability to add or remove items from the order
- Real-time display of the selected items and total price
- Automatic calculation of change based on the payment amount
- Option to print payment receipts or save them as text files
- Storage of purchase history in a CSV file

## Installation

1. Clone the repository:
   git clone https://github.com/fk0u/py-warteg
2. Navigate to the project directory:
   cd warteg-actune-self-service
3. Install the required dependencies:
   pip install -r requirements.txt
4. Run the application:
   python app.py


## Usage

1. Launch the application by running `python app.py`
2. Enter the customer's name
3. Browse the menu and click on the desired items to add them to the order
4. To remove an item from the order, click on the item in the order list and click the "Hapus Menu" button
5. Review the selected items and total price in the order summary area
6. Enter the payment amount in the designated field
7. Click the "Bayar" button to process the payment
8. The application will display a summary of the purchase, including the change amount
9. If the "Cetak Otomatis" checkbox is selected, the payment receipt will be automatically printed
10. The purchase history will be automatically saved in the `riwayat_pembelian.csv` file

## Dependencies

- Python 3.x
- Tkinter library
- csv module
- tempfile module
- win32api module
- win32print module
- datetime module

## Contributing

Contributions to the Warteg Actune Self-Service application are welcome! If you find any bugs, have suggestions for improvements, or would like to add new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- The application was developed as a project for [Your Course/Program Name]
- Special thanks to [Contributor Names] for their valuable contributions and feedback

## Contact

For any inquiries or feedback, please contact [Your Name] at [Your Email Address].
