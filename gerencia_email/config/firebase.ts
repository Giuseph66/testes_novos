import { initializeApp } from 'firebase/app';
import { collection, deleteDoc, doc, getDoc, getDocs, getFirestore, setDoc } from 'firebase/firestore';

const ENCRYPTION_KEY = "CTPJESUSATEULALALA";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCpdJK1PJ9oTbZj6pvpJxozV0BwVi0eVIY",
  authDomain: "gerenciador-dados.firebaseapp.com",
  databaseURL: "https://gerenciador-dados-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "gerenciador-dados",
  storageBucket: "gerenciador-dados.firebasestorage.app",
  messagingSenderId: "964632484627",
  appId: "1:964632484627:web:31b295cd5956889bb218e6",
  measurementId: "G-CSG8YMHEZ9"
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
const db = getFirestore(firebaseApp);

// Função simples de criptografia para compatibilidade web
const simpleEncrypt = (text: string, key: string): string => {
  try {
    let result = '';
    for (let i = 0; i < text.length; i++) {
      const charCode = text.charCodeAt(i) ^ key.charCodeAt(i % key.length);
      result += String.fromCharCode(charCode);
    }
    // Garantir que a string seja válida para base64
    return btoa(unescape(encodeURIComponent(result)));
  } catch (error) {
    console.error('Erro ao criptografar:', error);
    return '';
  }
};

const simpleDecrypt = (encryptedText: string, key: string): string => {
  try {
    if (!encryptedText || encryptedText.length === 0) {
      return '';
    }
    
    // Verificar se é uma string base64 válida
    const decoded = atob(encryptedText);
    const utf8String = decodeURIComponent(escape(decoded));
    
    let result = '';
    for (let i = 0; i < utf8String.length; i++) {
      const charCode = utf8String.charCodeAt(i) ^ key.charCodeAt(i % key.length);
      result += String.fromCharCode(charCode);
    }
    return result;
  } catch (error) {
    console.error('Erro ao descriptografar:', error);
    return '';
  }
};

// Funções de criptografia
export const encryptData = (data: any): string => {
  try {
    const jsonString = JSON.stringify(data);
    return simpleEncrypt(jsonString, ENCRYPTION_KEY);
  } catch (error) {
    console.error('Erro ao criptografar dados:', error);
    return '';
  }
};

export const decryptData = (encryptedData: string): any => {
  try {
    if (!encryptedData || encryptedData.length === 0) {
      return null;
    }
    
    const decryptedString = simpleDecrypt(encryptedData, ENCRYPTION_KEY);
    if (!decryptedString) return null;
    
    return JSON.parse(decryptedString);
  } catch (error) {
    console.error('Erro ao descriptografar dados:', error);
    return null;
  }
};

// Função para limpar todos os dados e começar do zero
export const clearAllData = async (): Promise<void> => {
  try {
    console.log('Limpando todos os dados do Firebase...');
    
    // Limpar todos os usuários
    const usersSnapshot = await getDocs(collection(db, 'users'));
    const userDeletePromises = usersSnapshot.docs.map(doc => deleteDoc(doc.ref));
    await Promise.all(userDeletePromises);
    
    // Limpar todos os e-mails
    const emailsSnapshot = await getDocs(collection(db, 'emailAccounts'));
    const emailDeletePromises = emailsSnapshot.docs.map(doc => deleteDoc(doc.ref));
    await Promise.all(emailDeletePromises);
    
    console.log('Todos os dados foram limpos com sucesso');
  } catch (error) {
    console.error('Erro ao limpar dados:', error);
    throw error;
  }
};

// Funções para salvar e carregar dados do usuário
export const saveUserData = async (userId: string, userData: any): Promise<void> => {
  try {
    const encryptedData = encryptData(userData);
    if (!encryptedData) {
      throw new Error('Falha ao criptografar dados do usuário');
    }
    
    await setDoc(doc(db, 'users', userId), {
      id: userData.id,
      username: userData.username,
      encryptedPassword: encryptedData, // Senha criptografada
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    });
    console.log('Dados do usuário salvos com sucesso');
  } catch (error) {
    console.error('Erro ao salvar dados do usuário:', error);
    throw error;
  }
};

export const loadUserData = async (userId: string): Promise<any> => {
  try {
    const docRef = doc(db, 'users', userId);
    const docSnap = await getDoc(docRef);
    
    if (docSnap.exists()) {
      const data = docSnap.data();
      const decryptedPassword = decryptData(data.encryptedPassword);
      return {
        id: data.id,
        username: data.username,
        password: decryptedPassword?.password || '123456'
      };
    }
    return null;
  } catch (error) {
    console.error('Erro ao carregar dados do usuário:', error);
    return null;
  }
};

