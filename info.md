# Home Assistant Correios

## Curtiu? Pague-me um café!

Sinta-se livre para me pagar um café: Chave aleatória Pix `20b16bb2-d827-48a6-9e2c-924cd11a1a79` ou pelo QR CODE abaixo ❤.

![pix](https://raw.githubusercontent.com/oridestomkiel/home-assistant-correios/main/pix.jpg)

## Rastreamento de objetos nos correios.

![exemplo1](https://github.com/oridestomkiel/home-assistant-correios/blob/main/exemplo1.jpg)

## Instalação
- [x] Necessário ter o HACS instalado: https://github.com/hacs/integration

Para começar coloque todos os arquivos de `/custom_components/correios/` aqui:
`<config directory>/custom_components/correios/` ou clone o repositório https://github.com/oridestomkiel/home-assistant-correios via HACS

## Examplo do arquivo configuration.yaml

```yaml
sensor:
  platform: correios
  track: "OT238304072BR"
  description: "Camera para garagem"
```

## Variáveis de configuração

chave | tipo | descrição
:--- | :--- | :---
**platform (obrigatório)** | texto | Nome da plataforma.
**track (obrigatório)** | texto | Código de rastreamento do objeto nos Correios.
**description (opcional)** | texto | Descrição para identificar o objeto.

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

![exemplo2](https://github.com/oridestomkiel/home-assistant-correios/blob/main/exemplo2.jpg)

***
