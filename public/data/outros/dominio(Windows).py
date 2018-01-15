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
#con = MySQLdb.connect('localhost','root','admin')
con = MySQLdb.connect('172.16.32.70','crp','crp123')
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
            cursor.execute('''SELECT Max(cd_pessoa) from crp_pessoa''')
            resultSet = cursor.fetchone()
            if resultSet:
                self._id_pessoa = resultSet[0]
            else:
                logging.error("ID da Pessoa não existe %s" % (self.matricula))
        return self._id_pessoa



    def insert_or_update(self):

         self.insert_or_update_pessoa()
         self.insert_or_update_pessoa_fisica()
         self.insert_or_update_uorg()
         self.insert_or_update_situacao()
         self.insert_or_update_funcao()
         self.insert_or_update_cargo()
         self.insert_or_update_servidor()
         self.insert_or_update_endereco_servidor()
         self.insert_or_update_cargo_servidor()
         self.insert_or_update_funcao_servidor()
         self.insert_or_update_historico_uorg_servidor()
         self.insert_or_update_ocorrencia_ingresso_servico_publico()
         self.insert_or_update_ocorrencia_ingresso_orgao()
         self.insert_or_update_ocorrencia_exclusao()
         self.insert_or_update_ocorrencia_afastamento()
         self.insert_or_update_ocorrencia_inatividade()
         self.insert_or_update_ocorrencia_modificacao_funcional()
         self.insert_or_update_ocorrencia_aposentadoria()



    @property
    def esta_na_base(self):
        cursor.execute('''select cd_servidor from crp_servidor where CD_MATRIC_SIAPE=%s''', (self.matricula,))
        return cursor.fetchall()




    def insert_or_update_pessoa(self):
        print "Analisando existencia de Pessoa " + self.nome + "..."
        ic_tipo_pessoa = "F"
        try:
            cursor.execute('''SELECT cd_servidor FROM crp_servidor WHERE cd_matric_siape=%s''',(self.matricula,))
            if not cursor.fetchall():
                print "               Inserindo pessoa..."
                cursor.execute('''INSERT INTO crp_pessoa (CD_VINCULO,
                                                             NM_PESSOA,
                                                             IC_TIPO_PESSOA,
                                                             CD_DOCUMENTO,
                                                             CD_NATURALIDADE,
                                                             CD_NACIONALIDADE) values (%s,%s,%s,%s,%s,%s)''',
                                                             (1,
                                                              self.nome,
                                                              ic_tipo_pessoa,
                                                              self.cpf,
                                                              self.naturalidade,
                                                              self.nacionalidade))
                con.commit()                
            else:
                print "               Atualizando pessoa..." 
                cursor.execute('''UPDATE crp_pessoa SET CD_VINCULO=%s,
                                                           NM_PESSOA=%s,
                                                           IC_TIPO_PESSOA=%s,
                                                           CD_DOCUMENTO=%s,
                                                           CD_NATURALIDADE=%s,
                                                           CD_NACIONALIDADE=%s
                                                           WHERE CD_PESSOA=%s''',
                                                           (1,
                                                            self.nome,
                                                            ic_tipo_pessoa,
                                                            self.cpf,
                                                            self.naturalidade,
                                                            self.nacionalidade,
                                                            self.id))
                con.commit()
        except:
              logging.error("Erro no método Pessoa %s para %s %s")


    def insert_or_update_pessoa_fisica(self):
        print "Analisando existencia de pessoa fisica..."
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
        print "Analisando existência da uorg..."
        if self.funcao == "DAS" and self.dataSaidaFuncao == "00000000":
            unidade_valida = self.unidadeOrganizacionalFuncao
        else:
            unidade_valida = self.unidadeOrganizacionalLotacao
        numero_uorg = unidade_valida[5:9]
        uorg_superior = "000000000"
        uorg = "Atualizar UORG " + numero_uorg
        sigla_uorg = "desc"
        nome_diretoria = "desc"
        nome_coordenacao = "desc"
        try:
            cursor.execute('''SELECT cd_unidade_organiz FROM crp_unidade_organizacional WHERE cd_unidade_organiz=%s''',(unidade_valida,))
            if not cursor.fetchall():
                print "               Inserindo UORG..."
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
        print "Analisando existencia de codigo da situacao: " + self.codigo_situacao
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






    def insert_or_update_funcao(self):
        print "Verificando Existencia de Funcao na Base..."
        nome_funcao = "Atualizar nome para funcao " + self.codigo_nivel

        try:
