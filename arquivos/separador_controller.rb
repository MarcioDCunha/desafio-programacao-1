#=begin
require 'rubygems'
require 'csv'
require 'mysql2'

caminho_da_fita = Dir.pwd.sub("/app/controllers","").concat("/arquivos/INPUT_DE_DADOS.TXT")
fita_espelho = open(caminho_da_fita, 'r')
puts "CAMINHO DA FITA: #{caminho_da_fita}"
#dbh = Mysql.real_connect("localhost","root","root","teste_development")
#dbh = mysql.init
#dbh.real_connect 'localhost', 'root', 'root', 'teste_development', '3306', nil, nil


#------------------------------------------------------------------------------------------------

def formata_data(data)
  data_formatada = data.slice(4,4) + "-" + data.slice(2,2) + "-" + data.slice(0,2)
  return data_formatada
end

### Inicio da leitura do arquivo

fita_espelho.each_line do |linha|

  case linha[0...9]  # Na 1ª linha
    when 'purchaser'
    
    else
      #Dados do arquivo.txt
      @vt1 = "#{ linha[0...80] }"
      puts "@vt1: #{@vt1}"
      #@vt2 = "#{ @vt1.split(/	/).slice(0..6) }"
      #puts "@vt2: #{@vt2}"
      @venda = {
        :purchaser_name => "#{@vt1.split('	').first}",              :purchaser_count => "#{@vt1.split(/	/).slice(1..-1)[0]}",    
        :item_description => "#{@vt1.split(/	/).slice(1..-1)[1]}",    :item_price => "#{@vt1.split(/	/).slice(1..-1)[2]}",
        :merchant_name => "#{@vt1.split(/	/).slice(1..-1)[3]}",    :merchant_address => "#{@vt1.split('	').last}"
         }
     puts "\n"
    puts ":linha_toda => #{@venda[:linha_toda]} \n"
    puts ":purchaser_name => #{@venda[:purchaser_name]}      :purchaser_count => #{@venda[:purchaser_count] } \n"
    puts ":item_description => #{@venda[:item_description]}  :item_price => #{@venda[:item_price] } \n"
    puts ":merchant_name => #{ @venda[:merchant_name]}       :merchant_address => #{ @venda[:merchant_address] } \n \n"


      #Verifica se a @venda estï¿½ na base.

      @venda[:n] = dbh.query("SELECT id from purchasers where purchaser_name=#{@venda[:purchaser_name]} and 
      purchaser_count=#{@venda[:purchaser_count]} and item_description=#{@venda[:item_description]} and 
      item_price=#{@venda[:item_price]} and merchant_name=#{@venda[:merchant_name]} ").fetch_row
      @venda[:n] != nil ? @venda[:ja_existente] = true : @venda[:ja_existente] = false
      
      
      ###Inicio da insercao dos dados no bando de dados


   if servidor[:ja_existente] == false
    puts "Inserindo #{venda[:purchaser_name]}\n"
    dbh.query("INSERT INTO purchasers (purchaser_name,
                                       purchaser_count,
                                       item_description,
                                       item_price,
                                       merchant_name,
                                       merchant_address,
				       created_at,
                                       updated_at) values (#{venda[:purchaser_name]},
                                                      '#{venda[:purchaser_count]}',
                                                      '#{venda[:item_description]}',
                                                      '#{venda[:item_price]}',
                                                      '#{venda[:merchant_name]}',
                                                      '#{venda[:merchant_address]}',
                                                      '#{data_formatada}',
                                                       #{data_formatada})")

      end
    end
end

