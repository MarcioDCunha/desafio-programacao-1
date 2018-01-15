# -*- coding: UTF-8 -*-
#The built-in open function lets you create, open, and modify files. This module
#adds those extra functions you need to rename and remove files:
import os
import logging

# LOGGING: Ao importar o 'logging' definimos sua 'configuração básica', seguinte:
try:
    logging.basicConfig( level    = logging.DEBUG,
                      format   = '%(asctime)s %(levelname)-8s %(message)s',
                      datefmt  = '%a, %d %b %Y %H:%M:%S',
                      filename = os.path.join('log_erros_SIAPE.txt'),
                      filemode = 'a' )
except: raise


import MySQLdb
con = MySQLdb.connect('localhost','root','admin')
#con = MySQLdb.connect('172.16.111.50','crp','crp123')
con.select_db('corp')
cursor = con.cursor()

class Dominio(object):
    def __str__(self):
        repr = ''
        for k, v in self.__dict__.items():
            repr += '? -> ?\n' % (k, v)
        return repr


class Endereco(Dominio):
    def strip(self): return self


class Servidores(dict):
    def _exibir(self, atributo):
        return '\n'.join(sorted(a for a in atributo if a)) + '\n'



    def __getattr__(self, attr):
        try:
            retorno = set([getattr(servidor, attr).strip() for servidor in self.values()])
        except AttributeError:
            retorno = set([])
        return retorno


class Servidor(Dominio):
    def __init__(self, d={}, morto=''):
        self.morto = morto
        self.endereco = Endereco()

        if d:
            for k, v in d.items():
                k = k.strip(' ')
                v = v.strip(' ')
                if k == 'nome':
                    v = ' '.join(v.split())
                if k:
                    setattr(self, k.strip(), v.strip())

    _id = ''
    @property
    def id(self):
        if not self._id:
            cursor.execute('''select cd_servidor from crp_servidor where CD_MATRIC_SIAPE=%s''', (self.matricula,))
            resultSet = cursor.fetchone()
            if resultSet:
                self._id = resultSet[0]
            else:
                logging.error("ID do Servidor não existe %s" % (self.matricula))
        return self._id

    _id_pessoa = ''
    @property
    def id_pessoa(self):
        if not self._id_pessoa:
            cursor.execute('''vvvvvvvv''')
            resultSet = cursor.fetchone()
            if resultSet:
                self._id_pessoa = resultSet[0]
            else:
                logging.error("ID da Pessoa não existe %s" % (self.matricula))
        return self._id_pessoa



    def insert_or_update(self):

#         self.insert_or_update_pessoa()
#         self.insert_or_update_pessoa_fisica()
#         self.insert_or_update_uorg()
#         self.insert_or_update_situacao()
#         self.insert_or_update_funcoes()
#         self.insert_or_update_cargo()
#         self.insert_or_update_servidor()
#         self.insert_or_update_endereco_servidor()
#         self.insert_or_update_cargo_servidor()
#         self.insert_or_update_historico_funcao_servidor()
         self.insert_or_update_historico_uorg_servidor()
#         self.insert_or_update_ocorrencia_ingresso_servico_publico()
#         self.insert_or_update_ocorrencia_ingresso_orgao()
#         self.insert_or_update_ocorrencia_exclusao()
#         self.insert_or_update_ocorrencia_afastamento()
#         self.insert_or_update_ocorrencia_inatividade()
#         self.insert_or_update_ocorrencia_modificacao_funcional()
#         self.insert_or_update_ocorrencia_aposentadoria()
#         self.insert_or_update_usuario()
#         self.insert_or_update_email()
#         self.insert_or_update_telefone()


    @property
    def esta_na_base(self):
        cursor.execute('''select cd_servidor from crp_servidor where CD_MATRIC_SIAPE=%s''', (self.matricula))
        return cursor.fetchall()




    def insert_or_update_pessoa(self):
        print "PESSOA " + self.nome + "..."
        ic_tipo_pessoa = "F"
        if (self.funcao == "ETG"):
            vinculo = 9
        else:
            vinculo = 1
        try:
            cursor.execute('''SELECT cd_servidor FROM crp_servidor WHERE cd_matric_siape=%s''',(self.matricula))
            if not cursor.fetchall():

                cursor.execute('''INSERT INTO crp_pessoa (CD_VINCULO,
                                                             NM_PESSOA,
                                                             IC_TIPO_PESSOA,
                                                             CD_DOCUMENTO,
                                                             CD_NATURALIDADE,
                                                             CD_NACIONALIDADE,
                                                             CD_RG) values (%s,%s,%s,%s,%s,%s,%s)''',
                                                             (vinculo,
                                                              self.nome,
                                                              ic_tipo_pessoa,
                                                              self.cpf,
                                                              self.naturalidade,
                                                              self.nacionalidade,
                                                              self.registroGeral))
                con.commit()
            else:
                print "               Atualizando pessoa..." 
                cursor.execute('''UPDATE crp_pessoa SET CD_VINCULO=%s,
                                                           NM_PESSOA=%s,
                                                           IC_TIPO_PESSOA=%s,
                                                           CD_DOCUMENTO=%s,
                                                           CD_NATURALIDADE=%s,
                                                           CD_NACIONALIDADE=%s,
                                                           CD_RG=%s
                                                           WHERE CD_PESSOA=%s''',
                                                           (vinculo,
                                                            self.nome,
                                                            ic_tipo_pessoa,
                                                            self.cpf,
                                                            self.naturalidade,
                                                            self.nacionalidade,
                                                            self.registroGeral,
                                                            self.id))
                con.commit()
        except:
              logging.error("Erro no método Pessoa %s para %s %s")


    def insert_or_update_pessoa_fisica(self):
        print "      PESSOA FISICA..."
        try:
            if self.codigo_estado_civil == "1":
                sigla_estado_civil = "S"
            elif self.codigo_estado_civil == "2":
                sigla_estado_civil = "C"
            elif self.codigo_estado_civil == "3":
                sigla_estado_civil = "J"
            elif self.codigo_estado_civil == "4":
                sigla_estado_civil = "D"
            else:
                sigla_estado_civil = "V"
            data_nascimento_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.data_nascimento))))
            if self.data_nascimento == "00000000":
                data_nascimento = None
            else:
                data_nascimento = data_nascimento_formatada
            cursor.execute('''SELECT cd_servidor FROM crp_servidor WHERE cd_matric_siape=%s''',(self.matricula,))
            if not cursor.fetchall():
                print "               Inserindo pessoa fisica..."
                cursor.execute('''INSERT INTO crp_pessoa_fisica (CD_PESSOA_FISICA,
                                                                 DT_NASCIMENTO,
                                                                 IC_SEXO,
                                                                 IC_ESTADO_CIVIL) values (%s,%s,%s,%s)''',
                                                                 (self.id_pessoa,
                                                                 data_nascimento,
                                                                 self.sexo,
                                                                 sigla_estado_civil))
                con.commit()
            else:
                print "               Atualizando pessoa fisica..."
                cursor.execute('''UPDATE crp_pessoa_fisica SET DT_NASCIMENTO=%s,
                                                           IC_SEXO=%s,
                                                           IC_ESTADO_CIVIL=%s
                                                           WHERE CD_PESSOA_FISICA=%s''',
                                                           (data_nascimento,
                                                            self.sexo,
                                                            sigla_estado_civil,
                                                            self.id))
                con.commit()
        except:
              logging.error("Erro gerado no metodo insert_or_update_pessoa_fisica")# % (unidade_valida, self.nome, self.matricula))


    def insert_or_update_uorg(self):
        print "            UORG..."
#        if self.funcao == "DAS" and self.dataSaidaFuncao == "00000000":
        if (self.funcao == "DAS") or (self.funcao == "FIN") or (self.funcao == "FGR"):
            unidade_valida = self.unidadeOrganizacionalFuncao
        else:
            unidade_valida = self.unidadeOrganizacionalLotacao
        if (self.siglaNovaFuncao == "DAS") or (self.siglaNovaFuncao == "FIN") or (self.siglaNovaFuncao == "FGR"):
            tem_uorg_na_nova_funcao_na_fita = True
            unidade_valida_nova = self.unidadeOrganizacionalNovaFuncao
            numero_uorg_nova = unidade_valida_nova[5:9]
            uorg_nova = "Atualizar UORG " + numero_uorg_nova 
        else:
            tem_uorg_na_nova_funcao_na_fita = False
        numero_uorg = unidade_valida[5:9]
        uorg_superior = "000000000"
        uorg = "Atualizar UORG " + numero_uorg
        sigla_uorg = "desc"
        nome_diretoria = "desc"
        nome_coordenacao = "desc"


        if tem_uorg_na_nova_funcao_na_fita == True:
            cursor.execute('''SELECT cd_unidade_organiz FROM crp_unidade_organizacional WHERE cd_unidade_organiz=%s''',(unidade_valida_nova))
            if not cursor.fetchall():
                cursor.execute('''INSERT INTO crp_unidade_organizacional (CD_UNIDADE_ORGANIZ,
                                                             CD_UNIDADE_SUPERIOR,
                                                             NM_UNIDADE_ORGANIZ,
                                                             SG_UNIDADE_ORGANIZ,
                                                             NM_DIRETORIA,
                                                             NM_COORDENACAO) values (%s,%s,%s,%s,%s,%s)''',
                                                             (unidade_valida_nova,
                                                              uorg_superior,
                                                              uorg_nova,
                                                              sigla_uorg,
                                                              nome_diretoria,
                                                              nome_coordenacao))
                con.commit()
            else:
                pass
        try:
            cursor.execute('''SELECT cd_unidade_organiz FROM crp_unidade_organizacional WHERE cd_unidade_organiz=%s''',(unidade_valida))
            if not cursor.fetchall():
                cursor.execute('''INSERT INTO crp_unidade_organizacional (CD_UNIDADE_ORGANIZ,
                                                             CD_UNIDADE_SUPERIOR,
                                                             NM_UNIDADE_ORGANIZ,
                                                             SG_UNIDADE_ORGANIZ,
                                                             NM_DIRETORIA,
                                                             NM_COORDENACAO) values (%s,%s,%s,%s,%s,%s)''',
                                                             (unidade_valida,
                                                              uorg_superior,
                                                              uorg,
                                                              sigla_uorg,
                                                              nome_diretoria,
                                                              nome_coordenacao))
                con.commit()
            else:
                pass

        except:
              logging.error("Impossível inserir uorg %s " % (unidade_valida))


    def insert_or_update_situacao(self):
        print "                  SITUACAO " + self.codigo_situacao
        nome_situacao = "Atualizar situacao " + self.codigo_situacao
        try:
            cursor.execute('''SELECT cd_situacao_servidor FROM crp_situacao_servidor WHERE cd_situacao_servidor=%s''',(self.codigo_situacao,))
            if not cursor.fetchall():
                print "               Inserindo situacao na base..."
                cursor.execute('''INSERT INTO crp_situacao_servidor (CD_SITUACAO_SERVIDOR,
                                                             DS_SITUACAO_SERVIDOR) values (%s,%s)''',
                                                             (self.codigo_situacao,
                                                              nome_situacao))
                con.commit()
            else:
                pass
        except:
              logging.error("Impossível inserir situacao %s " % (self.codigo_situacao))






    def insert_or_update_funcoes(self):
        print "                        FUNCAO"
        nome_funcao = "Atualizar nome para funcao " + self.codigo_nivel
        nome_nova_funcao = "Atualizar nome para nova funcao " + self.codigoNivelNovaFuncao
        try:
#VERIFICA SE O CODIGO DA FUNCAO DO SERVIDOR E DIFERENTE DE ZERO(TEM FUNCAO), E NÃO ESTÁ NA BASE,
            cursor.execute('''SELECT cd_nivel FROM crp_funcao WHERE cd_nivel=%s and sg_funcao= %s''',(self.codigo_nivel,str(self.funcao)))
            if not cursor.fetchall():
                if self.codigo_nivel != "00000":
                    print "inserindo funcao"
                    cursor.execute('''INSERT INTO crp_funcao (SG_FUNCAO,
                                                                CD_NIVEL,
                                                                NM_FUNCAO,
                                                                IC_OPCAO) values (%s,%s,%s,%s)''',
                                                               (self.funcao,
                                                                self.codigo_nivel,
                                                                nome_funcao,
                                                                self.opcaoFuncao))
                    con.commit()
            else:
                print "atualizando funcao"
                cursor.execute('''UPDATE crp_funcao SET SG_FUNCAO=%s,
                                                             IC_OPCAO=%s
                                                             WHERE CD_NIVEL=%s and SG_FUNCAO=%s''',
                                                            (self.funcao,
                                                             self.opcaoFuncao,
                                                             self.codigo_nivel,
                                                             self.funcao))
                con.commit()

            cursor.execute('''SELECT cd_nivel FROM crp_funcao WHERE cd_nivel=%s and sg_funcao= %s''',(self.codigoNivelNovaFuncao,str(self.siglaNovaFuncao)))
            if not cursor.fetchall():
                if self.codigoNivelNovaFuncao != "00000":
                    print "inserindo nova funcao"
                    cursor.execute('''INSERT INTO crp_funcao (SG_FUNCAO,
                                                                CD_NIVEL,
                                                                NM_FUNCAO,
                                                                IC_OPCAO) values (%s,%s,%s,%s)''',
                                                               (self.siglaNovaFuncao,
                                                                self.codigoNivelNovaFuncao,
                                                                nome_nova_funcao,
                                                                self.opcaoNovaFuncao))
                    con.commit()
            else:
                print "atualizando nova funcao"
                cursor.execute('''UPDATE crp_funcao SET SG_FUNCAO=%s,
                                                             IC_OPCAO=%s
                                                             WHERE CD_NIVEL=%s and SG_FUNCAO=%s''',
                                                            (self.siglaNovaFuncao,
                                                             self.opcaoNovaFuncao,
                                                             self.codigoNivelNovaFuncao,
                                                             self.siglaNovaFuncao))
                con.commit()
        except:
              logging.error("Impossível inserir funcao %s " % (self.codigo_nivel))


    def insert_or_update_cargo(self):
        print "                              CARGO"
        nome_cargo = "Outros"
        situacao_cargo = "I"
        codigo_cargo = self.grupo+self.codigo_cargo
        try:
#VERIFICA SE O CODIGO DO CARGO ESTA NA BASE A PARTIR DA JUNÇÃO DE GRUPO E NUMERO CARGO
            cursor.execute('''SELECT cd_cargo FROM crp_cargo WHERE cd_cargo=%s''',(codigo_cargo,))
            if not cursor.fetchall():
                print "               Inserindo Novo Cargo..."
                cursor.execute('''INSERT INTO crp_cargo (CD_CARGO,
                                                                NM_CARGO,
                                                                IC_SITUACAO_CARGO) values (%s,%s,%s)''',
                                                               (codigo_cargo,
                                                                nome_cargo,
                                                                situacao_cargo))
                con.commit()                
            else:
                pass

        except:
              logging.error("Impossível inserir cargo %s " % (nome_cargo))



    def insert_or_update_servidor(self):
        print "                                                 SERVIDOR..."

        '''if ((self.funcao == "DAS") or (self.funcao == "ETG") or (self.funcao == "FIN") or (self.funcao == "FGR")) and (self.dataIngressoNovaFuncao == "00000000"):
            tem_funcao_s = True
        else:
            tem_funcao_s = False
        if ((self.siglaNovaFuncao == "DAS") or (self.siglaNovaFuncao == "ETG") or (self.siglaNovaFuncao == "FIN") or (self.siglaNovaFuncao == "FGR")) and (self.dataSaidaNovaFuncao == "00000000"):
            tem_nova_funcao_s = True
        else:
            tem_nova_funcao_s = False

        if tem_nova_funcao_s == True:
            unidade_valida_2 = self.unidadeOrganizacionalNovaFuncao
        elif tem_funcao_s == True:
            unidade_valida_2 = self.unidadeOrganizacionalFuncao
        else:
            unidade_valida_2 = self.unidadeOrganizacionalLotacao



        if self.funcao == "DAS" and self.dataSaidaFuncao == "00000000":
            unidade_valida = self.unidadeOrganizacionalFuncao
        else:
            unidade_valida = self.unidadeOrganizacionalLotacao'''




        if self.esta_na_base:
            print "id_da_pessoa"
            print self.id
            print "                                         Atualizando servidor..."
#SER FOR ESTAGIÁRIO NÃO ATUALIZA POIS É ATUALIZADO NA MÃO
#            if (self.funcao == "ETG"):
#                pass
#            else:
            cursor.execute('''UPDATE crp_servidor SET CD_SITUACAO_SERVIDOR=%s
                                                         WHERE CD_MATRIC_SIAPE=%s''',
                                                        (self.codigo_situacao,
                                                         self.matricula))
            con.commit()
        else:
            id_da_pessoa = self.id_pessoa
            print "id_da_pessoa"
            print id_da_pessoa
            print "                                          Inserindo servidor..."
            cursor.execute('''INSERT INTO crp_servidor (CD_SERVIDOR,
                                                               CD_MATRIC_SIAPE,
                                                               CD_SITUACAO_SERVIDOR) values (%s,%s,%s)''',
                                                              (id_da_pessoa,
                                                               self.matricula,
                                                               self.codigo_situacao))
            con.commit()


    def insert_or_update_endereco_servidor(self):
