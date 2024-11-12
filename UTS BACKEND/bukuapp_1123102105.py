from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql

app = Flask(__name__)

db = pymysql.connect(
    host="localhost",
    user="root",
    password="delonik",
    database="library"
)

@app.route("/api/buku", methods=["GET"])
def get_all_buku():
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM buku")
            books = cursor.fetchall()
        return jsonify({
            "status": "success",
            "data": books
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/buku/<int:id>", methods=["GET"])
def get_buku_by_id(id):
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM buku WHERE id=%s", (id,))
            book = cursor.fetchone()
            if book:
                return jsonify({
                    "status": "success",
                    "data": book
                }), 200
            return jsonify({
                "status": "error",
                "message": "Buku tidak ditemukan"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/buku", methods=["POST"])
def add_buku():
    try:
        # Cek Content-Type header
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({
                "status": "error",
                "message": "Content-Type harus application/json"
            }), 400

        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Tidak ada data"
            }), 400

        required_fields = ["judul", "penulis", "tahun"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Field {field} harus diisi"
                }), 400

        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO buku (judul, penulis, tahun) VALUES (%s, %s, %s)",
                (data["judul"], data["penulis"], data["tahun"])
            )
        db.commit()

        return jsonify({
            "status": "success",
            "message": "Buku berhasil ditambahkan",
            "data": data
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/buku/<int:id>", methods=["PUT"])
def update_buku(id):
    try:
        if request.headers.get('Content-Type') != 'application/json':
            return jsonify({
                "status": "error",
                "message": "Content-Type harus application/json"
            }), 400

        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Tidak ada data"
            }), 400

        required_fields = ["judul", "penulis", "tahun"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Field {field} harus diisi"
                }), 400

        with db.cursor() as cursor:
            # Cek apakah buku ada
            cursor.execute("SELECT * FROM buku WHERE id=%s", (id,))
            if not cursor.fetchone():
                return jsonify({
                    "status": "error",
                    "message": "Buku tidak ditemukan"
                }), 404

            # Update buku
            cursor.execute(
                "UPDATE buku SET judul=%s, penulis=%s, tahun=%s WHERE id=%s",
                (data["judul"], data["penulis"], data["tahun"], id)
            )
        db.commit()

        return jsonify({
            "status": "success",
            "message": "Buku berhasil diupdate",
            "data": data
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/')
def index():
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM buku")
        books = cursor.fetchall()
    return render_template('index_1123102105.html', books=books)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        tahun = request.form['tahun']
        
        if not judul or not penulis or not tahun:
            return render_template('tambah_1123102105.html', error="Judul, penulis, dan tahun harus diisi")

        with db.cursor() as cursor:
            cursor.execute("INSERT INTO buku (judul, penulis, tahun) VALUES (%s, %s, %s)", 
                         (judul, penulis, tahun))
        db.commit()
        return redirect(url_for('index'))
    return render_template('tambah_1123102105.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        tahun = request.form['tahun']
        
        if not judul or not penulis or not tahun:
            return render_template('edit_1123102105.html', id=id, error="Judul, penulis, dan tahun harus diisi")

        with db.cursor() as cursor:
            cursor.execute("UPDATE buku SET judul=%s, penulis=%s, tahun=%s WHERE id=%s",
                         (judul, penulis, tahun, id))
        db.commit()
        return redirect(url_for('index'))
    
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM buku WHERE id=%s", (id,))
        book = cursor.fetchone()
    return render_template('edit_1123102105.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
