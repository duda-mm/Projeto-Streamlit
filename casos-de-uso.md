# Reserva de Salas
## Casos de Uso
### 1 - Gerenciar Sala

#### Nome do Caso de Uso: 
Gerenciar Sala
#### Atores Envolvidos: 
Administrador 
#### Fluxo Principal de Eventos:
A. Criar Sala

1. [IN] O Administrador acessa a área de gerenciamento de salas.

2. [OUT] O sistema exibe um formulário para cadastrar uma nova sala.

3. [IN] O Administrador preenche os dados da sala (nome, capacidade, recursos, descrição).

4. [IN] O Administrador confirma o cadastro.

5. [OUT] O sistema valida e salva a sala no banco de dados.

6. [OUT] O sistema exibe mensagem de sucesso.

B. Visualizar Salas

1. [IN] O Administrador acessa a lista de salas cadastradas.

2. [OUT] O sistema exibe todas as salas com informações como nome, capacidade e recursos.

C. Atualizar Sala

1. [IN] O Administrador seleciona uma sala para editar.

2. [OUT] O sistema exibe os dados atuais da sala.

3. [IN] O Administrador altera os campos desejados.

4. [IN] O Administrador confirma a atualização.

5. [OUT] O sistema valida e salva as alterações.

6. [OUT] O sistema exibe mensagem de sucesso.

D. Excluir Sala

1. [IN] O Administrador seleciona uma sala para excluir.

2. [OUT] O sistema solicita confirmação.

3. [IN] O Administrador confirma.

4. [OUT] O sistema exclui a sala do banco de dados.

- O sistema exibe mensagem de sucesso.
#### Fluxos de Excessão:
A. Dados Inválidos no Cadastro ou Atualização
- Se o Administrador enviar dados incompletos ou incorretos, o sistema avisa quais campos precisam ser corrigidos. O fluxo retorna ao passo de edição/preenchimento.

B. Exclusão de Sala Com Reservas Ativas
- Se a sala possuir reservas futuras, o sistema impede a exclusão e informa ao Administrador.
Fluxo retorna ao passo de seleção da sala.
#### Pré-condições:
- O Administrador deve estar autenticado.

- O sistema deve estar funcionando e com acesso ao banco de dados.
#### Pós-condições:
- Uma sala pode ser criada, visualizada, atualizada ou excluída conforme a ação realizada.

- As alterações ficam imediatamente disponíveis no sistema.

### 2 - Gerenciar Reserva

#### Nome do Caso de Uso: 
Gerenciar Reserva
#### Atores Envolvidos: 
Usuário 
#### Fluxo Principal de Eventos:
A. Criar Reserva

1. [IN] O Usuário realiza login e acessa o calendário de disponibilidade.

2. [IN] O Usuário seleciona sala, data e horário.

3. [IN] O Usuário preenche informações adicionais.

4. [OUT] O sistema verifica conflitos de horário.

5. [OUT] Não havendo conflito, a reserva é registrada com status pendente.

6. [IN] O Usuário recebe notificação da criação.

B. Visualizar Reservas

1. [IN] O Usuário acessa a área “Minhas Reservas”.
 
2. [OUT] O sistema lista as reservas do Usuário com status (pendente, aprovada, recusada).

C. Atualizar Reserva

1. [IN] O Usuário seleciona uma reserva pendente ou aprovada.

2. [OUT] O sistema exibe os dados atuais.

3. [IN] O Usuário altera data, horário ou sala.

4. [OUT] O sistema verifica eventuais conflitos.

5. [OUT] Estando tudo correto, o sistema salva as atualizações.

6. [OUT] O sistema exibe mensagem de sucesso.

D. Excluir/Cancelar Reserva

1. [IN] O Usuário seleciona uma reserva para cancelar.

2. [OUT] O sistema solicita confirmação.

3. [IN] O Usuário confirma.

4. [OUT] O sistema altera o status para “Cancelada”.

