class ArquivosController < ApplicationController

  def index
    @arquivos = Arquivo.order(id: :desc)
  end

  def upload_arquivo
    @arquivo = Arquivo.new
    Arquivo.upload_arquivo(params[:arquivo], "#{Rails.root}/arquivos")
    @arquivo.save

    redirect_to controller: :extrator, action: :index
    
  end

  def download_arquivo
    Arquivo.download_arquivo(params[:diretorio])
    send_file params[:diretorio]+'.zip'
  end

end