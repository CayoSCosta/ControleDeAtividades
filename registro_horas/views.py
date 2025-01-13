from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now, datetime
from .models import Registro
from .forms import RegistroForm

def index_view(request):
    # Obtém os últimos 5 registros de tickets (ordem decrescente por data e hora de criação)
    ultimos_tickets = Registro.objects.order_by('-data_de_inicio', '-hora_de_inicio')[:10]    
    return render(request, 'index.html', {'ultimos_tickets': ultimos_tickets})

def criar_tarefa_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            acao = request.POST.get('acao')
            registro = form.save(commit=False)

            if acao == 'salvar':
                # Salva o registro inicial
                registro.data_de_inicio = datetime.now().date()
                registro.hora_de_inicio = datetime.now().time()
                registro.save()
                return render(request, 'registro.html', {
                    'form': form,
                    'data_de_inicio': registro.data_de_inicio,
                    'hora_de_inicio': registro.hora_de_inicio,
                })
            elif acao == 'encerrar':
                # Busca o último registro em andamento e encerra
                ultimo_registro = Registro.objects.filter(hora_de_termino__isnull=True).last()
                if ultimo_registro:
                    ultimo_registro.hora_de_termino = datetime.now().time()
                    ultimo_registro.save()
                return redirect('index')  # Ajuste para a URL ou página inicial desejada
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})


# def encerrar_tarefa_view(request, pk):
#     registro = get_object_or_404(Registro, pk=pk)
#     registro.hora_de_termino = now().time()
    
#     # Calcular horas utilizadas
#     if registro.hora_de_inicio and registro.hora_de_termino:
#         delta = datetime.combine(date.min, registro.hora_de_termino) - datetime.combine(date.min, registro.hora_de_inicio)
#         registro.horas_utilizadas = (datetime.min + delta).time()
    
#     registro.save()
#     return redirect('index')  # Redirecionar para a página inicial

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
    return render(request, 'visualizar.html', {'registro': registro})