#Método feito em função dos relacionamento pessoa x endereco ser: um para um
        print "                                                ENDERECO"
        try:
            if self.pais == "073":
                pais = "HT"
            elif self.pais == "088":
                pais = "IT"
            elif self.pais == "129":
                pais = "PT"
            elif self.pais == "040":
                pais = "CO"
            elif self.pais == "055":
                pais = "US"
            elif self.pais == "037":
                pais = "CN"
            elif self.pais == "011":
                pais = "AR"
            elif self.pais == "128":
                pais = "PL"
            else:
                pais = "BR"

            cursor.execute('''select cd_pessoa from crp_endereco_pessoa where cd_pessoa=%s''', (self.id,))
            if cursor.fetchall():
                print "               Atualizando endereco da pessoa..."
                cursor.execute('''UPDATE crp_endereco_pessoa SET CD_PAIS=%s,
                                                                   NM_CIDADE=%s,
                                                                   NM_LOGRADOURO=%s,
                                                                   NO_ENDERECO=%s,
                                                                   DS_COMPLEMENTO=%s,
                                                                   NM_BAIRRO=%s,
                                                                   NO_CEP=%s,
                                                                   SG_UF=%s
                                                                   WHERE CD_PESSOA=%s''',
                                                                   (pais,
                                                                    self.endereco.municipio,
                                                                    self.endereco.logradouro,
                                                                    self.endereco.numero,
                                                                    self.endereco.complemento,
                                                                    self.endereco.bairro,
                                                                    self.endereco.cep,
                                                                    self.endereco.uf,
                                                                    self.id))
                con.commit()
            else:
                print "               Inserindo de endereco da pessoa"

                cursor.execute('''INSERT INTO crp_endereco_pessoa (CD_PAIS,
                                                                   NM_CIDADE,
                                                                   NM_LOGRADOURO,
                                                                   NO_ENDERECO,
                                                                   DS_COMPLEMENTO,
                                                                   NM_BAIRRO,
                                                                   NO_CEP,
                                                                   SG_UF,
                                                                   CD_PESSOA) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                                   (pais,
                                                                    self.endereco.municipio,
                                                                    self.endereco.logradouro,
                                                                    self.endereco.numero,
                                                                    self.endereco.complemento,
                                                                    self.endereco.bairro,
                                                                    self.endereco.cep,
                                                                    self.endereco.uf,
                                                                    self.id))
                con.commit()
        except:
            logging.error("Pessoa-Fisica não existe para ID %s" % ( self.id))



    def insert_or_update_cargo_servidor(self):
        print "                                                            CARGO"
        try:
            data_entrada_cargo_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.data_entrada_cargo))))
            data_saida_cargo_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.data_saida_cargo))))

            if self.grupo != "000":
                if self.data_saida_cargo == "00000000":
                    data_saida_cargo_fita = None
                else:
                    data_saida_cargo_fita = data_saida_cargo_formatada

#SELECIONA DATA FINAL DE SAIDA
                data_saida_cargo_fita_str = str(data_saida_cargo_fita)

#SELECIONA O GRUPO, CARGO DA FITA
                cd_grupo_cargo_fita = self.grupo+self.codigo_cargo

#SELECIONA A CLASSE DA FITA
                cd_classe_cargo_fita = self.classe

#SELECIONA O NIVEL DA FITA
                cd_nivel_cargo_fita = self.referencia_nivel_padrao

#SELECIONA DATA DE INGRESSO NO CARGO DA FITA_ESPELHO
                data_ingresso_cargo_fita = data_entrada_cargo_formatada
                data_ingresso_cargo_fita_str = str(data_ingresso_cargo_fita)


#SELECIONA 
#                cursor.execute('''select cd_servidor from crp_cargo_servidor where CD_SERVIDOR=%s''', (self.id,))
#EXTRAI ID MAXIMO DE CARGO DE SERVIDOR DA BASE
                cursor.execute('''select max(cd_cargo_servidor)
                                  from corp.crp_cargo_servidor where cd_servidor =%s''',(self.id,))
                resultado_maximo_id_cargo = cursor.fetchone()
                id_max_cargo_servidor_banco = resultado_maximo_id_cargo[0]

                
#                if cursor.fetchall():
#SE O SERVIDOR NÃO TEM CARGO NA BASE E TEM CARGO NA FITA ENTÃO INSERIR:
                if (id_max_cargo_servidor_banco == None) or (id_max_cargo_servidor_banco == 0):
                    print "               Inserindo cargo do servidor..."
                    cursor.execute('''INSERT INTO crp_cargo_servidor (CD_GRUPO_CARGO,
                                                                      CD_SERVIDOR,
                                                                      CD_CLASSE,
                                                                      CD_NIVEL,
                                                                      DT_INGRESSO_CARGO,
                                                                      DT_SAIDA_CARGO)
                                                                      values (%s,%s,%s,%s,%s,%s)''',
                                                                     (self.grupo+self.codigo_cargo,
                                                                      self.id,
                                                                      self.classe,
                                                                      self.referencia_nivel_padrao,
                                                                      data_ingresso_cargo_fita_str,
                                                                      data_saida_cargo_fita))
                    con.commit()
                elif (id_max_cargo_servidor_banco != None) or (id_max_cargo_servidor_banco != 0):
                    try:
                        cursor.execute('''SELECT cd_grupo_cargo FROM corp.crp_cargo_servidor
                                          WHERE cd_cargo_servidor =%s''',(id_max_cargo_servidor_banco))
                        resultado_cargo_banco = cursor.fetchone()
                        id_grupo_cargo_banco = resultado_cargo_banco[0]


                        cursor.execute('''SELECT cd_classe FROM crp_cargo_servidor
                                          WHERE cd_cargo_servidor =%s''',(id_max_cargo_servidor_banco))
                        resultado_classe_banco = cursor.fetchone()
                        id_classe_banco = resultado_classe_banco[0]


                        cursor.execute('''SELECT dt_ingresso_cargo FROM crp_cargo_servidor
                                          WHERE cd_cargo_servidor =%s''',(id_max_cargo_servidor_banco))
                        resultado_ingresso_cargo_banco = cursor.fetchone()
                        data_ingresso_cargo_banco = resultado_ingresso_cargo_banco[0]
                        data_ingresso_cargo_banco_str = str(data_ingresso_cargo_banco)


                        cursor.execute('''SELECT dt_saida_cargo FROM crp_cargo_servidor
                                          WHERE cd_cargo_servidor =%s''',(id_max_cargo_servidor_banco))
                        resultado_saida_cargo_banco = cursor.fetchone()
                        data_saida_cargo_banco = resultado_saida_cargo_banco[0]
                        data_saida_cargo_banco_str = str(data_saida_cargo_banco)



                        cursor.execute('''SELECT cd_nivel FROM crp_cargo_servidor
                                          WHERE cd_cargo_servidor =%s''',(id_max_cargo_servidor_banco))
                        resultado_nivel_banco = cursor.fetchone()
                        nivel_cargo_banco = resultado_nivel_banco[0]


#SE O CÓDIGO DO GRUPO+CARGO FOR DIFERENTE NA FITA E NO BANCO ENTÃO *ATUALIZE O ULTIMO DO BANCO* E INSIRA O NOVO
                        if (cd_grupo_cargo_fita != id_grupo_cargo_banco):
                            print "               Inserindo cargo do servidor..."

                            cursor.execute('''INSERT INTO crp_cargo_servidor (CD_GRUPO_CARGO,
                                                                      CD_SERVIDOR,
                                                                      CD_CLASSE,
                                                                      CD_NIVEL,
                                                                      DT_INGRESSO_CARGO,
                                                                      DT_SAIDA_CARGO)
                                                                      values (%s,%s,%s,%s,%s,%s)''',
                                                                     (cd_grupo_cargo_fita,
                                                                      self.id,
                                                                      cd_classe_cargo_fita,
                                                                      cd_nivel_cargo_fita,
                                                                      data_ingresso_cargo_fita_str,
                                                                      data_saida_cargo_fita))
                            con.commit()

                        elif (data_ingresso_cargo_banco_str != data_ingresso_cargo_fita_str) or (nivel_cargo_banco != cd_nivel_cargo_fita) or (id_classe_banco != cd_classe_cargo_fita) or (data_saida_cargo_fita_str != None):
                            print "               Atualizando cargo do servidor..."
                            cursor.execute('''UPDATE crp_cargo_servidor SET CD_GRUPO_CARGO=%s,
                                                                    CD_CLASSE=%s,
                                                                    CD_NIVEL=%s,
                                                                    DT_INGRESSO_CARGO=%s,
                                                                    DT_SAIDA_CARGO=%s,
                                                                    CD_SERVIDOR=%s
                                                                    WHERE CD_CARGO_SERVIDOR=%s''',
                                                                   (self.grupo+self.codigo_cargo,
                                                                    self.classe,
                                                                    self.referencia_nivel_padrao,
                                                                    data_ingresso_cargo_fita_str,
                                                                    data_saida_cargo_fita,
                                                                    self.id,
                                                                    id_max_cargo_servidor_banco))
                            con.commit()

                        else:
                            print "NAO HA ATUALIZACOES NO CARGO"

                    except:
                        logging.error("Erro no try de tramite de cargo")

        except:
            logging.error("Cargo não existe %s para ID %s" % (self.grupo+self.codigo_cargo, self.id))



    def insert_or_update_historico_funcao_servidor(self):
        print "                                                            HISTORICO FUNCAO..."
#se o servidor possuir função no banco sem data de saída e na fita não existir
#relato sobre funções, então o método vai verificar exclusão do servidor e atua-
#lizar a saída da função com a entrada da ocorrência de exclusão

        try:
            print self.nome
#Verifica a existencia das funções
            if self.codigo_nivel != "00000":
               tem_funcao_fita = True
            else:
               tem_funcao_fita = False
            if self.codigoNivelNovaFuncao != "00000":
               tem_nova_funcao_fita = True
            else:
               tem_nova_funcao_fita = False

#Se não tem função, faz o if
            if tem_funcao_fita == False:
#Verifica se possui ocorrencia de exclusão na fita
                if self.dataOcorrenciaExclu != "00000000":
                    tem_ocorrencia_exclusao = True
                    data_exclusao = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataOcorrenciaExclu))))
#                    print "data exclusao"
#                    print data_exclusao
                else:
                    tem_ocorrencia_exclusao = False
#Atualiza com data de exclusão a última função
                if (tem_ocorrencia_exclusao == True) and (self.dataSaidaFuncao == "00000000"):
                    cursor.execute('''UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO=%s
                                                      WHERE CD_SERVIDOR=%s and 
                                                      (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)''',
                                                      (data_exclusao,self.id))
                    con.commit()

#Caso exista formata as datas e pega os valores da funcao da fita
            if tem_funcao_fita == True:
               data_entrada_funcao_fita_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataIngressoFuncao))))
               data_saida_funcao_fita_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataSaidaFuncao))))
##verifica se tem data de saída na fita
#               print "tem funcao"
               if self.dataSaidaFuncao == "00000000":
                    data_funcao_saida_fita_verificada = None
               else:
                    data_funcao_saida_fita_verificada = data_saida_funcao_fita_formatada
##pega o id da funcao na fita
               cursor.execute('''SELECT cd_funcao FROM crp_funcao WHERE cd_nivel =%s and sg_funcao =%s''',(self.codigo_nivel,str(self.funcao)))
               resultado_funcao_fita = cursor.fetchone()
               id_funcao_fita = resultado_funcao_fita[0]
##pega o id da uorg na fita
#               print "id_funcao_fita"
#               print id_funcao_fita
               id_uorg_fita = self.unidadeOrganizacionalFuncao
##pega as data de ingresso e de saida na fita
               data_ingresso_fita = data_entrada_funcao_fita_formatada
               data_saida_fita = data_funcao_saida_fita_verificada


#Verifica dados da funcao no banco para inserir ou não
               cursor.execute('''select cd_funcao_servidor
                                 from corp.crp_funcao_servidor where cd_servidor =%s
                                 and cd_funcao =%s and dt_ingresso_funcao =%s and cd_unidade_organiz =%s''',(self.id, id_funcao_fita, data_ingresso_fita, id_uorg_fita))
               if cursor.fetchone():
                   cursor.execute('''select cd_funcao_servidor
                                     from corp.crp_funcao_servidor where cd_servidor =%s
                                     and cd_funcao =%s and dt_ingresso_funcao =%s and cd_unidade_organiz =%s''',(self.id, id_funcao_fita, data_ingresso_fita, id_uorg_fita))
                   resultado_funcao_historico = cursor.fetchone()
                   funcao_esta_no_historico_do_banco = resultado_funcao_historico[0]
               else:
                   funcao_esta_no_historico_do_banco = False

               if (funcao_esta_no_historico_do_banco == False) or (funcao_esta_no_historico_do_banco == 0):
                  precisa_inserir_funcao_no_banco = True
               else:
                  precisa_inserir_funcao_no_banco = False


#numero de uorg diferente mas com mesma data de entrada




#Caso exista formata as datas e pega os valores da nova funcao da fita
            if tem_nova_funcao_fita == True:

               data_entrada_nova_funcao_fita_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataIngressoNovaFuncao))))
               data_saida_nova_funcao_fita_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataSaidaNovaFuncao))))
##verifica se tem data de saída na fita
               if self.dataSaidaNovaFuncao == "00000000":
                    data_nova_funcao_saida_verificada = None
               else:
                    data_nova_funcao_saida_verificada = data_saida_nova_funcao_fita_formatada
##pega o id da nova funcao na fita
               cursor.execute('''SELECT cd_funcao FROM crp_funcao WHERE cd_nivel =%s and sg_funcao =%s''',(self.codigoNivelNovaFuncao,str(self.siglaNovaFuncao)))
               resultado_nova_funcao_fita = cursor.fetchone()
               id_nova_funcao_fita = resultado_nova_funcao_fita[0]

               id_uorg_funcao_nova_fita = self.unidadeOrganizacionalNovaFuncao

               data_ingresso_funcao_nova_fita = data_entrada_nova_funcao_fita_formatada
               data_saida_nova_funcao_fita = data_nova_funcao_saida_verificada



#Verifica dados da nova funcao no banco para inserir ou não
               cursor.execute('''select cd_funcao_servidor
                                 from corp.crp_funcao_servidor where cd_servidor =%s
                                 and cd_funcao =%s and dt_ingresso_funcao =%s''',(self.id, id_nova_funcao_fita, data_ingresso_funcao_nova_fita))
               if cursor.fetchone():
                   cursor.execute('''select cd_funcao_servidor
                                     from corp.crp_funcao_servidor where cd_servidor =%s
                                     and cd_funcao =%s and dt_ingresso_funcao =%s''',(self.id, id_nova_funcao_fita, data_ingresso_funcao_nova_fita))
                   resultado_nova_funcao_historico = cursor.fetchone()
                   funcao_nova_esta_no_historico_do_banco = resultado_nova_funcao_historico[0]
               else:
                   funcao_nova_esta_no_historico_do_banco = False
               if (funcao_nova_esta_no_historico_do_banco == False) or (funcao_nova_esta_no_historico_do_banco == 0):
                  precisa_inserir_funcao_nova_no_banco = True
               else:
                  precisa_inserir_funcao_nova_no_banco = False


#verifica se a data de saida é menor que...
            if (data_saida_fita < '2011-01-01') and (data_saida_fita != None):
                menor_que_2011 = True
            else:
                menor_que_2011 = False


#verifica se tem um campo nulo no banco
##PRESTAR ATENÇÃO PARA O VERIFICAR DA DATA DE INGRESSO, POIS NÃO PRECISA SER EXATAMENTE A DATA DE INGRESSO, PODE SER UM CAMPO NULO
            cursor.execute('''select cd_funcao_servidor from crp_funcao_servidor 
                              where cd_servidor =%s and
                              (dt_saida_funcao is null or dt_saida_funcao = 0000-00-00)''',
                              (self.id))
#                              (self.id, data_ingresso_fita))
            if cursor.fetchone():
                esta_em_uma_funcao = True
                cursor.execute('''select cd_funcao_servidor from crp_funcao_servidor 
                              where cd_servidor =%s and
                              (dt_saida_funcao is null or dt_saida_funcao = 0000-00-00)''',
                              (self.id))
                id_funcao_atual = cursor.fetchone()
                id_funcao_atual_banco = id_funcao_atual[0]
                cursor.execute('''select dt_ingresso_funcao from crp_funcao_servidor 
                              where cd_servidor =%s and
                              (dt_saida_funcao is null or dt_saida_funcao = 0000-00-00)''',
                              (self.id))
                data_entrada_funcao_atual = cursor.fetchone()
                data_entrada_funcao_banco = data_entrada_funcao_atual[0]

            else:
                esta_em_uma_funcao = False


#Inseri ou Atualiza a função

            if precisa_inserir_funcao_no_banco == True:
#verifica um campo anterior caso tenha que inserir um novo
                print "identificado que precisa inserir funcao no banco"
                if esta_em_uma_funcao == True:
                    print ".........identificado que servidor(a) esta em uma funcao"
                    if menor_que_2011 == True:
#                        print "...................identificado que a saida na fita e menor que 2011-01-01"
                        cursor.execute('''UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO=%s
                                                      WHERE CD_SERVIDOR=%s and 
                                                      DT_INGRESSO_FUNCAO=%s and 
                                                      (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)''',
                                                      (data_saida_fita,
                                                       self.id,
                                                       data_ingresso_fita))
                        con.commit()
                    else:
#SABENDO-SE QUE É UMA DATA DE SAIDA NA FITA SUPERIOR A 2011-01-01, VERIFICAR-SE-A SE A ENTRADA NESSA 
#FUNÇÃO OCORREU EXATAMENTE EM 2011-01-01(DIA DA MUDANÇA HIERARQUICA), SE SIM ENTÃO A SAÍDA DELA NÃO DEVE SER NO MESMO
#DIA(INSERIR NA SAÍDA A ENTRADA DA PRÓXIMA),SENÃO INSERIR NA SAÍDA 2011-01-01
                        if (str(data_entrada_funcao_banco) >= '2011-01-01'):
#                            print "                             identificado que a entrada da funcao atual e igual a 2011-01-01"
                            cursor.execute('''UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO=%s
                                                      WHERE CD_FUNCAO_SERVIDOR=%s and 
                                                      (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)''',
                                                      (data_ingresso_fita,
                                                       id_funcao_atual_banco))
                            con.commit()
                        else:
#                            print "                             identificado que a entrada da funcao atual e diferente de 2011"
#                            print "atualizando ultima funcao com saida de 2011-01-01"
                            cursor.execute('''UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO = '2011-01-01'
                                                      WHERE CD_FUNCAO_SERVIDOR=%s and 
                                                      (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)''',
                                                      (id_funcao_atual_banco))
                            con.commit()
#                            print "atualizou...."
                logging.error("INSERIU: matricula não existe %s para NOME %s" % (self.matricula, self.nome))
                cursor.execute('''INSERT INTO crp_funcao_servidor (CD_SERVIDOR,
                                                                        CD_UNIDADE_ORGANIZ,
                                                                        CD_FUNCAO,
                                                                        DT_INGRESSO_FUNCAO,
                                                                        DT_SAIDA_FUNCAO) values (%s,%s,%s,%s,%s)''',
                                                                       (self.id,
                                                                        self.unidadeOrganizacionalFuncao,
                                                                        id_funcao_fita,
                                                                        data_ingresso_fita,
                                                                        data_saida_fita))
                con.commit()
            else:
#??se a data de saida for menor então vai atualizar todos os ids que a data de en-
#??trada, funcao, e cd_servidor sejam iguais com 2011-01-01
#                print "atualizando pois o historico ja esta registrado..."
                cursor.execute('''UPDATE crp_funcao_servidor SET CD_FUNCAO=%s,
                                                      DT_INGRESSO_FUNCAO=%s,
                                                      DT_SAIDA_FUNCAO=%s
                                                      WHERE CD_FUNCAO_SERVIDOR=%s''',
                                                      (id_funcao_fita,
                                                       data_ingresso_fita,
                                                       data_saida_fita,
                                                       funcao_esta_no_historico_do_banco))
                con.commit()

#verifica se a data de saida é menor que...
            if (data_saida_nova_funcao_fita < '2011-01-01') and (data_saida_nova_funcao_fita != None):
                menor_nf = True
            else:
                menor_nf = False

#verifica se tem um campo nulo no banco
            cursor.execute('''select cd_funcao_servidor from crp_funcao_servidor 
                              where cd_servidor =%s and dt_ingresso_funcao =%s and
                              (dt_saida_funcao is null or dt_saida_funcao = 0000-00-00)''',
                              (self.id, data_ingresso_funcao_nova_fita))
            if cursor.fetchone():
                esta_em_uma_nova_funcao = True
                cursor.execute('''select dt_ingresso_funcao from crp_funcao_servidor 
                              where cd_servidor =%s and
                              (dt_saida_funcao is null or dt_saida_funcao = 0000-00-00)''',
                              (self.id))
                data_entrada_funcao_nova_atual = cursor.fetchone()
                data_entrada_funcao_nova_banco = data_entrada_funcao_atual[0]
            else:
                esta_em_uma_nova_funcao = False

            print precisa_inserir_funcao_no_banco
#Inseri ou Atualiza a função nova do servidor
            if precisa_inserir_funcao_nova_no_banco == True:
                if esta_em_uma_nova_funcao == True:
                    if menor_nf == True:
                        cursor.execute('''UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO=%s
                                                      WHERE CD_SERVIDOR=%s and 
                                                      DT_INGRESSO_FUNCAO=%s and 
                                                      (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)''',
                                                      (data_saida_nova_funcao_fita,
                                                       self.id,
                                                       data_ingresso_funcao_nova_fita))
                        con.commit()
                    else:
                        if (str(data_entrada_funcao_nova_banco) >= '2011-01-01'):
#                            print "                             identificado que a entrada da nova funcao atual e igual ou maior a 2011-01-01"
                            cursor.execute('''UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO=%s
                                                      WHERE CD_FUNCAO_SERVIDOR=%s and 
                                                      (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)''',
                                                      (data_ingresso_funcao_nova_fita,
                                                       id_funcao_atual))
                            con.commit()
                        else:
#                            print "                             identificado que a entrada da funcao atual e diferente de 2011"
#                            print "atualizando ultima funcao com saida de 2011-01-01"
                            cursor.execute('''UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO = '2011-01-01'
                                                      WHERE CD_FUNCAO_SERVIDOR=%s and 
                                                      (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)''',
                                                      (id_funcao_atual))
                            con.commit()
#                        cursor.execute('''UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO= '2011-01-01'
#                                                      WHERE CD_SERVIDOR=%s and 
#                                                      DT_INGRESSO_FUNCAO=%s and 
#                                                      (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)''',
#                                                      (self.id,
#                                                       data_ingresso_funcao_nova_fita))
#                        con.commit()
                logging.error("INSERIU: matricula não existe %s para NOME %s" % (self.matricula, self.nome))
                cursor.execute('''INSERT INTO crp_funcao_servidor (CD_SERVIDOR,
                                                                        CD_UNIDADE_ORGANIZ,
                                                                        CD_FUNCAO,
                                                                        DT_INGRESSO_FUNCAO,
                                                                        DT_SAIDA_FUNCAO) values (%s,%s,%s,%s,%s)''',
                                                                       (self.id,
                                                                        self.unidadeOrganizacionalNovaFuncao,
                                                                        id_nova_funcao_fita,
                                                                        data_ingresso_funcao_nova_fita,
                                                                        data_saida_nova_funcao_fita))
                con.commit()
            else:
                cursor.execute('''UPDATE crp_funcao_servidor SET CD_FUNCAO=%s,
                                                      DT_INGRESSO_FUNCAO=%s,
                                                      DT_SAIDA_FUNCAO=%s
                                                      WHERE CD_FUNCAO_SERVIDOR=%s''',
                                                      (id_nova_funcao_fita,
                                                       data_ingresso_funcao_nova_fita,
                                                       data_saida_nova_funcao_fita,
                                                       funcao_nova_esta_no_historico_do_banco))
                con.commit()



        except:
            print "EXCEPT"







    def insert_or_update_historico_uorg_servidor(self):
        print "                                                                  HISTORICO UORG..."
#verifica que função vem na fita
        if self.codigoNivelNovaFuncao == "00000":
            tem_nova_funcao_fita = False
        else:
            tem_nova_funcao_fita = True
        if self.codigo_nivel == "00000":
            tem_funcao_fita = False
        else:
            tem_funcao_fita = True


# armazena dados da fita
# caso a data de entrada na lotacao seja nula ele vai pegar a saida da maior funcao que existir
        if (self.dataLotacao == "00000000") and (self.dataSaidaNovaFuncao != "00000000"):
            data_lotacao_fita = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataSaidaNovaFuncao))))
        elif (self.dataLotacao == "00000000") and (self.dataSaidaFuncao != "00000000"):
            data_lotacao_fita = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataSaidaFuncao))))
        elif (self.dataLotacao == "00000000") and (self.dataOcoInatividade != "00000000"):
            data_lotacao_fita = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataOcoInatividade))))
        elif (self.dataLotacao != "00000000"):
            data_lotacao_fita = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataLotacao))))
        else:
            data_lotacao_fita = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataIngressoOrgao))))


        if self.codigo_lotacao == "000000000":
            uorg_lotacao_fita = self.unidadeOrganizacionalLocalizacao
        else:
            uorg_lotacao_fita = self.codigo_lotacao


        if tem_nova_funcao_fita == True:
            uorg_nova_funcao_fita = self.unidadeOrganizacionalNovaFuncao
            data_ingresso_nova_funcao_fita = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataIngressoNovaFuncao))))
            data_saida_nova_funcao_fita = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataSaidaNovaFuncao))))
        if tem_funcao_fita == True:
            uorg_funcao_fita = self.unidadeOrganizacionalFuncao
            data_ingresso_funcao_fita = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataIngressoFuncao))))
            data_saida_funcao_fita = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataSaidaFuncao))))

