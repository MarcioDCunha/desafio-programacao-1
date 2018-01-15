require "rubygems"
require "csv"
require "mysql"

caminho_da_fita = Dir.pwd.concat("/public/data/FITA_ESPELHO_FERIAS.TXT")

fita_espelho = open(caminho_da_fita, 'r')

#dbh = Mysql.real_connect("localhost","root","admin","corp")
dbh = Mysql.real_connect("172.19.0.43","crp","crp123","corp")#
#dbh = Mysql.real_connect("172.16.85.17","crp","crp123","corp")

def formata_data(data)

  dia = data.slice(0,2)
  mes = data.slice(2,3)
  ano = data.slice(5,4)

  case mes
  when 'JAN'
    mes_nm = '01'
  when 'FEV'
    mes_nm = '02'
  when 'MAR'
    mes_nm = '03'
  when 'ABR'
    mes_nm = '04'
  when 'MAI'
    mes_nm = '05'
  when 'JUN'
    mes_nm = '06'
  when 'JUL'
    mes_nm = '07'
  when 'AGO'
    mes_nm = '08'
  when 'SET'
    mes_nm = '09'
  when 'OUT'
    mes_nm = '10'
  when 'NOV'
    mes_nm = '11'
  when 'DEZ'
    mes_nm = '12'

  end

  data_formatada = "#{ano}-#{mes_nm}-#{dia}"
  return data_formatada
end

#puts fita_espelho.methods.sort
#puts fita_espelho.class

@hoje = Time.now.strftime("%Y-%m-%d")

arquivo = fita_espelho.readlines

arquivo.shift

arquivo.each do |linha|
  nome = ""
  letra = 0
  for i in 8..60

    if linha[i..i].between?('A','z') or (linha[i..i] == " ") or (linha[i..i] == "\t")
      nome.concat(linha[i..i])
      letra += 1
    end
    if linha[i..i].between?('0','9')
      break
    end
  end

  n = letra+7

  @dados_ferias = {
    :matricula => "#{ linha[0...7] }",
    :nome      => "#{ linha[8...n] }",
    :ano       => "#{ linha[n+1...n+5] }",
    :inicio    => "#{ linha[n+6...n+15] }",
    :fim       => "#{ linha[n+16...n+25] }",
    :parcela   => "#{ linha[n+26...n+27] }"
  }

 puts "Matricula: #{@dados_ferias[:matricula]}"
 puts "#{@dados_ferias[:nome]} "
 puts "Inicio: #{formata_data(@dados_ferias[:inicio])}"
 puts "Fim: #{formata_data(@dados_ferias[:fim])} "
 puts "Ano: #{@dados_ferias[:ano]}"
 puts "Parcela: #{@dados_ferias[:parcela]}"

  data_inicio = formata_data(@dados_ferias[:inicio])
  data_fim    = formata_data(@dados_ferias[:fim])

  #Verifica se o Servidor Público está na base e qual seu Id.
  cd_servidor = dbh.query("SELECT cd_servidor from crp_servidor where CD_MATRIC_SIAPE=#{@dados_ferias[:matricula]}").fetch_row

  puts "Id: #{cd_servidor} - Matricula: #{@dados_ferias[:matricula]} - Nome: #{@dados_ferias[:nome]}\n"
  puts "Inicio: #{formata_data(@dados_ferias[:inicio])} - Fim: #{formata_data(@dados_ferias[:fim])}\n"
  puts "Ano: #{@dados_ferias[:ano]} - Parcela: #{@dados_ferias[:parcela]}\n"

  #Verifica se o registro já está na Tabela "crp_circunstancia"
  cadastro = dbh.query("SELECT cd_circunstancia
                                        from crp_circunstancia
                                        where CD_PESSOA_FISICA = #{cd_servidor}
                                        and CD_TIPO_CIRCUNSTANCIA = 169
                                        and DT_ENTRADA_CIRCUNSTANCIA = '#{data_inicio}'
                                        and DT_SAIDA_CIRCUNSTANCIA = '#{data_fim}'
                                        and ANO_EXEC = #{@dados_ferias[:ano]}
                                        and PARCELA = #{@dados_ferias[:parcela]}
                                        and DT_CANCELAMENTO is null
    ").fetch_row
  cadastro != nil ? registro_existe = true : registro_existe = false
  #Inicia a inserção dos dados no bando de dados

  puts "Registro Existe? #{registro_existe}"

  if registro_existe == false
    #Se não for encontrado, verifica se há algo parecido
    parecido = dbh.query("SELECT cd_circunstancia
                          from crp_circunstancia
                          where CD_PESSOA_FISICA = #{cd_servidor}
                          and CD_TIPO_CIRCUNSTANCIA = 169
                          and (('#{data_inicio}' BETWEEN dt_entrada_circunstancia AND dt_saida_circunstancia) or ('#{data_fim}' BETWEEN dt_entrada_circunstancia AND dt_saida_circunstancia))
                          and DT_CANCELAMENTO is null
                         ").fetch_row

    parecido != nil ? existe_parecido = true : existe_parecido = false

    puts "Existe Parecido? #{existe_parecido}\n"

    if existe_parecido == true
      puts "Parecido : #{parecido}"

      id_parecido = parecido.first
      puts "id_parecido : #{id_parecido}"

      
      puts "===  Cancelando! #{@dados_ferias[:nome]}\n"

      dbh.query("UPDATE crp_circunstancia
                 SET DT_CANCELAMENTO = '#{@hoje}',
                     DT_INCLUSAO = '#{@hoje}'
                 WHERE CD_CIRCUNSTANCIA = #{id_parecido}")

    end

      puts "===  Inserindo #{@dados_ferias[:nome]}\n"
      dbh.query("INSERT INTO crp_circunstancia (CD_PESSOA_FISICA,
                                                CD_TIPO_CIRCUNSTANCIA,
                                                DT_ENTRADA_CIRCUNSTANCIA,
                                                DT_SAIDA_CIRCUNSTANCIA,
                                                ANO_EXEC,
                                                PARCELA,
                                                DT_INCLUSAO) values (#{cd_servidor},
                                                                      169,
                                                                    '#{data_inicio}',
                                                                    '#{data_fim}',
                                                                    '#{@dados_ferias[:ano]}',
                                                                    '#{@dados_ferias[:parcela]}',
                                                                    '#{@hoje}')")


  end
  puts "-------------------------------------------------------------------------"
end
