import tkinter as tk
from tkinter import messagebox, simpledialog, font, ttk
import json
import os

class BookStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Bookiestore Pro - Toko Buku Digital")
        self.root.geometry("800x600")
        self.root.configure(bg="#90d4ff")
        
        # Data buku
        self.daftar_buku = []
        self.load_data()
        
        # Fonts
        self.judul_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.label_font = font.Font(family="Arial", size=10)
        self.button_font = font.Font(family="Arial", size=10, weight="bold")
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Label(self.root, text="📚 Bookiestore Pro", font=self.judul_font, 
                         bg="#ebebeb", fg="#333")
        header.pack(pady=10)
        
        # Search Frame
        search_frame = tk.Frame(self.root, bg="#eca8e0")
        search_frame.pack(pady=5)
        
        tk.Label(search_frame, text="Cari Buku:", font=self.label_font, bg="#f4f4f4").grid(row=0, column=0, padx=5)
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_books)
        
        search_btn = tk.Button(search_frame, text="🔍 Cari", command=self.search_books, 
                             bg="#2196F3", fg="white", font=self.button_font)
        search_btn.grid(row=0, column=2, padx=5)
        
        # Frame Input
        frame_input = tk.Frame(self.root, bg="#f4f4f4")
        frame_input.pack(pady=10)
        
        tk.Label(frame_input, text="Judul Buku:", font=self.label_font, bg="#f4f4f4").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_judul = tk.Entry(frame_input, width=40)
        self.entry_judul.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_input, text="Penulis:", font=self.label_font, bg="#f4f4f4").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_penulis = tk.Entry(frame_input, width=40)
        self.entry_penulis.grid(row=1, column=1, padx=5)
        
        tk.Label(frame_input, text="Harga (Rp):", font=self.label_font, bg="#f4f4f4").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.entry_harga = tk.Entry(frame_input, width=40)
        self.entry_harga.grid(row=2, column=1, padx=5)
        
        # Frame Tombol
        frame_tombol = tk.Frame(self.root, bg="#f4f4f4")
        frame_tombol.pack(pady=5)
        
        tk.Button(frame_tombol, text="➕ Tambah Buku", command=self.tambah_buku, 
                bg="#4CAF50", fg="white", font=self.button_font, width=18).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame_tombol, text="✏️ Ubah Buku", command=self.ubah_buku, 
                bg="#FFC107", fg="black", font=self.button_font, width=18).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_tombol, text="❌ Hapus Buku", command=self.hapus_buku, 
                bg="#F44336", fg="white", font=self.button_font, width=18).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(frame_tombol, text="💾 Simpan Data", command=self.save_data, 
                bg="#673AB7", fg="white", font=self.button_font, width=18).grid(row=0, column=3, padx=5, pady=5)
        
        # Treeview untuk menampilkan buku
        self.tree = ttk.Treeview(self.root, columns=("Judul", "Penulis", "Harga"), show="headings", height=15)
        self.tree.heading("Judul", text="Judul Buku")
        self.tree.heading("Penulis", text="Penulis")
        self.tree.heading("Harga", text="Harga (Rp)")
        
        self.tree.column("Judul", width=300)
        self.tree.column("Penulis", width=200)
        self.tree.column("Harga", width=100)
        
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text=f"Total Buku: {len(self.daftar_buku)}", 
                                 bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#eca8e0")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Tampilkan data awal
        self.tampilkan_buku()
        
    def tambah_buku(self):
        judul = self.entry_judul.get().strip()
        penulis = self.entry_penulis.get().strip()
        harga = self.entry_harga.get().strip()
        
        if not judul or not penulis or not harga:
            messagebox.showwarning("Peringatan", "Mohon isi semua data!")
            return
            
        try:
            harga = float(harga)
            if harga <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Harga harus berupa angka positif!")
            return

        self.daftar_buku.append({
            "judul": judul,
            "penulis": penulis,
            "harga": harga
        })
        
        self.tampilkan_buku()
        self.entry_judul.delete(0, tk.END)
        self.entry_penulis.delete(0, tk.END)
        self.entry_harga.delete(0, tk.END)
        self.update_status()
        messagebox.showinfo("Sukses", "✅ Buku berhasil ditambahkan!")
        
    def tampilkan_buku(self, buku_list=None):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Display all or filtered books
        display_list = buku_list if buku_list else self.daftar_buku
        
        for buku in display_list:
            self.tree.insert("", tk.END, values=(buku["judul"], buku["penulis"], f"Rp{buku['harga']:,.2f}"))
    
    def ubah_buku(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih buku yang ingin diubah!")
            return
            
        item = self.tree.item(selected[0])
        judul_lama = item["values"][0]
        
        # Find the book in our list
        for i, buku in enumerate(self.daftar_buku):
            if buku["judul"] == judul_lama:
                judul_baru = simpledialog.askstring("Ubah Judul", "Masukkan judul baru:", initialvalue=buku["judul"])
                if not judul_baru:
                    return
                    
                penulis_baru = simpledialog.askstring("Ubah Penulis", "Masukkan penulis baru:", initialvalue=buku["penulis"])
                if not penulis_baru:
                    return
                    
                try:
                    harga_baru = simpledialog.askstring("Ubah Harga", "Masukkan harga baru:", initialvalue=str(buku["harga"]))
                    if not harga_baru:
                        return
                    harga_baru = float(harga_baru)
                    if harga_baru <= 0:
                        raise ValueError
                except:
                    messagebox.showerror("Error", "Harga harus berupa angka positif!")
                    return

                self.daftar_buku[i] = {
                    "judul": judul_baru,
                    "penulis": penulis_baru,
                    "harga": harga_baru
                }
                
                self.tampilkan_buku()
                self.update_status()
                messagebox.showinfo("Berhasil", "✅ Buku berhasil diubah.")
                return
                
    def hapus_buku(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih buku yang ingin dihapus!")
            return
            
        item = self.tree.item(selected[0])
        judul = item["values"][0]
        
        for i, buku in enumerate(self.daftar_buku):
            if buku["judul"] == judul:
                confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus buku '{judul}'?")
                if confirm:
                    del self.daftar_buku[i]
                    self.tampilkan_buku()
                    self.update_status()
                    messagebox.showinfo("Berhasil", f"✅ Buku '{judul}' berhasil dihapus.")
                return
                
    def search_books(self, event=None):
        query = self.search_entry.get().lower()
        if not query:
            self.tampilkan_buku()
            return
            
        filtered_books = [
            buku for buku in self.daftar_buku 
            if query in buku["judul"].lower() or query in buku["penulis"].lower()
        ]
        self.tampilkan_buku(filtered_books)
        self.status_bar.config(text=f"Ditemukan {len(filtered_books)} buku dari pencarian '{query}'")
        
    def update_status(self):
        self.status_bar.config(text=f"Total Buku: {len(self.daftar_buku)}")
        
    def save_data(self):
        try:
            with open("bookstore_data.json", "w") as f:
                json.dump(self.daftar_buku, f, indent=4)
            messagebox.showinfo("Sukses", "Data berhasil disimpan ke file!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")
            
    def load_data(self):
        if os.path.exists("bookstore_data.json"):
            try:
                with open("bookstore_data.json", "r") as f:
                    self.daftar_buku = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = BookStoreApp(root)
    root.mainloop()