#VERIFICA SE O CODIGO DA FUNCAO DO SERVIDOR E DIFERENTE DE ZERO(TEM FUNCAO), E NÃO ESTÁ NA BASE,
            cursor.execute('''SELECT cd_nivel FROM crp_funcao WHERE cd_nivel=%s''',(self.codigo_nivel,))
            if not cursor.fetchall():
                if self.codigo_nivel != "00000":
                    print "               Inserindo Nova Funcao..."
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
                pass
        except:
              logging.error("Impossível inserir funcao %s " % (self.codigo_nivel))


    def insert_or_update_cargo(self):
        print "Analisando existencia de Cargo..."
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
        print "Verificando existência de servidor..."
        id_da_pessoa = self.id_pessoa
        if self.funcao == "DAS" and self.dataSaidaFuncao == "00000000":
            unidade_valida = self.unidadeOrganizacionalFuncao
        else:
            unidade_valida = self.unidadeOrganizacionalLotacao
        if self.esta_na_base:
            print "               Atualizando servidor..."
            cursor.execute('''UPDATE crp_servidor SET CD_UNIDADE_ORGANIZ=%s,
                                                             CD_SITUACAO_SERVIDOR=%s
                                                             WHERE CD_MATRIC_SIAPE=%s''',
                                                            (unidade_valida,
                                                             self.codigo_situacao,
                                                             self.matricula))
            con.commit()


        else:
            print "               Inserindo servidor..."
            cursor.execute('''INSERT INTO crp_servidor (CD_SERVIDOR,
                                                               CD_UNIDADE_ORGANIZ,
                                                               CD_MATRIC_SIAPE,
                                                               CD_SITUACAO_SERVIDOR) values (%s,%s,%s,%s)''',
                                                              (self.id_pessoa,
                                                               unidade_valida,
                                                               self.matricula,
                                                               self.codigo_situacao))
            con.commit()


    def insert_or_update_endereco_servidor(self):
#Método feito em função dos relacionamento pessoa x endereco ser: um para um
        print "Verificando existencia de endereco..."
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
            logging.error("Pessoa-Fisica não existe %s para ID %s" % ( self.id))




    def insert_or_update_cargo_servidor(self):
        print "Analisando existencia de cargo do servidor..."
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

    def insert_or_update_funcao_servidor(self):
        print "Analisando existencia de funcao do servidor..."
        try:
            if self.codigo_nivel != "00000":

               cursor.execute('''SELECT cd_unidade_organiz FROM crp_unidade_organizacional
                                                            WHERE cd_unidade_organiz=%s''',
                                                           (self.unidadeOrganizacionalFuncao,))

               if cursor.fetchall():

                    data_entrada_funcao_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataIngressoFuncao))))
                    data_saida_funcao_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataSaidaFuncao))))
                    if self.dataSaidaFuncao == "00000000":
                        data_funcao_saida_verificada = None
                    else:
                        data_funcao_saida_verificada = data_saida_funcao_formatada

                    cursor.execute('''SELECT cd_funcao FROM crp_funcao WHERE cd_nivel =%s''',(self.codigo_nivel,))
                    resultado_funcao_fita = cursor.fetchone()
                    id_funcao_fita = resultado_funcao_fita[0]

                    id_uorg_fita = self.unidadeOrganizacionalFuncao

                    data_ingresso_fita = data_entrada_funcao_formatada

                    data_saida_fita = data_funcao_saida_verificada

                    cursor.execute('''select max(cd_funcao_servidor)
                                      from corp.crp_funcao_servidor where cd_servidor =%s''',(self.id,))
                    resultado_maximo_id = cursor.fetchone()
                    id_max_funcao_servidor_banco = resultado_maximo_id[0]


                    if (id_max_funcao_servidor_banco == None) or (id_max_funcao_servidor_banco == 0):

                        print "               Inserindo nova funcao do servidor ..."
                        cursor.execute('''INSERT INTO crp_funcao_servidor (CD_SERVIDOR,
                                                                           CD_UNIDADE_ORGANIZ,
                                                                           CD_FUNCAO,
                                                                           DT_INGRESSO_FUNCAO,
                                                                           DT_SAIDA_FUNCAO) values (%s,%s,%s,%s,%s)''',
                                                                          (self.id,
                                                                           self.unidadeOrganizacionalFuncao,
                                                                           id_funcao_fita,
                                                                           data_entrada_funcao_formatada,
                                                                           data_funcao_saida_verificada))
                        con.commit()



