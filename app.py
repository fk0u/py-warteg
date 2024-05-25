import tkinter as tk
from tkinter import ttk, messagebox
import tempfile
import win32api
import win32print
import csv
from datetime import datetime

class WartegActuneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warteg Actune Self-Service")
        
        self.menu_map = {
            1: {"nama": "Nasi Putih", "harga": 5000},
            2: {"nama": "Sayur Asem", "harga": 3000},
            3: {"nama": "Ayam Goreng", "harga": 10000},
            4: {"nama": "Tempe Goreng", "harga": 5000},
            5: {"nama": "Sambal", "harga": 2000},
            6: {"nama": "Telur Dadar", "harga": 3000},
            7: {"nama": "Telur Balado", "harga": 5000},
            8: {"nama": "Cah Kangkung", "harga": 4000},
            9: {"nama": "Ikan Goreng", "harga": 8000},
            10: {"nama": "Nasi Uduk", "harga": 6000},
            11: {"nama": "Mie Goreng", "harga": 7000},
            12: {"nama": "Kangkung Goreng", "harga": 4000},
            13: {"nama": "Tahu Bacem", "harga": 3000},
            14: {"nama": "Es Teh", "harga": 3000},
            15: {"nama": "Es Jeruk", "harga": 3000},
            16: {"nama": "Teh Panas", "harga": 3000},
            17: {"nama": "Kopi Hitam", "harga": 3000},
            18: {"nama": "Air Putih", "harga": 2000}
        }
        
        self.pesanan = {}
        
        self.cetak_otomatis = tk.BooleanVar()
        self.cetak_otomatis.set(True)
        
        self.create_widgets()
    
    def create_widgets(self):
        self.menu_label = ttk.Label(self.root, text="Selamat datang di Warteg Actune Self-Service!", font=("Arial", 16, "bold"))
        self.menu_label.grid(row=0, column=0, columnspan=3, pady=20)
        
        self.nama_label = ttk.Label(self.root, text="Nama Pelanggan:")
        self.nama_label.grid(row=1, column=0, padx=20, pady=5, sticky="e")
        
        self.nama_entry = ttk.Entry(self.root)
        self.nama_entry.grid(row=1, column=1, padx=20, pady=5)
        
        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ns")
        
        for i, (menu_id, menu_info) in enumerate(self.menu_map.items()):
            menu_button = ttk.Button(self.menu_frame, text=f"{menu_info['nama']} (Rp{menu_info['harga']})", width=20, command=lambda id=menu_id: self.tambah_pesanan(id))
            menu_button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
        
        self.pesanan_frame = ttk.Frame(self.root)
        self.pesanan_frame.grid(row=2, column=1, padx=20, pady=10, sticky="ns")
        
        self.pesanan_label = ttk.Label(self.pesanan_frame, text="Pesanan Anda:", font=("Arial", 14, "bold"))
        self.pesanan_label.pack(pady=10)
        
        self.pesanan_text = tk.Text(self.pesanan_frame, height=10, width=40)
        self.pesanan_text.pack(pady=5)
        
        self.pesanan_text.tag_configure("sel", background="lightblue")
        self.pesanan_text.bind("<Button-1>", self.on_pesanan_click)
        
        self.hapus_button = ttk.Button(self.pesanan_frame, text="Hapus Menu", command=self.hapus_pesanan)
        self.hapus_button.pack(pady=5)
        
        self.total_harga_label = ttk.Label(self.pesanan_frame, text="Total Harga: Rp0", font=("Arial", 12))
        self.total_harga_label.pack(pady=10)
        
        self.bayar_frame = ttk.Frame(self.root)
        self.bayar_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
        
        self.jumlah_bayar_label = ttk.Label(self.bayar_frame, text="Jumlah Bayar:")
        self.jumlah_bayar_label.pack(side=tk.LEFT, padx=5)
        
        self.jumlah_bayar_entry = ttk.Entry(self.bayar_frame, width=10)
        self.jumlah_bayar_entry.pack(side=tk.LEFT, padx=5)
        
        self.bayar_button = ttk.Button(self.bayar_frame, text="Bayar", command=self.bayar)
        self.bayar_button.pack(side=tk.LEFT, padx=5)
        
        self.cetak_otomatis_checkbutton = ttk.Checkbutton(self.bayar_frame, text="Cetak Otomatis", variable=self.cetak_otomatis)
        self.cetak_otomatis_checkbutton.pack(side=tk.LEFT, padx=5)
    
    def on_pesanan_click(self, event):
        self.pesanan_text.tag_remove("sel", "1.0", tk.END)
        self.pesanan_text.tag_add("sel", "current linestart", "current lineend")
    
    def tambah_pesanan(self, menu_id):
        menu_info = self.menu_map[menu_id]
        nama_menu = menu_info['nama']
        harga_menu = menu_info['harga']
        
        if menu_id in self.pesanan:
            self.pesanan[menu_id]['jumlah'] += 1
        else:
            self.pesanan[menu_id] = {'nama': nama_menu, 'harga': harga_menu, 'jumlah': 1}
        
        self.update_pesanan_text()
    
    def hapus_pesanan(self):
        if not self.pesanan_text.tag_ranges("sel"):
            return

        index = self.pesanan_text.index("sel.first")
        line = self.pesanan_text.get(index, f"{index} lineend")
        menu_info = line.split(" x ")
        nama_menu = menu_info[1].strip()

        for menu_id, menu_data in list(self.pesanan.items()):
            if menu_data['nama'] == nama_menu:
                if menu_data['jumlah'] > 1:
                    self.pesanan[menu_id]['jumlah'] -= 1
                else:
                    del self.pesanan[menu_id]
                break

        self.update_pesanan_text()
    
    def update_pesanan_text(self):
        self.pesanan_text.delete('1.0', tk.END)
        
        total_harga = 0
        for menu_id, menu_info in self.pesanan.items():
            nama_menu = menu_info['nama']
            harga_menu = menu_info['harga']
            jumlah_menu = menu_info['jumlah']
            
            subtotal = harga_menu * jumlah_menu
            total_harga += subtotal
            
            self.pesanan_text.insert(tk.END, f"{jumlah_menu} x {nama_menu}\t\tRp{harga_menu}\n")
        
        self.total_harga_label.config(text=f"Total Harga: Rp{total_harga}")
    
    def bayar(self):
        total_harga = sum(menu_info['harga'] * menu_info['jumlah'] for menu_info in self.pesanan.values())
        if total_harga == 0:
            messagebox.showwarning("Peringatan", "Mohon tambahkan pesanan terlebih dahulu!")
            return
        
        jumlah_bayar = int(self.jumlah_bayar_entry.get())
        
        if jumlah_bayar < total_harga:
            messagebox.showwarning("Peringatan", "Jumlah bayar tidak mencukupi!")
            return
        
        kembalian = jumlah_bayar - total_harga
        
        nama_pelanggan = self.nama_entry.get()
        
        tanggal_waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        bukti_pembayaran = f"Warteg Actune\n============\n{tanggal_waktu}\nNama Pelanggan: {nama_pelanggan}\n============\nPesanan:\n"
        
        for menu_id, menu_info in self.pesanan.items():
            nama_menu = menu_info['nama']
            jumlah_menu = menu_info['jumlah']
            
            bukti_pembayaran += f"{jumlah_menu}x {nama_menu}\n"
        
        bukti_pembayaran += f"\nTotal Harga: Rp{total_harga}\nJumlah Uang: Rp{jumlah_bayar}\nKembalian: Rp{kembalian}\n"
        bukti_pembayaran += "============\nTerimakasih telah makan di Warteg Actune\n"
        
        messagebox.showinfo("Bukti Pembayaran", bukti_pembayaran)
        
        if self.cetak_otomatis.get():
            self.cetak_bukti_pembayaran(bukti_pembayaran)
        
        self.simpan_data_pembelian(tanggal_waktu, nama_pelanggan, total_harga, self.pesanan)
        
        self.pesanan.clear()
        self.update_pesanan_text()
        self.nama_entry.delete(0, tk.END)
        self.jumlah_bayar_entry.delete(0, tk.END)
    
    def cetak_bukti_pembayaran(self, bukti_pembayaran):
        temp_file = tempfile.mktemp(".txt")
        with open(temp_file, "w") as file:
            file.write(bukti_pembayaran)
        
        win32api.ShellExecute(
            0,
            "print",
            temp_file,
            '/d:"%s"' % win32print.GetDefaultPrinter(),
            ".",
            0
        )
        
    def simpan_data_pembelian(self, tanggal, nama_pelanggan, total_harga, pesanan):
        with open("riwayat_pembelian.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([tanggal, nama_pelanggan, total_harga, pesanan])

if __name__ == "__main__":
    root = tk.Tk()
    app = WartegActuneApp(root)
    root.mainloop()