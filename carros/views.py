from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Carro, Compra
from .forms import CarroForm
from django.http import HttpResponse


# View para listar carros com busca
# View para listar carros com busca
def listar_carros(request):
    # Obtém o termo de pesquisa da barra de pesquisa
    query = request.GET.get('query', '').strip()

    # Se houver um termo de pesquisa, filtra os carros
    if query:
        carros = Carro.objects.filter(
            Q(nome__icontains=query) |  # Pesquisa por nome do carro
            Q(marca__icontains=query) |  # Pesquisa por marca do carro
            Q(ano__icontains=query)      # Pesquisa por ano do carro
        )
    else:
        carros = Carro.objects.all()  # Caso não haja termo de pesquisa, lista todos os carros

    mensagem_sucesso = None
    if request.method == 'POST':
        carro_id = request.POST.get('carro_id')
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        endereco = request.POST.get('endereco')

        if not carro_id or not nome or not telefone or not email or not endereco:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return redirect('listar_carros')  # Se algum campo estiver vazio, retorna para a página

        carro = get_object_or_404(Carro, id=carro_id)

        if carro.em_estoque:
            try:
                compra = Compra(
                    carro=carro,
                    nome_cliente=nome,
                    numero_cliente=telefone,
                    email_cliente=email,
                    endereco_cliente=endereco,
                )
                compra.save()
                
                carro.vendido = True
                carro.em_estoque = False
                carro.save()

                mensagem_sucesso = f"Compra do {carro.nome} realizada com sucesso!"
                messages.success(request, mensagem_sucesso)
                return redirect('listar_carros')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro: {str(e)}")
                return redirect('listar_carros')

        else:
            mensagem_sucesso = f"Desculpe, o carro {carro.nome} já foi vendido!"
            messages.error(request, mensagem_sucesso)

    return render(request, 'carros/listar_carros.html', {
        'carros': carros,
        'mensagem_sucesso': mensagem_sucesso,
        'query': query,  # Passa o termo de busca para o template
    })


# View para exibir detalhes de um carro específico
def detalhes_carro(request, carro_id):
    """
    Exibe os detalhes de um carro específico identificado pelo ID.
    """
    carro = get_object_or_404(Carro, id=carro_id)  # Obtém o carro ou retorna 404
    context = {'carro': carro}
    return render(request, 'carros/detalhes_carro.html', context)