#Verificar se, sendo a unidade organizacional e a funcao diferente, consequentemente a data de ingresso
#também será diferente.
                    elif (id_max_funcao_servidor_banco != None) or (id_max_funcao_servidor_banco != 0):
                        try:
                            cursor.execute('''SELECT cd_funcao FROM corp.crp_funcao_servidor
                                              WHERE cd_funcao_servidor =%s''',(id_max_funcao_servidor_banco))
                            resultado_funcao_banco = cursor.fetchone()
                            id_funcao_banco = resultado_funcao_banco[0]

                            cursor.execute('''SELECT cd_unidade_organiz FROM crp_funcao_servidor
                                              WHERE cd_funcao_servidor =%s''',(id_max_funcao_servidor_banco))
                            resultado_uorg_banco = cursor.fetchone()
                            id_uorg_banco = resultado_uorg_banco[0]

                            cursor.execute('''SELECT dt_ingresso_funcao FROM crp_funcao_servidor
                                              WHERE cd_funcao_servidor =%s''',(id_max_funcao_servidor_banco))
                            resultado_ingresso_banco = cursor.fetchone()
                            data_ingresso_banco = resultado_ingresso_banco[0]
                            data_ingresso_banco_str = str(data_ingresso_banco)

                            cursor.execute('''SELECT dt_saida_funcao FROM crp_funcao_servidor
                                              WHERE cd_funcao_servidor =%s''',(id_max_funcao_servidor_banco))
                            resultado_saida_banco = cursor.fetchone()
                            data_saida_banco = resultado_saida_banco[0]
                            data_saida_banco_str = str(data_saida_banco)


                            if (id_uorg_fita != id_uorg_banco) or (id_funcao_fita != id_funcao_banco):
                                print "               Inserindo funcao do servidor em razao da uorg diferente..."
                                cursor.execute('''INSERT INTO crp_funcao_servidor (CD_SERVIDOR,
                                                                           CD_UNIDADE_ORGANIZ,
                                                                           CD_FUNCAO,
                                                                           DT_INGRESSO_FUNCAO,
                                                                           DT_SAIDA_FUNCAO) values (%s,%s,%s,%s,%s)''',
                                                                          (self.id,
                                                                           self.unidadeOrganizacionalFuncao,
                                                                           id_funcao_fita,
                                                                           data_entrada_funcao_formatada,
                                                                           data_funcao_saida_verificada))
                                con.commit()

                            elif (data_ingresso_fita != data_ingresso_banco_str) and (id_uorg_fita == id_uorg_banco):
                                print "               Inserindo funcao do servidor em razao da data de ingresso ser diferente e uorg da fita igual..."
                                cursor.execute('''UPDATE crp_funcao_servidor SET CD_UNIDADE_ORGANIZ=%s,
                                                                         CD_FUNCAO=%s,
                                                                         DT_INGRESSO_FUNCAO=%s,
                                                                         DT_SAIDA_FUNCAO=%s
                                                                         WHERE CD_SERVIDOR=%s''',
                                                                        (self.unidadeOrganizacionalFuncao,
                                                                         id_funcao_fita,
                                                                         data_entrada_funcao_formatada,
                                                                         data_funcao_saida_verificada,
                                                                         self.id))
                                con.commit()

                            elif (data_saida_fita != None) and (id_uorg_fita == id_uorg_banco):
                                    print "               Atualizando funcao do servidor em razao da data da saida ser diferente de nulo e uorg da fita igual..."
                                    cursor.execute('''UPDATE crp_funcao_servidor SET CD_UNIDADE_ORGANIZ=%s,
                                                                         CD_FUNCAO=%s,
                                                                         DT_INGRESSO_FUNCAO=%s,
                                                                         DT_SAIDA_FUNCAO=%s
                                                                         WHERE CD_SERVIDOR=%s''',
                                                                        (self.unidadeOrganizacionalFuncao,
                                                                         id_funcao_fita,
                                                                         data_entrada_funcao_formatada,
                                                                         data_funcao_saida_verificada,
                                                                         self.id))
                                    con.commit()
                            else:
                                print "NAO HA ATUALIZACOES NO HISTORICO DE FUNCOES"
                        except:
                            logging.error("Erro na comparacao de dados da fita com dados do banco")
        except:
            logging.error("Função não existe %s para ID %s" % (self.unidadeOrganizacionalFuncao, self.id))












    def insert_or_update_historico_uorg_servidor(self):


