from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_folder='static')

class Pedido:
    def __init__(self, nome_cliente, itens):
        self.nome_cliente = nome_cliente
        self.itens = itens

    def calcular_total_geral():
        total_geral = 0
        for pedido in pedidos:
            total_geral += pedido.calcular_total()
        return total_geral

    def calcular_total(self):
        total = 0
        for item in self.itens:
            total += item.quantidade * 13.00  # Valor fixo de R$ 13,00 por item
        return total

    def salvar_pedidos():
        with open('pedidos.txt', 'w') as file:
            for pedido in pedidos:
                file.write(f"Cliente: {pedido.nome_cliente}\n")
                file.write("Itens:\n")
                for item in pedido.itens:
                    file.write(f"- {item.nome_produto}: {item.quantidade} unidades\n")
                file.write(f"Total: R$ {pedido.calcular_total()}\n\n")

class ItemPedido:
    def __init__(self, nome_produto, quantidade):
        self.nome_produto = nome_produto
        self.quantidade = quantidade
        self.valor = 13.00  # Valor fixo de R$ 13,00 por item

pedidos = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome_cliente = request.form['cliente']
        nome_produto = request.form['opcao']
        quantidade = int(request.form['quantidade'])

        pedido_atual = None
        for pedido in pedidos:
            if pedido.nome_cliente == nome_cliente:
                pedido_atual = pedido
                break

        if pedido_atual:
            pedido_atual.itens.append(ItemPedido(nome_produto, quantidade))
        else:
            pedido = Pedido(nome_cliente, [ItemPedido(nome_produto, quantidade)])
            pedidos.append(pedido)

        return redirect('/')
    else:
        return render_template('index.html', pedidos=pedidos)


@app.route('/pedidos')
def visualizar_pedidos():
    return render_template('pedidos.html', pedidos=pedidos, calcular_total_geral=Pedido.calcular_total_geral)


@app.route('/adicionar-pedido', methods=['POST'])
def adicionar_pedido():
    nome_cliente = request.form['cliente']
    nome_produto = request.form['opcao']
    quantidade = int(request.form['quantidade'])

    pedido_atual = None
    for pedido in pedidos:
        if pedido.nome_cliente == nome_cliente:
            pedido_atual = pedido
            break

    if pedido_atual:
        pedido_atual.itens.append(ItemPedido(nome_produto, quantidade))
    else:
        pedido = Pedido(nome_cliente, [ItemPedido(nome_produto, quantidade)])
        pedidos.append(pedido)

    return redirect('/')


@app.route('/excluir-item', methods=['POST'])
def excluir_item():
    nome_cliente = request.form['cliente']
    nome_produto = request.form['produto']

    for pedido in pedidos:
        if pedido.nome_cliente == nome_cliente:
            for item in pedido.itens:
                if item.nome_produto == nome_produto:
                    pedido.itens.remove(item)
                    break

    return redirect('/pedidos')


@app.route('/salvar-pedidos', methods=['POST'])
def salvar_pedidos():
    Pedido.salvar_pedidos()
    return redirect('/pedidos')


if __name__ == '__main__':
    app.run()