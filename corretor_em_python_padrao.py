# Aqui nós abrimos o arquivo e jogamos para dentro da variável "artigos"
with open('artigos.txt', 'r', encoding='UTF8') as f:
  artigos = f.read()
#   No nosso caso, utilizaremos uma biblioteca para facilitar o nosso trabalho de 
# processamento de linguagem natural, a NLTK -> (Natural Language Toolkit),
# para isso precisaremos importar a mesma com o comando baixo

import nltk
nltk.download('punkt')

# Agora usaremos uma função que nos retornará uma lista com os tokens do nosso arquivo de texto:
# Obs: não chamamos a lista com o nome palavras ainda, já que a nossa lista retornada contém
# pontuações, quebras de linha, etc.

tokens = nltk.tokenize.word_tokenize(artigos)

# Se você conhece a linguagem Python, pensará agora, porque ele não usou o método split()
# das strings?
# E a resposta nesse caso é simples. Vamos levar como exemplo o seguinte código:

# input(dados que iriamos digitar):
#   frase_exemplo = 'Olá fulano, tudo bem?'
#   palavras_separadas = frase_exemplo.split()
#   print(palavras_separadas)
# output(saída que teriamos):
#   ['Olá', 'fulano,', 'tudo', 'bem?']

#   Repare que no nosso caso o programa nos retornou a frase separada pelos espaços,
# mas ela trouxe junto todos os caracteres, como por exemplo a "," e o "?". Oque seria
# ruim para treinar nosso algoritmo.

#   E é para salvar a nossa vida que aparece a biblioteca nltk com a função que acabamos de usar
# acima. Vamos executar o mesmo código do que o acima mas com uma função da biblioteca nltk.

# input:
#   frase_exemplo = 'Olá fulano, tudo bem?'
#   palavras_separadas = nltk.tokenize.word_tokenize(frase_exemplo)
#   print(palavras_separadas)
# output:
#   ['Olá', 'fulano', ',', 'tudo', 'bem', '?']

#   Repare que ele retornou os caracteres "não alfabéticos" separados, oque é perfeito para nós,
# agora só precisaremos varrer essa lista verificando oque é uma palavra, e oque não é. Para isso,
# usaremos a função abaixo:

def separa_palavras(lista_de_tokens):
  lista_de_palavras = []
  for token in lista_de_tokens:
    if token.isalpha():
      lista_de_palavras.append(token.lower())

  return lista_de_palavras

#   Oque a função acima faz é o seguinte, ela recebe a nossa lista de tokens, e varre toda ela
# verificando se aquele elemento da nossa lista é "alfabético" ou não. Se a nossa verificação
# der como verdadeiro e o algoritmo indetificar o token como uma palavra válida, ele adiciona
# a uma lista para depois retornar ela no fim da função.
# Sabendo disso, vamos agora executar essa função e vamos retornar ela para uma variável
# chamada de "palavras_separadas". Repare que somente agora é semanticamente válido usar 
# o nome palavras para nossa variável, já que antes nós não tinhamos uma lista de palavras,
# tinhamos na verdade uma lista de tokens por conter pontuações e caracteres "não alfabéticos".
#   Obs: Repare que na função "separa_palavras", quando adicionamos a palavra na lista,
# estamos transformando ela em minúscula para facilitar a verificação do nosso algoritmo no futuro.

palavras_separadas = separa_palavras(tokens)
frequencia = nltk.FreqDist(palavras_separadas)
palavras = set(palavras_separadas)

#   Aqui usamos mais uma função da biblioteca nltk que vai retornar para dentro da nossa variável
# "frequencia", um dicionário contendo todas as palavras do nosso texto com a contagem de
# aparições de cada uma delas.
#   Logo embaixo declaramos a variável "palavras" que recebe uma lista de todas as palavras do nosso
# artigo, mas sem a repetição das mesmas

#   Agora com todos os nossos dados importados e tratados, precisaremos começar toda a lógica por
# trás do nosso algoritmo de correção de texto
#   Primeiro precisaremos pensar, como o nosso corretor vai funcionar?
# O nosso corretor vai tentar corrigir as nossas frases aplicando várias operações nas palavras
# digitadas pelo usuário, como: tirar letras, adicionar, trocar e inverter a posição de letras.
# Para só depois poder calcular a probabilidade de cada uma delas, e retornar como correção a 
# palavra com a maior porcentagem de aparições no nosso arquivo de texto que estamos usando
# como base para testar e verificar as palavras.
#   Vamos começar então pensando em como vamos fazer cada uma dessas operações. Começando pela
# operação de adicionar letras, oque ela irá fazer?
# No nosso caso ela receberá uma tupla com as duas fatias da palavra (direita e esquerda), e irá
# adicionar uma letra no meio das duas fatias, e retornar a nova palavra para quem chamou
# a função "insere_letras()" Então, por exemplo. Vamos supor que o usuário digitou a palavra
# lógica mas por descuido, esqueceu o "g", transformando assim a palavra "lógica" no erro "lóica".
# E as duas fatias recebidas foram as ('ló', 'ica'). A função irá inserir no meio das fatias
# uma letra e fará isso repetidamente para o alfabeto inteiro. Depois retornará uma lista com 
# todas as palavras geradas para ser verificada a frequência de cada uma e retornar como correção
# para o usuário a palavra com maior aparição no texto.

