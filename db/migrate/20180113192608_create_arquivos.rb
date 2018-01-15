class CreateArquivos < ActiveRecord::Migration[5.1]
  def change
    create_table :arquivos do |t|

      t.timestamps
    end
  end
end
