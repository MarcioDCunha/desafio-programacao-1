Rails.application.routes.draw do
  root to: 'arquivos#index'
  get 'arquivos/index'
  post 'arquivos/upload_arquivo'
  post 'arquivos/download_arquivo'

#root to: 'extrator#index'
  #get 'extrator/index'
  #post 'extrator/index'

  resources :purchasers
  resources :extrator

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