def insere_letras(fatias):
  novas_palavras = []
  letras = 'abcdefghijklmnopqrstuvwxyzàáâãèéêìíîòóôõùúûç'
  for E, D in fatias:
    for letra in letras:
      novas_palavras.append(E + letra + D)
  return novas_palavras

# Agora, vamos criar uma função para verificar todas as fatias possíveis dentro de uma palavra.
# Por exemplo, a palavra lóica, tem vários pontos onde podemos fatiar ela para enviar para a
# nossa função. Podemos fatiar ela em esquerda e direita, tanto no meio da palavra como no final.
# Então vamos criar uma função que vai receber como parâmetro uma palavra, e vai enviar uma
# lista com todas as fatias possíveis da palavra para a função "insere_letras."

def gerador_palavras(palavra):
  fatias = []
  # Loop criador das fatias
  for i in range(len(palavra)+1):
    fatias.append((palavra[:i],palavra[i:]))

  # Chama a função insere_letras e guarda o valor recebido dentro da variável "palavras_geradas"
  palavras_geradas = insere_letras(fatias)
  return palavras_geradas

#   Agora, se chamarmos a função "gerador_palavras", ela vai nos retornar uma lista
# com todas as palavras que a função "insere_letras" gerou.
#   Vamos verificar então se quando chamamos a função "gerador_palavras" com a palavra "lóica"
# como paramêtro, a lista que ela nos retorna contém a palavra "lógica" inserida nela:

# input:
#   lista_palavras_geradas = gerador_palavras('lóica')
#   print('lógica' in lista_palavras_geradas)
# output:
#   True

#   FUNCIONOU!!! Agora precisaremos verificar qual das palavras tem a maior frequência
# para poder corrigir o usuário quando ele digitar algo errado.
#   Para isso, precisaremos criar duas funções. A primeira será uma que receberá como
# parâmetro uma palavra e retornará a sua probabilidade de estar correta (em porcentagem):

def probabilidade(palavra_gerada):
  return frequencia[palavra_gerada]/len(palavras_separadas)

#   E agora, vamos criar mais uma que chamará a função "probabilidade" e escolherá a palavra
# com a maior probabilidade de estar correta.

def corretor(palavra):
  
  palavras_geradas = gerador_palavras(palavra)
  # Retorna a palavra com maior probabilidade para a variável "palavra_correta"
  palavra_correta = max(palavras_geradas, key=probabilidade)

  return palavra_correta

#   Vamos testar a nossa função "corretor" agora?

# Input:
#   palavra_correta = corretor('lóica')
#   print(palavra_correta)
# Output:
#   lógica

#   Agora sim está funcionando, mas e se o nosso usuário digitar errado a palavra "lógiica"
# por exemplo. O nosso algoritmo atual não vai conseguir ainda corrigir esse erro certo? Então, o
# próximo passo vai ser adicionar uma função que vai deletar uma letra, a "deleta_letras".

def deleta_letras(fatias):
  novas_palavras = []
  letras = 'abcdefghijklmnopqrstuvwxyzàáâãèéêìíîòóôõùúûç'
  for E, D in fatias:
    # Ela só concatena com o lado esquerdo, o lado direito a partir do segundo caracter
    novas_palavras.append(E + D[1:])
  return novas_palavras

#   Ela agora segue a mesma estratégia da função "insere_letras", mas dessa vez vai deletar uma.
# agora precisamos adicionar a chamada dela dentro da função "gerador_palavras":

def gerador_palavras(palavra):
  fatias = []
  # Loop criador das fatias
  for i in range(len(palavra)+1):
    fatias.append((palavra[:i],palavra[i:]))

  # Chama a função insere_letras e guarda a lista recebido dentro da variável 
  palavras_geradas = insere_letras(fatias)
  #   Chama a função deleta_letras e junta a lista "palavras_geradas" com a nova lista retornada
  # da função "deleta_letras"
  palavras_geradas += deleta_letras(fatias)

  return palavras_geradas

# Agora vamos testar a nossa nova função "deleta_letras" digitando no corretor a palavra "lógiica":

# Input:
#   palavra_correta = corretor('lógiica')
#   print(palavra_correta)
# Output:
#   lógica

#   Vamos supor novamente um novo erro muito comum. Vamos imaginar que o nosso usuário acabou
# por descuido, digitando a palavra "lúgica" ao invés de "lógica". Nenhuma das nossa funções 
# consegue trocar letras certo? Oque significa que iremos precisar criar uma nova função
#  a "troca_letras".

