# Home Assistant Correios

## Rastreamento de objetos nos correios.

![exemplo1][exampleimg1]

## Instalação
- [x] Necessário ter o HACS instalado: https://github.com/hacs/integration

Para começar coloque todos os arquivos de `/custom_components/correios/` aqui:
`<config directory>/custom_components/correios/` ou clone o repositório https://github.com/oridestomkiel/home-assistant-correios via HACS

## Configuração

A adição da integração à sua instância do Home Assistant pode ser feita através da interface do usuário, usando este botão:
<a href="https://my.home-assistant.io/redirect/config_flow_start?domain=correios" rel="some text">![Foo](https://my.home-assistant.io/badges/config_flow_start.svg)</a>

### Configuração Manual:

* Navegue até sua instância do Home Assistant.
* Na barra lateral clique em Configuração .
* No menu de configuração selecione Dispositivos e Serviços .
* No canto inferior direito, clique no botão botão Adicionar Integração .
* Na lista, pesquise e selecione “Rastreamento Correios” .
* Digite a descrição e o código da ecomenda e clique no botão Enviar.

## State and Attributes

### State

* Descrição do status atual do objeto

#### - EVENTOS SRO - CORREIOS

https://www.correios.com.br/atendimento/ferramentas/sistemas/arquivos/lista-de-eventos-rastreamento-de-objetos

### Attributes

* Descrição: Apelido dado ao objeto no arquivio de configuração 
* Código Objeto: Código identificador do objeto nos Correios
* Data Prevista: Quando existente, exibe a previsão de entrega do objeto
* Tipo Postal: Tipo de serviço referente ao pacote enviado.
* Movimentações: Lista com todas as movimenrações do pacote, desde a postagem até a entrega.

![exemplo2][exampleimg2]

***

## Curtiu? Pague-me um café!

Sinta-se livre para me pagar um café: Chave aleatória Pix `20b16bb2-d827-48a6-9e2c-924cd11a1a79` ou pelo QR CODE abaixo ❤.

![pix][pix]

***

[exampleimg1]: exemplo1.jpg
[exampleimg2]: exemplo2.jpg
[pix]: pix.jpg
