# ==========================================
# SMARTCASHIER ID - SQLITE VERSION
# ==========================================

import sqlite3
from datetime import datetime

PPN = 0.11

# ==========================
# KONEKSI SQLITE
# ==========================
db = sqlite3.connect("tugas_project.db")
cursor = db.cursor()

# ==========================
# AUTO CREATE TABLE
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    userid TEXT PRIMARY KEY,
    password TEXT,
    nama TEXT,
    email TEXT,
    gender TEXT,
    usia INTEGER,
    pekerjaan TEXT,
    hobi TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS alamat (
    userid TEXT,
    kota TEXT,
    rt TEXT,
    rw TEXT,
    zip_code TEXT,
    latitude REAL,
    longitude REAL,
    nohp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS barang (
    kode_barang TEXT PRIMARY KEY,
    nama_barang TEXT,
    harga INTEGER,
    stok INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
    userid TEXT,
    tanggal TEXT,
    total INTEGER,
    diskon INTEGER,
    pajak INTEGER,
    grand_total INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS detail_transaksi (
    id_detail INTEGER PRIMARY KEY AUTOINCREMENT,
    id_transaksi INTEGER,
    kode_barang TEXT,
    qty INTEGER,
    subtotal INTEGER
)
""")

db.commit()

# ==========================================
# UI HELPER
# ==========================================
def header(title):
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)

def line():
    print("-" * 60)

# ==========================================
# VALIDASI EMAIL
# ==========================================
def validasi_email(email):
    if email.count("@") != 1:
        return False
    username, domain = email.split("@")
    if "." not in domain:
        return False
    if not username[0].isalnum():
        return False
    for c in username:
        if not (c.isalnum() or c in "_."):
            return False
    parts = domain.split(".")
    if len(parts) < 2 or len(parts) > 3:
        return False
    for c in parts[0]:
        if not c.isalnum():
            return False
    for ext in parts[1:]:
        if not ext.isalpha() or len(ext) > 5:
            return False
    return True

# ==========================================
# VALIDASI FLOAT
# ==========================================
def validasi_float_strict(data):
    if data.count(".") != 1:
        return False
    if data.startswith("-"):
        data = data[1:]
    kiri, kanan = data.split(".")
    if not (kiri.isdigit() and kanan.isdigit()):
        return False
    return True

# ==========================================
# REGISTER
# ==========================================
def register():

    header("REGISTER ACCOUNT")

    print("KETENTUAN USERID:")
    print("- 6 sampai 20 karakter")
    print("- Kombinasi huruf dan angka")
    print("- Tidak boleh simbol")
    line()

    while True:
        userid = input("UserId : ")

        if not userid.isalnum() or not (6 <= len(userid) <= 20):
            print("[!] Format UserId salah!")
            continue

        if not any(c.isalpha() for c in userid):
            print("[!] Harus ada huruf!")
            continue

        if not any(c.isdigit() for c in userid):
            print("[!] Harus ada angka!")
            continue

        cursor.execute("SELECT userid FROM users WHERE userid=?", (userid,))
        if cursor.fetchone():
            print("[!] UserId sudah ada!")
            continue
        break

    print("\nKETENTUAN PASSWORD:")
    print("- Minimal 8 karakter")
    print("- Mengandung angka")
    print("- Karakter khusus: / . , @ # $ %")
    line()

    while True:
        password = input("Password : ")

        if len(password) < 8:
            print("[!] Password minimal 8 karakter!")
            continue

        upper = lower = digit = special = False

        for c in password:
            if c.isupper(): upper = True
            elif c.islower(): lower = True
            elif c.isdigit(): digit = True
            elif c in "/.,@#$%": special = True

        if not upper:
            print("[!] Harus ada huruf besar!")
            continue
        if not lower:
            print("[!] Harus ada huruf kecil!")
            continue
        if not digit:
            print("[!] Harus ada angka!")
            continue
        if not special:
            print("[!] Harus ada karakter khusus (/.,@#$%)!")
            continue
        break

    while True:
        email = input("Email: ")
        if validasi_email(email):
            break
        print("[!] Email tidak valid!")

    while True:
        nama = input("Nama (alfabet): ")
        if nama.replace(" ","").isalpha():
            break
        print("[!] Nama hanya boleh alfabet!")

    while True:
        gender = input("Gender (Female/Male/Pria/Wanita): ")
        if gender.lower() in ["female","male","pria","wanita"]:
            break
        print("[!] Gender tidak valid!")

    while True:
        usia = input("Usia (17-80): ")
        if usia.isdigit() and 17 <= int(usia) <= 80:
            usia = int(usia)
            break
        print("[!] Usia harus 17-80!")

    while True:
        pekerjaan = input("Pekerjaan (alfabet): ")
        if pekerjaan.replace(" ","").isalpha():
            break
        print("[!] Pekerjaan hanya boleh alfabet!")

    while True:
        hobi = input("Hobi (lebih dari satu): ")
        h = hobi.split()
        if len(h) > 1 and all(x.isalpha() for x in h):
            break
        print("[!] Masukkan minimal 2 hobi alfabet!")

    while True:
        kota = input("Nama Kota (alfabet): ")
        if kota.replace(" ","").isalpha():
            break
        print("[!] Kota hanya boleh alfabet!")

    while True:
        rt = input("RT (angka): ")
        if rt.isdigit():
            break
        print("[!] RT hanya boleh angka!")

    while True:
        rw = input("RW (angka): ")
        if rw.isdigit():
            break
        print("[!] RW hanya boleh angka!")

    while True:
        zip_code = input("Zip Code (5 digit): ")
        if zip_code.isdigit() and len(zip_code) == 5:
            break
        print("[!] Zip Code harus 5 digit angka!")

    while True:
        lat = input("Latitude (-90 s/d 90): ")
        if validasi_float_strict(lat) and -90 <= float(lat) <= 90:
            lat = float(lat)
            break
        print("[!] Latitude tidak valid!")

    while True:
        long = input("Longitude (-180 s/d 180): ")
        if validasi_float_strict(long) and -180 <= float(long) <= 180:
            long = float(long)
            break
        print("[!] Longitude tidak valid!")

    while True:
        nohp = input("No HP (11-13 digit): ")
        if nohp.isdigit() and 11 <= len(nohp) <= 13:
            break
        print("[!] Nomor HP tidak valid!")

    while True:
        simpan = input("Simpan Data? (Y/N): ").upper()

        if simpan == "Y":
            try:
                cursor.execute("""
                    INSERT INTO users
                    (userid,password,nama,email,gender,usia,pekerjaan,hobi)
                    VALUES (?,?,?,?,?,?,?,?)
                """,(userid,password,nama,email,gender,usia,pekerjaan,hobi))

                cursor.execute("""
                    INSERT INTO alamat
                    (userid,kota,rt,rw,zip_code,latitude,longitude,nohp)
                    VALUES (?,?,?,?,?,?,?,?)
                """,(userid,kota,rt,rw,zip_code,lat,long,nohp))

                db.commit()
                print("[✓] Data berhasil disimpan!")
                break

            except Exception as e:
                print("[!] Error:", e)
                db.rollback()
                break

        elif simpan == "N":
            print("Penyimpanan dibatalkan.")
            break
        else:
            print("[!] Harus pilih Y atau N!")

# ==========================================
# LOGIN
# ==========================================
def login():

    header("LOGIN")

    percobaan = 0

    while percobaan < 5:

        userid = input("User ID: ")
        password = input("Password: ")

        cursor.execute("SELECT password FROM users WHERE userid=?", (userid,))
        data = cursor.fetchone()

        if not data:
            print("[!] ID Tidak Terdaftar")
        else:
            if password != data[0]:
                print("[!] Password Salah")
            else:
                print("[✓] Login Berhasil")
                return userid

        percobaan += 1
        print(f"[!] Percobaan {percobaan}/5")

    print("[!] Terlalu banyak percobaan gagal.")
    return None

# ==========================================
# PROFIL (DATABASE VERSION)
# ==========================================
def profil(user):

    header("PROFIL USER")

    # ==========================
    # AMBIL DATA USER
    # ==========================
    cursor.execute("""
        SELECT nama, email, gender, usia, pekerjaan, hobi
        FROM users
        WHERE userid=?
    """, (user,))

    data_user = cursor.fetchone()

    if not data_user:
        print("[!] Data user tidak ditemukan.")
        return

    nama, email, gender, usia, pekerjaan, hobi = data_user

    # ==========================
    # AMBIL DATA ALAMAT
    # ==========================
    cursor.execute("""
        SELECT kota, rt, rw, zip_code, latitude, longitude, nohp
        FROM alamat
        WHERE userid=?
    """, (user,))

    data_alamat = cursor.fetchone()

    if not data_alamat:
        print("[!] Data alamat tidak ditemukan.")
        return

    kota, rt, rw, zip_code, lat, long, nohp = data_alamat

    # ==========================
    # TAMPILKAN DATA
    # ==========================
    print("DATA PRIBADI")
    line()
    print(f"{'Nama':15}: {nama}")
    print(f"{'Email':15}: {email}")
    print(f"{'Gender':15}: {gender}")
    print(f"{'Usia':15}: {usia}")
    print(f"{'Pekerjaan':15}: {pekerjaan}")
    print(f"{'Hobi':15}: {hobi}")

    print("\nDATA ALAMAT")
    line()
    print(f"{'Kota':15}: {kota}")
    print(f"{'RT':15}: {rt}")
    print(f"{'RW':15}: {rw}")
    print(f"{'Zip Code':15}: {zip_code}")
    print(f"{'Latitude':15}: {lat}")
    print(f"{'Longitude':15}: {long}")
    print(f"{'No HP':15}: {nohp}")

    print("="*80)


# ==========================================
# CRUD
# ==========================================
def read_barang():

    header("DAFTAR BARANG")

    cursor.execute("SELECT * FROM barang")
    semua = cursor.fetchall()

    if not semua:
        print("Daftar barang masih kosong")
        return

    print("1. Tampilkan Semua")
    print("2. Cari Barang")
    print("-"*60)

    pilih = input("Pilih: ")

    print("+" + "-"*60 + "+")
    print("| {:<10} | {:<20} | {:<10} | {:<8} |".format(
        "KODE","NAMA","HARGA","STOK"))
    print("+" + "-"*60 + "+")

    data = semua

    if pilih == "2":
        cari = input("Masukkan kode/nama: ").lower()

        cursor.execute("""
            SELECT * FROM barang
            WHERE LOWER(kode_barang) LIKE ?
            OR LOWER(nama_barang) LIKE ?
        """, (f"%{cari}%", f"%{cari}%"))

        data = cursor.fetchall()

        if not data:
            print("| {:^58} |".format("Barang tidak ditemukan"))
            print("+" + "-"*60 + "+")
            return

    for row in data:
        kode, nama, harga, stok = row
        print("| {:<10} | {:<20} | {:<10} | {:<8} |".format(
            kode, nama, harga, stok))

    print("+" + "-"*60 + "+")


def create_barang():

    header("TAMBAH BARANG")

    while True:

        kode = input("Kode Barang: ").upper()
        if not kode.isalnum():
            print("[!] Kode salah!")
            continue

        nama = input("Nama Barang: ").title()
        if not nama.replace(" ","").isalpha():
            print("[!] Nama harus alfabet!")
            continue

        # CEK DUPLIKAT DI DATABASE
        cursor.execute("""
            SELECT * FROM barang
            WHERE LOWER(kode_barang)=LOWER(?)
            OR LOWER(nama_barang)=LOWER(?)
        """, (kode, nama))

        duplikat = cursor.fetchone()

        if duplikat:
            print("[!] Data sudah ada!")

            konfirmasi = input("Update data? (Y/N): ").upper()

            if konfirmasi == "Y":

                while True:
                    try:
                        harga = int(input("Harga (>0): "))
                        stok  = int(input("Stok (>=0): "))
                    except:
                        print("[!] Harus angka!")
                        continue

                    if harga <= 0 or stok < 0:
                        print("[!] Harga/Stok tidak valid!")
                        continue

                    cursor.execute("""
                        UPDATE barang
                        SET nama_barang=?, harga=?, stok=?
                        WHERE kode_barang=?
                    """, (nama, harga, stok, kode))

                    db.commit()

                    print("[✓] Data berhasil diupdate!")
                    break

            else:
                print("Update dibatalkan.")

        else:
            while True:
                try:
                    harga = int(input("Harga (>0): "))
                    stok  = int(input("Stok (>=0): "))
                except:
                    print("[!] Harus angka!")
                    continue

                if harga <= 0 or stok < 0:
                    print("[!] Harga/Stok tidak valid!")
                    continue
                break

            cursor.execute("""
                INSERT INTO barang
                (kode_barang, nama_barang, harga, stok)
                VALUES (?,?,?,?)
            """, (kode, nama, harga, stok))

            db.commit()

            print("[✓] Barang berhasil ditambahkan!")

        while True:
            lagi = input("Tambah lagi? (Y/N): ").upper()

            if lagi == "Y":
                break
            elif lagi == "N":
                return
            else:
                print("[!] Harus pilih Y atau N!")

def update_barang():

    header("UPDATE BARANG")

    cursor.execute("SELECT * FROM barang")
    if not cursor.fetchall():
        print("Daftar barang masih kosong.")
        return

    # =========================
    # INPUT KODE
    # =========================
    while True:
        kode = input("Kode yang ingin diupdate: ").upper()

        cursor.execute("SELECT * FROM barang WHERE kode_barang=?", (kode,))
        data = cursor.fetchone()

        if data:
            break

        print("[!] Barang tidak ditemukan!")

        while True:
            kembali = input("Coba lagi? (Y/N): ").upper()

            if kembali == "Y":
                break   # kembali ke input kode
            elif kembali == "N":
                return  # keluar fungsi
            else:
                print("[!] Harus pilih Y atau N!")

    # =========================
    # MENU UPDATE
    # =========================
    while True:

        print("\nApa yang ingin diupdate?")
        print("1. Nama")
        print("2. Harga")
        print("3. Stok")
        print("4. Semua")
        print("5. Batal")

        pilih = input("Pilih: ")

        # ========================
        # UPDATE NAMA
        # ========================
        if pilih == "1":

            while True:
                nama = input("Nama baru: ").title()

                if not nama.replace(" ","").isalpha():
                    print("[!] Nama tidak valid!")
                    continue

                cursor.execute("""
                    UPDATE barang SET nama_barang=?
                    WHERE kode_barang=?
                """, (nama, kode))

                db.commit()
                print("[✓] Nama berhasil diupdate!")
                break

        # ========================
        # UPDATE HARGA
        # ========================
        elif pilih == "2":

            while True:
                try:
                    harga = int(input("Harga baru: "))
                except:
                    print("[!] Harus angka!")
                    continue

                if harga <= 0:
                    print("[!] Harga tidak valid!")
                    continue

                cursor.execute("""
                    UPDATE barang SET harga=?
                    WHERE kode_barang=?
                """, (harga, kode))

                db.commit()
                print("[✓] Harga berhasil diupdate!")
                break

        # ========================
        # UPDATE STOK
        # ========================
        elif pilih == "3":

            while True:
                try:
                    stok = int(input("Stok baru: "))
                except:
                    print("[!] Harus angka!")
                    continue

                if stok < 0:
                    print("[!] Stok tidak valid!")
                    continue

                cursor.execute("""
                    UPDATE barang SET stok=?
                    WHERE kode_barang=?
                """, (stok, kode))

                db.commit()
                print("[✓] Stok berhasil diupdate!")
                break

        # ========================
        # UPDATE SEMUA
        # ========================
        elif pilih == "4":

            while True:
                nama = input("Nama baru: ").title()
                if not nama.replace(" ","").isalpha():
                    print("[!] Nama tidak valid!")
                    continue
                break

            while True:
                try:
                    harga = int(input("Harga baru: "))
                    stok  = int(input("Stok baru: "))
                except:
                    print("[!] Harus angka!")
                    continue

                if harga <= 0 or stok < 0:
                    print("[!] Data tidak valid!")
                    continue
                break

            cursor.execute("""
                UPDATE barang
                SET nama_barang=?, harga=?, stok=?
                WHERE kode_barang=?
            """, (nama, harga, stok, kode))

            db.commit()
            print("[✓] Data berhasil diupdate!")

        # ========================
        # BATAL
        # ========================
        elif pilih == "5":
            print("Update dibatalkan.")
            return

        else:
            print("[!] Menu tidak valid!")
            continue

        # =========================
        # KONFIRMASI LANJUT UPDATE
        # =========================
        while True:
            lanjut = input("Update lagi? (Y/N): ").upper()

            if lanjut == "Y":
                break   # kembali ke menu update

            elif lanjut == "N":
                return  # keluar fungsi

            else:
                print("[!] Harus pilih Y atau N!")


def delete_barang():

    header("HAPUS BARANG")

    cursor.execute("SELECT * FROM barang")
    if not cursor.fetchall():
        print("Daftar barang masih kosong.")
        return

    while True:
        kode = input("Kode yang ingin dihapus: ").upper()

        cursor.execute("SELECT * FROM barang WHERE kode_barang=?", (kode,))
        data = cursor.fetchone()

        if not data:
            print("[!] Barang tidak ditemukan!")

            while True:
                kembali = input("Coba lagi? (Y/N): ").upper()

                if kembali == "Y":
                    break
                elif kembali == "N":
                    return
                else:
                    print("[!] Harus pilih Y atau N!")

            if kembali == "Y":
                continue

        else:
            break

    print("\nData yang akan dihapus:")
    print(f"Kode  : {data[0]}")
    print(f"Nama  : {data[1]}")
    print(f"Harga : {data[2]}")
    print(f"Stok  : {data[3]}")

    # ==========================
    # KONFIRMASI DELETE
    # ==========================
    while True:
        konfirmasi = input("Delete data? (Y/N): ").upper()

        if konfirmasi == "Y":
            cursor.execute("DELETE FROM barang WHERE kode_barang=?", (kode,))
            db.commit()
            print("[✓] Data berhasil dihapus!")
            return

        elif konfirmasi == "N":
            print("Penghapusan dibatalkan.")
            return

        else:
            print("[!] Harus pilih Y atau N!")

# ==========================================
# SUB MENU CRUD BARANG
# ==========================================
def menu_crud_barang():

    while True:

        header("MENU CRUD BARANG")

        print("1. Tampilkan Barang")
        print("2. Tambah Barang")
        print("3. Update Barang")
        print("4. Hapus Barang")
        print("5. Kembali")
        line()

        pilih = input("Pilih Menu: ")

        if pilih == "1":
            read_barang()

        elif pilih == "2":
            create_barang()

        elif pilih == "3":
            update_barang()

        elif pilih == "4":
            delete_barang()

        elif pilih == "5":
            break

        else:
            print("[!] Menu tidak valid!")

# ==========================================
# TRANSAKSI
# ==========================================
def transaksi(user):

    header("TRANSAKSI")

    keranjang = []

    while True:

        read_barang()

        kode = input("Kode Barang (X selesai): ").upper()
        if kode == "X":
            break

        # ==========================
        # CEK BARANG DI DATABASE
        # ==========================
        cursor.execute(
            "SELECT nama_barang, harga, stok FROM barang WHERE kode_barang=?",
            (kode,)
        )
        data_barang = cursor.fetchone()

        if not data_barang:
            print("[!] Barang tidak ditemukan!")
            continue

        nama_barang, harga_barang, stok_barang = data_barang

        # ==========================
        # INPUT QTY
        # ==========================
        while True:
            try:
                qty = int(input("Qty (>0) : "))

                if qty <= 0:
                    print("[!] Qty tidak boleh nol atau minus!")
                    continue

                if qty > stok_barang:
                    print("[!] Stok tidak cukup!")
                    continue

                break

            except ValueError:
                print("[!] Input harus berupa angka!")

        subtotal = harga_barang * qty

        item_sama = next(
            (item for item in keranjang if item["kode"] == kode),
            None
        )

        if item_sama:
            item_sama["qty"] += qty
            item_sama["subtotal"] += subtotal
        else:
            keranjang.append({
                "kode": kode,
                "nama": nama_barang,
                "harga": harga_barang,
                "qty": qty,
                "subtotal": subtotal
            })

        # ==========================
        # VALIDASI TAMBAH BARANG
        # ==========================
        while True:
            tambah = input("Tambah barang? (Y/N): ").upper()

            if tambah == "Y":
                break
            elif tambah == "N":
                break
            else:
                print("[!] Harus pilih Y atau N!")

        if tambah == "N":
            break

    if not keranjang:
        return

    # ==========================
    # PERHITUNGAN
    # ==========================
    total = sum(i["subtotal"] for i in keranjang)
    total_qty = sum(i["qty"] for i in keranjang)

    diskon_qty = total*0.15 if total_qty >= 10 else total*0.10 if total_qty >= 5 else 0
    diskon_harga = total*0.20 if total >= 500000 else total*0.10 if total >= 200000 else 0
    diskon = max(diskon_qty, diskon_harga)

    setelah = total - diskon
    pajak = setelah * PPN
    grand = setelah + pajak

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # ==========================
        # INSERT KE TABEL TRANSAKSI
        # ==========================
        cursor.execute("""
            INSERT INTO transaksi
            (userid, tanggal, total, diskon, pajak, grand_total)
            VALUES (?,?,?,?,?,?)
        """, (user, now, int(total), int(diskon), int(pajak), int(grand)))

        id_transaksi = cursor.lastrowid

        # ==========================
        # INSERT DETAIL + UPDATE STOK
        # ==========================
        for i in keranjang:

            cursor.execute("""
                INSERT INTO detail_transaksi
                (id_transaksi, kode_barang, qty, subtotal)
                VALUES (?,?,?,?)
            """, (id_transaksi, i["kode"], i["qty"], int(i["subtotal"])))

            cursor.execute("""
                UPDATE barang
                SET stok = stok - ?
                WHERE kode_barang = ?
            """, (i["qty"], i["kode"]))

        db.commit()

    except Exception as e:
        print("[!] Terjadi kesalahan:", e)
        db.rollback()
        return

    # ==========================
    # CETAK INVOICE
    # ==========================
    header("INVOICE")
    tanggal_obj = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
    print(f"Tanggal : {tanggal_obj.strftime('%d-%m-%Y')}")
    print(f"Jam     : {tanggal_obj.strftime('%H:%M:%S')}")
    line()

    for i in keranjang:
        print("{:<10} {:<15} {:>3} x {:>8} = {:>10}".format(
            i["kode"], i["nama"], i["qty"],
            i["harga"],
            i["subtotal"]
        ))

    line()
    print("{:<30} {:>15}".format("Subtotal", int(total)))
    print("{:<30} {:>15}".format("Diskon", int(diskon)))
    print("{:<30} {:>15}".format("PPN 11%", int(pajak)))
    print("="*60)
    print("{:<30} {:>15}".format("TOTAL BAYAR", int(grand)))
    print("="*60)

# ==========================================
# RIWAYAT TRANSAKSI
# ==========================================
def riwayat_transaksi(user):

    header("RIWAYAT TRANSAKSI")

    cursor.execute("""
        SELECT id_transaksi, tanggal, total, diskon, pajak, grand_total
        FROM transaksi
        WHERE userid=?
        ORDER BY tanggal DESC
    """, (user,))

    data = cursor.fetchall()

    if not data:
        print("Belum ada transaksi.")
        return

    print("+" + "-"*70 + "+")
    print("| {:<5} | {:<19} | {:<10} | {:<10} | {:<10} |".format(
        "ID","Tanggal","Total","Diskon","Grand"))
    print("+" + "-"*70 + "+")

    for row in data:
        id_trx, tanggal, total, diskon, pajak, grand = row
        print("| {:<5} | {:<19} | {:<10} | {:<10} | {:<10} |".format(
            id_trx,
            datetime.strptime(tanggal, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y %H:%M"),
            total,
            diskon,
            grand
        ))

    print("+" + "-"*70 + "+")

    # ==========================
    # LIHAT DETAIL
    # ==========================
    while True:
        pilih = input("Lihat detail transaksi? (Y/N): ").upper()

        if pilih == "Y":
            id_detail = input("Masukkan ID Transaksi: ")

            if not id_detail.isdigit():
                print("[!] ID harus berupa angka!")
                continue
            id_detail = int(id_detail)

            cursor.execute("""
                SELECT b.kode_barang, b.nama_barang, d.qty, d.subtotal
                FROM detail_transaksi d
                JOIN barang b ON d.kode_barang = b.kode_barang
                WHERE d.id_transaksi=?
            """, (id_detail,))

            detail = cursor.fetchall()

            if not detail:
                print("[!] ID Transaksi tidak ditemukan.")
                continue

            header(f"DETAIL TRANSAKSI ID {id_detail}")
            for item in detail:
                kode, nama, qty, subtotal = item
                print(f"{kode} - {nama} | Qty: {qty} | Subtotal: {subtotal}")

            print("="*60)
            return

        elif pilih == "N":
            return

        else:
            print("[!] Harus pilih Y atau N!")

# ==========================================
# MAIN
# ==========================================
while True:

    header("SMARTCASHIER ID")

    print("1. Register")
    print("2. Login")
    print("3. Exit")
    line()

    pilih = input("Pilih Menu: ")

    if pilih == "1":
        register()

    elif pilih == "2":
        user = login()

        if user:
            while True:

                header("MAIN MENU")

                print("1. Profil")
                print("2. Kelola Barang (CRUD)")
                print("3. Transaksi")
                print("4. Riwayat Transaksi")
                print("5. Logout")
                line()

                m = input("Pilih: ")

                if m == "1":
                    profil(user)

                elif m == "2":
                    menu_crud_barang()

                elif m == "3":
                    transaksi(user)

                elif m == "4":
                    riwayat_transaksi(user)

                elif m == "5":
                    print("Logout berhasil.")
                    break

                else:
                    print("[!] Menu tidak valid!")

    elif pilih == "3":
        print("Terima kasih telah menggunakan SMARTCASHIER ID.")
        break

    else:
        print("[!] Pilihan tidak valid!")


