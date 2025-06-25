import React, { createContext, ReactNode, useContext, useEffect, useState } from 'react';
import {
    clearAllData,
    deleteSingleEmail,
    loadEmailAccounts,
    loadUserData,
    saveEmailAccounts,
    saveSingleEmail,
    saveUserData
} from '../config/firebase';
import { EmailAccount, User } from '../types';

interface AppContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: User | null;
  emailAccounts: EmailAccount[];
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  addEmailAccount: (email: string, password: string, uses: string[]) => void;
  updateEmailAccount: (id: string, updates: Partial<EmailAccount>) => void;
  deleteEmailAccount: (id: string) => void;
  addUseToEmail: (emailId: string, use: string) => void;
  removeUseFromEmail: (emailId: string, use: string) => void;
  clearAllData: () => Promise<void>;
  syncData: () => Promise<void>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp deve ser usado dentro de um AppProvider');
  }
  return context;
};

interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [emailAccounts, setEmailAccounts] = useState<EmailAccount[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);
      
      // Tentar carregar dados do usuário admin (usuário padrão)
      const userId = 'admin';
      const savedUser = await loadUserData(userId);
      const savedEmailAccounts = await loadEmailAccounts(userId);
      
      console.log('Dados carregados:', { savedUser, savedEmailAccounts });
      
      if (savedUser) {
        setUser(savedUser);
        setIsAuthenticated(true);
        console.log('Usuário carregado:', savedUser);
      }
      
      if (savedEmailAccounts && savedEmailAccounts.length > 0) {
        setEmailAccounts(savedEmailAccounts);
        console.log('E-mails carregados:', savedEmailAccounts.length);
      } else {
        console.log('Nenhum e-mail encontrado');
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      // Em caso de erro, continuar sem dados carregados
    } finally {
      setIsLoading(false);
    }
  };

  const syncData = async () => {
    try {
      console.log('Iniciando sincronização manual...');
      await loadData();
      console.log('Sincronização concluída');
    } catch (error) {
      console.error('Erro durante sincronização:', error);
    }
  };

  const saveData = async () => {
    if (!user) return;
    
    try {
      const userId = user.id;
      await saveUserData(userId, user);
      await saveEmailAccounts(userId, emailAccounts);
      console.log('Dados salvos no Firebase com sucesso');
    } catch (error) {
      console.error('Erro ao salvar dados no Firebase:', error);
      // Em caso de erro, os dados ficam apenas em memória
      // Em uma aplicação real, você poderia implementar um sistema de retry
    }
  };

  const login = async (username: string, password: string): Promise<boolean> => {
    // Simulação de autenticação - em produção, isso seria uma chamada para API
    if (username === 'admin' && password === '123456') {
      const newUser: User = {
        id: 'admin',
        username,
        password
      };
      setUser(newUser);
      setIsAuthenticated(true);
      
      try {
        await saveUserData(newUser.id, newUser);
        return true;
      } catch (error) {
        console.error('Erro ao salvar dados do usuário:', error);
        // Mesmo com erro, permitir o login (dados ficam em memória)
        return true;
      }
    }
    return false;
  };

  const logout = async () => {
    setUser(null);
    setIsAuthenticated(false);
    setEmailAccounts([]);
  };

  const handleClearAllData = async () => {
    try {
      await clearAllData();
      setUser(null);
      setIsAuthenticated(false);
      setEmailAccounts([]);
      console.log('Todos os dados foram limpos');
    } catch (error) {
      console.error('Erro ao limpar dados:', error);
    }
  };

  const addEmailAccount = async (email: string, password: string, uses: string[]) => {
    const newAccount: EmailAccount = {
      id: Date.now().toString(),
      email,
      password,
      uses,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    setEmailAccounts(prev => {
      const newAccounts = [...prev, newAccount];
      return newAccounts;
    });

    // Salvar individualmente no Firebase
    if (user) {
      try {
        await saveSingleEmail(user.id, newAccount);
        console.log('E-mail adicionado e salvo no Firebase');
      } catch (error) {
        console.error('Erro ao salvar e-mail no Firebase:', error);
      }
    }
  };

  const updateEmailAccount = async (id: string, updates: Partial<EmailAccount>) => {
    setEmailAccounts(prev => {
      const newAccounts = prev.map(account => 
        account.id === id 
          ? { ...account, ...updates, updatedAt: new Date() }
          : account
      );
      return newAccounts;
    });

    // Salvar alterações no Firebase
    if (user) {
      try {
        const updatedAccount = emailAccounts.find(acc => acc.id === id);
        if (updatedAccount) {
          const finalAccount = { ...updatedAccount, ...updates, updatedAt: new Date() };
          await saveSingleEmail(user.id, finalAccount);
          console.log('E-mail atualizado no Firebase');
        }
      } catch (error) {
        console.error('Erro ao atualizar e-mail no Firebase:', error);
      }
    }
  };

  const deleteEmailAccount = async (id: string) => {
    setEmailAccounts(prev => {
      const newAccounts = prev.filter(account => account.id !== id);
      return newAccounts;
    });

    // Deletar do Firebase
    if (user) {
      try {
        await deleteSingleEmail(user.id, id);
        console.log('E-mail deletado do Firebase');
      } catch (error) {
        console.error('Erro ao deletar e-mail do Firebase:', error);
      }
    }
  };

  const addUseToEmail = async (emailId: string, use: string) => {
    setEmailAccounts(prev => {
      const newAccounts = prev.map(account =>
        account.id === emailId
          ? { 
              ...account, 
              uses: [...account.uses, use],
              updatedAt: new Date()
            }
          : account
      );
      return newAccounts;
    });

    // Salvar alterações no Firebase
    if (user) {
      try {
        const updatedAccount = emailAccounts.find(acc => acc.id === emailId);
        if (updatedAccount) {
          const finalAccount = { 
            ...updatedAccount, 
            uses: [...updatedAccount.uses, use],
            updatedAt: new Date()
          };
          await saveSingleEmail(user.id, finalAccount);
          console.log('Uso adicionado e salvo no Firebase');
        }
      } catch (error) {
        console.error('Erro ao salvar uso no Firebase:', error);
      }
    }
  };

  const removeUseFromEmail = async (emailId: string, use: string) => {
    console.log('Removendo uso:', use, 'do e-mail:', emailId);
    setEmailAccounts(prev => {
      const newAccounts = prev.map(account =>
        account.id === emailId
          ? {
              ...account,
              uses: account.uses.filter(u => u !== use),
              updatedAt: new Date()
            }
          : account
      );
      return newAccounts;
    });

    // Salvar alterações no Firebase
    if (user) {
      try {
        const updatedAccount = emailAccounts.find(acc => acc.id === emailId);
        if (updatedAccount) {
          const finalAccount = {
            ...updatedAccount,
            uses: updatedAccount.uses.filter(u => u !== use),
            updatedAt: new Date()
          };
          await saveSingleEmail(user.id, finalAccount);
          console.log('Uso removido e salvo no Firebase');
        }
      } catch (error) {
        console.error('Erro ao remover uso no Firebase:', error);
      }
    }
  };

  const value: AppContextType = {
    isAuthenticated,
    isLoading,
    user,
    emailAccounts,
    login,
    logout,
    addEmailAccount,
    updateEmailAccount,
    deleteEmailAccount,
    addUseToEmail,
    removeUseFromEmail,
    clearAllData: handleClearAllData,
    syncData
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}; 