#!/usr/bin/env python
# -*- coding: cp1252 -*-


import csv
import os

from unicodedata import normalize

caminho_da_fita = os.path.abspath(os.path.join(os.curdir, 'FITA_ESPELHOdeTeste.TXT'))
print caminho_da_fita
def remover_acentos(txt, codif='cp1252'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

def extrator_fita_espelho(servidores, Servidor):
    fita_espelho = open(caminho_da_fita, 'r')
    fita_espelho.seek(0)

    for linha in fita_espelho.readlines():

        # Registro Mestre (header). Identifica o órgão processado:
				# Verifica a linha 18
        if linha[17:18] == '0':
            constanteHeader = linha[0:17]
            tipoRegistroHeader = linha[17:18]
            constanteHeader1 = linha[18:30]
            codigoHeader = linha[30:35]
            siglaHeader = linha[35:45]
            mesAnoPagamentoHeader = linha[45:51]
            fillerHeader = linha[51:764]

        # Dados Pessoais:
        if linha[17:18] == '1':
            servidor = servidores.get(linha[9:16], Servidor(morto='X'))  ###################
            servidor.upagadora = linha[0:9]
            servidor.matricula = linha[9:16]
            servidor.matricula_dv = linha[16:17]
            servidor.tipoRegistro = linha[17:18]
            servidor.nome = ' '.join(linha[20:80].split())
            servidor.cpf = linha[80:91]
            servidor.pis_pasep = linha[91:102]
            servidor.nome_mae = linha[102:152]
            servidor.sexo = linha[152:153]
            servidor.data_nascimento = linha[153:161]
            servidor.codigo_estado_civil = linha[161:162]
            servidor.nivel_escolaridade = linha[162:164]
            servidor.codigo_titulacao_formacao = linha[164:166]
            servidor.filler1 = linha[166:171]
            servidor.nacionalidade = linha[171:172]
            servidor.naturalidade = linha[172:174]
            servidor.pais = linha[174:177]
            servidor.ano_chegada = linha[177:181]
            servidor.ir = linha[181:183]
            servidor.sf = linha[183:185]
            servidor.data1Emprego = linha[185:193]
            servidor.identificacaoOrigem = linha[193:201]

            # endereco:
            servidor.endereco.logradouro = linha[201:241]
            servidor.endereco.numero = linha[241:247]
            servidor.endereco.complemento = linha[247:268]
            servidor.endereco.bairro = linha[268:293]
            servidor.endereco.municipio = linha[293:323]
            servidor.endereco.cep = linha[323:331]
            servidor.endereco.uf = linha[331:333]

            servidor.registroGeral = linha[333:347]
            servidor.siglaOrgaoExpeditor = linha[347:352]
            servidor.dataExpedicaoIdentidade = linha[352:360]
            servidor.siglaUfIdentidade = linha[360:362]

            servidor.tituloEleitor = linha[362:375]
            servidor.filler2 = linha[375:764]

        # Dados Funcionais:
        if linha[17:18] == '2':
            servidor.siglaRegimeJuridico = linha[20:23]
            servidor.codigo_situacao = linha[23:25]

            servidor.numeroCarteira = linha[25:31]
            servidor.serieCarteira = linha[31:36]
            servidor.ufCarteira = linha[36:38]

            servidor.bancoPagamento = linha[36:38]
            servidor.agenciaPagamento = linha[41:47]
            servidor.contaCorrentePagamento = linha[47:60]

            servidor.dataOpcaoFgts = linha[60:68]
            servidor.bancoFgts = linha[68:71]
            servidor.agenciaFgts = linha[71:77]
            servidor.contaCorrenteFgts = linha[77:90]

            servidor.jornadaTrabalho = linha[90:92]

            servidor.percentualTempoServico = linha[92:94]
            servidor.dataCadastramentoServidor = linha[94:102]
            servidor.indicadorSupressaoPagamento = linha[102:103]
            servidor.dataSupressaoPagamento = linha[103:109]
            servidor.numeradorProporcionalidade = linha[109:111]
            servidor.denominadorProporcionalidade = linha[111:113]

            # Cargo/Emprego
            servidor.grupo = linha[113:116]
            servidor.codigo_cargo = linha[116:119]
            servidor.classe = linha[119:120]
            servidor.referencia_nivel_padrao = linha[120:123]
            servidor.padrao = linha[120:123].strip('0').strip('0')
            servidor.data_entrada_cargo = linha[123:131]
            servidor.data_saida_cargo = linha[131:139]

            # Funcao
            servidor.funcao = linha[139:142]
            servidor.codigo_nivel = linha[142:147]
            servidor.escolaridadeFuncao = linha[147:149]
            servidor.opcaoFuncao = linha[149:150]
            servidor.dataIngressoFuncao = linha[150:158]
            servidor.dataSaidaFuncao = linha[158:166]
            servidor.unidadeOrganizacionalFuncao = linha[166:175]

            # Nova Funcao:
            servidor.siglaNovaFuncao = linha[175:178]
            servidor.codigoNivelNovaFuncao = linha[178:183]
            servidor.escolaridadeNovaFuncao = linha[183:185]
            servidor.opcaoNovaFuncao = linha[185:186]
            servidor.dataIngressoNovaFuncao = linha[186:194]
            servidor.dataSaidaNovaFuncao = linha[194:202]
            servidor.unidadeOrganizacionalNovaFuncao = linha[202:211]

            servidor.atividadeDaFuncao = linha[211:215]

            servidor.unidadeOrganizacionalLotacao = linha[215:224]
            servidor.codigo_lotacao = linha[215:224] #####################            servidor.codigo_lotacao = linha[215:224].strip('0') #####################

            servidor.dataLotacao = linha[224:232]
            servidor.orgaoLocalizacao = linha[232:237]
            servidor.unidadeOrganizacionalLocalizacao = linha[237:246]
            servidor.grupoIngressoOrgao = linha[246:248]
            servidor.ocorrenciaIngressoOrgao = linha[248:251]
            servidor.dataIngressoOrgao = linha[251:259]
            servidor.codigoDiplomaLegal = linha[259:261]
            servidor.numeroDiplomaLegal = linha[261:270]
            servidor.dataPublicacaoDiplomaLegal = linha[270:278]

            servidor.grupoIngreServPublico = linha[278:280]
            servidor.ocorrenciaIngreServPublico = linha[280:283]
            servidor.dataIngreServPublico = linha[283:291]
            servidor.codDipLegalIngreServPublico = linha[291:293]
            servidor.numDipLegalIngreServPublico = linha[293:302]
            servidor.dataDipLegalIngreServPublico = linha[302:310]

            servidor.grupoOcorrenciaExclu = linha[310:312]
            servidor.ocorrenciaExclu = linha[312:315]
            servidor.dataOcorrenciaExclu = linha[315:323]
            servidor.codDipLegalOcorrenciaExclu = linha[323:325]
            servidor.numDipLegalOcorrenciaExclu = linha[325:334]
            servidor.dataDipLegalOcorrenciaExclu = linha[334:342]

            servidor.grupoOcoAfastamento = linha[342:344]
            servidor.ocorrenciaAfastamento = linha[344:347]
            servidor.dataInicioOcoAfastamento = linha[347:355]
            servidor.dataTerminoOcoAfastamento = linha[355:363]
            servidor.codDipLegalOcoAfastamento = linha[363:365]
            servidor.numDipLegalOcoAfastamento = linha[365:374]
            servidor.dataDipLegalOcoAfastamento = linha[374:382]

            servidor.grupoOcoInatividade = linha[382:384]
            servidor.ocorrenciaInatividade = linha[384:387]
            servidor.dataOcoInatividade = linha[387:395]
            servidor.codDipLegalOcoInatividade = linha[395:397]
            servidor.numDipLegalOcoInatividade = linha[397:406]
            servidor.dataDipLegalOcoInatividade = linha[406:414]

            servidor.numProcOcoAposentadoria = linha[414:429]
            servidor.anoPrevOcoAposentadoria = linha[429:433]
            servidor.opcaoIntOcoAposentadoria = linha[433:434]

            servidor.uorgControle = linha[434:443]
            servidor.grupoOcoModFuncional = linha[443:445]
            servidor.ocorrenciaModFuncional = linha[445:448]
            servidor.dataOcoModFuncional = linha[448:456]
            servidor.codDipLegalOcoModFuncional = linha[456:458]
            servidor.numDipLegalOcoModFuncional = linha[458:467]
            servidor.dataDipLegalOcoModFuncional = linha[467:475]

            servidor.regJuAnterior = linha[475:478]
            servidor.sitServAnterior = linha[478:480]
            servidor.orgDestMudOrg = linha[480:485]
            servidor.dataLibDestMudOrg = linha[485:493]
            servidor.orgOriLibDestMudOrg = linha[493:498]
            servidor.orgAnterior = linha[498:503]
            servidor.matAnterior = linha[503:510]
            servidor.codOrgExtMod = linha[510:515]
            servidor.matServExtMod = linha[515:522]
            servidor.orgaoAtual = linha[522:527]
            servidor.matriculaAtual = linha[527:534]
            servidor.codUpagMud = linha[534:543]
            servidor.dataLibUpagMud = linha[543:551]
            servidor.motivoUpagMud = linha[551:552]
            servidor.indPagServidor = linha[552:553]
            servidor.nomeCartRegObito = linha[553:603]
            servidor.numLivroRegObito = linha[603:611]
            servidor.numFolhaRegObito = linha[611:617]
            servidor.numRegistroRegObito = linha[617:625]
            servidor.dataRegObito = linha[625:633]
            servidor.indExcluInstituidor = linha[633:634]
            servidor.dataExcluInstituidor = linha[634:642]
            servidor.tipoValeAlimentacao = linha[642:643]
            servidor.dataInicioValeAlimentacao = linha[643:651]
            servidor.dataFimValeAlimentacao = linha[651:659]
            servidor.indOpeRaiox = linha[659:660]
            servidor.orgaoRequisitante = linha[660:665]
            servidor.codVaga = linha[665:672]
            servidor.mesConceAnuenio = linha[672:674]
            servidor.perOpeRaiox = linha[674:679]
            servidor.codGrupoPosse = linha[679:681]
            servidor.ocorrenciaPosse = linha[681:684]
            servidor.dataPosse = linha[684:692]
            servidor.codDiplomaPosse = linha[692:694]
            servidor.dataDiplomaPosse = linha[694:702]
            servidor.numeroDiplomaPosse = linha[702:711]
            servidor.grupoOcoRevAtividade = linha[711:713]
            servidor.codOcoRevAtividade = linha[713:716]
            servidor.dataOcoRevAtividade = linha[716:724]
            servidor.codDiploRevAtividade = linha[724:726]
            servidor.dataDiploRevAtividade = linha[726:734]
            servidor.numDiploRevAtividade = linha[734:743]
            servidor.cargoCalcAutomatico = linha[743:744]
            servidor.funcaoCalcAutomatico = linha[744:745]
            servidor.salFamiliaCalcAutomatico = linha[745:746]
            servidor.adicTemServCalcAutomatico = linha[746:747]
            servidor.fgtsCalcAutomatico = linha[747:748]
            servidor.prevSocialCalcAutomatico = linha[748:749]
            servidor.impRendaCalcAutomatico = linha[749:750]
            servidor.marConsigCalcAutomatico = linha[750:751]
            servidor.contriSindiCalcAutomatico = linha[751:752]
            servidor.adian13CalcAutomatico = linha[752:753]
            servidor.abateTetoConstCalcAutomatico = linha[753:754]
            servidor.sal13CalcAutomatico = linha[754:755]
            servidor.planSegSocial6CalcAutomatico = linha[755:756]
            servidor.feriasCalcAutomatico = linha[756:757]
            servidor.pensaoCalcAutomatico = linha[757:758]
            servidor.beneficiosCalcAutomatico = linha[758:759]
            servidor.ipmfCpmfCalcAutomatico = linha[759:760]
            servidor.raisCalcAutomatico = linha[760:761]
            servidor.difUrvCalcAutomatico = linha[761:762]
            servidor.adiantamentoCalcAutomatico = linha[762:763]
            servidor.rendPasepCalcAutomatico = linha[763:764]

        try:
            servidores[servidor.matricula] = servidor
            servidores[remover_acentos(servidor.nome.lower())] = servidor
        except NameError: pass


        # Dados Financeiros:
        if linha[17:18] == '3':
            pass

        # Dados Financeiros, totalização:
        if linha[17:18] == '4':
            pass

        # Registro Trailler. Quantidades de UPAG's e de servidores no arquivo:
        if linha[17:18] == '9':
            quantidadeServidores = linha[21:27]

    return servidores






# def extrator_planilha(servidores, Servidor):
    # caminhos = ['D:\\avaliacao\\arquivos\\servidores_ativos.csv',
                # 'D:\\avaliacao\\arquivos\\servidores_ativos2.csv']

    # for caminho in caminhos:
        # row_dics = csv.DictReader(open(caminho, 'rb'), delimiter=';')
        # for d in row_dics:
            # s = servidores.get(d['matricula'], Servidor(d))
            # #s = servidores.get(d['matricula'], Servidor())
            # #s.__dict__.update(d)
            # servidores[d['matricula']] = s
            # nome = remover_acentos(' '.join(d['nome'].split())).lower()
            # servidores[nome] = s

    # return servidores


# def extrator_ad(servidores, Servidor):
    # logins_txt = open('arquivos\\usuarios_login_AD.txt', 'rb')

    # for linha in logins_txt.readlines()[1:]:
        # nome, sei_la, login = linha.strip().split(',')
        # nome = remover_acentos(nome).lower()
        # #servidor = servidores.get(nome, Servidor(morto='X'))
        # try:
            # servidor = servidores[nome]
        # except KeyError:
            # continue
        # servidor.login = login
        # servidores[nome] = servidor

    # logins_txt.close()

    # return servidores
