import { router } from 'expo-router';
import React, { useEffect, useState } from 'react';
import {
    FlatList,
    SafeAreaView,
    StatusBar,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
} from 'react-native';
import AddEmailModal from '../../components/AddEmailModal';
import AddUseModal from '../../components/AddUseModal';
import CustomAlert from '../../components/CustomAlert';
import SyncStatus from '../../components/SyncStatus';
import { useApp } from '../../contexts/AppContext';
import { createConfirmAlert, createDeleteAlert, useCustomAlert } from '../../hooks/useCustomAlert';
import { EmailAccount } from '../../types';

export default function HomeScreen() {
  const { emailAccounts, addEmailAccount, addUseToEmail, removeUseFromEmail, deleteEmailAccount, logout, isAuthenticated, clearAllData, syncData } = useApp();
  const [showAddEmailModal, setShowAddEmailModal] = useState(false);
  const [showAddUseModal, setShowAddUseModal] = useState(false);
  const [selectedEmail, setSelectedEmail] = useState<EmailAccount | null>(null);
  const [lastSync, setLastSync] = useState<Date | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);
  
  const customAlert = useCustomAlert();

  // Redirecionar se não estiver autenticado
  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated]);

  const handleAddEmail = async (email: string, password: string, uses: string[]) => {
    await addEmailAccount(email, password, uses);
    setLastSync(new Date());
  };

  const handleAddUse = async (use: string) => {
    if (selectedEmail) {
      await addUseToEmail(selectedEmail.id, use);
      setLastSync(new Date());
    }
  };

  const handleDeleteEmail = (email: EmailAccount) => {
    const buttons = createDeleteAlert(
      'Confirmar Exclusão',
      `Deseja realmente excluir o e-mail ${email.email}?`,
      async () => {
        await deleteEmailAccount(email.id);
        setLastSync(new Date());
      }
    );
    customAlert.showAlert('Confirmar Exclusão', `Deseja realmente excluir o e-mail ${email.email}?`, buttons);
  };

  const handleRemoveUse = (email: EmailAccount, use: string) => {
    const buttons = createConfirmAlert(
      'Confirmar Remoção',
      `Deseja remover "${use}" dos usos do e-mail ${email.email}?`,
      async () => {
        await removeUseFromEmail(email.id, use);
        setLastSync(new Date());
      }
    );
    customAlert.showAlert('Confirmar Remoção', `Deseja remover "${use}" dos usos do e-mail ${email.email}?`, buttons);
  };

  const handleClearData = () => {
    const buttons = createConfirmAlert(
      'Limpar Todos os Dados',
      'Isso irá apagar todos os e-mails salvos. Tem certeza?',
      async () => {
        await clearAllData();
        setLastSync(new Date());
      }
    );
    customAlert.showAlert('Limpar Todos os Dados', 'Isso irá apagar todos os e-mails salvos. Tem certeza?', buttons);
  };

  const handleSyncData = async () => {
    setIsSyncing(true);
    try {
      await syncData();
      setLastSync(new Date());
    } catch (error) {
      console.error('Erro na sincronização:', error);
    } finally {
      setIsSyncing(false);
    }
  };

  const renderEmailCard = ({ item }: { item: EmailAccount }) => (
    <View style={styles.emailCard}>
      <View style={styles.emailHeader}>
        <View style={styles.emailInfo}>
          <Text style={styles.emailAddress}>{item.email}</Text>
          <Text style={styles.emailPassword}>{item.password}</Text>
        </View>
        <View style={styles.emailActions}>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => {
              setSelectedEmail(item);
              setShowAddUseModal(true);
            }}
          >
            <Text style={styles.actionButtonText}>+</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.actionButton, styles.deleteButton]}
            onPress={() => handleDeleteEmail(item)}
          >
            <Text style={styles.actionButtonText}>×</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.usesContainer}>
        <View style={styles.usesHeader}>
          <Text style={styles.usesTitle}>Usos:</Text>
          <Text style={styles.usesHint}>Toque para remover</Text>
        </View>
        {item.uses.length > 0 ? (
          <View style={styles.usesList}>
            {item.uses.map((use, index) => (
              <TouchableOpacity
                key={index}
                style={styles.useTag}
                onPress={() => handleRemoveUse(item, use)}
                activeOpacity={0.7}
              >
                <Text style={styles.useTagText}>{use}</Text>
                <View style={styles.removeUseIcon}>
                  <Text style={styles.removeUseText}>×</Text>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        ) : (
          <Text style={styles.noUsesText}>Nenhum uso cadastrado</Text>
        )}
      </View>
    </View>
  );

  // Se não estiver autenticado, não renderizar nada
  if (!isAuthenticated) {
    return null;
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0a0a0a" />
      
      <View style={styles.header}>
        <Text style={styles.title}>Meus E-mails</Text>
        <View style={styles.headerActions}>
          <TouchableOpacity 
            style={[styles.syncButton, isSyncing && styles.syncButtonDisabled]} 
            onPress={handleSyncData}
            disabled={isSyncing}
          >
            <Text style={styles.syncButtonText}>
              {isSyncing ? 'Sinc...' : 'Sinc'}
            </Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.clearButton} onPress={handleClearData}>
            <Text style={styles.clearButtonText}>Limpar</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.logoutButton} onPress={logout}>
            <Text style={styles.logoutButtonText}>Sair</Text>
          </TouchableOpacity>
        </View>
      </View>

      {emailAccounts.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyStateTitle}>Nenhum e-mail cadastrado</Text>
          <Text style={styles.emptyStateSubtitle}>
            Adicione seu primeiro e-mail para começar a gerenciar
          </Text>
        </View>
      ) : (
        <FlatList
          data={emailAccounts}
          renderItem={renderEmailCard}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.listContainer}
          showsVerticalScrollIndicator={false}
        />
      )}

      <TouchableOpacity
        style={styles.fab}
        onPress={() => setShowAddEmailModal(true)}
      >
        <Text style={styles.fabText}>+</Text>
      </TouchableOpacity>

      <SyncStatus isOnline={true} lastSync={lastSync || undefined} isSyncing={isSyncing} />

      <AddEmailModal
        visible={showAddEmailModal}
        onClose={() => setShowAddEmailModal(false)}
        onAdd={handleAddEmail}
      />

      <AddUseModal
        visible={showAddUseModal}
        onClose={() => {
          setShowAddUseModal(false);
          setSelectedEmail(null);
        }}
        onAdd={handleAddUse}
        emailAddress={selectedEmail?.email || ''}
      />

      <CustomAlert
        visible={customAlert.alertVisible}
        title={customAlert.alertTitle}
        message={customAlert.alertMessage}
        buttons={customAlert.alertButtons}
        onClose={customAlert.hideAlert}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0a',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#333',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  headerActions: {
    flexDirection: 'row',
    gap: 8,
  },
  syncButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  syncButtonDisabled: {
    backgroundColor: '#666',
  },
  syncButtonText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '600',
  },
  clearButton: {
    backgroundColor: '#ff9500',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
  },
  clearButtonText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '600',
  },
  logoutButton: {
    backgroundColor: '#333',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  logoutButtonText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  emptyStateTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 8,
    textAlign: 'center',
  },
  emptyStateSubtitle: {
    fontSize: 16,
    color: '#888',
    textAlign: 'center',
    lineHeight: 24,
  },
  listContainer: {
    padding: 20,
    paddingBottom: 80, // Espaço para o FAB e status
  },
  emailCard: {
    backgroundColor: '#1a1a1a',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#333',
  },
  emailHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  emailInfo: {
    flex: 1,
  },
  emailAddress: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 4,
  },
  emailPassword: {
    fontSize: 14,
    color: '#888',
    fontFamily: 'monospace',
  },
  emailActions: {
    flexDirection: 'row',
    gap: 8,
  },
  actionButton: {
    backgroundColor: '#007AFF',
    borderRadius: 20,
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
  },
  deleteButton: {
    backgroundColor: '#ff3b30',
  },
  actionButtonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  usesContainer: {
    marginTop: 8,
  },
  usesHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  usesTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
  },
  usesHint: {
    fontSize: 14,
    color: '#888',
    fontStyle: 'italic',
  },
  usesList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  useTag: {
    backgroundColor: '#007AFF',
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 6,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#0056CC',
  },
  useTagText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '500',
    marginRight: 6,
  },
  removeUseIcon: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 10,
    width: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  removeUseText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  noUsesText: {
    fontSize: 14,
    color: '#666',
    fontStyle: 'italic',
  },
  fab: {
    position: 'absolute',
    bottom: 80, // Ajustado para dar espaço ao status
    right: 24,
    backgroundColor: '#007AFF',
    borderRadius: 28,
    width: 56,
    height: 56,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  fabText: {
    color: '#ffffff',
    fontSize: 24,
    fontWeight: 'bold',
  },
});
