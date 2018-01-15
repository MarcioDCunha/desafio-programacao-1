# -*- coding: cp1252 -*-

try:
    reload(dominio)
except:
    import dominio

from dominio import Servidor, Servidores
from extratores import *

dominio.logging.info(': inciando...')


servidores = Servidores()
servidores = extrator_fita_espelho(servidores, Servidor)



for servidor in servidores.values():
    servidor.insert_or_update()


# eu = servidores['1529094']
# print "Sincronizando o servidor: %s de matricula: %s de id: %s" % (eu.nome,eu.matricula,eu.id)
# eu.insert_or_update_servidor()
# eu.insert_or_update_cargo()
# eu.insert_or_update_funcao()
# eu.insert_or_update_ocorrencias()

dominio.logging.info(': final')


# contador = 0
# for servidor in servidores.values():
    # if servidor.morto == '':
        # try:
            # #print '%s - %s' % (servidor.login, servidor.nome)
            # contador +=1
        # except:
            # pass
# #print 'TOTAL', contador



# # matriculas = [chave for chave in servidores.keys() if chave.isdigit()]
#print len(matriculas)
#print servidores['0764088'] Celso
#print servidores['1556564'] Claudia
#print servidores['1529094'] Claudio
# eu = servidores['1529094']
# print "Sincronizando o servidor: %s de matricula: %s" % (eu.nome,eu.matricula)
# eu.insert_or_update_servidor()
# idServidor = eu.obter_id_servidor()
# eu.insert_or_update_cargo(idServidor)
# eu.insert_or_update_funcao(idServidor)
# eu.insert_or_update_ocorrencias(idServidor)


#servidores = extrator_planilha(servidores, Servidor)
#print len([chave for chave in servidores.keys() if chave.isdigit()])
#servidores = extrator_fita_espelho(servidores, Servidor)
#print len([chave for chave in servidores.keys() if chave.isdigit()])
#servidores = extrator_ad(servidores, Servidor)
#print len([chave for chave in servidores.keys() if chave.isdigit()])


#print 'estados civis:'
#print servidores.estado_civil
#print 'situacoes:'
#print servidores.situacao
#print 'cargo:'
#print servidores.cargo
#print 'classe:'
#print servidores.classe
#print 'padrao:'
#print servidores.padrao
#print 'funcao:'
#print servidores.funcao
#print 'niveis:'
#print servidores.nivel
#print 'lotacoes:'
#print servidores.lotacao
#print 'coordenacoes:'
#print servidores.coordenacao
#print 'diretorias:'
#print servidores.diretoria

#print len(servidores)
#print len(servidores.values())



#for servidor in servidores.values():
#    try:
#        print servidor.codigo_situacao, servidor.situacao
#        print servidor.codigo_estado_civil, servidor.estado_civil
#        print servidor.codigo_cargo, servidor.cargo
#        print servidor.codigo_lotacao, servidor.lotacao
#    except:
#        print 'opa'


# l = [(servidor.nome, servidor.dataIngreServPublico) for servidor in servidores.values()
     # if (servidor.codigoSituacaoServidor == '04'
         # and servidor.dataIngreServPublico != '00000000')]

# l1 = [servidor for servidor in servidores.values()
     # if (servidor.codigoSituacaoServidor == '04'
         # and servidor.dataIngreServPublico != '00000000')]

# l2 = [servidor for servidor in servidores.values()
      # if servidor.codigoSituacaoServidor == '04']

# s = set(l1)
# s2 = set(l2)

# s3 = s ^ s2
# print len(s3)

# print servidores['0764088'] in s3

# print len(l2)

# print len(l)
# for i, j in l:
    # print i, '->', j

