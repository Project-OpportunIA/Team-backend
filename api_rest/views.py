from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ia_model.funcoes_IA import fazer_previsao
import requests

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator


from .models import Usuario 
from .models import Resultado_ia
from .serializers import UsuarioSerializer, UsuarioSerializerRegister, Resultado_iaSerializer

import json

@swagger_auto_schema(
    method='get',
    tags=["Usuário"],
    operation_summary='Lista de usuários',
    operation_description='Este endpoint serve para recuperar uma lista de usuários.',
    responses={200: openapi.Response('Success',), 400: openapi.Response('Bad request')},
    
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    if request.method == 'GET':
        users = Usuario.objects.all()
        serializer = UsuarioSerializer(users, many=True)
        formatted_response = {
            'success': True,
            'message': 'Lista de usuários recuperada com sucesso.',
            'data': serializer.data
        }
        return Response(formatted_response, status=status.HTTP_200_OK)
    return Response({'error': 'Requisição inválida'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    tags=["Usuário"],
    operation_summary='Buscar usuário por id',
    operation_description='Este endpoint serve para recuperar o usuário por seu id.',
    responses={200: openapi.Response('Success',), 404: openapi.Response('Not found')},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_by_id(request, id):
    try: 
        user = Usuario.objects.get(pk=id)
    except:
        formatted_response = {
            'success': False,
            'message': 'Usuário não localizado.'
        }
        return Response(formatted_response, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UsuarioSerializer(user)
        formatted_response = {
            'success': True,
            'message': 'Usuário recuperado com sucesso.',
            'data': serializer.data
        }
        return Response(formatted_response, status=status.HTTP_200_OK)
    
@swagger_auto_schema(
    method='post',
    tags=["Usuário"],
    operation_summary='Cadastrar usuário',
    operation_description='Este endpoint trata da criação de um novo usuário',
    responses={201: openapi.Response('Created'), 400: openapi.Response('Bad request')},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['nome', 'email', 'password', 'sexo', 'raca', 'regiao', 'nome_ies', 'modalidade_ensino', 'nome_curso', 'nome_turno_curso', 'sigla_uf_beneficiario', 'municipio_beneficiario', 'is_active', 'is_staff'],
        properties={
            'nome': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'sexo': openapi.Schema(type=openapi.TYPE_STRING),
            'raca': openapi.Schema(type=openapi.TYPE_STRING),
            'regiao': openapi.Schema(type=openapi.TYPE_STRING),
            'nome_ies': openapi.Schema(type=openapi.TYPE_STRING),
            'modalidade_ensino': openapi.Schema(type=openapi.TYPE_STRING),
            'nome_curso': openapi.Schema(type=openapi.TYPE_STRING),
            'nome_turno_curso': openapi.Schema(type=openapi.TYPE_STRING),
            'sigla_uf_beneficiario': openapi.Schema(type=openapi.TYPE_STRING),
            'municipio_beneficiario': openapi.Schema(type=openapi.TYPE_STRING)
        },
    ),
)
@api_view(['POST'])
def post_create_user(request):
    if request.method == 'POST':
        new_user = request.data
        email = new_user.get('email')
        
        if Usuario.objects.filter(email=email).exists():
            formatted_response = {
                'success': False,
                'message': 'Usuário já cadastrado.'
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = UsuarioSerializerRegister(data=new_user)

        if serializer.is_valid():
            serializer.save()

            formatted_response = {
                'success': True,
                'message': 'Usuário criado com sucesso.',
                'data': serializer.data
            }
            return Response(formatted_response, status=status.HTTP_201_CREATED)
        formatted_response = {
            'success': False,
            'message': 'Erro ao criar usuário.',
            'errors': serializer.errors
        }
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='put',
    tags=["Usuário"],
    operation_summary='Atualizar usuário por id',
    operation_description='Este endpoint trata da atualização dos dados de um usuário',
    responses={202: openapi.Response('Accepted'), 400: openapi.Response('Bad request')},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['nome', 'email', 'password', 'sexo', 'raca', 'regiao', 'nome_ies', 'modalidade_ensino', 'nome_curso', 'nome_turno_curso', 'sigla_uf_beneficiario', 'municipio_beneficiario', 'is_active', 'is_staff'],
        properties={
            'nome': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'sexo': openapi.Schema(type=openapi.TYPE_STRING),
            'raca': openapi.Schema(type=openapi.TYPE_STRING),
            'regiao': openapi.Schema(type=openapi.TYPE_STRING),
            'nome_ies': openapi.Schema(type=openapi.TYPE_STRING),
            'modalidade_ensino': openapi.Schema(type=openapi.TYPE_STRING),
            'nome_curso': openapi.Schema(type=openapi.TYPE_STRING),
            'nome_turno_curso': openapi.Schema(type=openapi.TYPE_STRING),
            'sigla_uf_beneficiario': openapi.Schema(type=openapi.TYPE_STRING),
            'municipio_beneficiario': openapi.Schema(type=openapi.TYPE_STRING)
        },
    ),
)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_edit_user(request, id):
    try:
        update_request = request.data
        update_user = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        formatted_response = {
            'success': False,
            'message': 'Usuário não localizado.'
        }
        return Response(formatted_response, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UsuarioSerializerRegister(update_user, data=update_request, partial=True)
        if serializer.is_valid():
            serializer.save()
            formatted_response = {
                'success': True,
                'message': 'Usuário editado com sucesso.',
                'data': serializer.data
            }
            return Response(formatted_response, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='delete',
    tags=["Usuário"],
    operation_summary='Deletar usuário por id',
    operation_description='Este endpoint trata da exclusão de um usuário',
    responses={200: openapi.Response('Sucess'), 404: openapi.Response('Not found')},
    
)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, id):
    try:
        if request.method == 'DELETE':
            user_exists = Usuario.objects.filter(id=id).exists()
            if user_exists:
                Usuario.objects.filter(id=id).delete()
                return JsonResponse({'success': True, 'message': 'Usuário deletado com sucesso.'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'success': False, 'message': 'Usuário não localizado.'}, status=status.HTTP_404_NOT_FOUND)
    
    except:
        return JsonResponse({'success': False, 'message': 'Erro interno no servidor:'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(name='post', decorator=swagger_auto_schema(
        operation_summary='Fazer login',
        tags=["Login"],
        operation_description='Este endpoint trata do login do usuário no sistema',
        responses={200: 'Sucesso', 401: 'Não autorizado', 400: 'Requisição inválida'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
        )
    ))

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Campos não preenchidos'}, status=status.HTTP_400_BAD_REQUEST)

        user = Usuario.objects.filter(email=email).first()

        if user is None:
            return Response({'error': 'Email inválido'}, status=status.HTTP_401_UNAUTHORIZED)
        
        authenticated_user = authenticate(email=email, password=password)
        
        if not authenticated_user:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(authenticated_user)
        return Response({
            'success': True,
            'message': 'Usuário autenticado com sucesso.',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    

@swagger_auto_schema(
    method='get',
    tags=["Usuário"],
    operation_summary='Buscar resultado por id',
    operation_description='Este endpoint serve para recuperar o resultado do usuário por seu id.',
    responses={200: openapi.Response('Success',), 404: openapi.Response('Not found')},
    
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result_ia_by_id(request, id):
    try:
        resultado = Resultado_ia.objects.get(usuario=id)
    except:
        formatted_response = {
            'success': False,
            'message': 'Resultado não localizado.'
        }
        return Response(formatted_response, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = Resultado_iaSerializer(resultado)
        formatted_response = {
            'success': True,
            'message': 'Resultado recuperado com sucesso.',
            'data': serializer.data
        }
        return Response(formatted_response, status=status.HTTP_200_OK)
    

@swagger_auto_schema(
    method='post',
    tags=["Usuário"],
    operation_summary='Gerar resultado por id',
    operation_description='Este endpoint serve para gerar o resultado do usuário por seu id.',
    responses={200: openapi.Response('Success',), 404: openapi.Response('Not found')},
    
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_resultado_ia(request, id):
    if request.method == 'POST':
        try:
            user = Usuario.objects.get(pk=id)
            dados = {
                'NOME_IES_BOLSA': [user.nome_ies],
                'MODALIDADE_ENSINO_BOLSA': [user.modalidade_ensino],
                'NOME_CURSO_BOLSA': [user.nome_curso],
                'NOME_TURNO_CURSO_BOLSA': [user.nome_turno_curso],
                'SEXO_BENEFICIARIO_BOLSA': [user.sexo],
                'RACA_BENEFICIARIO_BOLSA': [user.raca],
                'REGIAO_BENEFICIARIO_BOLSA': [user.regiao],
                'SIGLA_UF_BENEFICIARIO_BOLSA': [user.sigla_uf_beneficiario],
                'MUNICIPIO_BENEFICIARIO_BOLSA': [user.municipio_beneficiario]
            }
            resultado = fazer_previsao(dados)

            resultado = resultado.tolist()[0]
            
            serializer = Resultado_iaSerializer(data={
                'resultado': resultado,
                'usuario': user.id
            })
            if serializer.is_valid():
                serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_200_OK) 
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Erro interno no servidor: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    

@swagger_auto_schema(
    method='get',
    tags=["Buscar CEP"],
    operation_summary='Buscar os dados através do CEP',
    operation_description='Este endpoint serve para recuperar as informações de CEP.',
    responses={200: openapi.Response('Success',), 500: openapi.Response('Internal server error')},
    
)
@api_view(['GET'])
def consultar_cep(request, cep):
    if request.method == 'GET':
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)

    if response.status_code == 200:
        dados_cep = response.json()
        return JsonResponse(dados_cep)
    else:
        return JsonResponse({'error': 'Erro ao obter informações do CEP'}, status=500)





        