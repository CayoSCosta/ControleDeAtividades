from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now, datetime
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