// Funções para salvar e carregar e-mails em campos separados
export const saveEmailAccounts = async (userId: string, emailAccounts: any[]): Promise<void> => {
  try {
    // Primeiro, limpar e-mails existentes
    const existingEmails = await getDocs(collection(db, 'emailAccounts'));
    const deletePromises = existingEmails.docs
      .filter(doc => doc.data().userId === userId)
      .map(doc => deleteDoc(doc.ref));
    
    if (deletePromises.length > 0) {
      await Promise.all(deletePromises);
    }

    // Salvar cada e-mail como um documento separado
    const savePromises = emailAccounts.map(async (email, index) => {
      const emailDoc = {
        id: email.id,
        userId: userId,
        email: email.email,
        encryptedPassword: encryptData({ password: email.password }),
        uses: email.uses,
        createdAt: email.createdAt?.toISOString() || new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        order: index
      };

      await setDoc(doc(db, 'emailAccounts', `${userId}_${email.id}`), emailDoc);
    });

    await Promise.all(savePromises);
    console.log(`${emailAccounts.length} e-mails salvos com sucesso`);
  } catch (error) {
    console.error('Erro ao salvar e-mails:', error);
    throw error;
  }
};

export const loadEmailAccounts = async (userId: string): Promise<any[]> => {
  try {
    console.log('Carregando e-mails para usuário:', userId);
    const querySnapshot = await getDocs(collection(db, 'emailAccounts'));
    const emailAccounts: any[] = [];

    console.log('Total de documentos encontrados:', querySnapshot.size);

    querySnapshot.forEach((doc) => {
      const data = doc.data();
      console.log('Documento encontrado:', { id: doc.id, userId: data.userId, email: data.email });
      
      if (data.userId === userId) {
        try {
          const decryptedPassword = decryptData(data.encryptedPassword);
          const emailAccount = {
            id: data.id,
            email: data.email,
            password: decryptedPassword?.password || '',
            uses: data.uses || [],
            createdAt: new Date(data.createdAt),
            updatedAt: new Date(data.updatedAt)
          };
          
          emailAccounts.push(emailAccount);
          console.log('E-mail processado com sucesso:', emailAccount.email);
        } catch (error) {
          console.error(`Erro ao processar e-mail ${data.email}:`, error);
          // Adicionar e-mail mesmo com erro de descriptografia
          const emailAccount = {
            id: data.id,
            email: data.email,
            password: '',
            uses: data.uses || [],
            createdAt: new Date(data.createdAt),
            updatedAt: new Date(data.updatedAt)
          };
          emailAccounts.push(emailAccount);
          console.log('E-mail adicionado com senha vazia devido a erro de descriptografia');
        }
      } else {
        console.log('Documento não pertence ao usuário:', data.userId, '!=', userId);
      }
    });

    // Ordenar por ordem de criação
    emailAccounts.sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());
    
    console.log(`Carregados ${emailAccounts.length} e-mails para o usuário ${userId}`);
    return emailAccounts;
  } catch (error) {
    console.error('Erro ao carregar e-mails:', error);
    return [];
  }
};

// Função para salvar um e-mail individual
export const saveSingleEmail = async (userId: string, emailAccount: any): Promise<void> => {
  try {
    const emailDoc = {
      id: emailAccount.id,
      userId: userId,
      email: emailAccount.email,
      encryptedPassword: encryptData({ password: emailAccount.password }),
      uses: emailAccount.uses,
      createdAt: emailAccount.createdAt?.toISOString() || new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    await setDoc(doc(db, 'emailAccounts', `${userId}_${emailAccount.id}`), emailDoc);
    console.log(`E-mail ${emailAccount.email} salvo com sucesso`);
  } catch (error) {
    console.error('Erro ao salvar e-mail individual:', error);
    throw error;
  }
};

// Função para deletar um e-mail individual
export const deleteSingleEmail = async (userId: string, emailId: string): Promise<void> => {
  try {
    await deleteDoc(doc(db, 'emailAccounts', `${userId}_${emailId}`));
    console.log(`E-mail ${emailId} deletado com sucesso`);
  } catch (error) {
    console.error('Erro ao deletar e-mail:', error);
    throw error;
  }
};

export const deleteUserData = async (userId: string): Promise<void> => {
  try {
    // Deletar usuário
    await deleteDoc(doc(db, 'users', userId));
    
    // Deletar todos os e-mails do usuário
    const querySnapshot = await getDocs(collection(db, 'emailAccounts'));
    const deletePromises = querySnapshot.docs
      .filter(doc => doc.data().userId === userId)
      .map(doc => deleteDoc(doc.ref));
    
    if (deletePromises.length > 0) {
      await Promise.all(deletePromises);
    }
    
    console.log('Dados do usuário excluídos com sucesso');
  } catch (error) {
    console.error('Erro ao excluir dados do usuário:', error);
    throw error;
  }
};

export { db };
