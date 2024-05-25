import tkinter as tk
from tkinter import ttk
import csv
from datetime import datetime

class RiwayatPembelianApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Riwayat Pembelian Warteg Actune")
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("Tanggal", "Nama Pelanggan", "Total Harga"))
        self.tree.heading("Tanggal", text="Tanggal")
        self.tree.heading("Nama Pelanggan", text="Nama Pelanggan")
        self.tree.heading("Total Harga", text="Total Harga")
        self.tree.pack(pady=20)
        
        self.tree.bind("<Double-1>", self.show_detail)
        
        self.total_penghasilan_label = ttk.Label(self.root, text="Total Penghasilan: Rp0", font=("Arial", 12, "bold"))
        self.total_penghasilan_label.pack(pady=10)
    
    def load_data(self):
        try:
            with open("riwayat_pembelian.csv", "r") as file:
                reader = csv.reader(file)
                
                total_penghasilan = 0
                
                for row in reader:
                    tanggal = row[0]
                    nama_pelanggan = row[1]
                    total_harga = int(row[2])
                    
                    self.tree.insert("", "end", values=(tanggal, nama_pelanggan, total_harga))
                    
                    total_penghasilan += total_harga
                
                self.total_penghasilan_label.config(text=f"Total Penghasilan: Rp{total_penghasilan}")
        except FileNotFoundError:
            pass
    
    def show_detail(self, event):
        item = self.tree.selection()[0]
        tanggal, nama_pelanggan, _ = self.tree.item(item, "values")
        
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Detail Pembelian - {nama_pelanggan}")
        
        detail_text = tk.Text(detail_window, height=10, width=40)
        detail_text.pack(pady=10)
        
        try:
            with open("riwayat_pembelian.csv", "r") as file:
                reader = csv.reader(file)
                
                for row in reader:
                    if row[0] == tanggal and row[1] == nama_pelanggan:
                        detail_text.insert(tk.END, f"Tanggal: {row[0]}\n")
                        detail_text.insert(tk.END, f"Nama Pelanggan: {row[1]}\n")
                        detail_text.insert(tk.END, f"Total Harga: Rp{row[2]}\n")
                        detail_text.insert(tk.END, "Pesanan:\n")
                        
                        pesanan = eval(row[3])
                        for menu, jumlah in pesanan.items():
                            detail_text.insert(tk.END, f"{jumlah}x {menu}\n")
                        
                        break
        except FileNotFoundError:
            pass
        
        detail_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
app = RiwayatPembelianApp(root)
root.mainloop()