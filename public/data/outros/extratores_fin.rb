require 'csv'
require 'mysql'
#require 'os'

dbh = Mysql.real_connect("localhost","root","admin","financeiro")

if RUBY_PLATFORM.downcase.include?("darwin")
	plataforma = "mac"
elsif
	RUBY_PLATFORM.downcase.include?("windows")		
		plataforma = "windows"
else
	plataforma = "linux"
end

if plataforma == "linux"
	caminho_da_fita = Dir.pwd.concat("/FITA_ESPELHO.TXT")
end

fita_espelho = open(caminho_da_fita, 'r')
#puts fita_espelho.methods.sort
fita_espelho.each_line do |servidor|
        # Dados Financeiros...
if servidor[17...18] == '1'
	@nome = servidor[20...80].strip
end

if servidor[17...18] == '3'
	#Nao inclui dados do beneficiario
	matricula_siape = servidor[9...16]
	#Dados da Rubrica
	rendimento = servidor[20...21]
	codigo = servidor[21...26]
	sequencia = servidor[26...27]
	valor = servidor[27...38]
	prazo = servidor[38...41]
	#Parametrizacao Rubrica
	percentual = servidor[41...46]
	#Fracao
	numerador = servidor[46...49]
	denominador = servidor[49...52]
	#Nivel Salarial
	sist_clsf_nsal = servidor[54...55]
	nsal_cemp_funcao = servidor[55...67]

	puts "DADOS FINANCEIROS"
	puts "..........MATRICULA SIAPE"
	puts "........................" + matricula_siape.to_s
	puts "........................" + @nome.to_s
	#puts "rendimento"
	#puts rendimento
	#puts "codigo"
	#puts codigo
	#puts "sequencia"
	#puts sequencia
	#puts "valor"
	#puts valor
	#puts "prazo"
	#puts prazo
	#puts "percentual"
	#puts percentual
	#puts "numerador"
	#puts numerador
	#puts "denominador"
	#puts denominador	
	#puts "sist_clsf_nsal"
	#puts sist_clsf_nsal
	#puts "nsal_cemp_funcao"
	#puts nsal_cemp_funcao


	procura_dado_financeiro = dbh.query("SELECT MATRICULA FROM financeiro.crp_financeiro WHERE (MATRICULA = #{matricula_siape} and
															 CODIGO = #{codigo} and
															 SEQUENCIA = #{sequencia} and
															 VALOR = #{valor})")
	encontrou_no_banco = procura_dado_financeiro.fetch_row
	if encontrou_no_banco != nil
	puts "................................................VALOR JA EXISTE NO BANCO"

	else

	dbh.query("INSERT INTO financeiro.crp_financeiro (MATRICULA,RENDIMENTO,CODIGO,
								  SEQUENCIA, VALOR, PRAZO, 
								  PERCENTUAL, NUMERADOR, DENOMINADOR,
								  SIST_CLSF_NSAL, NSAL_CEMP_FUNCAO, NOME)
		 VALUES ('#{matricula_siape}','#{rendimento}','#{codigo}',
				'#{sequencia}','#{valor}','#{prazo}','#{percentual}',
				'#{numerador}','#{denominador}','#{sist_clsf_nsal}',
				'#{nsal_cemp_funcao}', '#{@nome}')")
	end
	


end

        # Dados Financeiros, totalização...
if servidor[17...18] == '4'
	
        matricula_siape = servidor[9...16]
	total_bruto = servidor[20...32]
	total_descontos = servidor[32...44]
	liquido = servidor[44...56]
	total_registros_tipo_3 = servidor[56...59]
	
	#puts "TOTALIZACAO FINANCEIRA"
	#puts "total_bruto"
	#puts total_bruto
	#puts "total_descontos"
	#puts total_descontos
	#puts "liquido"
	#puts liquido
	#puts "total_registros_tipo_3"
	#puts total_registros_tipo_3

	procura_total_financeiro = dbh.query("SELECT MATRICULA FROM financeiro.crp_financeiro_total 
								  WHERE ( MATRICULA = #{matricula_siape} and
								      	 TOTAL_BRUTO = #{total_bruto} and
										 TOTAL_DESCONTOS = #{total_descontos} and
										 LIQUIDO = #{liquido} and
										 TOTAL_REGISTROS_3 = #{total_registros_tipo_3})")
	
	encontrou_total_no_banco = procura_total_financeiro.fetch_row
	if encontrou_total_no_banco != nil
	puts "......................................................TOTAL JA EXISTE NO BANCO"

	else

	dbh.query("INSERT INTO financeiro.crp_financeiro_total (MATRICULA,TOTAL_BRUTO,
								  TOTAL_DESCONTOS, LIQUIDO, TOTAL_REGISTROS_3,
								  NOME)
		 VALUES ('#{matricula_siape}','#{total_bruto}','#{total_descontos}',
				'#{liquido}','#{total_registros_tipo_3}', '#{@nome}')")
	end
end
        # Registro Trailler. Quantidades de UPAG's e de servidores no arquivo...
if servidor[17...18] == '9'
            quantidadeServidores = servidor[21...27]
end

end

