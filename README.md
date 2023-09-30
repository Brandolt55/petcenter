## Este foi um projeto real para uma empresa, o cliente me pediu uma programa para poder controlar seu estoque e que fosse bem simples de mexer

# petcenter projeto Desktop- Back-end

**Controle de Estoque para Agropecuária em Python**

Este é um projeto em Python desenvolvido para controlar o estoque de uma agropecuária. A aplicação utiliza a biblioteca Tkinter para criar uma interface gráfica intuitiva. Aqui está uma descrição detalhada das funcionalidades principais:

1. **Conexão com o Banco de Dados:**
   - Estabelece uma conexão com um banco de dados SQLite chamado "produtos.db" para armazenar informações sobre os produtos, incluindo nome, preço, quantidade, peso e vendas.

2. **Adição de Insumos:**
   - A função `adicionar_insumo` permite a adição de novos produtos ao estoque, considerando nome, preço, quantidade e peso. Se o produto já existe, a quantidade é atualizada.

3. **Venda de Produtos:**
   - A função `registrar_venda` possibilita a venda de produtos, atualizando a quantidade disponível e registrando o valor da venda no banco de dados.

4. **Visualização do Estoque:**
   - A função `visualizar_estoque` abre uma janela com uma planilha interativa mostrando os produtos em estoque, incluindo preço, quantidade, peso e vendas.

5. **Verificação de Produtos Abaixo da Quantidade Mínima:**
   - A função `produtos_abaixo_quantidade_minima` identifica e exibe produtos que estão abaixo da quantidade mínima estabelecida.

6. **Redefinição das Vendas:**
   - A função `resetar_vendas` permite a redefinição da coluna de vendas para zero, com confirmação do usuário.

7. **Interface Gráfica Intuitiva:**
   - Utiliza Tkinter para criar uma interface gráfica com botões para ações como adicionar, vender e visualizar o estoque. As entradas permitem inserir informações dos produtos.

8. **Notificações em Caixa de Texto:**
   - Uma caixa de texto na interface exibe mensagens informativas sobre ações realizadas, como adição de produtos, vendas e operações de estoque.

Este projeto é uma solução eficiente para gerenciar o estoque de uma agropecuária, oferecendo uma interface fácil de usar para as operações diárias. Certifique-se de fornecer documentação clara e contribua para um ambiente de desenvolvimento colaborativo e transparente.
