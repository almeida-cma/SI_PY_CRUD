from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuração da conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mypy",
    port=7306
)

@app.route('/')
def index():
    # Consulta para recuperar todos os registros da tabela de vendas
    cursor = conexao.cursor()
    query = "SELECT * FROM vendas"
    cursor.execute(query)
    vendas = cursor.fetchall()
    cursor.close()
    return render_template('index.html', vendas=vendas)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        # Receber os dados do formulário
        data = request.form['data']
        produto = request.form['produto']
        quantidade = int(request.form['quantidade'])
        valor_unitario = float(request.form['valor_unitario'])
        total = quantidade * valor_unitario

        # Inserir os dados na tabela de vendas
        cursor = conexao.cursor()
        query = "INSERT INTO vendas (data, produto, quantidade, valor_unitario, total) VALUES (%s, %s, %s, %s, %s)"
        values = (data, produto, quantidade, valor_unitario, total)
        cursor.execute(query, values)
        conexao.commit()
        cursor.close()

        return redirect(url_for('index'))

    return render_template('insert.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        # Receber os dados do formulário
        data = request.form['data']
        produto = request.form['produto']
        quantidade = int(request.form['quantidade'])
        valor_unitario = float(request.form['valor_unitario'])
        total = quantidade * valor_unitario

        # Atualizar os dados na tabela de vendas
        cursor = conexao.cursor()
        query = "UPDATE vendas SET data = %s, produto = %s, quantidade = %s, valor_unitario = %s, total = %s WHERE id = %s"
        values = (data, produto, quantidade, valor_unitario, total, id)
        cursor.execute(query, values)
        conexao.commit()
        cursor.close()

        return redirect(url_for('index'))

    # Recuperar os dados do registro a ser atualizado
    cursor = conexao.cursor()
    query = "SELECT * FROM vendas WHERE id = %s"
    cursor.execute(query, (id,))
    venda = cursor.fetchone()
    cursor.close()

    return render_template('update_modal.html', venda=venda)

@app.route('/delete/<int:id>')
def delete(id):
    # Deletar o registro da tabela de vendas
    cursor = conexao.cursor()
    query = "DELETE FROM vendas WHERE id = %s"
    cursor.execute(query, (id,))
    conexao.commit()
    cursor.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
