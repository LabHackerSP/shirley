import base64
import urllib2
from StringIO import StringIO
from lxml.etree import parse
from util import striprtf
import re, codecs
import markov

#sentencas = codecs.open('sentencas.txt','w', encoding='utf-8')
#sentencas.close()

def get_discursos(lista_discursos, deputado):
	for url in lista_discursos:
		source = urllib2.urlopen(url)
		soup = parse(source)
		rtf = base64.b64decode(soup.xpath('discursoRTFBase64')[0].text)
		rtf = striprtf(rtf)

		sentencas = codecs.open('input.txt','a', encoding='utf-8')
		for p in rtf.split('\n'):
			for linha in re.split("[.!?;\n\t]", p.lower()):
				linha = linha.strip()
				if len(linha)>20:
					if 'do orador' not in linha and '-' not in linha and not re.match("^"+deputado.lower(),linha):
						sentencas.write(linha+'\n')
		sentencas.close()

for ano in range(2016,2017):
	deputado = 'JAIR%20BOLSONARO'
	discursos = "http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/ListarDiscursosPlenario?dataIni=15/01/"+str(ano)+"&dataFim=30/12/"+str(ano)+"&codigoSessao=&parteNomeParlamentar="+deputado.upper()+"&siglaPartido=&siglaUF="
	source = urllib2.urlopen(discursos)
	soup = parse(source)
	lista_discursos = []
	for d in soup.xpath('//discurso'):
		codigo = d.xpath('./ancestor::sessao[1]/codigo')[0].text.strip()
		numOrador = d.xpath('./orador/numero')[0].text.strip()
		numQuarto = d.xpath('./numeroQuarto')[0].text.strip()
		numInsercao = d.xpath('./numeroInsercao')[0].text.strip()
		url = 'http://www.camara.leg.br/SitCamaraWS/SessoesReunioes.asmx/obterInteiroTeorDiscursosPlenario?codSessao='+codigo+'&numOrador='+numOrador+'&numQuarto='+numQuarto+'&numInsercao='+numInsercao
		lista_discursos.append(url)
	print "Baixando " + str(len(lista_discursos)) + " discursos de " + str(ano)
	get_discursos(lista_discursos, deputado)