#so usa a lotacao se não existirem funções ou estarem com data de saida preenchida

        if tem_nova_funcao_fita == False:
            if tem_funcao_fita == False:
                usar_lotacao = True
            else:
                if data_saida_funcao_fita == "0000-00-00":
                    usar_lotacao = False
                else:
                    usar_lotacao = True
        else:
            if data_saida_nova_funcao_fita == "0000-00-00":
                usar_lotacao = False
            else:
                usar_lotacao = True



#se não tiver que usar lotação(pois há, função ou nova função)
        if usar_lotacao == False:

#verifica uorg da nova funcao no historico do banco
            if tem_nova_funcao_fita == True:

                 cursor.execute('''select Max(cd_unidade_organiz_hist)
                                   from corp.crp_unidade_organizacional_hist where cd_pessoa_fisica =%s
                                   and cd_unidade_organiz =%s and dt_ingresso_lotacao =%s''',(self.id, uorg_nova_funcao_fita, data_ingresso_nova_funcao_fita))
                 resultado_nova_funcao_uorg_banco = cursor.fetchone()
                 cd_hist_uorg_nova_funcao_banco = resultado_nova_funcao_uorg_banco[0]
                 if cd_hist_uorg_nova_funcao_banco == None:
                     tem_hist_uorg_nova_funcao_banco = False
                 else:
                     tem_hist_uorg_nova_funcao_banco = True
                 if tem_hist_uorg_nova_funcao_banco == True:
                     precisa_inserir_uorg_nova_funcao_fita = False
                 else:
                     precisa_inserir_uorg_nova_funcao_fita = True
            else:
                 precisa_inserir_uorg_nova_funcao_fita = False



