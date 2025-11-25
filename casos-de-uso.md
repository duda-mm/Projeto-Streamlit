# Reserva de Salas
## Casos de Uso
### 1 - Cadastrar Salas

#### Nome do Caso de Uso: 
Realizar Cadastro
#### Atores Envolvidos: 
Administrador 
#### Fluxo Principal de Eventos:
- O Administrador acessa a área de gerenciamento de salas do sistema.

- O sistema exibe um formulário para o cadastro de uma nova sala.

- O Administrador preenche os dados da sala, como nome, capacidade, descrição e recursos disponíveis (projetor, ar-condicionado, etc.).

- O Administrador confirma o cadastro.

- O sistema valida as informações e salva a nova sala no banco de dados.

- O sistema exibe uma mensagem de sucesso, e a nova sala fica disponível para consultas e reservas.
#### Fluxos de Excessão:
A. Dados Inválidos: Se o Administrador submeter o formulário com dados incompletos ou em formato incorreto, o sistema exibirá uma mensagem de erro indicando os campos que precisam ser corrigidos. O fluxo retorna ao passo 3.
#### Pré-condições:
- O Administrador deve estar autenticado no sistema (ter realizado login).
#### Pós-condições:
- Uma nova sala é cadastrada no sistema e fica disponível para ser reservada.

### 2 - Solicitar Reserva

#### Nome do Caso de Uso: 
Solicitar Reserva
#### Atores Envolvidos: 
Cliente 
#### Fluxo Principal de Eventos:
- O Cliente, após realizar o login, acessa a funcionalidade para visualizar a disponibilidade das salas , geralmente por meio de um calendário.

- O Cliente seleciona a sala, a data e o horário desejados.

- O Cliente preenche informações adicionais, se necessário, e confirma a solicitação de reserva.

- O sistema verifica automaticamente se há conflito de horário com outras reservas já existentes para aquela sala.

- Não havendo conflito, o sistema registra a solicitação com o status "pendente de avaliação".

- O sistema notifica o Cliente de que a solicitação foi enviada e está aguardando aprovação.

#### Fluxos de Excessão:
A. Conflito de Horário: Se o sistema detectar um conflito de horário no passo 4, ele informará ao Cliente que o período selecionado não está disponível. O fluxo retorna ao passo 2, para que o Cliente possa escolher outro horário.
#### Pré-condições:
- O Cliente deve estar autenticado no sistema.
- Deve haver salas cadastradas no sistema.
#### Pós-condições:
- Uma nova solicitação de reserva é registrada no sistema com status "pendente".

### 3 - Avaliar Solicitação de Reserva

#### Nome do Caso de Uso: 
Avaliar Solicitação
#### Atores Envolvidos:
Avaliador 
#### Fluxo Principal de Eventos:
- O Avaliador acessa o painel de solicitações de reserva pendentes.

- O sistema exibe uma lista de solicitações aguardando avaliação.

- O Avaliador seleciona uma solicitação para analisar os detalhes (sala, horário, solicitante).

- O Avaliador decide se aprova ou recusa a solicitação.

- O sistema atualiza o status da reserva para "Aprovada" ou "Recusada".

- O sistema notifica o Cliente sobre a decisão.
#### Fluxos de Excessão: 
Nenhum fluxo de excessão identificado neste caso de uso.
#### Pré-condições:
- O Avaliador deve estar autenticado no sistema.

- Deve existir pelo menos uma solicitação de reserva com status "pendente".

- O usuário deve ter sido designado como Avaliador por um Administrador.

#### Pós-condições:
- A solicitação de reserva tem seu status atualizado para "Aprovada" ou "Recusada".

- Se aprovada, a reserva é confirmada e o horário bloqueado no calendário. Se recusada, o horário volta a ficar disponível.
