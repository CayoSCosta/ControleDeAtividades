from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.timezone import datetime
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from openpyxl import Workbook
from .models import Registro
from .forms import RegistroForm

class IndexView(ListView):
    model = Registro
    template_name = 'index.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        return Registro.objects.order_by('-data_de_inicio', '-hora_de_inicio')

class CriarTarefaView(CreateView):
    model = Registro
    form_class = RegistroForm
    template_name = 'registro.html'

    def form_valid(self, form):
        registro = form.save(commit=False)
        acao = self.request.POST.get('acao')

        if acao == 'salvar':
            registro.data_de_inicio = datetime.now().date()
            registro.hora_de_inicio = datetime.now().time()
            registro.save()
            return self.render_to_response(self.get_context_data(form=form, \
                data_de_inicio=registro.data_de_inicio, \
                hora_de_inicio=registro.hora_de_inicio))

        elif acao == 'encerrar':
            ultimo_registro = Registro.objects.filter(hora_de_termino__isnull=True).last()
            if ultimo_registro:
                return redirect('encerrar', pk=ultimo_registro.id)

        return super().form_valid(form)

class PararTarefaView(UpdateView):
    model = Registro
    template_name = 'pausar.html'
    fields = []

    def post(self, request, *args, **kwargs):
        registro = self.get_object()

        if not registro.hora_de_pausa:
            registro.hora_de_pausa = datetime.now().time()
        else:
            pausa_inicial = datetime.combine(datetime.today(), registro.hora_de_pausa)
            pausa_final = datetime.now()
            registro.tempo_pausado += (pausa_final - pausa_inicial)
            registro.hora_de_pausa = None

        registro.save()
        return redirect('index')

class EncerrarTarefaView(UpdateView):
    model = Registro
    template_name = 'encerrar.html'
    fields = []

    def post(self, request, *args, **kwargs):
        registro = self.get_object()
        descricao = request.POST.get('descricao', '').strip()
        registro.hora_de_termino = datetime.now().time()
        registro.horas_utilizadas = (
            datetime.combine(datetime.today(), registro.hora_de_termino) -
            datetime.combine(datetime.today(), registro.hora_de_inicio)
        )
        registro.descricao = descricao
        registro.save()
        return redirect('index')

class VisualizarTarefaView(DetailView):
    model = Registro
    template_name = 'visualizar.html'
    context_object_name = 'registro'

class ExportXLSView(View):
    def get(self, request, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        ws.title = 'Tickets'

        ws.append(['Ticket', 'Cliente', 'Descrição', 'Data de Início', 'Hora de Início', 'Horas Utilizadas', 'Status'])

        tickets = Registro.objects.all()
        for ticket in tickets:
            horas_utilizadas = ticket.horas_utilizadas if ticket.horas_utilizadas else 0

            ws.append([
                ticket.ticket,
                ticket.cliente,
                ticket.descricao,
                ticket.data_de_inicio,
                ticket.hora_de_inicio,
                horas_utilizadas,
                'Em Andamento' if not ticket.hora_de_termino else 'Encerrado',
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Atividades.xlsx"'
        wb.save(response)

        return response