#verifica uorg da funcao no historico do banco
            if (tem_funcao_fita == True) and (data_saida_funcao_fita == "0000-00-00"):
                cursor.execute('''select Max(cd_unidade_organiz_hist)
                                   from corp.crp_unidade_organizacional_hist where cd_pessoa_fisica =%s
                                   and cd_unidade_organiz =%s and dt_ingresso_lotacao =%s''',(self.id, uorg_funcao_fita, data_ingresso_funcao_fita))
                resultado_funcao_uorg_banco = cursor.fetchone()
                cd_hist_uorg_funcao_banco = resultado_funcao_uorg_banco[0]

                if cd_hist_uorg_funcao_banco == None:
                    tem_hist_uorg_funcao_banco = False
                else:
                    tem_hist_uorg_funcao_banco = True

                if tem_hist_uorg_funcao_banco == True:
                    precisa_inserir_uorg_funcao_fita = False
                else:
                    precisa_inserir_uorg_funcao_fita = True
            else:
                precisa_inserir_uorg_funcao_fita = False
                precisa_inserir_uorg_lotacao_fita = True
#se não tiver função e nova função utiliza a lotação(que sempre vai existir)
        else:
            cursor.execute('''select Max(cd_unidade_organiz_hist)
                              from corp.crp_unidade_organizacional_hist where cd_pessoa_fisica =%s
                               and (dt_saida_lotacao is null or dt_saida_lotacao= 0000-00-00)''',(self.id))
            resultado_lotacao_uorg_banco = cursor.fetchone()
            cd_hist_uorg_lotacao_banco = resultado_lotacao_uorg_banco[0]

            if cd_hist_uorg_lotacao_banco == None:
                tem_hist_uorg_lotacao_banco = False
            else:
                tem_hist_uorg_lotacao_banco = True
            if tem_hist_uorg_lotacao_banco == True:
                cursor.execute('''select dt_ingresso_lotacao
                               from corp.crp_unidade_organizacional_hist where cd_pessoa_fisica =%s
                               and (dt_saida_lotacao is null or dt_saida_lotacao= 0000-00-00)''',(self.id))
                resultado_ingresso_lotacao_banco = cursor.fetchone()
                data_ingresso_lotacao_banco = resultado_ingresso_lotacao_banco[0]

                if (data_lotacao_fita <= str(data_ingresso_lotacao_banco)):
                    precisa_inserir_uorg_lotacao_fita = False
                else:
                    precisa_inserir_uorg_lotacao_fita = True

#                print "tem_hist_uorg_lotacao_banco?"
#                print tem_hist_uorg_lotacao_banco
#                print "data_ingresso_lotacao_banco"
#                print data_ingresso_lotacao_banco
#                print "data_lotacao_fita"
#                print data_lotacao_fita
            else:
                precisa_inserir_uorg_lotacao_fita = True
#            print "precisa_inserir_uorg_lotacao_fita?"
#            print precisa_inserir_uorg_lotacao_fita
#procurar a existencia de qualquer coisa no banco e,
#pega o historico mais atual, caso exista
        cursor.execute('''SELECT Max(cd_unidade_organiz_hist) from crp_unidade_organizacional_hist
                          WHERE cd_pessoa_fisica =%s and (dt_saida_lotacao is null or dt_saida_lotacao= 0000-00-00)''',(self.id))
        if cursor.fetchone() != None:
            cursor.execute('''SELECT Max(cd_unidade_organiz_hist) from crp_unidade_organizacional_hist
                              WHERE cd_pessoa_fisica =%s and (dt_saida_lotacao is null or dt_saida_lotacao = 0000-00-00)''',(self.id))
            cd_unidade_atual_encontrada = cursor.fetchone()
            cd_unidade_atual = cd_unidade_atual_encontrada[0]
            cursor.execute('''SELECT cd_unidade_organiz from crp_unidade_organizacional_hist
                              WHERE cd_pessoa_fisica =%s and (dt_saida_lotacao is null or dt_saida_lotacao = 0000-00-00)''',(self.id))
            uorg_unidade_atual_encontrada = cursor.fetchone()
            if uorg_unidade_atual_encontrada != None:
                uorg_unidade_atual = uorg_unidade_atual_encontrada[0]
            else:
                uorg_unidade_atual = None

            cursor.execute('''SELECT dt_ingresso_lotacao from crp_unidade_organizacional_hist
                              WHERE cd_pessoa_fisica =%s and (dt_saida_lotacao is null or dt_saida_lotacao = 0000-00-00)''',(self.id))
            dt_ingresso_atual_encontrada = cursor.fetchone()
            if dt_ingresso_atual_encontrada != None:
                dt_ingresso_atual = dt_ingresso_atual_encontrada[0]
            else:
                dt_ingresso_atual = None
            if cd_unidade_atual == None:
                tem_campo_na_base = False
            else:
                tem_campo_na_base = True
            if dt_ingresso_atual == None:
                tem_entrada_na_base = False
            else:
                tem_entrada_na_base = True
            if (uorg_unidade_atual == None) or (uorg_unidade_atual == '') or (uorg_unidade_atual == "000000000"):
                tem_uorg_na_base = False
            else:
                tem_uorg_na_base = True
        else:
            print "nao tem nada la"

        if usar_lotacao == True:
            if precisa_inserir_uorg_lotacao_fita == True:
                if tem_campo_na_base == True:
#                   esse \/if\/ é utilizado para esse modelo: uorg_base:"0000000000", data_base:"0000-00-00"
                    if (tem_uorg_na_base == False) and (tem_entrada_na_base == False):
