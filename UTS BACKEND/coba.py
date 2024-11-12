from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql

app = Flask(__name__)

# Konfigurasi koneksi database
db = pymysql.connect(
    host="localhost",
    user="delonik",
    password="delonik",
    database="library"
)

# Endpoint API untuk menambah buku dengan metode POST
@app.route("/api/buku", methods=["POST"])
def add_buku():
    data = request.get_json()  # Mengambil data JSON dari body request
    print("Received Data:", data)  # Debug print
    if not data:
        return jsonify({"message": "Tidak ada data"}), 400

    judul = data.get("judul")
    penulis = data.get("penulis")
    tahun = data.get("tahun")

    if not judul or not penulis or not tahun:
        return jsonify({"message": "Judul, penulis, dan tahun harus diisi"}), 400

    # Simpan buku ke database
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO buku (judul, penulis, tahun) VALUES (%s, %s, %s)", (judul, penulis, tahun))
    db.commit()

    return jsonify({"message": "Buku berhasil ditambahkan", "data": data}), 201


# Routing untuk halaman utama (daftar buku)
@app.route('/')
def index():
    with db.cursor() as cursor:
        # Ambil data buku dari database
        cursor.execute("SELECT * FROM buku")
        books = cursor.fetchall()
    return render_template('index_nim.html', books=books)

# Routing untuk halaman tambah buku
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        # Ambil data buku dari form
        judul = request.form['judul']
        penulis = request.form['penulis']
        tahun = request.form['tahun']
        
        if not judul or not penulis or not tahun:
            return render_template('tambah_nim.html', error="Judul, penulis, dan tahun harus diisi")

        with db.cursor() as cursor:
            # Simpan data buku ke database
            cursor.execute("INSERT INTO buku (judul, penulis, tahun) VALUES (%s, %s, %s)", (judul, penulis, tahun))
        db.commit()
        return redirect(url_for('index'))
    return render_template('tambah_nim.html')

# Routing untuk halaman edit buku
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        # Ambil data buku dari form
        judul = request.form['judul']
        penulis = request.form['penulis']
        tahun = request.form['tahun']
        
        if not judul or not penulis or not tahun:
            return render_template('edit_nim.html', id=id, error="Judul, penulis, dan tahun harus diisi")

        with db.cursor() as cursor:
            # Update data buku di database
            cursor.execute("UPDATE buku SET judul=%s, penulis=%s, tahun=%s WHERE id=%s", (judul, penulis, tahun, id))
        db.commit()
        return redirect(url_for('index'))
    
    with db.cursor() as cursor:
        # Ambil data buku dari database berdasarkan id
        cursor.execute("SELECT * FROM buku WHERE id=%s", (id,))
        book = cursor.fetchone()
    return render_template('edit_nim.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
