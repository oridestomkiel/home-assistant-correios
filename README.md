# Home Assistant Correios

[![Generic badge](https://img.shields.io/badge/contributor-@dougiteixeira-<COLOR>.svg)](https://github.com/dougiteixeira)

## Rastreamento de objetos nos correios.

![exemplo1][exampleimg1]

## Instalação
- [x] Necessário ter o HACS instalado: https://github.com/hacs/integration

Vá no HACS e clique em integrações:

![hacs1][hacs1]

Clique no menu e vá em Repositórios personalizados.

![hacs2][hacs2]

Preencha com o endereço do github do componente:

```markdown
https://github.com/oridestomkiel/home-assistant-correios
```

Selecione Integração. Clique em Adicionar:

![hacs3][hacs3]

Clique em Baixar:

![hacs4][hacs4]

Clique em Baixar:

![hacs5][hacs5]

Reinicie o Home Assistant:

![hacs6][hacs6]

### Configuração Automática

A adição da integração à sua instância do Home Assistant pode ser feita através da interface do usuário, usando este botão:

<a href="https://my.home-assistant.io/redirect/config_flow_start?domain=correios" rel="Rastreamento Correios">![Foo](https://my.home-assistant.io/badges/config_flow_start.svg)</a>

### Configuração Manual:

* Com ele reiniciado, navegue até sua instância do Home Assistant.
* Na barra lateral clique em Configuração .
* No menu de configuração selecione Dispositivos e Serviços .

![hacs10][hacs10]

* Vá no canto direito embaixo e clique em “+ Adicionar Integração”.
* Na lista, pesquise e selecione “Rastreamento Correios” .

![hacs7][hacs7]

* Digite a descrição e o código da ecomenda e clique no botão Enviar.

![hacs8][hacs8]

- [x] Pronto, agora você verá seus rastreios e poderá realizar as suas integrações!

![hacs9][hacs9]

***

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

[hacs1]: resources/hacs-01.png
[hacs2]: resources/hacs-02.png
[hacs3]: resources/hacs-03.png
[hacs4]: resources/hacs-04.png
[hacs5]: resources/hacs-05.png
[hacs6]: resources/hacs-06.png
[hacs7]: resources/hacs-07.png
[hacs8]: resources/hacs-08.png
[hacs9]: resources/hacs-09.png
[hacs10]: resources/hacs-10.png

[exampleimg1]: exemplo1.jpg
[exampleimg2]: exemplo2.jpg
[pix]: pix.jpg
