# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm, CharField, Form, BooleanField

from django.contrib.auth.models import User

class Voluntario(User):
	telefone = models.IntegerField(null=True)
	telefone2 = models.IntegerField(null=True)
	formacao = models.CharField(max_length=100)
	categoria = models.IntegerField(null=True) # 0 = condutor , 1 =  preto , 2 = verde

	def nome(self):
		return self.first_name + " " + self.last_name

class VoluntarioForm(ModelForm):
	first_name = CharField(label='Primeiro nome')
	last_name = CharField(label='Último nome')
	telefone2 = CharField(label='Telefone alternativo')
	formacao = CharField(label='Formação')

	class Meta:
		model = Voluntario
		fields = ('first_name', 'last_name', 'email', 'telefone', 'telefone2', 'formacao', 'categoria')

class Disponibilidade(models.Model):
	voluntario = models.ForeignKey(Voluntario)
	dia = models.IntegerField()
	turno = models.IntegerField()

class DisponibilidadeForm(Form):
	seg1 = BooleanField(required=False)
	seg2 = BooleanField(required=False)
	seg3 = BooleanField(required=False)
	ter1 = BooleanField(required=False)
	ter2 = BooleanField(required=False)
	ter3 = BooleanField(required=False)
	qua1 = BooleanField(required=False)
	qua2 = BooleanField(required=False)
	qua3 = BooleanField(required=False)
	qui1 = BooleanField(required=False)
	qui2 = BooleanField(required=False)
	qui3 = BooleanField(required=False)
	sex1 = BooleanField(required=False)
	sex2 = BooleanField(required=False)
	sex3 = BooleanField(required=False)
	sab1 = BooleanField(required=False)
	sab2 = BooleanField(required=False)
	sab3 = BooleanField(required=False)
	dom1 = BooleanField(required=False)
	dom2 = BooleanField(required=False)
	dom3 = BooleanField(required=False)

class Escala(models.Model):
	data = models.DateField()
	turno = models.IntegerField()
	condutor = models.ForeignKey(Voluntario, related_name="condutor", null=True)
	preto = models.ForeignKey(Voluntario, related_name="preto", null=True)
	outro = models.ForeignKey(Voluntario, related_name="outro", null=True)

class Aviso(models.Model):
	titulo = models.CharField(max_length=100)
	date = models.DateTimeField()
	mensagem = models.TextField()

class Apoio(models.Model):
	data_inicio = models.DateTimeField()
	data_fim = models.DateTimeField()
	nome = models.CharField(max_length=100)

class Turno(models.Model):
	apoio = models.ForeignKey(Apoio)
	data_inicio = models.DateTimeField()
	data_fim = models.DateTimeField()

class Inscricao(models.Model):
	turno = models.ForeignKey(Turno)
	voluntario = models.ForeignKey(Voluntario)
	observacoes = models.TextField()
	aprovado = models.BooleanField()

class Troca(models.Model):
	voluntario_req = models.ForeignKey(Voluntario, related_name="voluntario_req")
	escala_req = models.ForeignKey(Escala, null=True, related_name="escala_req")
	voluntario_ac = models.ForeignKey(Voluntario, null=True, related_name="voluntario_ac")
	escala_ac = models.ForeignKey(Escala, null=True, related_name="escala_ac")

	def get_tipo(self):
		if self.escala_req and self.voluntario_ac and escala_ac:
			return "Troca por Troca"
		elif escala_req and voluntario_ac and (not escala_ac):
			return "Fica em divida"
		elif escala_ac and (not voluntario_ac) and (not escala_req):
			return "Faz buraco"
		elif escala_ac and escala_req and (not voluntario_ac):
			return "Troca com burado"
		else:
			return "Erro na definição da funções"