#                        print "LOTACAO: ATUALIZANDO ULTIMA UORG COM DADOS NORMAIS DA FITA..."
                        nao_inserir_uorg_nova = True
                        cursor.execute('''UPDATE crp_unidade_organizacional_hist SET CD_UNIDADE_ORGANIZ =%s,
                                                                   DT_INGRESSO_LOTACAO=%s
                                                                   WHERE CD_UNIDADE_ORGANIZ_HIST=%s''',
                                                                   (uorg_lotacao_fita,
                                                                   data_lotacao_fita,
                                                                   cd_unidade_atual))
                        con.commit()
                    else:
                        nao_inserir_uorg_nova = False
#                       se a data de entrada do banco for igual a da fita, e as uorgs diferentes significa que 
#                       essa atualização surgiu da mudança de codigo de uorg então ele vai inserir data de 2011-01-01
                        if (str(dt_ingresso_atual) == data_lotacao_fita) and (uorg_unidade_atual != uorg_lotacao_fita):

                            print "LOTACAO: ATUALIZANDO ULTIMA UNIDADE COM DATA DE SAIDA 2011-01-01" 
                            cursor.execute('''UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO=%s
                                                                   WHERE CD_UNIDADE_ORGANIZ_HIST=%s''',
                                                                   ('2011-01-01',
                                                                   cd_unidade_atual))
                            con.commit()
                        else:
                            print "LOTACAO: ATUALIZANDO ULTIMA UNIDADE COM DATA DE SAIDA NORMAL DA FITA"
                            cursor.execute('''UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO=%s
                                                                   WHERE CD_UNIDADE_ORGANIZ_HIST=%s''',
                                                                   (data_lotacao_fita,
                                                                   cd_unidade_atual))
                            con.commit()
                else:
                    nao_inserir_uorg_nova = False
                if nao_inserir_uorg_nova == False:
                    if (str(dt_ingresso_atual) == data_lotacao_fita) and (uorg_unidade_atual != uorg_lotacao_fita):
                        print "LOTACAO: INSERINDO UNIDADE COM DATA DE ENTRADA DE 2011-01-01"
                        cursor.execute('''INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                           CD_UNIDADE_ORGANIZ,
                                                                           DT_INGRESSO_LOTACAO)
                                                                           values (%s,%s,%s)''',
                                                                          (self.id,
                                                                           uorg_lotacao_fita,
                                                                           '2011-01-01'))
                        con.commit()
                    else:
                        print "LOTACAO: INSERINDO UNIDADE COM DATA DE ENTRADA NORMAL"
                        cursor.execute('''INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                           CD_UNIDADE_ORGANIZ,
                                                                           DT_INGRESSO_LOTACAO)
                                                                           values (%s,%s,%s)''',
                                                                          (self.id,
                                                                           uorg_lotacao_fita,
                                                                           data_lotacao_fita))
                        con.commit()
            else:
                print "LOTACAO: ATUALIZANDO ULTIMA UNIDADE POIS NAO PRECISA INSERIR NADA"
                if (str(dt_ingresso_atual) != '2011-01-01'):
                    cursor.execute('''UPDATE crp_unidade_organizacional_hist SET CD_UNIDADE_ORGANIZ =%s,
                                                                   DT_INGRESSO_LOTACAO=%s
                                                                   WHERE CD_UNIDADE_ORGANIZ_HIST=%s''',
                                                                   (uorg_lotacao_fita,
                                                                   data_lotacao_fita,
                                                                   cd_unidade_atual))
                    con.commit()

#inseri no banco funcao
        if (tem_funcao_fita == True) and (usar_lotacao == False):
            if ((precisa_inserir_uorg_funcao_fita == True) and (precisa_inserir_uorg_nova_funcao_fita == True)):
#verifica se existe aquela unidade já inserida com data de saida nula
                cursor.execute('''SELECT Max(cd_unidade_organiz_hist) FROM crp_unidade_organizacional_hist
                                  WHERE cd_pessoa_fisica =%s AND cd_unidade_organiz =%s AND (dt_saida_lotacao is null
                                  or dt_saida_lotacao = 0000-00-00) ''',(self.id, uorg_funcao_fita))
                if cursor.fetchone():
                    ja_tem_essa_uorg_da_funcao_e_com_saida_nula1 = True
                else:
                    ja_tem_essa_uorg_da_funcao_e_com_saida_nula1 = False
                if ja_tem_essa_uorg_da_funcao_e_com_saida_nula1 == False:
                    print "FUNCAO: INSERINDO DADOS COMPLETOS DE UORG FUNCAO POIS TEM TAMBÉM NOVA FUNCAO"
                    cursor.execute('''INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                                   CD_UNIDADE_ORGANIZ,
                                                                                   DT_INGRESSO_LOTACAO,
                                                                                   DT_SAIDA_LOTACAO)
                                                                                   values (%s,%s,%s,%s)''',
                                                                                  (self.id,
                                                                                   uorg_funcao_fita,
                                                                                   data_ingresso_funcao_fita,
                                                                                   data_saida_funcao_fita))
                    con.commit()
                else:
                    pass
            elif ((precisa_inserir_uorg_funcao_fita == True) and (precisa_inserir_uorg_nova_funcao_fita == False)):
                cursor.execute('''SELECT cd_unidade_organiz_hist FROM crp_unidade_organizacional_hist
                                  WHERE cd_pessoa_fisica =%s AND cd_unidade_organiz =%s AND (dt_saida_lotacao is null
                                  or dt_saida_lotacao = 0000-00-00) ''',(self.id, uorg_funcao_fita))
                if cursor.fetchone():
                    ja_tem_essa_uorg_da_funcao_e_com_saida_nula2 = True
                else:
                    ja_tem_essa_uorg_da_funcao_e_com_saida_nula2 = False


                if ja_tem_essa_uorg_da_funcao_e_com_saida_nula2 == False:
#se tem campo na base  e nao tem entrada e a saida da função na fita é nula: significa que a pessoa só mudou de uorg em 2011-01-01
                    if (tem_campo_na_base == True) and (dt_ingresso_atual == None) and (self.dataSaidaFuncao == "00000000"):
#atualiza a data de saida do ultimo historico com a data de entrada do servidor na função caso a saída seja nula
                        print "ATUALIZANDO ULTIMA UORG COM FUNCAO COM DATA DE SAIDA 2011-01-01"
                        cursor.execute('''UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO=%s,
                                                                DT_INGRESSO_LOTACAO=%s
                                                                WHERE CD_UNIDADE_ORGANIZ_HIST=%s''',
                                                               ('2011-01-01',
                                                                data_ingresso_funcao_fita,
                                                                cd_unidade_atual))
                        con.commit()
                    else:
                        print "ATUALIZANDO FUNCAO COM DATA NORMAL"
                        cursor.execute('''UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO=%s
                                                                WHERE CD_UNIDADE_ORGANIZ_HIST=%s''',
                                                               (data_ingresso_funcao_fita,
                                                                cd_unidade_atual))
                        con.commit()
                    print "FUNCAO: INSERINDO DADOS COMPLETOS DE UORG DE FUNCAO SEM SAIDA"
#inseri a função
                    cursor.execute('''INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                                   CD_UNIDADE_ORGANIZ,
                                                                                   DT_INGRESSO_LOTACAO)
                                                                                   values (%s,%s,%s)''',
                                                                                  (self.id,
                                                                                   uorg_funcao_fita,
                                                                                   data_ingresso_funcao_fita))
                    con.commit()
            else:
                pass
#inseri a nova função, não precisa atualizar a última data pois 

        if (tem_nova_funcao_fita == True) and (usar_lotacao == False):
#se precisa inserir, pois nao achou uorg igual nem entrada igual:
            if precisa_inserir_uorg_nova_funcao_fita == True:
                cursor.execute('''SELECT cd_unidade_organiz_hist FROM crp_unidade_organizacional_hist
                                  WHERE cd_pessoa_fisica =%s AND cd_unidade_organiz =%s AND (dt_saida_lotacao is null
                                  or dt_saida_lotacao = 0000-00-00) ''',(self.id, uorg_nova_funcao_fita))
#se encontrar uorg igual a essa e com saida nula, nao inseri
                if cursor.fetchone():
                    ja_tem_essa_uorg_da_funcao_e_com_saida_nula3 = True
                else:
                    ja_tem_essa_uorg_da_funcao_e_com_saida_nula3 = False
                if ja_tem_essa_uorg_da_funcao_e_com_saida_nula3 == False:
                    if tem_campo_na_base == True:
#atualiza a data de saida do ultimo historico com a data de entrada do servidor na nova função caso a saída seja nula
                        print "ATUALIZANDO ULTIMA UORG COM DATA DA NOVA FUNCAO"
                        cursor.execute('''UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO=%s
                                                                    WHERE CD_UNIDADE_ORGANIZ_HIST=%s''',
                                                                   (data_ingresso_nova_funcao_fita,
                                                                    cd_unidade_atual))
                        con.commit()
