# Gerenciador de E-mails

Uma aplicação moderna e segura para gerenciar múltiplos e-mails e seus usos, com interface dark e funcionalidades avançadas.

## 🚀 Funcionalidades

- **Interface Dark Moderna**: Design elegante e moderno com tema escuro
- **Gerenciamento de E-mails**: Adicione, edite e remova contas de e-mail
- **Usos Dinâmicos**: Adicione múltiplos usos para cada e-mail (ex: trabalho, pessoal, redes sociais)
- **Relatórios Detalhados**: Visualize estatísticas e usos mais frequentes
- **Sincronização na Nuvem**: Dados salvos no Firebase Firestore com criptografia
- **Segurança**: Todos os dados são criptografados antes de serem enviados para o servidor
- **Suporte Web**: Funciona tanto no React Native quanto na web
- **Alertas Customizados**: Sistema próprio de alertas que funciona em todas as plataformas
- **Status de Sincronização**: Visualização em tempo real do status de conexão

## 🔐 Segurança

- **Criptografia AES**: Todos os dados são criptografados usando AES-256 antes de serem enviados para o Firebase
- **Chave de Criptografia**: Configurada no arquivo `config/firebase.ts`
- **Firebase Firestore**: Armazenamento seguro na nuvem com sincronização automática
- **Dados Separados**: Cada e-mail é salvo como um documento separado para melhor performance

## 🛠️ Tecnologias

- **React Native** com **Expo**
- **TypeScript** para tipagem estática
- **Firebase Firestore** para armazenamento na nuvem
- **Criptografia Customizada** para compatibilidade web
- **Expo Router** para navegação
- **AsyncStorage** para cache local (fallback)

## 📱 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd gerenciador-emails
```

2. Instale as dependências:
```bash
npm install
```

3. Configure o Firebase:
   - As credenciais já estão configuradas no arquivo `config/firebase.ts`
   - O projeto Firebase já está configurado e pronto para uso

4. Execute a aplicação:
```bash
npm start
```

## 🔑 Credenciais de Teste

- **Usuário**: `admin`
- **Senha**: `123456`

## 📊 Estrutura do Projeto

```
├── app/                    # Telas da aplicação (Expo Router)
│   ├── (tabs)/            # Telas com abas
│   │   ├── index.tsx      # Tela principal (E-mails)
│   │   ├── relatorio.tsx  # Tela de relatórios
│   │   └── _layout.tsx    # Layout das abas
│   ├── login/             # Tela de login
│   │   └── index.tsx      # Tela de autenticação
│   └── _layout.tsx        # Layout principal
├── components/            # Componentes reutilizáveis
│   ├── AddEmailModal.tsx  # Modal para adicionar e-mail
│   ├── AddUseModal.tsx    # Modal para adicionar uso
│   ├── CustomAlert.tsx    # Sistema de alertas customizado
│   ├── LoadingScreen.tsx  # Tela de carregamento
│   └── SyncStatus.tsx     # Status de sincronização
├── config/               # Configurações
│   └── firebase.ts       # Configuração do Firebase e criptografia
├── contexts/             # Contextos React
│   └── AppContext.tsx    # Contexto principal da aplicação
├── hooks/                # Hooks customizados
│   └── useCustomAlert.ts # Hook para alertas customizados
└── types/                # Definições de tipos TypeScript
    └── index.ts          # Tipos da aplicação
```

## 🔧 Configuração do Firebase

A aplicação está configurada para usar o Firebase Firestore com as seguintes configurações:

- **Projeto**: `gerenciador-dados`
- **Database**: Firestore
- **Criptografia**: XOR customizada com chave personalizada
- **Estrutura de Dados**:
  - `users/{userId}` - Dados do usuário (campos separados)
  - `emailAccounts/{userId}_{emailId}` - Cada e-mail como documento separado

### Estrutura dos Dados no Firebase:

#### Usuário:
```json
{
  "id": "admin",
  "username": "admin",
  "encryptedPassword": "criptografado",
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

#### E-mail (documento separado):
```json
{
  "id": "1234567890",
  "userId": "admin",
  "email": "exemplo@gmail.com",
  "encryptedPassword": "criptografado",
  "uses": ["Netflix", "Trabalho", "Instagram"],
  "createdAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z",
  "order": 0
}
```

## 🎨 Componentes Principais

### CustomAlert
Sistema próprio de alertas que funciona tanto no React Native quanto na web:

```typescript
import { useCustomAlert } from '../hooks/useCustomAlert';

const customAlert = useCustomAlert();
customAlert.showAlert('Título', 'Mensagem', [
  { text: 'OK', onPress: () => console.log('OK') },
  { text: 'Cancelar', onPress: () => console.log('Cancelar') }
]);
```

### LoadingScreen
Componente de carregamento personalizado:

```typescript
import LoadingScreen from '../components/LoadingScreen';

<LoadingScreen message="Carregando dados..." />
```

### SyncStatus
Componente que mostra o status de sincronização:

```typescript
import SyncStatus from '../components/SyncStatus';

<SyncStatus isOnline={true} lastSync={new Date()} />
```

## 🔒 Criptografia

Todos os dados são criptografados antes de serem enviados para o Firebase:

```typescript
// Criptografia XOR simples e compatível com web
const simpleEncrypt = (text: string, key: string): string => {
  let result = '';
  for (let i = 0; i < text.length; i++) {
    const charCode = text.charCodeAt(i) ^ key.charCodeAt(i % key.length);
    result += String.fromCharCode(charCode);
  }
  return btoa(result); // Codificação base64
};
```

## 📱 Funcionalidades por Tela

### Tela de Login
- Autenticação com usuário e senha
- Redirecionamento automático após login
- Credenciais de teste disponíveis

### Tela Principal (E-mails)
- Lista de todos os e-mails cadastrados
- Adicionar novos e-mails
- Adicionar usos aos e-mails
- Remover usos dos e-mails
- Excluir e-mails
- Botão de logout
- Status de sincronização em tempo real

### Tela de Relatório
- Estatísticas gerais (total de e-mails, usos, média)
- Usos mais frequentes
- Detalhes por e-mail
- Visualização organizada dos dados

## 🔄 Sincronização

### Como Funciona:
1. **Salvamento Individual**: Cada e-mail é salvo como um documento separado
2. **Carregamento Filtrado**: Apenas e-mails do usuário atual são carregados
3. **Atualizações em Tempo Real**: Mudanças são salvas imediatamente
4. **Status Visual**: Indicador de sincronização na parte inferior da tela

### Vantagens:
- ✅ **Performance**: Carregamento mais rápido
- ✅ **Escalabilidade**: Suporte a muitos e-mails
- ✅ **Confiabilidade**: Dados sempre sincronizados
- ✅ **Transparência**: Status de sincronização visível

## 🚀 Deploy

### Web
```bash
npm run web
```

### Mobile
```bash
npm run android
npm run ios
```

## 🔧 Desenvolvimento

Para desenvolvimento local:

1. Instale as dependências de desenvolvimento:
```bash
npm install --save-dev @types/react @types/react-native
```

2. Execute em modo de desenvolvimento:
```bash
npm start
```

## 📄 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte ou dúvidas, abra uma issue no repositório.
