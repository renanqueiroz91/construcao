from django.http import HttpResponse
from .models import Construcao, Estoque, Material
from .forms import EstoqueForm, ConstrucaoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd
from io import BytesIO
from django.http import JsonResponse
from django.utils import timezone


def menu(request):
    construcoes = Construcao.objects.all()
    materiais = Material.objects.all()
    return render(request, 'app_almoxarifado/menu.html', {'construcoes': construcoes, 'materiais': materiais})

def deletar_local(request, local_id):
    local = get_object_or_404(Construcao, pk=local_id)
    local.delete()
    return render(request, "escolher_local.html")

def cadastrar_local(request):
    if request.method == 'POST':
        form = ConstrucaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_almoxarifado:escolher_local')  # Redirecionar para a página de escolher local
    else:
        form = ConstrucaoForm()
    return render(request, 'cadastrar_local.html', {'form': form})


def cadastrar_material(request, construcao_id):
    construcao = get_object_or_404(Construcao, pk=construcao_id)
    tipos_materiais = Material.TIPO_CHOICES  # Alterado para acessar TIPO_CHOICES diretamente do modelo Material
    error_messages = {}

    if request.method == 'POST':
        form = EstoqueForm(request.POST)
        if form.is_valid():
            estoque = form.save(commit=False)
            estoque.construcao = construcao
            estoque.save()
            return redirect('app_almoxarifado:visualizar_estoque', construcao_id=construcao_id)
        else:
            # Adicionando mensagens de erro específicas para cada campo
            for field, errors in form.errors.items():
                error_messages[field] = ', '.join(errors)
    else:
        form = EstoqueForm()

    return render(request, 'cadastrar_material.html', {'form': form, 'construcao': construcao, 'tipos_materiais': tipos_materiais, 'error_messages': error_messages})


def escolher_local(request):
    locais = Construcao.objects.all()
    return render(request, 'escolher_local.html', {'locais': locais})

def visualizar_estoque(request, construcao_id):
    construcao = Construcao.objects.get(pk=construcao_id)
    materiais = Estoque.objects.filter(construcao=construcao)
    return render(request, 'visualizar_estoque.html', {'construcao': construcao, 'materiais': materiais})



def deletar_material(request, material_id):
    material = get_object_or_404(Estoque, pk=material_id)
    material.delete()
    # Redirecionar de volta para a página de visualização de estoque
    return HttpResponseRedirect(reverse('app_almoxarifado:visualizar_estoque', args=(material.construcao.id,)))




def upload_lista_materiais(request, construcao_id):
    construcao = get_object_or_404(Construcao, pk=construcao_id)
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        
        if file and file.name.endswith(('.xlsx', '.xls')):
            try:
                # Ler o arquivo Excel ignorando o cabeçalho (primeira linha) e lendo apenas as colunas necessárias
                df = pd.read_excel(file, usecols="B:D", skiprows=1)
                
                # Iterar sobre as linhas do DataFrame e criar os registros de materiais
                for index, row in df.iterrows():
                    nome_material = row[0]  # Primeira coluna (índice 0) para o nome do material
                    tipo_material_excel = row[1]  # Segunda coluna (índice 1) para o tipo de material no Excel
                    quantidade = row[2]  # Terceira coluna (índice 2) para a quantidade
                    
                    # Verificar se a quantidade é um número válido ou se é um valor vazio ('nan')
                    if pd.isna(quantidade) or quantidade == '':
                        quantidade = 0  # Definir a quantidade como 0 se for um valor vazio ou 'nan'
                    else:
                        quantidade = int(quantidade)  # Converter a quantidade para inteiro
                    
                    # Verificar se o tipo de material no Excel está entre as opções válidas do modelo
                    tipo_material_modelo = 'und'  # Tipo padrão se não for encontrado
                    for tipo, _ in Material.TIPO_CHOICES:
                        if tipo_material_excel.lower() in tipo:
                            tipo_material_modelo = tipo
                            break
                    
                    # Criar ou obter o material com base no nome e na construção
                    material, _ = Material.objects.get_or_create(nome=nome_material, tipo=tipo_material_modelo, construcao=construcao)
                    
                    # Criar o estoque associado ao material
                    Estoque.objects.create(
                        construcao=construcao,
                        material=material.nome,  # Armazenar apenas o nome do material
                        tipo_material=tipo_material_modelo,
                        quantidade=quantidade
                    )
                
                return redirect('app_almoxarifado:visualizar_estoque', construcao_id=construcao.id)
            
            except Exception as e:
                return HttpResponse("Erro ao processar o arquivo: " + str(e))
        
        else:
            return HttpResponse("Formato de arquivo não suportado.")
    
    else:
        return HttpResponse("Método não suportado.")









def teste(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith(('.xlsx', '.xls')):
            try:
                # Ler o arquivo Excel ignorando o cabeçalho (primeira linha) e lendo apenas as colunas necessárias
                df = pd.read_excel(file, usecols="B:D", skiprows=1)
                
                # Transformar o DataFrame em HTML para renderização na página
                table_html = df.to_html(index=False)
                
                # Retornar o HTML para a página
                return render(request, 'app_almoxarifado/teste.html', {'table_html': table_html})
            except Exception as e:
                return HttpResponse("Erro ao processar o arquivo: " + str(e))
        else:
            return HttpResponse("Formato de arquivo não suportado.")
    else:
        return render(request, 'app_almoxarifado/teste.html')



def detalhe_material(request, material_id):
    material = get_object_or_404(Estoque, pk=material_id)
    return render(request, 'detalhe_material.html', {'material': material})



def atualizar_quantidade(request, material_id):
    material = get_object_or_404(Estoque, pk=material_id)
    
    if request.method == 'POST':
        # Verificar se foi uma entrada ou saída
        if 'saida' in request.POST:
            quantidade = int(request.POST.get('saidaInput'))
            material.quantidade -= quantidade
            material.save()
            return redirect('app_almoxarifado:detalhe_material', material_id=material.id)
        elif 'entrada' in request.POST:
            quantidade = int(request.POST.get('entradaInput'))
            material.quantidade += quantidade
            material.save()
            return redirect('app_almoxarifado:detalhe_material', material_id=material.id)
        else:
            return HttpResponse("Ação inválida.")
    else:
        return HttpResponse("Método não suportado.")
    

def movimentacoes_estoque(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        movimentacoes = Estoque.objects.filter(data_entrada=data) | Estoque.objects.filter(data_saida=data)
        return render(request, 'movimentacoes_estoque.html', {'movimentacoes': movimentacoes, 'data_selecionada': data})
    else:
        # Se não houver POST, exibir o formulário vazio
        return render(request, 'movimentacoes_estoque.html')


def exportar_lista_materiais(request, construcao_id):
    construcao = Construcao.objects.get(pk=construcao_id)
    materiais = Estoque.objects.filter(construcao=construcao)

    # Criar um DataFrame com os dados dos materiais
    data = {
        'Nome Material': [material.material for material in materiais],
        'Tipo': [material.tipo_material for material in materiais],
        'Quantidade': [material.quantidade for material in materiais],
    }
    df = pd.DataFrame(data)

    # Exportar o DataFrame para um arquivo Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Lista de Materiais')
    writer.close()  # Fechar o escritor após escrever o arquivo
    output.seek(0)

    # Retornar o arquivo Excel como resposta
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=lista_materiais.xlsx'
    return response