#inseri a nova função
                    print "INSERINDO UORG DA NOVA FUNCAO"
                    cursor.execute('''INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                               CD_UNIDADE_ORGANIZ,
                                                                               DT_INGRESSO_LOTACAO)
                                                                               values (%s,%s,%s)''',
                                                                              (self.id,
                                                                               uorg_nova_funcao_fita,
                                                                               data_ingresso_nova_funcao_fita))
                    con.commit()
            else:
                print "nao precisa inserir nova funcao"






    def insert_or_update_ocorrencia_ingresso_servico_publico(self):
        print "                                          OCORRENCIA INGRESSO SERVICO"
        if self.grupoIngreServPublico != "00":

            print "CONFIRMADO OCORRENCIA DE INGRESSO NO SERVICO PUBLICO." + self.nome

            data_ingresso_servico_publico_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataIngreServPublico))))
            data_diploma_legal_servico_publico_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataDipLegalIngreServPublico))))

            cursor.execute('''SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=%s and cd_tipo_ocorrencia=%s''',(self.id, 1))
            resultado_ocorrencia_ingresso_servico = cursor.fetchone()


            if resultado_ocorrencia_ingresso_servico != None:

                id_ocorrencia_ingresso_servico = resultado_ocorrencia_ingresso_servico[0]


                print "Atualizando ocorrencias de ingresso no servico publico..."
                cursor.execute('''UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=%s,
                                                            CD_GRUPO=%s,
                                                            NO_OCORRENCIA=%s,
                                                            DT_OCORRENCIA=%s,
                                                            CD_DIPLOMA_LEGAL=%s,
                                                            NO_DIPLOMA_LEGAL=%s,
                                                            DT_PUBLICACAO=%s,
                                                            CD_SERVIDOR=%s
                                                            WHERE CD_OCORRENCIA=%s''',
                                                           (1,
                                                            self.grupoIngreServPublico,

                                                            self.ocorrenciaIngreServPublico,
                                                            data_ingresso_servico_publico_formatada,
                                                            self.codDipLegalIngreServPublico,
                                                            self.numDipLegalIngreServPublico,
                                                            data_diploma_legal_servico_publico_formatada,
                                                            self.id,
                                                            id_ocorrencia_ingresso_servico))
                con.commit()


            else:
                print "Inserindo ocorrencias de ingresso nos serviço publico..."
                cursor.execute('''INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                              CD_SERVIDOR,
                                                              CD_GRUPO,
                                                              NO_OCORRENCIA,
                                                              DT_OCORRENCIA,
                                                              CD_DIPLOMA_LEGAL,
                                                              NO_DIPLOMA_LEGAL,
                                                              DT_PUBLICACAO) values (%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                             (1,
                                                              self.id,
                                                              self.grupoIngreServPublico,
                                                              self.ocorrenciaIngreServPublico,
                                                              data_ingresso_servico_publico_formatada,
                                                              self.codDipLegalIngreServPublico,
                                                              self.numDipLegalIngreServPublico,
                                                              data_diploma_legal_servico_publico_formatada))
                con.commit()


    def insert_or_update_ocorrencia_ingresso_orgao(self):
        print "                                          OCORRENCIA INGRESSO ORGAO"
        if self.grupoIngressoOrgao != "00":

            print "CONFIRMADO OCORRENCIA DE INGRESSO NO ORGAO." + self.nome

            data_ingresso_orgao_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataIngressoOrgao))))
            data_diploma_legal_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataPublicacaoDiplomaLegal))))

            cursor.execute('''SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=%s and cd_tipo_ocorrencia=%s''',(self.id, 2))
            resultado_ocorrencia_ingresso_orgao = cursor.fetchone()


            if resultado_ocorrencia_ingresso_orgao != None:

                id_ocorrencia_ingresso_orgao = resultado_ocorrencia_ingresso_orgao[0]


                print "Atualizando ocorrencias de ingresso no orgao..."
                cursor.execute('''UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=%s,
                                                            CD_GRUPO=%s,
                                                            NO_OCORRENCIA=%s,
                                                            DT_OCORRENCIA=%s,
                                                            CD_DIPLOMA_LEGAL=%s,
                                                            NO_DIPLOMA_LEGAL=%s,
                                                            DT_PUBLICACAO=%s,
                                                            CD_SERVIDOR=%s
                                                            WHERE CD_OCORRENCIA=%s''',
                                                           (2,
                                                            self.grupoIngressoOrgao,
                                                            self.ocorrenciaIngressoOrgao,
                                                            data_ingresso_orgao_formatada,

                                                            self.codigoDiplomaLegal,
                                                            self.numeroDiplomaLegal,
                                                            data_diploma_legal_formatada,
                                                            self.id,
                                                            id_ocorrencia_ingresso_orgao))
                con.commit()



            else:
                print "Inserindo ocorrencias de ingresso no orgao..."
                cursor.execute('''INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                              CD_SERVIDOR,
                                                              CD_GRUPO,
                                                              NO_OCORRENCIA,
                                                              DT_OCORRENCIA,
                                                              CD_DIPLOMA_LEGAL,
                                                              NO_DIPLOMA_LEGAL,
                                                              DT_PUBLICACAO) values (%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                             (2,
                                                              self.id,
                                                              self.grupoIngressoOrgao,
                                                              self.ocorrenciaIngressoOrgao,
                                                              data_ingresso_orgao_formatada,
                                                              self.codigoDiplomaLegal,
                                                              self.numeroDiplomaLegal,
                                                              data_diploma_legal_formatada))
                con.commit()




    def insert_or_update_ocorrencia_exclusao(self):
        print "                                          OCORRENCIA EXCLUSAO"
        if self.grupoOcorrenciaExclu != "00":

            print "CONFIRMADO OCORRENCIA DE EXCLUSAO" + self.nome

            data_exclusao_orgao_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataOcorrenciaExclu))))
            data_diploma_exclusao_legal_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataDipLegalOcorrenciaExclu))))

            cursor.execute('''SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=%s and cd_tipo_ocorrencia=%s''',(self.id, 3))
            resultado_ocorrencia_exclusao_servico = cursor.fetchone()
#            print "resultado_ocorrencia_exclusao_servico"
#            print resultado_ocorrencia_exclusao_servico

            if resultado_ocorrencia_exclusao_servico != None:

                id_ocorrencia_exclusao_servico = resultado_ocorrencia_exclusao_servico[0]


                cursor.execute('''UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=%s,
                                                            CD_GRUPO=%s,
                                                            NO_OCORRENCIA=%s,
                                                            DT_OCORRENCIA=%s,
                                                            CD_DIPLOMA_LEGAL=%s,
                                                            NO_DIPLOMA_LEGAL=%s,
                                                            DT_PUBLICACAO=%s,
                                                            CD_SERVIDOR=%s
                                                            WHERE cd_ocorrencia=%s''',
                                                           (3,
                                                            self.grupoOcorrenciaExclu,
                                                            self.ocorrenciaExclu,
                                                            data_exclusao_orgao_formatada,
                                                            self.codDipLegalOcorrenciaExclu,
                                                            self.numDipLegalOcorrenciaExclu,
                                                            data_diploma_exclusao_legal_formatada,
                                                            self.id,
                                                            id_ocorrencia_exclusao_servico))
                con.commit()


            else:
                print "Inserindo ocorrencias de exclusao do servidor..." + self.nome
                cursor.execute('''INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                              CD_SERVIDOR,CD_GRUPO,
                                                              NO_OCORRENCIA,
                                                              DT_OCORRENCIA,
                                                              CD_DIPLOMA_LEGAL,
                                                              NO_DIPLOMA_LEGAL,
                                                              DT_PUBLICACAO) values (%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                             (3,
                                                              self.id,
                                                              self.grupoOcorrenciaExclu,
                                                              self.ocorrenciaExclu,
                                                              data_exclusao_orgao_formatada,
                                                              self.codDipLegalOcorrenciaExclu,
                                                              self.numDipLegalOcorrenciaExclu,
                                                              data_diploma_exclusao_legal_formatada))
                con.commit()



    def insert_or_update_ocorrencia_afastamento(self):
        print "                                          OCORRENCIA AFASTAMENTO"
        if self.grupoOcoAfastamento != "00":

            print "CONFIRMADO OCORRENCIA DE AFASTAMENTO NO SERVICO PUBLICO." + self.nome

            data_ocorrencia_afastamento_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataInicioOcoAfastamento))))
            data_diploma_afastamento_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataDipLegalOcoAfastamento))))

            cursor.execute('''SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=%s and cd_tipo_ocorrencia=%s''',(self.id, 4))
            resultado_id_ocorrencia_afastamento = cursor.fetchone()

            if resultado_id_ocorrencia_afastamento != None:

                id_ocorrencia_afastamento = resultado_id_ocorrencia_afastamento[0]


                print "Atualizando ocorrencias de afastamento no orgao..."
                cursor.execute('''UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=%s,
                                                            CD_GRUPO=%s,
                                                            NO_OCORRENCIA=%s,
                                                            DT_OCORRENCIA=%s,
                                                            CD_DIPLOMA_LEGAL=%s,
                                                            NO_DIPLOMA_LEGAL=%s,
                                                            DT_PUBLICACAO=%s,
                                                            CD_SERVIDOR=%s
                                                            WHERE CD_OCORRENCIA=%s''',
                                                           (4,
                                                            self.grupoOcoAfastamento,
                                                            self.ocorrenciaAfastamento,
                                                            data_ocorrencia_afastamento_formatada,
                                                            self.codDipLegalOcoAfastamento,
                                                            self.numDipLegalOcoAfastamento,
                                                            data_diploma_afastamento_formatada,
                                                            self.id,
                                                            id_ocorrencia_afastamento))
                con.commit()


            else:

                print "Inserindo ocorrencias de afastamento do servidor..."
                cursor.execute('''INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                              CD_SERVIDOR,
                                                              CD_GRUPO,
                                                              NO_OCORRENCIA,
                                                              DT_OCORRENCIA,
                                                              CD_DIPLOMA_LEGAL,
                                                              NO_DIPLOMA_LEGAL,
                                                              DT_PUBLICACAO) values (%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                             (4,
                                                              self.id,
                                                              self.grupoOcoAfastamento,
                                                              self.ocorrenciaAfastamento,
                                                              data_ocorrencia_afastamento_formatada,
                                                              self.codDipLegalOcoAfastamento,
                                                              self.numDipLegalOcoAfastamento,
                                                              data_diploma_afastamento_formatada))
                con.commit()










    def insert_or_update_ocorrencia_inatividade(self):
        print "                                          OCORRENCIA INATIVIDADE"
        if self.grupoOcoInatividade != "00":

            print "CONFIRMADO OCORRENCIA DE INATIVIDADE NO SERVICO PUBLICO." + self.nome

            data_ocorrencia_inatividade_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataOcoInatividade))))
            data_diploma_inatividade_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataDipLegalOcoInatividade))))
            cursor.execute('''SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=%s and cd_tipo_ocorrencia=%s''',(self.id, 5))
            resultado_id_ocorrencia_inatividade = cursor.fetchone()
