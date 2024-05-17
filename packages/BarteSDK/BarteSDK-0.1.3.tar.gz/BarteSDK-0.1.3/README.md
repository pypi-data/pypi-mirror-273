# BarteSDK

Bem-vindo ao BarteSDK, a solução oficial para integração com as APIs de pagamento da Barte, projetada para simplificar e acelerar o desenvolvimento de aplicações fintech. Com nosso SDK, você pode facilmente integrar funcionalidades de pagamento, assinaturas, e gestão de compradores em sua aplicação.

## Recursos do SDK

O BarteSDK fornece métodos convenientes para interagir com as seguintes APIs:

- **API de Planos**: Facilita o gerenciamento dos planos cadastrados no seu checkout.
- **API de Pedidos**: Permite gerenciar os pedidos cadastrados no seu sistema.
- **API de Compradores**: Auxilia na gestão dos compradores cadastrados.
- **API de Cobranças**: Fornece ferramentas para o gerenciamento das cobranças.
- **API de Assinaturas**: Facilita a criação e gestão de assinaturas.
- **API de Criação de Link de Pagamento**: Permite a geração e gerenciamento de links de pagamento.

## Vantagens do BarteSDK

O BarteSDK foi desenvolvido pensando na eficiência e na otimização do tempo de desenvolvimento, oferecendo uma série de vantagens que vão além da simples integração com nossas APIs. Embora seu uso não seja obrigatório, recomendamos fortemente que você o adote para aproveitar os seguintes benefícios:

- **Mais Eficiência e Redução de Custos**: Implementar nosso SDK significa reduzir custos operacionais e de desenvolvimento. Ele já está pronto para uso e totalmente homologado pela Barte, garantindo que você esteja sempre alinhado com as melhores práticas e padrões do mercado.

- **Instalação Otimizada**: Facilitamos a instalação com nossa solução plug-and-play, que se integra perfeitamente a sistemas de gestão de pacotes como Composer, Gradle, Maven e NPM. Isso agiliza significativamente a integração do SDK ao seu projeto, economizando tempo valioso de desenvolvimento.

- **Construção de Requisições Simplificada**: Simplifique a construção de suas requisições com nossa interface intuitiva. O SDK foi projetado para minimizar a complexidade, otimizar o desenvolvimento e garantir uma implementação eficaz e livre de erros.

- **Segurança de Dados**: A segurança é uma prioridade absoluta no BarteSDK. Utilizamos as melhores práticas e padrões de segurança para proteger todas as informações transmitidas, garantindo a integridade e confidencialidade dos dados dos seus clientes.

Adotar o BarteSDK não é apenas uma questão de conveniência; é uma decisão estratégica que fortalece a segurança, reduz custos e aumenta a eficiência do desenvolvimento de software na sua organização.


## Como Começar

Para começar a usar o BarteSDK, siga os passos abaixo:

1. **Instalação**

   Instale o SDK via pip:

   ```bash
   pip install bartesdk

2. **Uso**

Para usar o BarteReportAPI, siga os passos abaixo:

### Código de Exemplo

```python
# Importe a classe do SDK
from BarteReportAPI import BarteReportAPI

# Crie uma instância da classe com os parâmetros necessários
api_key = "inserir-token"
api_client = BarteReportAPI(api_key)

# Faça chamadas aos métodos definidos
response = api_client.send_report(
    query_file='cobrancas-completo.sql',
    recipient_email='e-mail@barte.com',
    id_seller='1111',
    report_name='Vendas',
    days_ago='7'
)

# Imprima a resposta ou faça outras operações com ela
print(response)
```

### Parâmetros do Método `send_report`

- `query_file`: Nome do arquivo SQL que contém a query para gerar o relatório.
- `recipient_email`: Endereço de e-mail do Seller que receberá o relatório.
- `id_seller`: Identificação do Seller para quem o relatório é destinado.
- `report_name`: Título amigável do relatório, que será usado no título do e-mail.
- `days_ago`: Número de dias retroativos para geração do relatório.