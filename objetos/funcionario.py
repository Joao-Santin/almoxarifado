class Funcionario:
  def __init__(self, nome, telefone, camisa, calca, blusa, sapato):
    self.nome = nome
    self.telefone = telefone
    self.camisa = camisa
    self.calca = calca
    self.blusa = blusa
    self.sapato = sapato

  def json(self):
    dicionario = {
      "nome": self.nome,
      "telefone": self.telefone,
      "camisa": self.camisa,
      "calca": self.calca,
      "blusa": self.blusa,
      "sapato": self.sapato
    }
    return dicionario