5. [OUT] O sistema libera aquele horário no calendário.
#### Fluxos de Excessão:
A. Conflito de Horário
- Se o sistema detectar conflito ao criar ou atualizar a reserva, informa ao Usuário e retorna ao passo de seleção de horários.

B. Atualização de Reserva Já Avaliada
- Se a reserva já foi aprovada ou recusada, o sistema bloqueia alterações e avisa ao Usuário.

C. Tentativa de Cancelar Reserva Já Ocorrida
- Se o horário já passou, o sistema impede o cancelamento.
#### Pré-condições:
- O Usuário deve estar autenticado no sistema.

- Deve haver salas previamente cadastradas.

- O sistema deve estar operacional.
#### Pós-condições:
- Uma reserva pode ser criada, visualizada, atualizada ou cancelada.

- A disponibilidade das salas é atualizada conforme as ações do Usuário.

### 3 - Avaliar Solicitação de Reserva

#### Nome do Caso de Uso: 
Avaliar Solicitação de Reserva
#### Atores Envolvidos:
Avaliador 
#### Fluxo Principal de Eventos:
1. [IN] O Avaliador acessa o painel de solicitações de reserva pendentes.

2. [OUT] O sistema exibe uma lista de solicitações aguardando avaliação.

3. [IN] O Avaliador seleciona uma solicitação para analisar os detalhes (sala, horário, solicitante).

4. [IN] O Avaliador decide se aprova ou recusa a solicitação.

5. [OUT] O sistema atualiza o status da reserva para "Aprovada" ou "Recusada".

6. [OUT] O sistema notifica o Usuário sobre a decisão.
#### Fluxos de Excessão: 
Nenhum fluxo de excessão identificado neste caso de uso.
#### Pré-condições:
- O Avaliador deve estar autenticado no sistema.

- Deve existir pelo menos uma solicitação de reserva com status "pendente".

- O usuário deve ter sido designado como Avaliador por um Administrador.
#### Pós-condições:
- A solicitação de reserva tem seu status atualizado para "Aprovada" ou "Recusada".

- Se aprovada, a reserva é confirmada e o horário bloqueado no calendário. Se recusada, o horário volta a ficar disponível.

### 4 - Realizar Login

#### Nome do Caso de Uso: 
Realizar Login
#### Atores Envolvidos:
Usuário, Avaliador, Administrador
#### Fluxo Principal de Eventos:
1. [IN] O usuário (Usuário, Avaliador ou Administrador) acessa a tela de login do sistema.

2. [OUT] O sistema exibe os campos para inserção de e-mail/usuário e senha.

3. [IN] O usuário insere suas credenciais e confirma a ação clicando em "Entrar".

4. [OUT] O sistema valida as credenciais inseridas.
  
5. [OUT] Estando corretas, o sistema autentica o usuário.

6. [OUT] O sistema redireciona o usuário para a área correspondente ao seu perfil (Usuário, Avaliador ou Administrador).
#### Fluxos de Excessão: 
A. Credenciais Inválidas:
- Se o usuário inserir e-mail/usuário ou senha incorretos, o sistema exibirá uma mensagem informando que as credenciais são inválidas.

- O fluxo retorna ao passo 2.

B. Conta Inexistente ou Desativada:
- Se o usuário tentar fazer login com uma conta que não existe ou que foi desativada, o sistema exibirá uma mensagem informando a situação.

- O fluxo retorna ao passo 2.

C. Campos Vazios:
- Se o usuário tentar confirmar o login sem preencher todos os campos obrigatórios, o sistema informará que os dados são obrigatórios.

- O fluxo retorna ao passo 2.
#### Pré-condições:
- O usuário deve já possuir um cadastro ativo no sistema.

- O sistema deve estar disponível e funcional.

#### Pós-condições:
- O usuário passa a estar autenticado no sistema.

- O sistema libera acesso às funcionalidades de acordo com o perfil do usuário.