#            id_ocorrencia_ingresso_servico = resultado_ocorrencia_ingresso_servico[0]


            if resultado_id_ocorrencia_inatividade != None:

                id_ocorrencia_inatividade = resultado_id_ocorrencia_inatividade[0]



                print "Atualizando ocorrencias de inatividade..."
                cursor.execute('''UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=%s,
                                                            CD_GRUPO=%s,
                                                            NO_OCORRENCIA=%s,
                                                            DT_OCORRENCIA=%s,
                                                            CD_DIPLOMA_LEGAL=%s,
                                                            NO_DIPLOMA_LEGAL=%s,
                                                            DT_PUBLICACAO=%s,
                                                            CD_SERVIDOR=%s
                                                            WHERE CD_OCORRENCIA=%s''',
                                                           (5,
                                                            self.grupoOcoInatividade,
                                                            self.ocorrenciaInatividade,
                                                            data_ocorrencia_inatividade_formatada,
                                                            self.codDipLegalOcoInatividade,
                                                            self.numDipLegalOcoInatividade,
                                                            data_diploma_inatividade_formatada,
                                                            self.id,
                                                            id_ocorrencia_inatividade))
                con.commit()


            else:

                print "Inserindo ocorrencias de inatividade do servidor..."
                cursor.execute('''INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                              CD_SERVIDOR,
                                                              CD_GRUPO,
                                                              NO_OCORRENCIA,
                                                              DT_OCORRENCIA,
                                                              CD_DIPLOMA_LEGAL,
                                                              NO_DIPLOMA_LEGAL,
                                                              DT_PUBLICACAO) values (%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                             (5,
                                                              self.id,
                                                              self.grupoOcoInatividade,
                                                              self.ocorrenciaInatividade,
                                                              data_ocorrencia_inatividade_formatada,
                                                              self.codDipLegalOcoInatividade,
                                                              self.numDipLegalOcoInatividade,
                                                              data_diploma_inatividade_formatada))
                con.commit()






    def insert_or_update_ocorrencia_modificacao_funcional(self):
        print "                                          OCORRENCIA MODIFICACAO FUNCIONAL"
        if self.grupoOcoModFuncional != "00":


            data_ocorrencia_modificacao_funcional_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataOcoModFuncional))))
            data_diploma_modificacao_funcional_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataDipLegalOcoModFuncional))))

            cursor.execute('''SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=%s and cd_tipo_ocorrencia=%s''',(self.id, 6))
            resultado_id_ocorrencia_modificacao_funcional = cursor.fetchone()

            if resultado_id_ocorrencia_modificacao_funcional != None:

                id_ocorrencia_modificacao_funcional = resultado_id_ocorrencia_modificacao_funcional[0]



                print "Atualizando ocorrencias de inatividade..."
                cursor.execute('''UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=%s,
                                                            CD_GRUPO=%s,
                                                            NO_OCORRENCIA=%s,
                                                            DT_OCORRENCIA=%s,
                                                            CD_DIPLOMA_LEGAL=%s,
                                                            NO_DIPLOMA_LEGAL=%s,
                                                            DT_PUBLICACAO=%s,
                                                            CD_SERVIDOR=%s
                                                            WHERE CD_OCORRENCIA=%s''',
                                                           (6,
                                                            self.grupoOcoModFuncional,
                                                            self.ocorrenciaModFuncional,
                                                            data_ocorrencia_modificacao_funcional_formatada,
                                                            self.codDipLegalOcoModFuncional,
                                                            self.numDipLegalOcoModFuncional,
                                                            data_diploma_modificacao_funcional_formatada,
                                                            self.id,
                                                            id_ocorrencia_modificacao_funcional))
                con.commit()


            else:

                print "Inserindo ocorrencias de inatividade do servidor..."
                cursor.execute('''INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                              CD_SERVIDOR,
                                                              CD_GRUPO,
                                                              NO_OCORRENCIA,
                                                              DT_OCORRENCIA,
                                                              CD_DIPLOMA_LEGAL,
                                                              NO_DIPLOMA_LEGAL,
                                                              DT_PUBLICACAO) values (%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                             (6,
                                                              self.id,
                                                              self.grupoOcoModFuncional,
                                                              self.ocorrenciaModFuncional,
                                                              data_ocorrencia_modificacao_funcional_formatada,
                                                              self.codDipLegalOcoModFuncional,
                                                              self.numDipLegalOcoModFuncional,
                                                              data_diploma_modificacao_funcional_formatada))
                con.commit()








    def insert_or_update_ocorrencia_aposentadoria(self):
        print "                                          OCORRENCIA APOSENTADORIA"

        if (self.numProcOcoAposentadoria == "               ") or (self.numProcOcoAposentadoria == "000000000000000"):
            nao_tem_aposentadoria_fita = True
        else:
            nao_tem_aposentadoria_fita = False
        if nao_tem_aposentadoria_fita == False:


            zeros = '0000'
            data_publicacao_ocorrencia_aposentadoria = "00000000"
            ano_aposentadoria = zeros + self.anoPrevOcoAposentadoria
            data_ocorrencia_aposentadoria_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(ano_aposentadoria))))
            data_publicacao_ocorrencia_aposentadoria_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(data_publicacao_ocorrencia_aposentadoria))))
            cursor.execute('''SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=%s and cd_tipo_ocorrencia=%s''',(self.id, 7))
            resultado_id_ocorrencia_aposentadoria = cursor.fetchone()

            if resultado_id_ocorrencia_aposentadoria != None:

                id_ocorrencia_aposentadoria = resultado_id_ocorrencia_aposentadoria[0]

                print "Atualizando ocorrencias de aposentadoria..."
                cursor.execute('''UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=%s,
                                                            CD_GRUPO=%s,
                                                            NO_OCORRENCIA=%s,
                                                            DT_OCORRENCIA=%s,
                                                            CD_SERVIDOR=%s,
                                                            DT_PUBLICACAO=%s
                                                            WHERE CD_OCORRENCIA=%s''',
                                                           (7,
                                                            self.numProcOcoAposentadoria,
                                                            self.opcaoIntOcoAposentadoria,
                                                            data_ocorrencia_aposentadoria_formatada,
                                                            self.id,
                                                            data_publicacao_ocorrencia_aposentadoria_formatada,
                                                            id_ocorrencia_aposentadoria))
                con.commit()

            else:
                print "Inserindo ocorrencias de aposentadoria do servidor..."
                cursor.execute('''INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                              CD_SERVIDOR,
                                                              CD_GRUPO,
                                                              NO_OCORRENCIA,
                                                              DT_OCORRENCIA,
                                                              CD_DIPLOMA_LEGAL,
                                                              NO_DIPLOMA_LEGAL,
                                                              DT_PUBLICACAO) values (%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                             (7,
                                                              self.id,
                                                              self.numProcOcoAposentadoria,
                                                              self.opcaoIntOcoAposentadoria,
                                                              data_ocorrencia_aposentadoria_formatada,
                                                              0,
                                                              0,
                                                              data_publicacao_ocorrencia_aposentadoria_formatada))
                con.commit()

    def insert_or_update_usuario(self):

        cursor.execute('''SELECT cd_usuario FROM crp_usuario WHERE cd_usuario=%s''',(self.id))
        id_usuario = cursor.fetchone()

        if id_usuario != None:
            tem_login_de_usuario = True
        else:
            tem_login_de_usuario = False

        if tem_login_de_usuario == False:
            cursor.execute('''INSERT INTO crp_usuario (CD_USUARIO) values (%s)''',(self.id))
            con.commit()


    def insert_or_update_email(self):

        cursor.execute('''SELECT cd_email FROM crp_email_pessoa WHERE cd_pessoa = %s and 
                          ic_tipo_email = "T"''',(self.id))
        id_email_trabalho = cursor.fetchone()

        cursor.execute('''SELECT cd_email FROM crp_email_pessoa WHERE cd_pessoa = %s and 
                          ic_tipo_email = "P"''',(self.id))
        id_email_pessoal = cursor.fetchone()

        if id_email_trabalho != None:
            tem_email_trabalho = True
        else:
            tem_email_trabalho = False
        if id_email_pessoal != None:
            tem_email_pessoal = True
        else:
            tem_email_pessoal = False

        if tem_email_trabalho == False:
            cursor.execute('''INSERT INTO crp_email_pessoa (CD_PESSOA, IC_TIPO_EMAIL) values (%s,"T")''',(self.id))
            con.commit()
        if tem_email_pessoal == False:
            cursor.execute('''INSERT INTO crp_email_pessoa (CD_PESSOA, IC_TIPO_EMAIL) values (%s,"P")''',(self.id))
            con.commit()


    def insert_or_update_telefone(self):

        cursor.execute('''SELECT cd_telefone_pessoa FROM crp_telefone_pessoa WHERE cd_pessoa = %s and 
                          ic_tipo_telefone = "T"''',(self.id))
        id_telefone_trabalho = cursor.fetchone()

        cursor.execute('''SELECT cd_telefone_pessoa FROM crp_telefone_pessoa WHERE cd_pessoa = %s and 
                          ic_tipo_telefone = "P"''',(self.id))
        id_telefone_pessoal = cursor.fetchone()

        cursor.execute('''SELECT cd_telefone_pessoa FROM crp_telefone_pessoa WHERE cd_pessoa = %s and 
                          ic_tipo_telefone = "C"''',(self.id))
        id_telefone_celular = cursor.fetchone()


        if id_telefone_trabalho != None:
            tem_telefone_trabalho = True
        else:
            tem_telefone_trabalho = False
        if id_telefone_pessoal != None:
            tem_telefone_pessoal = True
        else:
            tem_telefone_pessoal = False
        if id_telefone_celular != None:
            tem_telefone_celular = True
        else:
            tem_telefone_celular = False

        if tem_telefone_trabalho == False:
            cursor.execute('''INSERT INTO crp_telefone_pessoa (CD_PESSOA, NO_DDD, IC_TIPO_TELEFONE) values (%s,21,"T")''',(self.id))
            con.commit()
        if tem_telefone_pessoal == False:
            cursor.execute('''INSERT INTO crp_telefone_pessoa (CD_PESSOA, NO_DDD, IC_TIPO_TELEFONE) values (%s,21,"P")''',(self.id))
            con.commit()
        if tem_telefone_celular == False:
            cursor.execute('''INSERT INTO crp_telefone_pessoa (CD_PESSOA, NO_DDD, IC_TIPO_TELEFONE) values (%s,21,"C")''',(self.id))
            con.commit()



    def atualizar(self, d):
        for k, v in d.values():
            setattr(self, k, v)

    @property
    def nome_corrigido(self):
        return ' '.join(self.nome.split())

def extract_date(date):
  return date[4:],date[2:4],date[:2]