def troca_letras(fatias):
  novas_palavras = []
  letras = 'abcdefghijklmnopqrstuvwxyzàáâãèéêìíîòóôõùúûç'
  for E, D in fatias:
    for letra in letras:
      # Concatena o lado esquerdo com o lado direito e com uma letra no meio
      # Obs: O lado direito só conta a partir do segundo caracter para ocorrer a troca de letra
      novas_palavras.append(E + letra + D[1:])
  return novas_palavras

# E agora só falta chamar ela na nossa função "gerador_palavras":

def gerador_palavras(palavra):
  fatias = []
  # Loop criador das fatias
  for i in range(len(palavra)+1):
    fatias.append((palavra[:i],palavra[i:]))

  # Chama a função insere_letras e guarda a lista recebido dentro da variável 
  palavras_geradas = insere_letras(fatias)
  # Chama a função deleta_letras e junta a lista "palavras_geradas" com a nova lista retornada
  # da função "deleta_letras"
  palavras_geradas += deleta_letras(fatias)
  # Chama a função deleta_letras e junta a lista "palavras_geradas" com a nova lista retornada
  # da função "troca_letras"
  palavras_geradas += troca_letras(fatias)

  return palavras_geradas

# Agora vamos testar o erro suposto acima:

# Input:
#   palavra_correta = corretor('lúgica')
#   print(palavra_correta)
# Output:
# lógica

# Deu certo mais uma vez, agora vamos partir para a nossa quarta e última função que adicionaremos.
#   Vamos supor a seguinte palavra foi escrita: "lógcia".
# Repare que o nosso usuário acabou por inverter a letra "i" com a "o", um erro muito comum já
# que as duas ficam muito próximas no teclado. Vamos criar uma função para resolver o problema então:

def inverte_letras(fatias):
  novas_palavras = []
  for E, D in fatias:
    if len(D) >= 2:
      primeira_letra_D = D[0]
      segunda_letra_D = D[1]
      # Inverte a primeira letra da direita com a segunda letra da fatia da direita
      novas_palavras.append(E + segunda_letra_D + primeira_letra_D + D[2:])
  return novas_palavras

# Agora vamos adicionar a chamada da nossa nova função, a "gerador_palavras"

def gerador_palavras(palavra):
  fatias = []
  # Loop criador das fatias
  for i in range(len(palavra)+1):
    fatias.append((palavra[:i],palavra[i:]))

  # Chama a função insere_letras e guarda a lista recebido dentro da variável 
  palavras_geradas = insere_letras(fatias)
  # Chama a função deleta_letras e junta a lista "palavras_geradas" com a nova lista retornada
  # da função "deleta_letras"
  palavras_geradas += deleta_letras(fatias)
  # Chama a função troca_letras e junta a lista "palavras_geradas" com a nova lista retornada
  # da função "troca_letras"
  palavras_geradas += troca_letras(fatias)
  # Chama a função inverte_letras e junta a lista "palavras_geradas" com a nova lista retornada
  # da função "inverte_letras"
  palavras_geradas += inverte_letras(fatias)
  
  return palavras_geradas

# Agora, vamos testar a nossa nova função "inverte_letras"

# Input:
#   palavra_correta = corretor('lógcia')
#   print(palavra_correta)
# Output:
#   lógica

#   Agora sim o nosso corretor está completo, mas se você prestar atenção, o nosso
# corretor só consegue interpretar as palavras sozinhas. Então se o nosso usuário digitar uma
# frase com várias palavras daria um erro e o nosso corretor não conseguiria corrigir. Para poder
# melhorar isso precisaremos criar uma função que vai separar as palavras da nossa string digitada
# pelo usuário e solicitar a correção do nosso corretor para cada uma delas. E a função que usaremos
# será a logo abaixo:




def input_usuario():
  frase = input('Digite algo: ')
  # Verifica se a primeira letra é maiúscula por questão de formatação
  if frase[0] == frase[0].upper():
    primeira_maiuscula = True
  else:
    primeira_maiuscula = False
  tokens = nltk.tokenize.word_tokenize(frase.lower())
  frase_corrigida = corrige_frase(tokens, primeira_maiuscula)
  print(frase_corrigida)

def corrige_frase(tokens, primeira_maiuscula):
  frase_corrigida = ''
  contador_palavras_corrigidas = 0
  for token in tokens:
    # Verifica se o token é "alfabético" para poder mandar ele para o corretor corrigir
    if token.isalpha():
      palavra_correta = corretor(token)
      # Verifica se ele vai precisar formatar a primeira letra como maiúscula
      if (primeira_maiuscula == True) and (contador_palavras_corrigidas == 0):
        frase_corrigida += palavra_correta[0].upper() + palavra_correta[1:]
      else:
        frase_corrigida += palavra_correta
      frase_corrigida += ' '
      contador_palavras_corrigidas += 1
    else:
      frase_corrigida += token
  return frase_corrigida

# Agora vamos testar:

# Input:
#   input_usuario()
# Output:
#   Digite algo: O coretor funcona agor
#   O corretor funciona agora 

# E assim terminamos o nosso primeiro corretor ortográfico feito em Python, obrigado por ler!

input_usuario()