#FORMATA A DATA DE LOTACAO
        data_ingresso_uorg_lotacao_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataLotacao))))
#PEGA A UORG DA FUNCAO OU A UORG DA LOTACAO
        if self.funcao == "DAS" and self.dataSaidaFuncao == "00000000":
            unidade_uorg_hist_fita = self.unidadeOrganizacionalFuncao

        else:
            unidade_uorg_hist_fita = self.unidadeOrganizacionalLotacao

#GUARDA A DATA DE INGRESSO NA UORG FORMATADA
        data_ingresso_uorg_hist = data_ingresso_uorg_lotacao_formatada
#SELECIONA O ID DO HISTORICO DA UORG DO SERVIDOR
        cursor.execute('''SELECT max(cd_unidade_organiz_hist) FROM crp_unidade_organizacional_hist
                          WHERE cd_pessoa_fisica=%s''',(self.id))
        resultado_select_uorg_hist = cursor.fetchone()
#SE O RESULTADO DA QUERY FOR None, ENTAO O ID SERA NONE...
        if resultado_select_uorg_hist == None:
            id_uorg_hist = None
#           resultado_uorg_hist_banco = None
# SENAO SERA O VALOR ORIGINAL QUE ELA TROUXER
        else:
            id_uorg_hist = resultado_select_uorg_hist[0]


#SE O ID PROCURADO FOR NONE SIGNIFICA QUE NAO TEM HISTORICO, ENTAO ELE VAI INSERIR PELA PRIMEIRA VEZ
        if id_uorg_hist == None:
            print "NAO EXISTE AINDA VALOR REGISTRADO DE HISTORICO NA BASE" + self.nome
            print "INSERINDO HISTORICO DE UORG NA BASE..."
            cursor.execute('''INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                              CD_UNIDADE_ORGANIZ,
                                                              DT_INGRESSO_LOTACAO) values (%s,%s,%s)''',
                                                             (self.id,
                                                              unidade_uorg_hist_fita,
                                                              data_ingresso_uorg_hist))
            con.commit()

#SE O ID FOR DIFERENTE DE NONE, ELE ENCONTROU UM VALOR MAXIMO PARA COMPARAR
        elif id_uorg_hist != None:
            try:
#SELECIONA A UORG DA BASE IGUAL A DO ID QUE FOI TRAZIDO NO INICIO(DIFERENTE DE NONE)
                cursor.execute('''SELECT cd_unidade_organiz FROM crp_unidade_organizacional_hist
                                  WHERE cd_unidade_organiz_hist =%s''',(id_uorg_hist))
                resultado_uorg_hist_banco = cursor.fetchone()
                unidade_uorg_hist_banco = resultado_uorg_hist_banco[0]