# View para marcar um carro como comprado
def comprar_carro(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    
    if carro.em_estoque:  # Verifica se o carro está disponível
        try:
            # Criação da compra
            compra = Compra(
                carro=carro,
                nome_cliente=request.POST['nome'],
                numero_cliente=request.POST['telefone'],
                email_cliente=request.POST['email'],
                endereco_cliente=request.POST['endereco'],
            )
            compra.save()  # Salva a compra no banco de dados

            # Marca o carro como vendido
            carro.vendido = True
            carro.em_estoque = False
            carro.save()  # Atualiza o carro

            messages.success(request, 'Carro comprado com sucesso!')
            return redirect('listar_carros')  # Redireciona para a listagem de carros
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {str(e)}")
            return redirect('listar_carros')  # Caso ocorra algum erro
    else:
        messages.error(request, 'Este carro não está mais disponível para venda.')
        return redirect('listar_carros')

# View para adicionar um carro
def adicionar_carro(request):
    """
    Função para adicionar um novo carro ao sistema e exibir mensagem de sucesso.
    """
    if request.method == 'POST':
        form = CarroForm(request.POST, request.FILES)
        if form.is_valid():
            carro = form.save()
            messages.success(request, 'Carro adicionado com sucesso!')
            # Re-renderiza a página com o formulário preenchido
            return render(request, 'carros/adicionar_carro.html', {'form': form, 'carro': carro})
        else:
            messages.error(request, 'Erro ao adicionar o carro. Verifique os dados informados.')
    else:
        form = CarroForm()

    return render(request, 'carros/adicionar_carro.html', {'form': form})

# View para remover um carro
def remover_carro(request):
    """
    Exibe a lista de carros com opção de busca e permite selecionar e remover carros específicos.
    """
    query = request.GET.get('query', '').strip()  # Obtém o termo de busca da barra de pesquisa

    # Aplica o filtro de busca, se houver um termo
    if query:
        carros = Carro.objects.filter(
            Q(nome__icontains=query) |
            Q(marca__icontains=query) |
            Q(ano__icontains=query)
        )
    else:
        carros = Carro.objects.all()  # Lista todos os carros se não houver termo de busca

    if request.method == 'POST':
        carros_remover = request.POST.getlist('carros_remover')  # IDs dos carros a serem removidos

        if carros_remover:
            try:
                Carro.objects.filter(id__in=carros_remover).delete()  # Remove os carros selecionados
                messages.success(request, 'Carros removidos com sucesso!')
            except Carro.DoesNotExist:
                messages.error(request, 'Erro: Carro(s) não encontrados.')
        else:
            messages.error(request, 'Nenhum carro foi selecionado para remoção.')

        return redirect('remover_carro')

    context = {
        'carros': carros,
        'query': query,  # Inclui o termo de busca no contexto para exibição no template
    }
    return render(request, 'carros/remover_carro.html', context)


# View para editar um carro
def editar_carro(request, carro_id=None):
    """
    Exibe a lista de carros disponíveis e permite editar um carro específico.
    Agora inclui funcionalidade de busca por nome, ano ou marca.
    """
    query = request.GET.get('query', '').strip()  # Obtém o termo de busca da barra de pesquisa
    
    # Filtra os carros com base no termo de busca, se houver
    if query:
        carros = Carro.objects.filter(
            Q(nome__icontains=query) |
            Q(ano__icontains=query) |
            Q(marca__icontains=query)
        )
    else:
        carros = Carro.objects.all()

    carro = None
    if carro_id:  # Verifica se um carro específico foi selecionado para edição
        carro = get_object_or_404(Carro, id=carro_id)

    if request.method == 'POST':
        if carro:
            form = CarroForm(request.POST, request.FILES, instance=carro)
        else:
            form = CarroForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()  # Salva o carro editado
            messages.success(request, 'Carro salvo com sucesso!')
            return redirect('editar_carro')  # Redireciona para a página de edição
        else:
            messages.error(request, 'Erro ao salvar as informações do carro.')

    else:
        form = CarroForm(instance=carro) if carro else CarroForm()  # Formulário preenchido ou vazio

    context = {
        'form': form,
        'carros': carros,  # Lista de carros (filtrada ou completa)
        'carro_editar': carro,  # Carro selecionado para edição
        'query': query,  # Termo de busca
    }

    return render(request, 'carros/editar_carro.html', context)


# View para a página inicial (opcional)
def home(request):
    """
    Exibe a página inicial do site.
    """
    return render(request, 'carros/home.html')


# View para exibir o histórico de compras

def historico_compras(request):
    # Recebe a consulta de pesquisa, se houver
    query = request.GET.get('query', '') 

    # Filtrando as compras se houver uma consulta de pesquisa
    if query:
        compras = Compra.objects.filter(
            Q(nome_cliente__icontains=query) | 
            Q(carro__nome__icontains=query)
        ).select_related('carro')  # Usando select_related para otimizar a consulta
    else:
        compras = Compra.objects.all().select_related('carro')  # Carrega as compras com os carros

    return render(request, 'carros/historico.html', {'compras': compras, 'query': query})

def enviar_contato(request):
    """
    View para processar o envio de um formulário de contato.
    """
    if request.method == "POST":
        # Lógica para processar o formulário de contato
        # Aqui você pode adicionar o código para enviar um e-mail ou salvar as informações do formulário no banco de dados
        return HttpResponse("Formulário enviado com sucesso!")
    
    return render(request, 'carros/enviar_contato.html')