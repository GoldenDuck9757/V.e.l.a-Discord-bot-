#  Discord Sync Bot (V.E.L.A BOT)



**Language:** [Português](#portuguese)

---

##  Sobre o Bot

Este bot é uma ferramenta para **sincronização de mensagens** entre usuários do Discord, com uma interface simples e clara. Ele permite que duas pessoas sincronizem suas conversas, com todas as mensagens trocadas sendo automaticamente encaminhadas entre os dois. Isso pode ser útil para diversos casos de uso, como moderação, verificação de mensagens e testes.

O bot também possui um sistema de **termos de uso** que deve ser aceito pelos usuários antes de utilizarem o bot, garantindo que todos estejam cientes das regras de uso e do comportamento esperado.

---

##  Como Funciona

### 1. **Aceitar os Termos de Uso**

Ao usar o comando `.guides` no DM, o bot enviará uma mensagem com os **termos de uso**. O usuário deve aceitar os termos para poder usar o bot. Caso o usuário rejeite, o bot não permitirá o uso.

### 2. **Sincronizar Conversas**

Após aceitar os termos, os usuários podem usar o comando `.chat [user_id]` para sincronizar sua conversa com outro usuário. Isso permitirá que todas as mensagens enviadas sejam automaticamente encaminhadas entre ambos.

### 3. **Gerenciar Conversas**

O bot também permite que as conversas sejam **limpas** com o comando `.clear`, o que desativa a sincronização de mensagens e apaga o histórico de mensagens trocadas.

---

##  Comandos Disponíveis

- **.guides**: Mostra os termos de uso e ajuda para começar a usar o bot.
- **.chat [user_id]**: Sincroniza a conversa com outro usuário especificado pelo ID.
- **.clear**: Limpa a sincronização da conversa e apaga mensagens trocadas.

---

##  Como Adicionar e Usar o Bot

1. **Clonar ou baixar o repositório**:
   - Você pode clonar o repositório com o comando:
     ```bash
     git clone https://github.com/GoldenDuck9757/V.e.l.a-Discord-bot-
     ```

2. **Instalar as dependências**:
   - Instale as dependências necessárias com:
     ```bash
     pip install -r requirements.txt
     ```

3. **Adicionar o Token do Bot**:
   - No arquivo `app.py`, substitua `"YOUR_BOT_TOKEN"` pelo **token** do seu bot do Discord.

4. **Rodar o Bot**:
   - Para rodar o bot, use o seguinte comando:
     ```bash
     python app.py
     ```

---

##  Personalizando para Outros Usos

Este bot pode ser facilmente adaptado para diversos casos de uso. Aqui estão algumas sugestões para personalização:

- **Adicionar novos comandos**: Você pode adicionar novos comandos para expandir a funcionalidade do bot.
- **Alterar a lógica de mensagens**: O comportamento do bot ao encaminhar ou editar mensagens pode ser modificado para atender a necessidades específicas.

---

##  Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo LICENSE para mais detalhes.

---

##  Contribuições

Se você deseja contribuir para este projeto, sinta-se à vontade para **abrir um Pull Request** ou **criar um novo issue** para sugerir melhorias.

---

##  Desenvolvedor

- **Golden4484** (desenvolvedor principal)

---