#SELECTIONA A DATA DE INGRESSO REGISTRADA NA BASE PARA O ID QUE FOI TRAGO
                cursor.execute('''SELECT dt_ingresso_lotacao FROM crp_unidade_organizacional_hist
                                  WHERE cd_unidade_organiz_hist =%s''',(id_uorg_hist))
                resultado_data_banco_hist = cursor.fetchone()
                data_banco_hist = resultado_data_banco_hist[0]



#SE A DATA DO BANCO VIER COMO None ENTAO A VARIAVEL VAI ARMAZENAR ZERO, SENAO O PROPRIO VALOR
                if data_banco_hist == None:
                   data_banco_hist_str = "0000-00-00"
                else:
                   data_banco_hist_str = str(data_banco_hist)


#SE A UORG DA FITA FOR DIFERENTE DA DO BANCO ENTAO VAI INSERIR
                if unidade_uorg_hist_fita != unidade_uorg_hist_banco:
                    print "INSERINDO NOVO HISTORICO DE UORG NA BASE PELA UORG DIFERENTE"
                    cursor.execute('''INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                          CD_UNIDADE_ORGANIZ,
                                                                          DT_INGRESSO_LOTACAO) values (%s,%s,%s)''',
                                                                         (self.id,
                                                                          unidade_uorg_hist_fita,
                                                                          data_ingresso_uorg_hist))
                    con.commit()


#        elif unidade_uorg_hist_fita == unidade_uorg_hist_banco:
                elif data_ingresso_uorg_hist != data_banco_hist_str:
                    print "INSERINDO NOVO HISTORICO DE UORG NA BASE PELA DATA DE INGRESSO DIFERENTE"
                    print data_ingresso_uorg_hist + data_banco_hist_str
                    cursor.execute('''INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                              CD_UNIDADE_ORGANIZ,
                                                              DT_INGRESSO_LOTACAO) values (%s,%s,%s)''',
                                                             (self.id,
                                                              unidade_uorg_hist_fita,
                                                              data_ingresso_uorg_hist))
                    con.commit()
                else:
                    print "NAO HA HISTORICO NOVO"
            except:
                pass



    def insert_or_update_ocorrencia_ingresso_servico_publico(self):

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

        if self.grupoOcorrenciaExclu != "00":

            print "CONFIRMADO OCORRENCIA DE EXCLUSAO" + self.nome

            data_exclusao_orgao_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataOcorrenciaExclu))))
            data_diploma_exclusao_legal_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(self.dataDipLegalOcorrenciaExclu))))

            cursor.execute('''SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=%s and cd_tipo_ocorrencia=%s''',(self.id, 3))
            resultado_ocorrencia_exclusao_servico = cursor.fetchone()
            print "resultado_ocorrencia_exclusao_servico"
            print resultado_ocorrencia_exclusao_servico

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

        if self.grupoOcoModFuncional != "00":

            print "CONFIRMADO OCORRENCIA DE MODIFICACAO FUNCIONAL" + self.nome

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

        if self.numProcOcoAposentadoria != "000000000000000":

            print "CONFIRMADO OCORRENCIA DE APOSENTADORIA" + self.nome

            zeros = '0000'
            data_publicacao_ocorrencia_aposentadoria = "00000000"
            ano_aposentadoria = zeros + self.anoPrevOcoAposentadoria
            data_ocorrencia_aposentadoria_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(ano_aposentadoria))))
            data_publicacao_ocorrencia_aposentadoria_formatada = "%04d-%02d-%02d" % tuple(map(int, (extract_date(data_publicacao_ocorrencia_aposentadoria))))
            cursor.execute('''SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=%s and cd_tipo_ocorrencia=%s''',(self.id, 7))
            resultado_id_ocorrencia_aposentadoria = cursor.fetchone()
#            id_ocorrencia_ingresso_servico = resultado_ocorrencia_ingresso_servico[0]


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



    def atualizar(self, d):
        for k, v in d.values():
            setattr(self, k, v)

    @property
    def nome_corrigido(self):
        return ' '.join(self.nome.split())

def extract_date(date):
  return date[4:],date[2:4],date[:2]
