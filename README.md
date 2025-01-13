# Sistema de Controle de Horas em Tickets

Este projeto é um sistema desenvolvido com Django para o controle de horas utilizadas em tickets. Ele permite registrar, visualizar e encerrar atividades, fornecendo um resumo detalhado de cada registro.

---

## **Recursos**

- Registro de atividades com informações detalhadas:
  - Ticket
  - Cliente
  - Descrição
  - Data e hora de início
  - Data e hora de término
  - Status da atividade
  
- Tela de resumo com:
  - Listagem de registros recentes
  - Botões para visualizar e encerrar atividades
  
- Visualização detalhada de registros:
  - Exibição de todos os dados de um registro
  - Opção de encerrar atividades em andamento

---

## **Requisitos do Sistema**

- Python 3.10+
- Django 4.2+
- SQLite (banco de dados padrão)
- Bootstrap 5 (para estilização)

---

## **Configuração do Projeto**

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. **Crie e Ative um Ambiente Virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. **Instale as Dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Execute as Migrações:**

   ```bash
   python manage.py migrate
   ```

5. **Inicie o Servidor:**

   ```bash
   python manage.py runserver
   ```

6. **Acesse a Aplicação:**

   Abra o navegador e acesse [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## **Estrutura do Projeto**

- **registro_horas/**: App principal com as funcionalidades de registro e gerenciamento de atividades.
  - **models.py**: Definições dos modelos `BaseModel` e `Registro`.
  - **views.py**: Lógica das views para criação, visualização e encerramento.
  - **templates/**: Arquivos HTML para as interfaces do usuário.
  - **urls.py**: Roteamento das páginas.

---

## **Funcionalidades Principais**

### **1. Tela de Resumo**
- Exibe os últimos registros com:
  - Ticket
  - Cliente
  - Descrição
  - Data e hora de início
  - Status ("Em Andamento" ou "Encerrado")
- Ações:
  - Botão para visualizar detalhes
  - Botão para encerrar atividades em andamento

### **2. Registro de Atividades**
- Formulário para registrar um novo ticket.
- Campos: Ticket, Cliente, Descrição.
- Após salvar, exibe data e hora de início.

### **3. Visualização de Registros**
- Exibe detalhes completos do registro.
- Permite encerrar registros "Em Andamento" diretamente na tela de visualização.

### **4. Encerramento de Atividades**
- Tela específica para preencher:
  - Data e hora de término
  - Horas utilizadas
  - Descrição do que foi feito

---

## **Próximos Passos**
- Implementação de autenticação de usuários.
- Exportação de relatórios em PDF ou Excel.
- Melhorias no layout utilizando componentes adicionais do Bootstrap.

---

## **Contribuições**

Sinta-se à vontade para abrir issues e enviar pull requests para melhorias ou correções.

---

## **Licença**

Este projeto está licenciado sob a [MIT License](LICENSE).

