
require 'csv'
require 'mysql'

caminho_da_fita = Dir.pwd.sub("/app/controllers","").concat("/public/data/FITA_ESPELHO.TXT")
fita_espelho = open(caminho_da_fita, 'r')
#dbh = Mysql.real_connect("localhost","root","admin","corp")
dbh = Mysql.real_connect("172.16.111.50","crp","crp123","corp")#
#dbh = Mysql.real_connect("localhost","root","","corp")

### Início das definições de métodos

def formata_data(data)
  data_formatada = data.slice(4,4) + "-" + data.slice(2,2) + "-" + data.slice(0,2)
  return data_formatada
end

### Início da leitura da fita_espelho

fita_espelho.each_line do |linha|  
  case linha[17...18]
    when '1'
      #Dados do @servidor
      @servidor = {
        :upagadora => "#{ linha[0...9] }",                     :matricula => "#{ linha[9...16] }", 
        :matricula_dv => "#{ linha[16...17] }",                :tipoRegistro => "#{ linha[17...18] }",
        :nome => "#{ linha[20...80] }".strip,                  :cpf => "#{ linha[80...91] }", 
        :pis_pasep => "#{ linha[91...102] }",                  :nome_mae => "#{ linha[102...152] }", 
        :sexo => "#{ linha[152...153] }",                      :data_nascimento => "#{ linha[153...161] }", 
        :codigo_estado_civil => "#{ linha[161...162] }",       :nivel_escolaridade => "#{ linha[162...164] }", 
        :codigo_titulacao_formacao => "#{ linha[164...166] }", :filler1 => "#{ linha[166...171] }", 
        :nacionalidade => "#{ linha[171...172] }",             :naturalidade => "#{ linha[172...174] }", 
        :pais => "#{ linha[174...177] }",                      :ano_chegada => "#{ linha[177...181] }", 
        :ir => "#{ linha[181...183] }",                        :sf => "#{ linha[183...185] }", 
        :data1Emprego => "#{ linha[185...193] }",              :identificacaoOrigem => "#{ linha[193...201] }",
        # endereco... 
        :logradouro => "#{ linha[201...241] }".strip,                :numero_endereco => "#{ linha[241...247] }".strip,
        :complemento => "#{ linha[247...268] }".strip,               :bairro => "#{ linha[268...293] }".strip,
        :municipio => "#{ linha[293...323] }",                 :cep => "#{ linha[323...331] }", 
        :uf => "#{ linha[331...333] }",                        :registroGeral => "#{ linha[333...347] }", 
        :siglaOrgaoExpeditor => "#{ linha[347...352] }",       :dataExpedicaoIdentidade => "#{ linha[352...360] }", 
        :siglaUfIdentidade => "#{ linha[360...362] }",         :tituloEleitor => "#{ linha[362...375] }", 
        :filler2 => "#{ linha[375...764] }" }
                 
    when '2'
      #REGISTRO_DOIS
      @servidor.merge!(
        :siglaRegimeJuridico => "#{ linha[20...23] }",        :codigo_situacao => "#{ linha[23...25] }", 
        :numeroCarteira => "#{ linha[25...31] }",             :serieCarteira => "#{ linha[31...36] }", 
        :ufCarteira => "#{ linha[36...38] }",                 :bancoPagamento => "#{ linha[36...38] }", 
        :agenciaPagamento => "#{ linha[41...47] }",           :contaCorrentePagamento => "#{ linha[47...60] }", 
        :dataOpcaoFgts => "#{ linha[60...68] }",              :bancoFgts => "#{ linha[68...71] }", 
        :agenciaFgts => "#{ linha[71...77] }",                :contaCorrenteFgts => "#{ linha[77...90] }", 
        :jornadaTrabalho => "#{ linha[90...92] }",            :percentualTempoServico => "#{ linha[92...94] }", 
        :dataCadastramentoServidor => "#{ linha[94...102] }", :indicadorSupressaoPagamento => "#{ linha[102...103] }", 
        :dataSupressaoPagamento => "#{ linha[103...109] }",   :numeradorProporcionalidade => "#{ linha[109...111] }", 
        :denominadorProporcionalidade => "#{ linha[111...113] }",
        # Cargo/Emprego 
        :grupo => "#{ linha[113...116] }",           :codigo_cargo => "#{ linha[116...119] }", 
        :classe => "#{ linha[119...120] }",          :referencia_nivel_padrao => "#{ linha[120...123] }", 
        :padrao => "#{ linha[120...123] }",          :data_entrada_cargo => "#{ linha[123...131] }", 
        :data_saida_cargo => "#{ linha[131...139] }",
        # Funcao 
        :funcao => "#{ linha[139...142] }",                      :codigo_nivel => "#{ linha[142...147] }", 
        :escolaridadeFuncao => "#{ linha[147...149] }",          :opcaoFuncao => "#{ linha[149...150] }", 
        :dataIngressoFuncao => "#{ linha[150...158] }",          :dataSaidaFuncao => "#{ linha[158...166] }", 
        :unidadeOrganizacionalFuncao => "#{ linha[166...175] }",
        # Nova Funcao... 
        :siglaNovaFuncao => "#{ linha[175...178] }",                 :codigoNivelNovaFuncao => "#{ linha[178...183] }", 
        :escolaridadeNovaFuncao => "#{ linha[183...185] }",          :opcaoNovaFuncao => "#{ linha[185...186] }", 
        :dataIngressoNovaFuncao => "#{ linha[186...194] }",          :dataSaidaNovaFuncao => "#{ linha[194...202] }", 
        :unidadeOrganizacionalNovaFuncao => "#{ linha[202...211] }", :atividadeDaFuncao => "#{ linha[211...215] }",
        # Lotacao... 
        :unidadeOrganizacionalLotacao => "#{ linha[215...224] }",     :codigo_lotacao => "#{ linha[215...224] }", 
        :dataLotacao => "#{ linha[224...232] }",                      :orgaoLocalizacao => "#{ linha[232...237] }", 
        :unidadeOrganizacionalLocalizacao => "#{ linha[237...246] }", :grupoIngressoOrgao => "#{ linha[246...248] }", 
        :ocorrenciaIngressoOrgao => "#{ linha[248...251] }",          :dataIngressoOrgao => "#{ linha[251...259] }", 
        :codigoDiplomaLegal => "#{ linha[259...261] }",               :numeroDiplomaLegal => "#{ linha[261...270] }", 
        :dataPublicacaoDiplomaLegal => "#{ linha[270...278] }",       :grupoIngreServPublico => "#{ linha[278...280] }", 
        :ocorrenciaIngreServPublico => "#{ linha[280...283] }",       :dataIngreServPublico => "#{ linha[283...291] }", 
        :codDipLegalIngreServPublico => "#{ linha[291...293] }",      :numDipLegalIngreServPublico => "#{ linha[293...302] }", 
        :dataDipLegalIngreServPublico => "#{ linha[302...310] }",     :grupoOcorrenciaExclu => "#{ linha[310...312] }", 
        :ocorrenciaExclu => "#{ linha[312...315] }",                  :dataOcorrenciaExclu => "#{ linha[315...323] }", 
        :codDipLegalOcorrenciaExclu => "#{ linha[323...325] }",       :numDipLegalOcorrenciaExclu => "#{ linha[325...334] }", 
        :dataDipLegalOcorrenciaExclu => "#{ linha[334...342] }",      :grupoOcoAfastamento => "#{ linha[342...344] }", 
        :ocorrenciaAfastamento => "#{ linha[344...347] }",            :dataInicioOcoAfastamento => "#{ linha[347...355] }", 
        :dataTerminoOcoAfastamento => "#{ linha[355...363] }",        :codDipLegalOcoAfastamento => "#{ linha[363...365] }", 
        :numDipLegalOcoAfastamento => "#{ linha[365...374] }",        :dataDipLegalOcoAfastamento => "#{ linha[374...382] }", 
        :grupoOcoInatividade => "#{ linha[382...384] }",              :ocorrenciaInatividade => "#{ linha[384...387] }", 
        :dataOcoInatividade => "#{ linha[387...395] }",               :codDipLegalOcoInatividade => "#{ linha[395...397] }", 
        :numDipLegalOcoInatividade => "#{ linha[397...406] }",        :dataDipLegalOcoInatividade => "#{ linha[406...414] }", 
        :numProcOcoAposentadoria => "#{ linha[414...429] }",          :anoPrevOcoAposentadoria => "#{ linha[429...433] }", 
        :opcaoIntOcoAposentadoria => "#{ linha[433...434] }",         :uorgControle => "#{ linha[434...443] }", 
        :grupoOcoModFuncional => "#{ linha[443...445] }",             :ocorrenciaModFuncional => "#{ linha[445...448] }", 
        :dataOcoModFuncional => "#{ linha[448...456] }",              :codDipLegalOcoModFuncional => "#{ linha[456...458] }", 
        :numDipLegalOcoModFuncional => "#{ linha[458...467] }",       :dataDipLegalOcoModFuncional => "#{ linha[467...475] }", 
        :regJuAnterior => "#{ linha[475...478] }",                    :sitServAnterior => "#{ linha[478...480] }", 
        :orgDestMudOrg => "#{ linha[480...485] }",                    :dataLibDestMudOrg => "#{ linha[485...493] }", 
        :orgOriLibDestMudOrg => "#{ linha[493...498] }",              :orgAnterior => "#{ linha[498...503] }", 
        :matAnterior => "#{ linha[503...510] }",                      :codOrgExtMod => "#{ linha[510...515] }", 
        :matServExtMod => "#{ linha[515...522] }",                    :orgaoAtual => "#{ linha[522...527] }", 
        :matriculaAtual => "#{ linha[527...534] }",                   :codUpagMud => "#{ linha[534...543] }", 
        :dataLibUpagMud => "#{ linha[543...551] }",                   :motivoUpagMud => "#{ linha[551...552] }", 
        :indPagServidor => "#{ linha[552...553] }",                   :nomeCartRegObito => "#{ linha[553...603] }", 
        :numLivroRegObito => "#{ linha[603...611] }",                 :numFolhaRegObito => "#{ linha[611...617] }", 
        :numRegistroRegObito => "#{ linha[617...625] }",              :dataRegObito => "#{ linha[625...633] }", 
        :indExcluInstituidor => "#{ linha[633...634] }",              :dataExcluInstituidor => "#{ linha[634...642] }", 
        :tipoValeAlimentacao => "#{ linha[642...643] }",              :dataInicioValeAlimentacao => "#{ linha[643...651] }", 
        :dataFimValeAlimentacao => "#{ linha[651...659] }",           :indOpeRaiox => "#{ linha[659...660] }", 
        :orgaoRequisitante => "#{ linha[660...665] }",                :codVaga => "#{ linha[665...672] }", 
        :mesConceAnuenio => "#{ linha[672...674] }",                  :perOpeRaiox => "#{ linha[674...679] }", 
        :codGrupoPosse => "#{ linha[679...681] }",                    :ocorrenciaPosse => "#{ linha[681...684] }", 
        :dataPosse => "#{ linha[684...692] }",                        :codDiplomaPosse => "#{ linha[692...694] }", 
        :dataDiplomaPosse => "#{ linha[694...702] }",                 :numeroDiplomaPosse => "#{ linha[702...711] }", 
        :grupoOcoRevAtividade => "#{ linha[711...713] }",             :codOcoRevAtividade => "#{ linha[713...716] }", 
        :dataOcoRevAtividade => "#{ linha[716...724] }",              :codDiploRevAtividade => "#{ linha[724...726] }", 
        :dataDiploRevAtividade => "#{ linha[726...734] }",            :numDiploRevAtividade => "#{ linha[734...743] }", 
        :cargoCalcAutomatico => "#{ linha[743...744] }",              :funcaoCalcAutomatico => "#{ linha[744...745] }", 
        :salFamiliaCalcAutomatico => "#{ linha[745...746] }",         :adicTemServCalcAutomatico => "#{ linha[746...747] }", 
        :fgtsCalcAutomatico => "#{ linha[747...748] }",               :prevSocialCalcAutomatico => "#{ linha[748...749] }", 
        :impRendaCalcAutomatico => "#{ linha[749...750] }",           :marConsigCalcAutomatico => "#{ linha[750...751] }", 
        :contriSindiCalcAutomatico => "#{ linha[751...752] }",        :adian13CalcAutomatico => "#{ linha[752...753] }", 
        :abateTetoConstCalcAutomatico => "#{ linha[753...754] }",     :sal13CalcAutomatico => "#{ linha[754...755] }", 
        :planSegSocial6CalcAutomatico => "#{ linha[755...756] }",     :feriasCalcAutomatico => "#{ linha[756...757] }", 
        :pensaoCalcAutomatico => "#{ linha[757...758] }",             :beneficiosCalcAutomatico => "#{ linha[758...759] }", 
        :ipmfCpmfCalcAutomatico => "#{ linha[759...760] }",           :raisCalcAutomatico => "#{ linha[760...761] }", 
        :difUrvCalcAutomatico => "#{ linha[761...762] }",             :adiantamentoCalcAutomatico => "#{ linha[762...763] }", 
        :rendPasepCalcAutomatico => "#{ linha[763...764] }" )
      
      #Verifica se o @servidor está na base, será utilizado em vários métodos
      @servidor[:cd_servidor] = dbh.query("SELECT cd_servidor from crp_servidor where CD_MATRIC_SIAPE=#{@servidor[:matricula]}").fetch_row
      @servidor[:cd_servidor] != nil ? @servidor[:ja_existente] = true : @servidor[:ja_existente] = false
      ###Inicia a inserção dos dados no bando de dados

      puts "\n"   
         
