class ExtratorController < ApplicationController

  def index

    if system("ruby #{Rails.root}/arquivos/separador_controller.rb")
      puts "Banco Atualizado com Sucesso!"
    else
      puts "Erro na atualizacao! Tente novamente."
    end

   redirect_to :controller => "purchasers", :action => :index
  end


end
