from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import datetime
from openpyxl import Workbook
from django.http import HttpResponse
from .models import Registro
from .forms import RegistroForm

def index_view(request):
    # Obtém os últimos registros de tickets, ordenados por data e hora de criação
    ultimos_tickets = Registro.objects.order_by('-data_de_inicio', '-hora_de_inicio')
    
    # Configuração da paginação
    paginator = Paginator(ultimos_tickets, 10)  # 10 tickets por página
    page_number = request.GET.get('page')  # Pega o número da página da query string
    page_obj = paginator.get_page(page_number)
    
    # Passa os tickets paginados para o template
    return render(request, 'index.html', {'page_obj': page_obj})

def criar_tarefa_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            acao = request.POST.get('acao')
            print(f"Ação: {acao}")
            registro = form.save(commit=False)

            if acao == 'salvar':
                # Salva o registro inicial
                registro.data_de_inicio = datetime.now().date()
                registro.hora_de_inicio = datetime.now().time()
                registro.save()
                print(f"Registro salvo: {registro.id}")
                return render(request, 'registro.html', {
                    'form': form,
                    'data_de_inicio': registro.data_de_inicio,
                    'hora_de_inicio': registro.hora_de_inicio,
                })
            elif acao == 'encerrar':
                # Busca o último registro em andamento e redireciona para a view de encerramento
                ultimo_registro = Registro.objects.filter(hora_de_termino__isnull=True).last()
                print(f"Encerrando ultimo registro salvo: {ultimo_registro.id}")
                if ultimo_registro:
                    return redirect('encerrar', pk=ultimo_registro.id)
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

def encerrar_tarefa_view(request, pk):
    registro = get_object_or_404(Registro, id=pk)
    
    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        registro.hora_de_termino = datetime.now().time()
        registro.horas_utilizadas = (
            datetime.combine(datetime.today(), registro.hora_de_termino) -
            datetime.combine(datetime.today(), registro.hora_de_inicio)
        )
        registro.descricao = descricao
        
        registro.save()
        return redirect('index')  # Redireciona para a tela inicial após encerrar
    
    return render(request, 'encerrar.html', {'registro': registro})



def visualizar_tarefa_view(request, pk):
    registro = get_object_or_404(Registro, pk=pk)
    print(f"Horas utilizadas: {registro.horas_utilizadas}")
    return render(request, 'visualizar.html', {'registro': registro})


def export_xls(request):
    # Cria o arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = 'Tickets'

    # Escreve o cabeçalho
    ws.append(['Ticket', 'Cliente', 'Descrição', 'Data de Início', 'Hora de Início', 'Horas Utilizadas', 'Status'])

    # Escreve os dados dos tickets
    tickets = Registro.objects.all()
    for ticket in tickets:
        horas_utilizadas = ticket.horas_utilizadas if ticket.horas_utilizadas else 0  # Caso não tenha horas, coloca 0

        ws.append([
            ticket.ticket,
            ticket.cliente,
            ticket.descricao,
            ticket.data_de_inicio,
            ticket.hora_de_inicio,
            horas_utilizadas,  # Hora utilizada
            'Em Andamento' if not ticket.hora_de_termino else 'Encerrado',
        ])

    # Cria a resposta HTTP com o tipo MIME para Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tickets.xlsx"'

    # Salva o arquivo Excel na resposta
    wb.save(response)

    return response
def export_xls(request):
    # Cria o arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = 'Tickets'

    # Escreve o cabeçalho
    ws.append(['Ticket', 'Cliente', 'Descrição', 'Data de Início', 'Hora de Início', 'Horas Utilizadas', 'Status'])

    # Escreve os dados dos tickets
    tickets = Registro.objects.all()
    for ticket in tickets:
        horas_utilizadas = ticket.horas_utilizadas if ticket.horas_utilizadas else 0  # Caso não tenha horas, coloca 0

        ws.append([
            ticket.ticket,
            ticket.cliente,
            ticket.descricao,
            ticket.data_de_inicio,
            ticket.hora_de_inicio,
            horas_utilizadas,  # Hora utilizada
            'Em Andamento' if not ticket.hora_de_termino else 'Encerrado',
        ])

    # Cria a resposta HTTP com o tipo MIME para Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Atividades.xlsx"'

    # Salva o arquivo Excel na resposta
    wb.save(response)

    return response