###################################################################################################################################
#######################    Insere ou Atualiza Pessoa    ###########################################################################
###################################################################################################################################

      #puts "#{@servidor[:nome]}\n"
      #Define vinculo e tipo de pessoa
      @servidor[:funcao] == "ETG"? @servidor[:vinculo] = "9" : @servidor[:vinculo] = "1"
      @servidor[:ic_tipo_pessoa] = "F"
      
      #Se o @servidor for encontrado, insere ou atualiza os seus dados
      #***Sem tratamento de erro***
      if @servidor[:cd_servidor]
        puts "Atualizando #{@servidor[:nome]}\n"
      #puts "ID: #{@servidor[:cd_servidor]}"
        puts @servidor[:registroGeral].length
      dbh.query("UPDATE crp_pessoa SET CD_VINCULO=#{@servidor[:vinculo]},
                                         NM_PESSOA='#{@servidor[:nome]}',
                                         IC_TIPO_PESSOA='#{@servidor[:ic_tipo_pessoa]}',
                                         CD_DOCUMENTO='#{@servidor[:cpf]}',
                                         CD_NATURALIDADE='#{@servidor[:naturalidade]}',
                                         CD_NACIONALIDADE='#{@servidor[:nacionalidade]}',
                                         CD_RG='#{@servidor[:registroGeral]}'
                                     WHERE CD_PESSOA=#{@servidor[:cd_servidor]}")
      else
        puts "Inserindo #{@servidor[:nome]}\n"
        dbh.query("INSERT INTO crp_pessoa (CD_VINCULO,
                                           NM_PESSOA,
                                           IC_TIPO_PESSOA,
                                           CD_DOCUMENTO,
                                           CD_NATURALIDADE,
                                           CD_NACIONALIDADE,
                                           CD_RG) values (#{@servidor[:vinculo]},
                                                          '#{@servidor[:nome]}',
                                                          '#{@servidor[:ic_tipo_pessoa]}',
                                                          '#{@servidor[:cpf]}',
                                                          '#{@servidor[:naturalidade]}',
                                                          '#{@servidor[:nacionalidade]}',
                                                          '#{@servidor[:registroGeral]}')")


         @servidor[:cd_servidor] = dbh.query("SELECT Max(cd_pessoa) from crp_pessoa").fetch_row.first
#        @servidor[:cd_servidor] = dbh.query("SELECT Max(cd_pessoa) from crp_pessoa").fetch_row.first

        #Insere registro, telefone e email na tabela crp_email_pessoa e crp_telefone_pessoa

        dbh.query("INSERT INTO crp_email_pessoa (CD_PESSOA, IC_TIPO_EMAIL) values (#{@servidor[:cd_servidor]},'T')")
        dbh.query("INSERT INTO crp_email_pessoa (CD_PESSOA, IC_TIPO_EMAIL) values (#{@servidor[:cd_servidor]},'P')")
        dbh.query("INSERT INTO crp_telefone_pessoa (CD_PESSOA, NO_DDD, IC_TIPO_TELEFONE) values (#{@servidor[:cd_servidor]},21,'T')")
        dbh.query("INSERT INTO crp_telefone_pessoa (CD_PESSOA, NO_DDD, IC_TIPO_TELEFONE) values (#{@servidor[:cd_servidor]},21,'P')")
        dbh.query("INSERT INTO crp_telefone_pessoa (CD_PESSOA, NO_DDD, IC_TIPO_TELEFONE) values (#{@servidor[:cd_servidor]},21,'C')")
      end
      puts "cd_servidor = #{@servidor[:cd_servidor]}"
      puts "matricula   = #{@servidor[:matricula]}"

###################################################################################################################################
#######################    Fim de Insere ou Atualiza Pessoa     ###################################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Pessoa Física    ####################################################################
################################################################################################################################### 

      case @servidor[:codigo_estado_civil]
        when '1'
          sigla_estado_civil = 'S'
        when '2'
          sigla_estado_civil = 'C'
        when '3'
          sigla_estado_civil = 'J'
        when '4'
          sigla_estado_civil = 'D'
        else
          sigla_estado_civil = 'V'
      end
  
      if @servidor[:ja_existente] == false
        #puts "    Inserindo pessoa fisica..."
        dbh.query("INSERT INTO crp_pessoa_fisica (CD_PESSOA_FISICA,
                                                  DT_NASCIMENTO,
                                                  IC_SEXO,
                                                  IC_ESTADO_CIVIL) values (#{@servidor[:cd_servidor]},
                                                                           '#{formata_data(@servidor[:data_nascimento])}',
                                                                           '#{@servidor[:sexo]}',
                                                                           '#{sigla_estado_civil}')")
        #Insere registro de usuario na tabela crp_usuario
        dbh.query("INSERT INTO crp_usuario (CD_USUARIO) values (#{@servidor[:cd_servidor]})")
      else
        #puts "    Atualizando pessoa fisica..."
        dbh.query("UPDATE crp_pessoa_fisica SET DT_NASCIMENTO='#{formata_data(@servidor[:data_nascimento])}',
                                                IC_SEXO='#{@servidor[:sexo]}',
                                                IC_ESTADO_CIVIL='#{sigla_estado_civil}'
                                                WHERE CD_PESSOA_FISICA=#{@servidor[:cd_servidor]}")
      end
  
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Pessoa Física    #############################################################
################################################################################################################################### 

###################################################################################################################################
#######################    Insere ou Atualiza UORG    #############################################################################
################################################################################################################################### 

      if @servidor[:funcao] != "000" and @servidor[:funcao] != "   "
        unidade_valida = @servidor[:unidadeOrganizacionalFuncao]
      else
        unidade_valida = @servidor[:unidadeOrganizacionalLotacao]
      end

      if @servidor[:siglaNovaFuncao] != "000" and @servidor[:siglaNovaFuncao] != "   "
        tem_uorg_na_nova_funcao_na_fita = true
        unidade_valida_nova = @servidor[:unidadeOrganizacionalNovaFuncao]
        numero_uorg_nova = unidade_valida_nova[5...9]
        uorg_nova = "Atualizar UORG #{numero_uorg_nova}"
      else
        tem_uorg_na_nova_funcao_na_fita = false
      end
      numero_uorg = unidade_valida[5...9]
      uorg_superior = "000000000"
      uorg = "Atualizar UORG #{numero_uorg}"
      sigla_uorg = "desc"
      nome_diretoria = "desc"
      nome_coordenacao = "desc"

      #Insere Unidade Organizacional nova se ela não existir no banco
      if tem_uorg_na_nova_funcao_na_fita
        cd_unidade_organiz_nova_funcao = dbh.query("SELECT cd_unidade_organiz FROM crp_unidade_organizacional 
                                                    WHERE cd_unidade_organiz='#{unidade_valida_nova}'").fetch_row
        if cd_unidade_organiz_nova_funcao.nil?
          #puts "    Inserindo nova Unidade Organizacional..."
          dbh.query("INSERT INTO crp_unidade_organizacional (CD_UNIDADE_ORGANIZ,
                                                             CD_UNIDADE_SUPERIOR,
                                                             NM_UNIDADE_ORGANIZ,
                                                             SG_UNIDADE_ORGANIZ,
                                                             NM_DIRETORIA,
                                                             NM_COORDENACAO) values ('#{unidade_valida_nova}',
                                                                                     '#{uorg_superior}',
                                                                                     '#{uorg_nova}',
                                                                                     '#{sigla_uorg}',
                                                                                     '#{nome_diretoria}',
                                                                                     '#{nome_coordenacao}')")
        end
      end
      
      #Insere Unidade Organizacional válida se ela não existir no banco
      ###Sem tratamento de erros###
      cd_unidade_organiz_funcao_ou_lotacao = dbh.query("SELECT cd_unidade_organiz FROM crp_unidade_organizacional 
                                                        WHERE cd_unidade_organiz='#{unidade_valida}'").fetch_row
      if cd_unidade_organiz_funcao_ou_lotacao.nil?
        #puts "    Inserindo nova Unidade Organizacional..."
        dbh.query("INSERT INTO crp_unidade_organizacional (CD_UNIDADE_ORGANIZ,
                                                           CD_UNIDADE_SUPERIOR,
                                                           NM_UNIDADE_ORGANIZ,
                                                           SG_UNIDADE_ORGANIZ,
                                                           NM_DIRETORIA,
                                                           NM_COORDENACAO) values ('#{unidade_valida}',
                                                                                   '#{uorg_superior}',
                                                                                   '#{uorg}',
                                                                                   '#{sigla_uorg}',
                                                                                   '#{nome_diretoria}',
                                                                                   '#{nome_coordenacao}')")
      end
      
###################################################################################################################################
#######################    Fim de Insere ou Atualiza UORG    ######################################################################
################################################################################################################################### 

###################################################################################################################################
#######################    Insere ou Atualiza Situação    #########################################################################
################################################################################################################################### 

      nome_situacao = "Atualizar situacao " + @servidor[:codigo_situacao]
      cd_situacao_base = dbh.query("SELECT cd_situacao_servidor FROM crp_situacao_servidor 
                                    WHERE cd_situacao_servidor = '#{@servidor[:codigo_situacao]}'").fetch_row
      if cd_situacao_base.nil?
        #puts "    Inserindo situação do @servidor..."
        dbh.query("INSERT INTO crp_situacao_servidor (CD_SITUACAO_servidor,
                                                      DS_SITUACAO_servidor) values ('#{@servidor[:codigo_situacao]}',
                                                                                    '#{nome_situacao}')")
      end
  
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Situação    ##################################################################
################################################################################################################################### 

###################################################################################################################################
#######################    Insere ou Atualiza Funções    ##########################################################################
################################################################################################################################### 

      nome_funcao = "Atualizar nome para funcao " + @servidor[:codigo_nivel]
      nome_nova_funcao = "Atualizar nome para nova funcao " + @servidor[:codigoNivelNovaFuncao]
      
      cd_funcao = dbh.query("SELECT cd_nivel FROM crp_funcao 
                             WHERE cd_nivel = '#{@servidor[:codigo_nivel]}' 
                             AND sg_funcao = '#{@servidor[:funcao]}'").fetch_row
      if cd_funcao.nil?
        #puts "    Inserindo dados da funcao..."
        dbh.query("INSERT INTO crp_funcao (SG_FUNCAO,
                                           CD_NIVEL,
                                           NM_FUNCAO,
                                           IC_OPCAO) values ('#{@servidor[:funcao]}',
                                                             '#{@servidor[:codigo_nivel]}',
                                                             '#{nome_funcao}',
                                                             '#{@servidor[:opcaoFuncao]}')")
      else
        #puts "    Atualizando dados da funcao..."
        dbh.query("UPDATE crp_funcao SET IC_OPCAO='#{@servidor[:opcaoFuncao]}'
                                         WHERE CD_NIVEL='#{@servidor[:codigo_nivel]}'
                                         and SG_FUNCAO='#{@servidor[:funcao]}'")
      end

      cd_nova_funcao_base = dbh.query("SELECT cd_nivel FROM crp_funcao 
                                       WHERE cd_nivel = '#{@servidor[:codigoNivelNovaFuncao]}' 
                                       AND sg_funcao = '#{@servidor[:siglaNovaFuncao]}'").fetch_row
      if cd_nova_funcao_base.nil?
        #puts "    Inserindo dados de nova funcao..."
        dbh.query("INSERT INTO crp_funcao (SG_FUNCAO,
                                            CD_NIVEL,
                                            NM_FUNCAO,
                                            IC_OPCAO) values ('#{@servidor[:siglaNovaFuncao]}',
                                                              '#{@servidor[:codigoNivelNovaFuncao]}',
                                                              '#{nome_nova_funcao}',
                                                              '#{@servidor[:opcaoNovaFuncao]}')")

      else
        #puts "    Atualizando dados de nova funcao..."
        dbh.query("UPDATE crp_funcao SET IC_OPCAO='#{@servidor[:opcaoNovaFuncao]}'
                                         WHERE CD_NIVEL='#{@servidor[:codigoNivelNovaFuncao]}'
                                         and SG_FUNCAO='#{@servidor[:siglaNovaFuncao]}'")
      end
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Funções    ###################################################################
################################################################################################################################### 

###################################################################################################################################
#######################    Insere ou Atualiza Cargo    ############################################################################
################################################################################################################################### 

      nome_cargo = "Outros"
      situacao_cargo = "I"
      codigo_cargo = @servidor[:grupo] + @servidor[:codigo_cargo]
      cd_cargo_banco = dbh.query("SELECT cd_cargo FROM crp_cargo 
                                  WHERE cd_cargo= '#{codigo_cargo}'").fetch_row
      if cd_cargo_banco.nil?
        #puts "    Inserindo dados relativos ao cargo..."
        dbh.query("INSERT INTO crp_cargo (CD_CARGO,
                                          NM_CARGO,
                                          IC_SITUACAO_CARGO) values
                                          ('#{codigo_cargo}',
                                          '#{nome_cargo}',
                                          '#{situacao_cargo}')")
      end
  
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Cargo    #####################################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Servidor    #########################################################################
###################################################################################################################################

      #VERIFICAR A DATA DA FITA-ESPELHO POIS ESTE MÉTODO PODE ATUALIZAR UMA SITUACAÇÃO ANTIGA
      if @servidor[:ja_existente] == false
        #puts "inserindo matricula"
        dbh.query("INSERT INTO crp_servidor (cd_servidor,
                                             CD_MATRIC_SIAPE,
                                             CD_SITUACAO_servidor) values ('#{@servidor[:cd_servidor]}',
                                                                           '#{@servidor[:matricula]}',
                                                                           '#{@servidor[:codigo_situacao]}')")
      else
        dbh.query("UPDATE crp_servidor SET CD_SITUACAO_servidor= '#{@servidor[:codigo_situacao]}'
                                           WHERE CD_MATRIC_SIAPE= '#{@servidor[:matricula]}'")
      end

###################################################################################################################################
#######################    Fim de Insere ou Atualiza Servidor    ##################################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Endereço Servidor   #################################################################
###################################################################################################################################

      #Método feito em função dos relacionamento pessoa x endereco ser: um para um
      ### Sem tratamento de erros ###
      case @servidor[:pais]
        when "073":
            pais = "HT"
        when "088":
            pais = "IT"
        when "129":
            pais = "PT"
        when "040":
            pais = "CO"
        when "055":
            pais = "US"
        when "037":
            pais = "CN"
        when "011":
            pais = "AR"
        when "128":
            pais = "PL"
        else
            pais = "BR"
      end
      
      cd_pessoa = dbh.query("SELECT cd_pessoa FROM crp_endereco_pessoa WHERE cd_pessoa='#{@servidor[:cd_servidor]}'").fetch_row
    
      if @servidor[:bairro].include?("'")
        @servidor[:bairro] = @servidor[:bairro].sub("'"," ")
      end
      while @servidor[:logradouro].include?("'")
        @servidor[:logradouro] = @servidor[:logradouro].sub("'"," ")
      end
      if @servidor[:numero_endereco].include?("N/I") or @servidor[:numero_endereco] == ''
        @servidor[:numero_endereco] = 0
      end
      #puts "bairro ----- #{@servidor[:bairro]}"
      #puts "logradouro-- #{@servidor[:logradouro]}"
      #puts "no_endereco #{@servidor[:numero_endereco]}"
      #puts "complemento- #{@servidor[:complemento]}"
    
      if !cd_pessoa.nil?
    
      #puts "    Atualizando endereco..."
        dbh.query("UPDATE crp_endereco_pessoa SET CD_PAIS='#{pais}',
                                                  NM_LOGRADOURO='#{@servidor[:logradouro]}',
                                                  NO_ENDERECO='#{@servidor[:numero_endereco]}',
                                                  DS_COMPLEMENTO='#{@servidor[:complemento]}',
                                                  NM_BAIRRO='#{@servidor[:bairro]}',
                                                  NO_CEP='#{@servidor[:cep]}',
                                                  SG_UF='#{@servidor[:uf]}'
                                              WHERE CD_PESSOA=#{@servidor[:cd_servidor]}")
      else
      #puts "    Inserindo de endereco..."
        dbh.query("INSERT INTO crp_endereco_pessoa (CD_PAIS,
                                                    NM_CIDADE,
                                                    NM_LOGRADOURO,
                                                    NO_ENDERECO,
                                                    DS_COMPLEMENTO,
                                                    NM_BAIRRO,
                                                    NO_CEP,
                                                    SG_UF,
                                                    CD_PESSOA) values ('#{pais}',
                                                                       '#{@servidor[:municipio]}',
                                                                       '#{@servidor[:logradouro]}',
                                                                       '#{@servidor[:numero_endereco]}',
                                                                       '#{@servidor[:complemento]}',
                                                                       '#{@servidor[:bairro]}',
                                                                       '#{@servidor[:cep]}',
                                                                       '#{@servidor[:uf]}',
                                                                       '#{@servidor[:cd_servidor]}')")
      end
  
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Endereço Servidor    #########################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Cargo Servidor    ###################################################################
###################################################################################################################################


      if @servidor[:data_entrada_cargo] == "00000000"
        @servidor[:data_entrada_cargo] = @servidor[:dataIngressoOrgao]
      end                           
    
      if @servidor[:grupo] != "000"
        @servidor[:data_saida_cargo] == "00000000"? data_saida_cargo_fita = nil : data_saida_cargo_fita = formata_data(@servidor[:data_saida_cargo])
        cd_grupo_cargo_fita = @servidor[:grupo] + @servidor[:codigo_cargo]
    
        #EXTRAI ID MAXIMO DE CARGO DE @servidor DA BASE
        max_cd_cargo_servidor = dbh.query("select max(cd_cargo_servidor)
                                            from corp.crp_cargo_servidor where cd_servidor = '#{@servidor[:cd_servidor]}'").fetch_row.first
    
        #    puts "@servidor[:cd_servidor]  --> #{@servidor[:cd_servidor].first}, #{@servidor[:cd_servidor].first.class}"
        #    puts "cd_cargo_servidor       --> #{max_cd_cargo_servidor}, #{max_cd_cargo_servidor.class}"
    
        #SE O @servidor NÃO TEM CARGO NA BASE E TEM CARGO NA FITA ENTÃO INSERIR:
        if (@servidor[:cd_servidor].first == nil) or (max_cd_cargo_servidor == nil)
        #      puts "    Inserindo cargo por razao de inexistencia na base...."
          puts "cd_grupo_cargo_fita                 ---> #{cd_grupo_cargo_fita}"
          puts "@servidor[:classe]                   ---> #{@servidor[:classe]}"
          puts "@servidor[:referencia_nivel_padrao]  ---> #{@servidor[:referencia_nivel_padrao]}"
          puts "data_entrada_cargo_formatada        ---> #{formata_data(@servidor[:data_entrada_cargo])}"
          puts "data_saida_cargo_formatada          ---> #{formata_data(@servidor[:data_saida_cargo])}"
          dbh.query("INSERT INTO crp_cargo_servidor (CD_GRUPO_CARGO,
                                                      cd_servidor,
                                                      CD_CLASSE,
                                                      CD_NIVEL,
                                                      DT_INGRESSO_CARGO,
                                                      DT_SAIDA_CARGO)
                                                      values ('#{cd_grupo_cargo_fita}',
                                                              #{@servidor[:cd_servidor]},
                                                              '#{@servidor[:classe]}',
                                                              '#{@servidor[:referencia_nivel_padrao]}',
                                                              '#{formata_data(@servidor[:data_entrada_cargo])}',
                                                              '#{formata_data(@servidor[:data_saida_cargo])}')")
    
        elsif (max_cd_cargo_servidor != nil)
    
          cd_grupo_cargo_banco = dbh.query("SELECT cd_grupo_cargo FROM corp.crp_cargo_servidor
                                            WHERE cd_cargo_servidor ='#{max_cd_cargo_servidor}'").fetch_row.first
          cd_cargo_classe_banco = dbh.query("SELECT cd_classe FROM crp_cargo_servidor
                                             WHERE cd_cargo_servidor ='#{max_cd_cargo_servidor}'").fetch_row.first
          cd_nivel_cargo_banco = dbh.query("SELECT cd_nivel FROM crp_cargo_servidor
                                            WHERE cd_cargo_servidor ='#{max_cd_cargo_servidor}'").fetch_row.first
          data_ingresso_cargo_banco = dbh.query("SELECT dt_ingresso_cargo FROM crp_cargo_servidor
                                                 WHERE cd_cargo_servidor ='#{max_cd_cargo_servidor}'").fetch_row.first
          data_saida_cargo_banco =  dbh.query("SELECT dt_saida_cargo FROM crp_cargo_servidor
                                               WHERE cd_cargo_servidor ='#{max_cd_cargo_servidor}'").fetch_row.first
    
        #      puts "  cd_grupo_cargo_fita X banco            --> #{cd_grupo_cargo_fita},#{cd_grupo_cargo_fita.class} X #{cd_grupo_cargo_banco},#{cd_grupo_cargo_banco.class}"
        #      puts "  @servidor[:classe] X banco              --> #{@servidor[:classe]},#{@servidor[:classe].class} X #{cd_cargo_classe_banco},#{cd_cargo_classe_banco.class}"
        #      puts "  @servidor[:referencia_nivel_padrao]X bco--> #{@servidor[:referencia_nivel_padrao]},#{@servidor[:referencia_nivel_padrao].class} X #{cd_nivel_cargo_banco},#{cd_nivel_cargo_banco.class}"
        #      puts "  Data de entrada do cargo X banco       --> #{data_entrada_cargo_formatada},#{data_entrada_cargo_formatada.class} X #{data_ingresso_cargo_banco},#{data_ingresso_cargo_banco.class}"
        #      puts "  Data de saida do cargo X banco         --> #{data_saida_cargo_formatada},#{data_saida_cargo_formatada.class} X #{data_saida_cargo_banco},#{data_saida_cargo_banco.class}"
        
        #SE O CÓDIGO DO GRUPO+CARGO FOR DIFERENTE NA FITA E NO BANCO ENTÃO *ATUALIZE O ULTIMO DO BANCO* E INSIRA O NOVO
          if (cd_grupo_cargo_fita.to_s != cd_grupo_cargo_banco.to_s)
        #puts "    Inserindo cargo com grupo diferente na fita e na base..."
            dbh.query("INSERT INTO crp_cargo_servidor (CD_GRUPO_CARGO,
                                                        cd_servidor,
                                                        CD_CLASSE,
                                                        CD_NIVEL,
                                                        DT_INGRESSO_CARGO,
                                                        DT_SAIDA_CARGO)
                                                        values ('#{cd_grupo_cargo_fita}',
                                                                '#{@servidor[:cd_servidor]}',
                                                                '#{@servidor[:classe]}',
                                                                '#{@servidor[:referencia_nivel_padrao]}',
                                                                '#{formata_data(@servidor[:data_entrada_cargo])}',
                                                                '#{formata_data(@servidor[:data_saida_cargo])}')")
    
          elsif ((data_ingresso_cargo_banco != formata_data(@servidor[:data_entrada_cargo])) or
                (cd_nivel_cargo_banco       != @servidor[:referencia_nivel_padrao].to_s) or
                (cd_cargo_classe_banco      != @servidor[:classe].to_s) or
                (data_saida_cargo_fita      != nil))
        #puts "    Atualizando cargo por razao de diferenca de valores na fita e na base..."
          data_saida_cargo_fita = '0000-00-00' unless data_saida_cargo_fita != nil
          dbh.query("UPDATE crp_cargo_servidor SET CD_GRUPO_CARGO='#{cd_grupo_cargo_fita}',
                                                        CD_CLASSE='#{@servidor[:classe]}',
                                                        CD_NIVEL='#{@servidor[:referencia_nivel_padrao]}',
                                                        DT_INGRESSO_CARGO='#{formata_data(@servidor[:data_entrada_cargo])}',
                                                        DT_SAIDA_CARGO='#{data_saida_cargo_fita}',
                                                        cd_servidor='#{@servidor[:cd_servidor]}'
                                                        WHERE CD_CARGO_servidor='#{max_cd_cargo_servidor}'")
          else
        #puts "    Nao ha atualizacoes no cargo."
          end
        end
      end
  
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Cargo Servidor   #############################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Função Servidor    ##################################################################
###################################################################################################################################

      #se o @servidor possuir função no banco sem data de saída e na fita não existir
      #relato sobre funções, então o método vai verificar exclusão do @servidor e atua-
      #lizar a saída da função com a entrada da ocorrência de exclusão
      
      #Verifica a existencia das funções
      @servidor[:codigo_nivel] != '00000' ? tem_funcao_fita = true : tem_funcao_fita = false
      @servidor[:codigoNivelNovaFuncao] != '00000'? tem_nova_funcao_fita = true : tem_nova_funcao_fita = false
      #Caso tenha função na fita, formata as datas e pega os valores da funcao da fita
      if tem_funcao_fita
        data_saida_funcao_fita = formata_data(@servidor[:dataSaidaFuncao])
        #Verifica se tem data de saída na fita
        @servidor[:dataSaidaFuncao] == '00000000' ? data_saida_fita = nil : data_saida_fita = data_saida_funcao_fita
        #pega id da função
        cd_funcao = dbh.query("SELECT cd_funcao FROM crp_funcao 
                               WHERE cd_nivel =#{@servidor[:codigo_nivel]} 
                               AND sg_funcao ='#{@servidor[:funcao]}'").fetch_row.first
        (cd_funcao != nil) ? (cd_funcao = cd_funcao.first) : (cd_funcao = nil)
        #pega o id da uorg na fita
        id_uorg_fita = @servidor[:unidadeOrganizacionalFuncao]  
        #Verifica dados da funcao no banco para inserir ou etc
        #puts "cd_funcao              --> #{cd_funcao}"
        #puts "@servidor[:cd_servidor] --> #{@servidor[:cd_servidor]}"
        #puts "data_ingresso_fita     --> #{data_ingresso_fita}"
        #puts "id_uorg_fita           --> #{id_uorg_fita}"
        #NÃO EXISTE O MÉTODO FIRST PARA NilClass
        cd_funcao_servidor = dbh.query("SELECT cd_funcao_servidor FROM corp.crp_funcao_servidor WHERE cd_servidor ='#{@servidor[:cd_servidor]}' and
                                                                                                      cd_funcao ='#{cd_funcao}' and
                                                                                                      dt_ingresso_funcao ='#{formata_data(@servidor[:dataIngressoFuncao])}' and
                                                                                                      cd_unidade_organiz ='#{id_uorg_fita}'").fetch_row
        #puts "cd_funcao_servidor --> #{cd_funcao_servidor.class}"
        cd_funcao_servidor ? precisa_inserir_funcao_no_banco = false : precisa_inserir_funcao_no_banco = true

      #Caso não tenha função na fita, verifica registro da data de saída da função(data de exclusão)  
      else
        #Verifica se possui ocorrencia de exclusão na fita
        if @servidor[:dataOcorrenciaExclu] != "00000000"
          tem_ocorrencia_exclusao = true
          data_exclusao = formata_data(@servidor[:dataOcorrenciaExclu])
        else
          tem_ocorrencia_exclusao = false
        end
        #Atualiza com data de exclusão a última função
        if tem_ocorrencia_exclusao && @servidor[:dataSaidaFuncao] == '00000000'
          dbh.query("UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO='#{data_exclusao}'
                                                WHERE cd_servidor=#{@servidor[:cd_servidor]} and
                                                (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)")
        end    
      end
      
      #Caso haja registro de nova função na fita, extrai-se os dados de ingresso e saída e a unidade organizacional referente à nova função
      if tem_nova_funcao_fita

        data_ingresso_nova_funcao_fita = formata_data(@servidor[:dataIngressoNovaFuncao])
        
        if @servidor[:dataSaidaNovaFuncao] == '00000000'
#          data_saida_nova_funcao_fita = nil
           data_saida_nova_funcao_fita = '0000-00-00'
        else
          data_saida_nova_funcao_fita = formata_data(@servidor[:dataSaidaNovaFuncao])
        end
        cd_nova_funcao =  dbh.query("SELECT cd_funcao FROM crp_funcao 
                                     WHERE cd_nivel ='#{@servidor[:codigoNivelNovaFuncao]}'
                                     AND sg_funcao ='#{@servidor[:siglaNovaFuncao]}'").fetch_row#.first
        id_uorg_nova_funcao_fita = @servidor[:unidadeOrganizacionalNovaFuncao]

        cd_nova_funcao_servidor = dbh.query("SELECT cd_funcao_servidor FROM corp.crp_funcao_servidor 
                                             WHERE cd_servidor =#{@servidor[:cd_servidor]} 
                                             AND cd_funcao ='#{cd_nova_funcao}' 
                                             AND dt_ingresso_funcao ='#{data_ingresso_nova_funcao_fita}'
                                             AND cd_unidade_organiz ='#{id_uorg_nova_funcao_fita}'").fetch_row
        
        #Se existe chave de nova função, não precisa inserir nova função no banco. A recíproca é verdadeira.
        cd_nova_funcao_servidor ? precisa_inserir_nova_funcao_no_banco = false : precisa_inserir_nova_funcao_no_banco = true
      end
      
      #verifica se a data de saida é menor que...
      # (data_saida_funcao_fita != '0000-00-00' and (data_saida_funcao_fita < '2011-01-01') ? funcao_data_anterior_2011 = true : funcao_data_anterior_2011 = false
      if data_saida_funcao_fita != '0000-00-00' and data_saida_funcao_fita != nil
        if data_saida_funcao_fita < '2011-01-01'
          funcao_data_anterior_2011 = true
        end
      else
        funcao_data_anterior_2011 = false
      end
      #Verifica se tem um campo nulo no banco
      ##PRESTAR ATENÇÃO PARA O VERIFICAR DA DATA DE INGRESSO, POIS NÃO PRECISA SER EXATAMENTE A DATA DE INGRESSO, PODE SER UM CAMPO NULO
      funcao_atual = dbh.query("SELECT cd_funcao_servidor FROM crp_funcao_servidor
                                WHERE cd_servidor =#{@servidor[:cd_servidor]} and
                                (dt_saida_funcao is null or dt_saida_funcao = 0000-00-00)").fetch_row
      if !funcao_atual.nil?
        funcao_atual = funcao_atual.first
        esta_em_uma_funcao = true
        data_entrada_funcao_atual = dbh.query("SELECT dt_ingresso_funcao FROM crp_funcao_servidor 
                                               WHERE cd_servidor = #{@servidor[:cd_servidor]} AND
                                               (dt_saida_funcao is null or dt_saida_funcao = 0000-00-00)").fetch_row.first
      else
        esta_em_uma_funcao = false
      end

      #puts "precisa_inserir_funcao_no_banco"
      #puts precisa_inserir_funcao_no_banco
 
      if precisa_inserir_funcao_no_banco == true
        #puts "esta_em_uma_funcao"
        #puts esta_em_uma_funcao
        if esta_em_uma_funcao == true
          #puts "funcao_data_anterior_2011"
          #puts funcao_data_anterior_2011
          if funcao_data_anterior_2011 == true
            #ATUALIZAÇÃO PARA CASOS ANTERIORES A 2011-01-01 E COM DATA DE SAIDA PREENCHIDA NA FUNÇÃO
            #A DATA DE SAIDA PRECISA ESTAR PREENCHIDA SENÃO CAIRA NO ELSE DO PROXIMO IF, QUE
            #ATUALIZA A SAIDA COM DATA 2011-01-01, POIS A FITA VEM COM O REGISTRO DA FUNÇÃO APENAS COM
            # A UORG ALTERADA, COMO SE O @servidor SEMPRE ESTIVESSE ESTADO NAQUELA FUNÇÃO
            #puts "FUNCAO NA FITA COM ENTRADA ANTERIOR A 2011 E COM REGISTRO DE SAIDA"
            dbh.query("UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO='#{data_saida_funcao_fita}'
                                                      WHERE cd_servidor=#{@servidor[:cd_servidor]} and
                                                      DT_INGRESSO_FUNCAO='#{formata_data(@servidor[:dataIngressoFuncao])}' and
                                                      (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)")
          else
            #ATUALIZAÇÃO PARA CASOS EM QUE A ENTRADA ATUAL NO BANCO É MAIOR OU IGUAL A 2011-01-01
            #SIGNIFICA QUE JÁ ESTÁ REGISTRADA A MUDANÇA DE ESTRUTURA DE UORG
            if data_entrada_funcao_atual >= "2011-01-01"
              #A MAIORIA DOS CASOS ESTÁ NESSA CONDIÇÃO
              #puts "CASO COMUM"
              dbh.query("UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO= '#{formata_data(@servidor[:dataIngressoFuncao])}'
                                                        WHERE CD_FUNCAO_servidor= #{funcao_atual} and
                                                        (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)")

            else
              #SENÃO CAI NO CASO DE TRANSIÇÃO DE ESTRUTURA DE UNIDADE ORGANIZACIONAL 2010/12 --> 2011/01
              #A SAIDA É ATUALIZADA COM DATA DE '2011-01-01'
              #puts "CASO DE TRANSICAO DE UORG"
              dbh.query("UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO = '2011-01-01'
                                                          WHERE CD_FUNCAO_servidor=#{funcao_atual} and
                                                          (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)")
            end
          end
        end
        #puts "INSERINDO FUNCAO @servidor"
        dbh.query("INSERT INTO crp_funcao_servidor (cd_servidor,
                                                    CD_UNIDADE_ORGANIZ,
                                                    CD_FUNCAO,
                                                    DT_INGRESSO_FUNCAO,
                                                    DT_SAIDA_FUNCAO) values (#{@servidor[:cd_servidor]},
                                                                              '#{@servidor[:unidadeOrganizacionalFuncao]}',
                                                                              #{cd_funcao},
                                                                              '#{formata_data(@servidor[:dataIngressoFuncao])}',
                                                                              '#{data_saida_funcao_fita}')")
      else
        #ESTE SENÃO CONCLUI QUE NÃO HÁ RAZÕES LÓGICAS PARA INSERÇÃO DE UM REGISTRO DE HISTORICO
        #dbh.query("UPDATE crp_funcao_servidor SET CD_FUNCAO= '#{cd_funcao}',
        #                                          DT_INGRESSO_FUNCAO='#{formata_data(@servidor[:dataIngressoFuncao])}',
        #                                          DT_SAIDA_FUNCAO='#{data_saida_funcao_fita}'
        #                                          WHERE CD_FUNCAO_servidor='#{funcao_atual}'")
        dbh.query("UPDATE crp_funcao_servidor SET CD_FUNCAO= '#{cd_funcao}',
                                                  DT_INGRESSO_FUNCAO='#{formata_data(@servidor[:dataIngressoFuncao])}',
                                                  DT_SAIDA_FUNCAO='#{data_saida_funcao_fita}'
                                                  WHERE CD_FUNCAO_servidor='#{cd_funcao_servidor}'")
      end
      
      #verifica se a data de saida é menor que...
      data_saida_nova_funcao_fita && data_saida_nova_funcao_fita < '2011-01-01' ? funcao_nova_data_anterior_2011 = true : funcao_nova_data_anterior_2011 = false
      #verifica se tem um campo nulo no banco
      cd_nova_funcao_servidor = dbh.query("SELECT cd_funcao_servidor FROM crp_funcao_servidor
                                           WHERE cd_servidor =#{@servidor[:cd_servidor]} AND dt_ingresso_funcao ='#{data_ingresso_nova_funcao_fita}' and
                                          (dt_saida_funcao is null or dt_saida_funcao = 0000-00-00)").fetch_row
      if cd_nova_funcao_servidor
        esta_em_uma_nova_funcao = true
        cd_nova_funcao_servidor = cd_nova_funcao_servidor.first
        dt_ingresso_funcao_nova_banco = dbh.query("SELECT dt_ingresso_funcao FROM crp_funcao_servidor
                                             WHERE cd_servidor =#{@servidor[:cd_servidor]} AND
                                             (dt_saida_funcao is null or dt_saida_funcao = 0000-00-00)").fetch_row.first
      else
        esta_em_uma_nova_funcao = false
      end
      
      #puts "precisa_inserir_nova_funcao_no_banco -------> #{precisa_inserir_nova_funcao_no_banco}"
      
      if precisa_inserir_nova_funcao_no_banco
        #puts "esta_em_uma_nova_funcao -------> #{esta_em_uma_nova_funcao}"
        if esta_em_uma_nova_funcao
          #puts "funcao_nova_data_anterior_2011 -------> #{funcao_nova_data_anterior_2011}"
          if funcao_nova_data_anterior_2011
      #puts "FUNCAO NOVA NA FITA COM ENTRADA ANTERIOR A 2011 E COM REGISTRO DE SAIDA"
            dbh.query("UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO='#{data_saida_nova_funcao_fita}'
                                                  WHERE cd_servidor='#{@servidor[:cd_servidor]}'
                                                  AND DT_INGRESSO_FUNCAO='#{data_ingresso_nova_funcao_fita}'
                                                  AND (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)")
          else
            if dt_ingresso_funcao_nova_banco >= '2011-01-01'
              #puts "FUNCAO NOVA CASO COMUM"
              dbh.query("UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO='#{data_ingresso_nova_funcao_fita}'
                                                    WHERE CD_FUNCAO_servidor='#{cd_nova_funcao_servidor}'
                                                    AND (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)")
            else
              #puts "FUNCAO NOVA CASO DE TRANSICAO DE UORG"
              dbh.query("UPDATE crp_funcao_servidor SET DT_SAIDA_FUNCAO = '2011-01-01'
                                                    WHERE CD_FUNCAO_servidor='#{cd_nova_funcao_servidor}'
                                                    AND (DT_SAIDA_FUNCAO is null or DT_SAIDA_FUNCAO = 0000-00-00)")
            end
          end
        end
        #puts "INSERINDO NOVA FUNCAO"
      
      puts data_saida_nova_funcao_fita
      dbh.query("INSERT INTO crp_funcao_servidor (cd_servidor,
                                                    CD_UNIDADE_ORGANIZ,
                                                    CD_FUNCAO,
                                                    DT_INGRESSO_FUNCAO,
                                                    DT_SAIDA_FUNCAO) values ('#{@servidor[:cd_servidor]}',
                                                                             '#{@servidor[:unidadeOrganizacionalNovaFuncao]}',
                                                                             '#{cd_nova_funcao}',
                                                                             '#{data_ingresso_nova_funcao_fita}',
                                                                             '#{data_saida_nova_funcao_fita}')")
      else #Se não precisa inserir nova função no banco
        #puts "Sem muitas alteracoes, atualizando nova funcao encontrada..."
        dbh.query("UPDATE crp_funcao_servidor SET CD_FUNCAO='#{cd_nova_funcao}',
                                                  DT_INGRESSO_FUNCAO='#{data_ingresso_nova_funcao_fita}',
                                                  DT_SAIDA_FUNCAO='#{data_saida_nova_funcao_fita}'
                                                  WHERE CD_FUNCAO_servidor='#{cd_nova_funcao_servidor}'")
      end
  
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Função Servidor   ############################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza UORG Servidor   #####################################################################
###################################################################################################################################

      #verifica que função vem na fita
      @servidor[:codigo_nivel] != "00000"? tem_funcao_fita = true : tem_funcao_fita = false
      @servidor[:codigoNivelNovaFuncao] != "00000"? tem_nova_funcao_fita = true : tem_nova_funcao_fita = false

      # armazena dados da fita
      # caso a data de entrada na lotacao seja nula ele vai pegar a saida da maior funcao que existir
      if (@servidor[:dataLotacao] == "00000000") and (@servidor[:dataSaidaNovaFuncao] != "00000000")
        data_lotacao_fita = formata_data(@servidor[:dataSaidaNovaFuncao])
      elsif (@servidor[:dataLotacao] == "00000000") and (@servidor[:dataSaidaFuncao] != "00000000")
        data_lotacao_fita = formata_data(@servidor[:dataSaidaFuncao])
      elsif (@servidor[:dataLotacao] == "00000000") and (@servidor[:dataOcoInatividade] != "00000000")
        data_lotacao_fita = formata_data(@servidor[:dataOcoInatividade])
      elsif (@servidor[:dataLotacao] != "00000000")
        data_lotacao_fita = formata_data(@servidor[:dataLotacao])
      else
        data_lotacao_fita = formata_data(@servidor[:dataIngressoOrgao])
      end

      if @servidor[:codigo_lotacao] == "000000000"
        uorg_lotacao_fita = @servidor[:unidadeOrganizacionalLocalizacao]
      else
        uorg_lotacao_fita = @servidor[:codigo_lotacao]
      end

      #so usa a lotacao se não existirem funções ou estarem com data de saida preenchida
      if tem_nova_funcao_fita
        uorg_nova_funcao_fita = @servidor[:unidadeOrganizacionalNovaFuncao]
        data_ingresso_nova_funcao_fita = formata_data(@servidor[:dataIngressoNovaFuncao])
        data_saida_nova_funcao_fita = formata_data(@servidor[:dataSaidaNovaFuncao])
        data_saida_nova_funcao_fita == "0000-00-00" ? usar_lotacao = false : usar_lotacao = true
      else #Caso não tenha nova função fita
        if tem_funcao_fita
          uorg_funcao_fita =@servidor[:unidadeOrganizacionalFuncao]
          data_ingresso_funcao_fita = formata_data(@servidor[:dataIngressoFuncao])
          data_saida_funcao_fita = formata_data(@servidor[:dataSaidaFuncao])
          data_saida_funcao_fita == "0000-00-00" ? usar_lotacao = false : usar_lotacao = true
        else
          usar_lotacao = true
        end
      end

      
      #se não tiver que usar lotação(pois há, função ou nova função)
      if !usar_lotacao

      #verifica uorg da nova funcao no historico do banco
        if tem_nova_funcao_fita
          cd_hist_uorg_nova_funcao_banco = dbh.query("SELECT Max(cd_unidade_organiz_hist)
                                                      FROM corp.crp_unidade_organizacional_hist 
                                                      WHERE cd_pessoa_fisica ='#{@servidor[:cd_servidor]}'
                                                      AND cd_unidade_organiz ='#{uorg_nova_funcao_fita}'
                                                      AND dt_ingresso_lotacao ='#{data_ingresso_nova_funcao_fita}'").fetch_row
           
          if cd_hist_uorg_nova_funcao_banco.first.nil?
            tem_hist_uorg_nova_funcao_banco = false 
          else
            cd_hist_uorg_nova_funcao_banco = cd_hist_uorg_nova_funcao_banco.first
            tem_hist_uorg_nova_funcao_banco = true
          end
          tem_hist_uorg_nova_funcao_banco ? precisa_inserir_uorg_nova_funcao_fita = false : precisa_inserir_uorg_nova_funcao_fita = true
        else #caso não tenha nova funcao fita
          precisa_inserir_uorg_nova_funcao_fita = false
        end
                     
      #verifica uorg da funcao no historico do banco
        if tem_funcao_fita and data_saida_funcao_fita == "0000-00-00"
           cd_hist_uorg_funcao_banco = dbh.query("SELECT Max(cd_unidade_organiz_hist)
                                                 FROM corp.crp_unidade_organizacional_hist 
                                                 WHERE cd_pessoa_fisica ='#{@servidor[:cd_servidor]}'
                                                 AND cd_unidade_organiz ='#{uorg_funcao_fita}'
                                                 AND dt_ingresso_lotacao ='#{data_ingresso_funcao_fita}'").fetch_row
          if cd_hist_uorg_funcao_banco.first.nil?
              tem_hist_uorg_funcao_banco = false
          else
              tem_hist_uorg_funcao_banco = true
              cd_hist_uorg_funcao_banco = cd_hist_uorg_funcao_banco.first
          end
           tem_hist_uorg_funcao_banco ? precisa_inserir_uorg_funcao_fita = false : precisa_inserir_uorg_funcao_fita = true    
        else
          precisa_inserir_uorg_funcao_fita = false
          precisa_inserir_uorg_lotacao_fita = true
        end
        
      #se não tiver função e nova função utiliza a lotação(que sempre vai existir)
      else #usar_lotacao == true
        cd_hist_uorg_lotacao_banco = dbh.query("SELECT Max(cd_unidade_organiz_hist)
                                                FROM corp.crp_unidade_organizacional_hist 
                                                WHERE cd_pessoa_fisica ='#{@servidor[:cd_servidor]}'
                                                AND (dt_saida_lotacao is null or dt_saida_lotacao= 0000-00-00)").fetch_row
        if cd_hist_uorg_lotacao_banco.first.nil?
            tem_hist_uorg_lotacao_banco = false
        else
            tem_hist_uorg_lotacao_banco = true
            cd_hist_uorg_lotacao_banco = cd_hist_uorg_lotacao_banco.first
        end
        if tem_hist_uorg_lotacao_banco
            data_ingresso_lotacao_banco = dbh.query("SELECT dt_ingresso_lotacao
                                                     FROM corp.crp_unidade_organizacional_hist 
                                                     WHERE cd_pessoa_fisica =#{@servidor[:cd_servidor]}
                                                     AND (dt_saida_lotacao is null or dt_saida_lotacao= 0000-00-00)").fetch_row.first
             data_lotacao_fita <= data_ingresso_lotacao_banco ? precisa_inserir_uorg_lotacao_fita = false : precisa_inserir_uorg_lotacao_fita = true            
        else #caso nao tenha hist_uorg_lotacao_banco
            precisa_inserir_uorg_lotacao_fita = true
        end
      end

      cd_unidade_atual = dbh.query("SELECT Max(cd_unidade_organiz_hist) from crp_unidade_organizacional_hist
                        WHERE cd_pessoa_fisica =#{@servidor[:cd_servidor]} and (dt_saida_lotacao is null or dt_saida_lotacao= 0000-00-00)").fetch_row
      if !cd_unidade_atual.nil?
        cd_unidade_atual = cd_unidade_atual.first
        
        uorg_unidade_atual = dbh.query("SELECT cd_unidade_organiz from crp_unidade_organizacional_hist
                                        WHERE cd_pessoa_fisica ='#{@servidor[:cd_servidor]}'
                                        AND (dt_saida_lotacao is null or dt_saida_lotacao = 0000-00-00)").fetch_row
        uorg_unidade_atual = uorg_unidade_atual.first unless uorg_unidade_atual.nil?

        dt_ingresso_atual = dbh.query("SELECT dt_ingresso_lotacao from crp_unidade_organizacional_hist
                                       WHERE cd_pessoa_fisica ='#{@servidor[:cd_servidor]}'
                                       AND (dt_saida_lotacao is null or dt_saida_lotacao = 0000-00-00)").fetch_row
        dt_ingresso_atual = dt_ingresso_atual.first unless dt_ingresso_atual.nil?

        cd_unidade_atual.nil? ? tem_campo_na_base = false : tem_campo_na_base = true

        dt_ingresso_atual.nil? ? tem_entrada_na_base = false : tem_entrada_na_base = true

        if (uorg_unidade_atual.nil?) or (uorg_unidade_atual == '') or (uorg_unidade_atual == "000000000")
            tem_uorg_na_base = false
        else
            tem_uorg_na_base = true
        end
      else
      #  puts "nao tem nada la"
      end

      #  puts "usar_lotacao                      ----->#{usar_lotacao}"
      if usar_lotacao == true
      #    puts "precisa_inserir_uorg_lotacao_fita -----> #{precisa_inserir_uorg_lotacao_fita}"
        if precisa_inserir_uorg_lotacao_fita == true
      #   puts "tem_campo_na_base ---------------------> #{tem_campo_na_base }"
          if tem_campo_na_base == true
            #\/\/ esse if é utilizado para campos na base que possuem uorg e data zerados
            if (tem_uorg_na_base == false) and (tem_entrada_na_base == false)
      #        puts "tem_uorg_na_base == false, tem_entrada_na_base == false"
      #        puts "LOTACAO: ATUALIZANDO ULTIMA UORG COM DADOS NORMAIS DA FITA..."
              nao_inserir_uorg_nova = true
              dbh.query("UPDATE crp_unidade_organizacional_hist SET CD_UNIDADE_ORGANIZ='#{uorg_lotacao_fita}',
                                                                       DT_INGRESSO_LOTACAO='#{data_lotacao_fita}'
                                                                       WHERE CD_UNIDADE_ORGANIZ_HIST='#{cd_unidade_atual}'")
            else
              nao_inserir_uorg_nova = false
      #       se a data de entrada do banco for igual a da fita, e as uorgs diferentes significa que
      #       essa atualização surgiu da mudança de codigo de uorg então ele vai inserir data de 2011-01-01
              if (dt_ingresso_atual == data_lotacao_fita) and (uorg_unidade_atual != uorg_lotacao_fita)
      #          puts "dt_ingresso_atual == data_lotacao_fita and uorg_unidade_atual != uorg_lotacao_fita"
      #          puts "LOTACAO: ATUALIZANDO ULTIMA UNIDADE COM DATA DE SAIDA 2011-01-01"
                dbh.query("UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO='2011-01-01' 
                                                                       WHERE CD_UNIDADE_ORGANIZ_HIST='#{cd_unidade_atual}'")
              else
      #          puts "dt_ingresso_atual != data_lotacao_fita or uorg_unidade_atual == uorg_lotacao_fita"
      #          puts "LOTACAO: ATUALIZANDO ULTIMA UNIDADE COM DATA DE SAIDA NORMAL DA FITA"
                dbh.query("UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO='#{data_lotacao_fita}'
                                                                       WHERE CD_UNIDADE_ORGANIZ_HIST='#{cd_unidade_atual}'")
              end
            end
          else
            nao_inserir_uorg_nova = false
          end
      #    puts "nao_inserir_uorg_nova -----> #{nao_inserir_uorg_nova}"
          if nao_inserir_uorg_nova == false
            if (dt_ingresso_atual == data_lotacao_fita) and (uorg_unidade_atual != uorg_lotacao_fita)
      #        puts "dt_ingresso_atual == data_lotacao_fita and uorg_unidade_atual != uorg_lotacao_fita"
      #        puts "LOTACAO: INSERINDO UNIDADE COM DATA DE ENTRADA DE 2011-01-01"
              dbh.query("INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                     CD_UNIDADE_ORGANIZ,
                                                                     DT_INGRESSO_LOTACAO)
                                                                     values ('#{@servidor[:cd_servidor]}',
                                                                             '#{uorg_lotacao_fita}',
                                                                             '2011-01-01')")
            else
      #        puts "dt_ingresso_atual != data_lotacao_fita or uorg_unidade_atual == uorg_lotacao_fita"
      #        puts "LOTACAO: INSERINDO UNIDADE COM DATA DE ENTRADA NORMAL"
              dbh.query("INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                       CD_UNIDADE_ORGANIZ,
                                                                       DT_INGRESSO_LOTACAO)
                                                                       values ('#{@servidor[:cd_servidor]}',
                                                                               '#{uorg_lotacao_fita}',
                                                                               '#{data_lotacao_fita}')")
            end
          end
        else
      #    puts "LOTACAO: ATUALIZANDO ULTIMA UNIDADE POIS NAO PRECISA INSERIR NADA"
      #    if dt_ingresso_atual != '2011-01-01'
      #      dbh.query("UPDATE crp_unidade_organizacional_hist SET CD_UNIDADE_ORGANIZ ='#{uorg_lotacao_fita}',
      #                                                            DT_INGRESSO_LOTACAO='#{data_lotacao_fita}'
      #                                                            WHERE CD_UNIDADE_ORGANIZ_HIST=#{cd_unidade_atual}")
      #    end
        end
      end

      #insere no banco funcao
      #  puts "tem_funcao_fita -----> #{tem_funcao_fita}"
      if (tem_funcao_fita == true) and (usar_lotacao == false)
      #  puts "tem_funcao_fita == true and usar_lotacao == false"
      #  puts "precisa_inserir_uorg_funcao_fita -----> #{precisa_inserir_uorg_funcao_fita}"
      #  puts "precisa_inserir_uorg_nova_funcao_fita ----->  #{precisa_inserir_uorg_nova_funcao_fita}"
        if (precisa_inserir_uorg_funcao_fita == true) and (precisa_inserir_uorg_nova_funcao_fita == true)
      #    puts "precisa_inserir_uorg_funcao_fita == true and precisa_inserir_uorg_nova_funcao_fita == true"
          #verifica se existe aquela unidade já inserida com data de saida nula
          verifica_uorg_funcao_saida_nula = dbh.query("SELECT Max(cd_unidade_organiz_hist) FROM crp_unidade_organizacional_hist
                                                     WHERE cd_pessoa_fisica ='#{@servidor[:cd_servidor]}'
                                                     AND cd_unidade_organiz ='#{uorg_funcao_fita}'
                                                     AND (dt_saida_lotacao is null or dt_saida_lotacao = 0000-00-00)").fetch_row
          verifica_uorg_funcao_saida_nula.nil? ? (existe_uorg_funcao_saida_nula = false) : (existe_uorg_funcao_saida_nula = true)
          if !existe_uorg_funcao_saida_nula
      #puts "nao existe_uorg_funcao_saida_nula -----> #{existe_uorg_funcao_saida_nula}"
      #puts "FUNCAO: INSERINDO DADOS COMPLETOS DE UORG FUNCAO POIS TEM TAMBÉM NOVA FUNCAO"
            dbh.query("INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                     CD_UNIDADE_ORGANIZ,
                                                                     DT_INGRESSO_LOTACAO,
                                                                     DT_SAIDA_LOTACAO)
                                                                     values ('#{@servidor[:cd_servidor]}',
                                                                             '#{uorg_funcao_fita}',
                                                                             '#{data_ingresso_funcao_fita}',
                                                                             '#{data_saida_funcao_fita}'")
          end
        elsif (precisa_inserir_uorg_funcao_fita == true) and (precisa_inserir_uorg_nova_funcao_fita == false)
      #    puts "precisa_inserir_uorg_funcao_fita == true and precisa_inserir_uorg_nova_funcao_fita == false"
          verifica_uorg_funcao_saida_nula2 = dbh.query("SELECT cd_unidade_organiz_hist FROM crp_unidade_organizacional_hist
                                                        WHERE cd_pessoa_fisica ='#{@servidor[:cd_servidor]}'
                                                        AND cd_unidade_organiz ='#{uorg_funcao_fita}'
                                                        AND (dt_saida_lotacao is null or dt_saida_lotacao = '0000-00-00')").fetch_row
    
      #    puts "verifica_uorg_funcao_saida_nula2.nil? ------>#{verifica_uorg_funcao_saida_nula2.nil?}"
          verifica_uorg_funcao_saida_nula2.nil? ? (existe_uorg_funcao_saida_nula2 = false) : (existe_uorg_funcao_saida_nula2 = true)
      #    puts "existe_uorg_funcao_saida_nula2 ------> #{existe_uorg_funcao_saida_nula2}"
          if !existe_uorg_funcao_saida_nula2
      #se tem campo na base  e nao tem entrada e a saida da função na fita é nula: significa que a pessoa só mudou de uorg em 2011-01-01
      #puts "/n /n /n /n /n"
      #puts "tem_campo_na_base - #{tem_campo_na_base}"
      #puts "dt_ingresso_atual - #{dt_ingresso_atual}"
      #puts "@servidor[:dataSaidaFuncao - #{@servidor[:dataSaidaFuncao]}"
            if ((tem_campo_na_base == true) and 
               ((dt_ingresso_atual == nil) or (dt_ingresso_atual == "0000-00-00")) and
               (@servidor[:dataSaidaFuncao] == "00000000"))
      #       if (tem_campo_na_base == true) and (dt_ingresso_atual == nil) and (@servidor[:dataSaidaFuncao] == "00000000")
      #atualiza a data de saida do ultimo historico com a data de entrada do @servidor na função caso a saída seja nula
      #          puts "(tem_campo_na_base == true) and (dt_ingresso_atual == nil) and (@servidor[:dataSaidaFuncao] == '00000000')"
      #          puts "ATUALIZANDO ULTIMA UORG COM FUNCAO E COM DATA DE SAIDA 2011-01-01"
              dbh.query("UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO='2011-01-01',
                                                              DT_INGRESSO_LOTACAO='#{data_ingresso_funcao_fita}'
                                                              WHERE CD_UNIDADE_ORGANIZ_HIST='#{cd_unidade_atual}'")
            else
      #          puts "ATUALIZANDO FUNCAO COM DATA NORMAL"
              dbh.query("UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO='#{data_ingresso_funcao_fita}'
                                                                WHERE CD_UNIDADE_ORGANIZ_HIST='#{cd_unidade_atual}'")
            end
      #puts "FUNCAO: INSERINDO DADOS COMPLETOS DE UORG DE FUNCAO SEM SAIDA"
            dbh.query("INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                    CD_UNIDADE_ORGANIZ,
                                                                    DT_INGRESSO_LOTACAO)
                                                                    values ('#{@servidor[:cd_servidor]}',
                                                                            '#{uorg_funcao_fita}',
                                                                            '#{data_ingresso_funcao_fita}')")
            
          end
        else
        end
      end
    
      #  puts "tem_nova_funcao_fita"
      if (tem_nova_funcao_fita == true) and (usar_lotacao == false)
      #se precisa inserir, pois nao achou uorg igual nem entrada igual:
        if precisa_inserir_uorg_nova_funcao_fita == true
    
          verifica_uorg_funcao_saida_nula3 = dbh.query("SELECT cd_unidade_organiz_hist FROM crp_unidade_organizacional_hist
                    WHERE cd_pessoa_fisica =#{@servidor[:cd_servidor]}
                    AND cd_unidade_organiz ='#{uorg_nova_funcao_fita}'
                    AND (dt_saida_lotacao is null or dt_saida_lotacao = '0000-00-00')").fetch_row
          verifica_uorg_funcao_saida_nula3.nil? ? (existe_uorg_funcao_saida_nula3 = false) : (existe_uorg_funcao_saida_nula3 = true)
          if !existe_uorg_funcao_saida_nula3
            if tem_campo_na_base == true
      #atualiza a data de saida do ultimo historico com a data de entrada do @servidor na nova função caso a saída seja nula
      #          puts "ATUALIZANDO ULTIMA UORG COM DATA DA NOVA FUNCAO"
              dbh.query("UPDATE crp_unidade_organizacional_hist SET DT_SAIDA_LOTACAO=#'{data_ingresso_nova_funcao_fita}'
                                                          WHERE CD_UNIDADE_ORGANIZ_HIST=#{cd_unidade_atual}")
            end
      #puts "INSERINDO UORG DA NOVA FUNCAO"
            dbh.query("INSERT INTO crp_unidade_organizacional_hist (CD_PESSOA_FISICA,
                                                                     CD_UNIDADE_ORGANIZ,
                                                                     DT_INGRESSO_LOTACAO)
                                                                     values ('#{@servidor[:cd_servidor]}',
                                                                             '#{uorg_nova_funcao_fita}',
                                                                             '#{data_ingresso_nova_funcao_fita}')")
          end
        else
      #      puts "NAO PRECISA INSERIR NOVA FUNCAO"
        end
      end

###################################################################################################################################
#######################    Fim de Insere ou Atualiza UORG Servidor   ##############################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Ocorrência Ingresso Serviço Público   ###############################################
###################################################################################################################################
      
      #  puts "    OCORRENCIA INGRESSO SERVICO"
      if @servidor[:grupoIngreServPublico] != "00"
        
      #    puts "    CONFIRMADO OCORRENCIA DE INGRESSO NO SERVICO PUBLICO." + @servidor[:nome]
         
        data_ingresso_servico_publico_formatada = formata_data(@servidor[:dataIngreServPublico])
        data_diploma_legal_servico_publico_formatada = formata_data(@servidor[:dataDipLegalIngreServPublico])
        
        id_ocorrencia_ingresso_servico = dbh.query("SELECT cd_ocorrencia FROM crp_ocorrencia 
                                                    WHERE cd_servidor=#{@servidor[:cd_servidor]} 
                                                    AND cd_tipo_ocorrencia=1").fetch_row
    
        if id_ocorrencia_ingresso_servico != nil
          id_ocorrencia_ingresso_servico = id_ocorrencia_ingresso_servico.first
          
      #      puts "    Atualizando ocorrencias de ingresso no servico publico..."
          dbh.query("UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=1,
                                           CD_GRUPO='#{@servidor[:gurpoIngreServPublico]}',
                                           NO_OCORRENCIA='#{@servidor[:ocorrenciaingreServPublico]}',
                                           DT_OCORRENCIA='#{data_ingresso_servico_publico_formatada}',
                                           CD_DIPLOMA_LEGAL='#{@servidor[:codDipLegalIngreServPublico]}',
                                           NO_DIPLOMA_LEGAL='#{@servidor[:numDipLegalIngreServPublico]}',
                                           DT_PUBLICACAO='#{data_diploma_legal_servico_publico_formatada}',
                                           cd_servidor='#{@servidor[:cd_servidor]}'
                                           WHERE CD_OCORRENCIA='#{id_ocorrencia_ingresso_servico}'")
        else
      #      puts "    Inserindo ocorrencias de ingresso nos serviço publico..."
          dbh.query("INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                 cd_servidor,
                                                 CD_GRUPO,
                                                 NO_OCORRENCIA,
                                                 DT_OCORRENCIA,
                                                 CD_DIPLOMA_LEGAL,
                                                 NO_DIPLOMA_LEGAL,
                                                 DT_PUBLICACAO) values (1,
                                                                        '#{@servidor[:cd_servidor]}',
                                                                        '#{@servidor[:grupoIngreServPublico]}',
                                                                        '#{@servidor[:ocorrenciaIngreServPublico]}',
                                                                        '#{data_ingresso_servico_publico_formatada}',
                                                                        '#{@servidor[:codDipLegalIngreServPublico]}',
                                                                        '#{@servidor[:numDipLegalIngreServPublico]}',
                                                                        '#{data_diploma_legal_servico_publico_formatada}')")
        end
      end
     
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Ocorrência Ingresso Serviço Público   ########################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Ocorrência Ingresso Órgão   #########################################################
###################################################################################################################################

      #  puts "    OCORRENCIA INGRESSO ORGAO"
      
      if @servidor[:grupoIngressoOrgao] != "00"
      #    puts "    CONFIRMADO OCORRENCIA DE INGRESSO NO ORGAO." + @servidor[:nome]
        data_ingresso_orgao_formatada = formata_data(@servidor[:dataIngressoOrgao])
        data_diploma_legal_formatada = formata_data(@servidor[:dataPublicacaoDiplomaLegal])
        
        id_ocorrencia_ingresso_orgao = dbh.query("SELECT cd_ocorrencia FROM crp_ocorrencia WHERE cd_servidor=#{@servidor[:cd_servidor]} and cd_tipo_ocorrencia=2").fetch_row
        
        if id_ocorrencia_ingresso_orgao != nil
            id_ocorrencia_ingresso_orgao = id_ocorrencia_ingresso_orgao.first
            
      #puts "    Atualizando ocorrencias de ingresso no orgao..."
            dbh.query("UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=2,
                                                 CD_GRUPO='#{@servidor[:grupoIngressoOrgao]}',
                                                 NO_OCORRENCIA='#{@servidor[:ocorrenciaIngressoOrgao]}',
                                                 DT_OCORRENCIA='#{data_ingresso_orgao_formatada}',
                                                 CD_DIPLOMA_LEGAL='#{@servidor[:codigoDiplomaLegal]}',
                                                 NO_DIPLOMA_LEGAL='#{@servidor[:numeroDiplomaLegal]}',
                                                 DT_PUBLICACAO='#{data_diploma_legal_formatada}',
                                                 cd_servidor='#{@servidor[:cd_servidor]}'
                                             WHERE CD_OCORRENCIA='#{id_ocorrencia_ingresso_orgao}'")
        else
      #puts "Inserindo ocorrencias de ingresso no orgao..."

        dbh.query("INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                   cd_servidor,
                                                   CD_GRUPO,
                                                   NO_OCORRENCIA,
                                                   DT_OCORRENCIA,
                                                   CD_DIPLOMA_LEGAL,
                                                   NO_DIPLOMA_LEGAL,
                                                   DT_PUBLICACAO) values (2,
                                                                          '#{@servidor[:cd_servidor]}',
                                                                          '#{@servidor[:grupoIngressoOrgao]}',
                                                                          '#{@servidor[:ocorrenciaIngressoOrgao]}',
                                                                          '#{data_ingresso_orgao_formatada}',
                                                                          '#{@servidor[:codigoDiplomaLegal].strip}',
                                                                          '#{@servidor[:numeroDiplomaLegal]}',
                                                                          '#{data_diploma_legal_formatada}')")
        end
      end
    
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Ocorrência Ingresso Órgão   ##################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Ocorrência Exclusão   ###############################################################
###################################################################################################################################

      #  puts "    OCORRENCIA EXCLUSAO"
      if @servidor[:grupoOcorrenciaExclu] != "00"
      #    puts "    CONFIRMADO OCORRENCIA DE EXCLUSAO" + @servidor[:nome]
        data_exclusao_orgao_formatada = formata_data(@servidor[:dataOcorrenciaExclu])
        data_diploma_exclusao_legal_formatada = formata_data(@servidor[:dataDipLegalOcorrenciaExclu])
        id_ocorrencia_exclusao_servico = dbh.query("SELECT cd_ocorrencia FROM crp_ocorrencia 
                                                    WHERE cd_servidor=#{@servidor[:cd_servidor]} 
                                                    AND cd_tipo_ocorrencia=3").fetch_row
        if id_ocorrencia_exclusao_servico != nil:
          id_ocorrencia_exclusao_servico = id_ocorrencia_exclusao_servico.first
          dbh.query("UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=3,
                                               CD_GRUPO='#{@servidor[:grupoOcorrenciaExclu]}',
                                               NO_OCORRENCIA='#{@servidor[:ocorrenciaExclu]}',
                                               DT_OCORRENCIA='#{data_exclusao_orgao_formatada}',
                                               CD_DIPLOMA_LEGAL='#{@servidor[:codDipLegalOcorrenciaExclu]}',
                                               NO_DIPLOMA_LEGAL='#{@servidor[:numDipLegalOcorrenciaExclu]}',
                                               DT_PUBLICACAO='#{data_diploma_exclusao_legal_formatada}',
                                               cd_servidor='#{@servidor[:cd_servidor]}'
                                           WHERE cd_ocorrencia='#{id_ocorrencia_exclusao_servico}'")
        else
      #      puts "Inserindo ocorrencias de exclusao do @servidor..." + @servidor[:nome]
          dbh.query("INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                 cd_servidor,CD_GRUPO,
                                                 NO_OCORRENCIA,
                                                 DT_OCORRENCIA,
                                                 CD_DIPLOMA_LEGAL,
                                                 NO_DIPLOMA_LEGAL,
                                                 DT_PUBLICACAO) values (3,
                                                                        '#{@servidor[:cd_servidor]}',
                                                                        '#{@servidor[:grupoOcorrenciaExclu]}',
                                                                        '#{@servidor[:ocorreciaExclu]}',
                                                                        '#{data_exclusao_orgao_formatada}',
                                                                        '#{@servidor[:codDipLegalOcorrenciaExclu]}',
                                                                        '#{@servidor[:numDipLegalOcorrenciaExclu]}',
                                                                        '#{data_diploma_exclusao_legal_formatada}')")
        end
      end

###################################################################################################################################
#######################    Fim de Insere ou Atualiza Ocorrência Exclusão   ########################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Ocorrência Afastamento   ############################################################
###################################################################################################################################

      #  puts "    OCORRENCIA AFASTAMENTO"
      if @servidor[:grupoOcoAfastamento] != "00"
      #    puts "    CONFIRMADO OCORRENCIA DE AFASTAMENTO NO SERVICO PUBLICO." + @servidor[:nome]
          
        data_ocorrencia_afastamento_formatada = formata_data(@servidor[:dataInicioOcoAfastamento])
        data_diploma_afastamento_formatada = formata_data(@servidor[:dataDipLegalOcoAfastamento])
         
        id_ocorrencia_afastamento = dbh.query("SELECT cd_ocorrencia FROM crp_ocorrencia 
                                               WHERE cd_servidor=#{@servidor[:cd_servidor]} 
                                               AND cd_tipo_ocorrencia=4").fetch_row
                                               
        if id_ocorrencia_afastamento != nil
            id_ocorrencia_afastamento = id_ocorrencia_afastamento.first
      puts "    Atualizando ocorrencias de afastamento no orgao..."
            dbh.query("UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=4,
                                                 CD_GRUPO='#{@servidor[:grupoOcoAfastamento]}',
                                                 NO_OCORRENCIA='#{@servidor[:ocorrenciaAfastamento]}',
                                                 DT_OCORRENCIA='#{data_ocorrencia_afastamento_formatada}',
                                                 CD_DIPLOMA_LEGAL='#{@servidor[:codDipLegalOcoAfastamento]}',
                                                 NO_DIPLOMA_LEGAL='#{@servidor[:numDipLegalOcoAfastamento]}',
                                                 DT_PUBLICACAO='#{data_diploma_afastamento_formatada}',
                                                 cd_servidor='#{@servidor[:cd_servidor]}'
                                                 WHERE CD_OCORRENCIA='#{id_ocorrencia_afastamento}'")
        else
      puts "    Inserindo ocorrencias de afastamento do @servidor..."
            dbh.query("INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                   cd_servidor,
                                                   CD_GRUPO,
                                                   NO_OCORRENCIA,
                                                   DT_OCORRENCIA,
                                                   CD_DIPLOMA_LEGAL,
                                                   NO_DIPLOMA_LEGAL,
                                                   DT_PUBLICACAO) values (4,
                                                                          '#{@servidor[:cd_servidor]}',
                                                                          '#{@servidor[:grupoOcoAfastamento]}',
                                                                          '#{@servidor[:ocorrenciaAfastamento]}',
                                                                          '#{data_ocorrencia_afastamento_formatada}',
                                                                          '#{@servidor[:codDipLegalOcoAfastamento]}',
                                                                          '#{@servidor[:numDipLegalOcoAfastamento]}',
                                                                          '#{data_diploma_afastamento_formatada}')")
        end
      end

###################################################################################################################################
#######################    Fim de Insere ou Atualiza Ocorrência Afastamento   #####################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Ocorrência Inatividade   ############################################################
###################################################################################################################################

      #  puts "    OCORRENCIA INATIVIDADE"
      
      if @servidor[:grupoOcoInatividade] != "00"
      #    puts "    CONFIRMADO OCORRENCIA DE INATIVIDADE NO SERVICO PUBLICO." + @servidor[:nome]
        data_ocorrencia_inatividade_formatada = formata_data(@servidor[:dataOcoInatividade])
        data_diploma_inatividade_formatada = formata_data(@servidor[:dataDipLegalOcoInatividade])
        id_ocorrencia_inatividade = dbh.query("SELECT cd_ocorrencia FROM crp_ocorrencia 
                                               WHERE cd_servidor=#{@servidor[:cd_servidor]} 
                                               AND cd_tipo_ocorrencia=5").fetch_row
        if id_ocorrencia_inatividade != nil
          id_ocorrencia_inatividade = id_ocorrencia_inatividade.first
      #      puts "    Atualizando ocorrencias de inatividade..."
          dbh.query("UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=5,
                                               CD_GRUPO='#{@servidor[:grupoOcoInatividade]}',
                                               NO_OCORRENCIA='#{@servidor[:ocorrenciaInatividade]}',
                                               DT_OCORRENCIA='#{data_ocorrencia_inatividade_formatada}',
                                               CD_DIPLOMA_LEGAL='#{@servidor[:codDipLegalOcoInatividade]}',
                                               NO_DIPLOMA_LEGAL='#{@servidor[:numDipLegalOcoInatividade]}',
                                               DT_PUBLICACAO='#{data_diploma_inatividade_formatada}',
                                               cd_servidor='#{@servidor[:cd_servidor]}'
                                           WHERE CD_OCORRENCIA='#{id_ocorrencia_inatividade}'")
        else
      #      puts "    Inserindo ocorrencias de inatividade do @servidor..."
          dbh.query("INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                 cd_servidor,
                                                 CD_GRUPO,
                                                 NO_OCORRENCIA,
                                                 DT_OCORRENCIA,
                                                 CD_DIPLOMA_LEGAL,
                                                 NO_DIPLOMA_LEGAL,
                                                 DT_PUBLICACAO) values (5,
                                                                        '#{@servidor[:cd_servidor]}',
                                                                        '#{@servidor[:grupoOcoInatividade]}',
                                                                        '#{@servidor[:ocorrenciaInatividade]}',
                                                                        '#{data_ocorrencia_inatividade_formatada}',
                                                                        '#{@servidor[:codDipLegalOcoInatividade]}',
                                                                        '#{@servidor[:numDipLegalOcoInatividade]}',
                                                                        '#{data_diploma_inatividade_formatada}')")
        end
      end
    
###################################################################################################################################
#######################    Fim de Insere ou Atualiza Ocorrência Inatividade   #####################################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Ocorrência Modificação Funcional   ##################################################
###################################################################################################################################

      #  puts "    OCORRENCIA MODIFICACAO FUNCIONAL"
      
      if @servidor[:grupoOcoModFuncional] != "00"
        data_ocorrencia_modificacao_funcional_formatada = formata_data(@servidor[:dataOcoModFuncional])
        data_diploma_modificacao_funcional_formatada = formata_data(@servidor[:dataDipLegalOcoModFuncional])
        id_ocorrencia_modificacao_funcional = dbh.query("SELECT cd_ocorrencia FROM crp_ocorrencia 
                                                         WHERE cd_servidor=#{@servidor[:cd_servidor]} and cd_tipo_ocorrencia=6").fetch_row
        if id_ocorrencia_modificacao_funcional != nil
          id_ocorrencia_modificacao_funcional = id_ocorrencia_modificacao_funcional.first
      #      puts "Atualizando ocorrencias de inatividade..."
          dbh.query("UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=6,
                                               CD_GRUPO='#{@servidor[:grupoOcoModFuncional]}',
                                               NO_OCORRENCIA='#{@servidor[:ocorrenciaModFuncional]}',
                                               DT_OCORRENCIA='#{data_ocorrencia_modificacao_funcional_formatada}',
                                               CD_DIPLOMA_LEGAL='#{@servidor[:codDipLegalOcoModFuncional]}',
                                               NO_DIPLOMA_LEGAL='#{@servidor[:numDipLegalOcoModFuncional]}',
                                               DT_PUBLICACAO='#{data_diploma_modificacao_funcional_formatada}',
                                               cd_servidor='#{@servidor[:cd_servidor]}'
                                           WHERE CD_OCORRENCIA='#{id_ocorrencia_modificacao_funcional}'")
        else
      #      puts "    Inserindo ocorrencias de inatividade do @servidor..."
          dbh.query("INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                 cd_servidor,
                                                 CD_GRUPO,
                                                 NO_OCORRENCIA,
                                                 DT_OCORRENCIA,
                                                 CD_DIPLOMA_LEGAL,
                                                 NO_DIPLOMA_LEGAL,
                                                 DT_PUBLICACAO) values (6,
                                                                        '#{@servidor[:cd_servidor]}',
                                                                        '#{@servidor[:grupoOcoModFuncional]}',
                                                                        '#{@servidor[:ocorrenciaModFuncional]}',
                                                                        '#{data_ocorrencia_modificacao_funcional_formatada}',
                                                                        '#{@servidor[:codDipLegalOcoModFuncional]}',
                                                                        '#{@servidor[:numDipLegalOcoModFuncional]}',
                                                                        '#{data_diploma_modificacao_funcional_formatada}')")
        end
      end

###################################################################################################################################
#######################    Fim de Insere ou Atualiza Ocorrência Modificação Funcional   ###########################################
###################################################################################################################################

###################################################################################################################################
#######################    Insere ou Atualiza Ocorrência Aposentadoria   ##########################################################
###################################################################################################################################

      #  puts "    OCORRENCIA APOSENTADORIA"
      if (@servidor[:numProcOcoAposentadoria] == "               ") or (@servidor[:numProcOcoAposentadoria] == "000000000000000")
        nao_tem_aposentadoria_fita = true
      else
        nao_tem_aposentadoria_fita = false
      end
      
      if !nao_tem_aposentadoria_fita
        zeros = '0000'
        data_publicacao_ocorrencia_aposentadoria = "00000000"
        ano_aposentadoria = zeros + @servidor[:anoPrevOcoAposentadoria]
        data_ocorrencia_aposentadoria_formatada = formata_data(ano_aposentadoria)
        data_publicacao_ocorrencia_aposentadoria_formatada = formata_data(data_publicacao_ocorrencia_aposentadoria)
        
        id_ocorrencia_aposentadoria =dbh.query("SELECT cd_ocorrencia FROM crp_ocorrencia 
                                                WHERE cd_servidor=#{@servidor[:cd_servidor]} and cd_tipo_ocorrencia=7").fetch_row
        
        if id_ocorrencia_aposentadoria != nil
          id_ocorrencia_aposentadoria = id_ocorrencia_aposentadoria.first
      #      puts "    Atualizando ocorrencias de aposentadoria..."
          dbh.query("UPDATE crp_ocorrencia SET CD_TIPO_OCORRENCIA=7,
                                               CD_GRUPO='#{@servidor[:numProcOcoAposentadoria]}',
                                               NO_OCORRENCIA='#{@servidor[:opcaoIntOcoAposentadoria]}',
                                               DT_OCORRENCIA='#{data_ocorrencia_aposentadoria_formatada}',
                                               cd_servidor='#{@servidor[:cd_servidor]}',
                                               DT_PUBLICACAO='#{data_publicacao_ocorrencia_aposentadoria_formatada}'
                                           WHERE CD_OCORRENCIA='#{id_ocorrencia_aposentadoria}'")
        else
      #      puts "Inserindo ocorrencias de aposentadoria do @servidor..."
          dbh.query("INSERT INTO crp_ocorrencia (CD_TIPO_OCORRENCIA,
                                                 cd_servidor,
                                                 CD_GRUPO,
                                                 NO_OCORRENCIA,
                                                 DT_OCORRENCIA,
                                                 CD_DIPLOMA_LEGAL,
                                                 NO_DIPLOMA_LEGAL,
                                                 DT_PUBLICACAO) values (7,
                                                                        '#{@servidor[:cd_servidor]}',
                                                                        '#{@servidor[:numProcOcoAposentadoria]}',
                                                                        '#{@servidor[:opcaoIntOcoAposentadoria]}',
                                                                        '#{data_ocorrencia_aposentadoria_formatada}',
                                                                        0,
                                                                        0,
                                                                        '#{data_publicacao_ocorrencia_aposentadoria_formatada}')")
        end
      end

###################################################################################################################################
#######################    Fim de Insere ou Atualiza Ocorrência Aposentadoria   ###################################################
###################################################################################################################################

  end #--FIM DO CASE E EXTRAÇÃO DE DADOS
end #-- Fim da leitura do arquivo


### Funções a serem implementadas ###
#
#   @servidor[:insert_or_update_historico_funcao_servidor
#   @servidor[:insert_or_update_historico_uorg_servidor
#   @servidor[:insert_or_update_ocorrencia_ingresso_servico_publico
#   @servidor[:insert_or_update_ocorrencia_ingresso_orgao
#   @servidor[:insert_or_update_ocorrencia_exclusao
#   @servidor[:insert_or_update_ocorrencia_afastamento
#   @servidor[:insert_or_update_ocorrencia_inatividade
#   @servidor[:insert_or_update_ocorrencia_modificacao_funcional
#   @servidor[:insert_or_update_ocorrencia_aposentadoria
